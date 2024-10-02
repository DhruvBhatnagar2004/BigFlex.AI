import os
import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Configure Gemini API
genai.configure(api_key="api_key_here")

def upload_to_gemini(image_path, mime_type=None):
    file = genai.upload_file(image_path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def generate_deal_text(image_file, user_prompt):
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    image_file,
                    "Analyze this product image.",
                ],
            }
        ]
    )

    response = chat_session.send_message(user_prompt)
    return response.text.strip()

def create_promo_images(product_img, deal_text):
    width, height = 1080, 1080
    
    # Calculate the aspect ratio of the original image
    aspect_ratio = product_img.width / product_img.height
    
    # Resize product image while maintaining aspect ratio
    new_height = 600
    new_width = int(new_height * aspect_ratio)
    product_img = product_img.resize((new_width, new_height), Image.LANCZOS)
    
    # Use default font
    font_large = ImageFont.truetype("arialdb.TTF", 90)  # Increase font size here
    font_small = ImageFont.truetype("arialdb.TTF", 30)  

    # Create three different layouts
    layouts = ['center', 'left', 'right']
    output_images = []
    
    for layout in layouts:
        image = Image.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        # Set image and text positions based on layout
        if layout == 'center':
            img_x = (width - new_width) // 2
            img_y = height - new_height - 20
            text_y = 50
        elif layout == 'left':
            img_x = 50
            img_y = height - new_height - 20
            text_y = 50
        else:  # right
            img_x = width - new_width - 50
            img_y = height - new_height - 20
            text_y = 50
        
        # Paste product image
        image.paste(product_img, (img_x, img_y), product_img.convert('RGBA'))
        
        # Add deal text
        y_text = text_y
        deal_lines = textwrap.wrap(deal_text, width=15)  # Increased width for smaller font
        for line in deal_lines:
            bbox = draw.textbbox((0, 0), line, font=font_large)
            text_width = bbox[2] - bbox[0]
            if layout == 'left':
                x_text = width - text_width - 50
            elif layout == 'right':
                x_text = 50
            else:  # center
                x_text = (width - text_width) // 2
            draw.text((x_text, y_text), line, font=font_large, fill=(0, 0, 0))
            y_text += bbox[3] - bbox[1]
        
        output_images.append(image)

    return output_images

def generate_promo_images(image, prompt):
    # Save the uploaded image temporarily
    temp_image_path = "temp_product_image.jpg"
    image.save(temp_image_path)

    # Upload image to Gemini first
    image_file = upload_to_gemini(temp_image_path, mime_type="image/jpeg")

    # Generate deal text using the uploaded image and prompt
    deal_text = generate_deal_text(image_file, prompt)

    # Create promo images
    promo_images = create_promo_images(image, deal_text)

    # Clean up temporary file
    os.remove(temp_image_path)

    return deal_text, promo_images[0], promo_images[1], promo_images[2]