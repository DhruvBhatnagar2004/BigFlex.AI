import os
import torch
from typing import List
from diffusers import DiffusionPipeline
from diffusers.utils import load_image
from PIL import ImageOps, Image
from transparent_background import Remover
import gradio as gr

MODEL_NAME = "yahoo-inc/photo-background-generation"
MODEL_CACHE = "model-cache"

# Check if CUDA is available, otherwise use CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
float_datatype = torch.float16 if device == "cuda" else torch.float32

print(f"Using device: {device}")

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
    def generate(
        self,
        input_image_path: str,
        output_dir: str,
        prompt: str = "mountains and city",
        negative_prompt: str = "3d, cgi, render, bad quality, normal quality",
        num_outputs: int = 1,
        num_inference_steps: int = 30,
        seed: int = None,
        controlnet_conditioning_scale: float = 1.0,
    ) -> List[str]:
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

        img = load_image(input_image_path).convert("RGB")
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

        output_paths = []
        for i, im in enumerate(output.images):
            output_path = os.path.join(output_dir, f"output_{i}.png")
            im.save(output_path)
            output_paths.append(output_path)

        return output_paths

# Initialize the generator
generator = BackgroundGenerator()

def generate_background(input_image, prompt, negative_prompt, num_outputs, num_inference_steps, seed, controlnet_conditioning_scale):
    output_dir = "temp_output"
    os.makedirs(output_dir, exist_ok=True)
    
    input_path = os.path.join(output_dir, "input.png")
    input_image.save(input_path)
    
    # Convert controlnet_conditioning_scale to float
    controlnet_conditioning_scale = float(controlnet_conditioning_scale)
    
    output_paths = generator.generate(
        input_image_path=input_path,
        output_dir=output_dir,
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_outputs=num_outputs,
        num_inference_steps=num_inference_steps,
        seed=seed,
        controlnet_conditioning_scale=controlnet_conditioning_scale
    )
    
    output_images = [Image.open(path) for path in output_paths]
    
    for path in output_paths + [input_path]:
        os.remove(path)
    os.rmdir(output_dir)
    
    return output_images

# Define the Gradio interface
iface = gr.Interface(
    fn=generate_background,
    inputs=[
        gr.Image(type="pil", label="Input Image"),
        gr.Textbox(label="Prompt", value="mountains and city"),
        gr.Textbox(label="Negative Prompt", value="3d, cgi, render, bad quality, normal quality"),
        gr.Slider(minimum=1, maximum=4, step=1, label="Number of Outputs", value=1),
        gr.Slider(minimum=10, maximum=50, step=1, label="Number of Inference Steps", value=30),
        gr.Number(label="Seed (optional)"),
        gr.Slider(minimum=0.1, maximum=2.0, step=0.1, label="ControlNet Conditioning Scale", value=1.0)
    ],
    outputs=[
        gr.Gallery(label="Generated Images", columns=2, rows=2)
    ],
    title="Background Generator",
    description="Generate new backgrounds for your images using AI."
)

# Launch the interface
if __name__ == "__main__":
    iface.launch(share=True)