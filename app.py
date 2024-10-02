import gradio as gr
from promo_generator import generate_promo_images
from background_generator import generate_background

def generate_promos(image, deal_prompt):
    deal_text, center_image, left_image, right_image = generate_promo_images(image, deal_prompt)
    return deal_text, center_image, left_image, right_image

def generate_new_backgrounds(selected_image, bg_prompt, negative_prompt, num_outputs, num_inference_steps, seed, controlnet_conditioning_scale):
    new_backgrounds = generate_background(
        input_image=selected_image,
        prompt=bg_prompt,
        negative_prompt=negative_prompt,
        num_outputs=num_outputs,
        num_inference_steps=num_inference_steps,
        seed=seed,
        controlnet_conditioning_scale=controlnet_conditioning_scale
    )
    # Pad the output list to always have 4 elements
    padded_backgrounds = new_backgrounds + [None] * (4 - len(new_backgrounds))
    return padded_backgrounds

# Define the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Promotional Image and Background Generator")
    
    with gr.Tab("Step 1: Generate Promo Images"):
        with gr.Row():
            input_image = gr.Image(type="pil", label="Upload Product Image")
            deal_prompt = gr.Textbox(
                label="Prompt for Deal Text", 
                lines=3, 
                value="Create a short and eye-catching minimum 10 sentence and simple heading for a sale offer. The offer is Big Basket 53% off in Big Indian Grocery Sale. Give me only the heading with no other text, no ##, ** or any other sign in start and end of text"
            )
        generate_button = gr.Button("Generate Promo Images")
        
        with gr.Row():
            deal_text_output = gr.Textbox(label="Generated Deal Text")
        
        with gr.Row():
            center_image_output = gr.Image(type="pil", label="Center Layout")
            left_image_output = gr.Image(type="pil", label="Left Layout")
            right_image_output = gr.Image(type="pil", label="Right Layout")
    
    with gr.Tab("Step 2: Generate New Backgrounds"):
        with gr.Row():
            selected_image = gr.Image(type="pil", label="Selected Promo Image")
            bg_prompt = gr.Textbox(label="Background Prompt", value="mountains and city")
        
        with gr.Row():
            negative_prompt = gr.Textbox(label="Negative Prompt", value="3d, cgi, render, bad quality, normal quality")
            num_outputs = gr.Slider(minimum=1, maximum=4, step=1, label="Number of Backgrounds", value=2)
            num_inference_steps = gr.Slider(minimum=10, maximum=50, step=1, label="Number of Inference Steps", value=15)
        
        with gr.Row():
            seed = gr.Number(label="Seed (optional)")
            controlnet_conditioning_scale = gr.Slider(minimum=0.1, maximum=2.0, step=0.1, label="ControlNet Conditioning Scale", value=1.5)
        
        generate_bg_button = gr.Button("Generate New Backgrounds")
        with gr.Row():
            text = gr.Textbox(("Creating Background in CPU take too much time almost 8 min for 4 image. Use T4 GPU for Fast Processing /n Running First take time to load the model"))
        
        with gr.Row():
            new_background_output1 = gr.Image(type="pil", label="Background 1")
            new_background_output2 = gr.Image(type="pil", label="Background 2")
            new_background_output3 = gr.Image(type="pil", label="Background 3")
            new_background_output4 = gr.Image(type="pil", label="Background 4")

    # Connect the components
    generate_button.click(
        generate_promos,
        inputs=[input_image, deal_prompt],
        outputs=[deal_text_output, center_image_output, left_image_output, right_image_output]
    )

    # Allow users to select one of the generated images for background generation
    center_image_output.select(lambda x: x, outputs=selected_image)
    left_image_output.select(lambda x: x, outputs=selected_image)
    right_image_output.select(lambda x: x, outputs=selected_image)

    generate_bg_button.click(
        generate_new_backgrounds,
        inputs=[selected_image, bg_prompt, negative_prompt, num_outputs, num_inference_steps, seed, controlnet_conditioning_scale],
        outputs=[new_background_output1, new_background_output2, new_background_output3, new_background_output4]
    )

# Launch the Gradio app
if __name__ == "__main__":
    demo.launch(share=True)