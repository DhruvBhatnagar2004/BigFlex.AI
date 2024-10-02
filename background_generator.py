import os
import torch
from diffusers import DiffusionPipeline
from diffusers.utils import load_image
from PIL import ImageOps
from transparent_background import Remover

# Set up device and model configurations
device = "cuda" if torch.cuda.is_available() else "cpu"
float_datatype = torch.float16 if device == "cuda" else torch.float32
MODEL_NAME = "yahoo-inc/photo-background-generation"
MODEL_CACHE = "model-cache"

class BackgroundGenerator:
    def __init__(self):
        self.setup()

    def setup(self):
        self.pipe = DiffusionPipeline.from_pretrained(
            MODEL_NAME,
            cache_dir=MODEL_CACHE,
            torch_dtype=float_datatype,
            custom_pipeline=MODEL_NAME,
        ).to(device)
        
        self.pipe.enable_attention_slicing()
        
        if device == "cuda":
            try:
                self.pipe.enable_xformers_memory_efficient_attention()
                print("xformers memory efficient attention enabled.")
            except ModuleNotFoundError:
                print("xformers not available. Using default attention mechanism.")
                self.pipe.enable_sequential_cpu_offload()
                print("Enabled sequential CPU offloading.")
        else:
            print("Running on CPU. Some optimizations are disabled.")

    def resize_with_padding(self, img, expected_size):
        img.thumbnail((expected_size[0], expected_size[1]))
        delta_width = expected_size[0] - img.size[0]
        delta_height = expected_size[1] - img.size[1]
        pad_width = delta_width // 2
        pad_height = delta_height // 2
        padding = (
            pad_width,
            pad_height,
            delta_width - pad_width,
            delta_height - pad_height,
        )
        return ImageOps.expand(img, padding)

    @torch.inference_mode()
    def generate(self, input_image, prompt, negative_prompt, num_outputs, num_inference_steps, seed, controlnet_conditioning_scale):
        if seed is None:
            seed = int.from_bytes(os.urandom(3), "big")
        print(f"Using seed: {seed}")
        generator = torch.Generator(device).manual_seed(seed)
        
        common_args = {
            "prompt": [prompt] * num_outputs,
            "negative_prompt": [negative_prompt] * num_outputs,
            "generator": generator,
            "num_inference_steps": num_inference_steps,
            "controlnet_conditioning_scale": controlnet_conditioning_scale,
            "guess_mode": False,
        }

        img = input_image.convert("RGB")
        img = self.resize_with_padding(img, (512, 512))
        
        remover = Remover(mode="base")
        fg_mask = remover.process(img, type="map")
        mask = ImageOps.invert(fg_mask)

        if device == "cuda":
            with torch.amp.autocast(device_type='cuda'):
                output = self.pipe(
                    **common_args, mask_image=mask, image=img, control_image=mask
                )
        else:
            output = self.pipe(
                **common_args, mask_image=mask, image=img, control_image=mask
            )

        return output.images

def generate_background(input_image, prompt, negative_prompt, num_outputs, num_inference_steps, seed, controlnet_conditioning_scale):
    generator = BackgroundGenerator()
    return generator.generate(
        input_image=input_image,
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_outputs=num_outputs,
        num_inference_steps=num_inference_steps,
        seed=seed,
        controlnet_conditioning_scale=controlnet_conditioning_scale
    )