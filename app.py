from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_promo_images(product_image_path, deal_text, output_path_prefix):
    # Create a white background
    width, height = 1080, 1080
    
    # Load the product image
    product_img = Image.open(product_image_path).convert('RGBA')
    
    # Resize product image
    product_img = product_img.resize((600, 700), Image.LANCZOS)
    
    # Prepare fonts
    try:
        font_large = ImageFont.truetype("arialbd.ttf", 80)
        font_small = ImageFont.truetype("arialbd.ttf", 60)
    except IOError:
        font_large = ImageFont.truetype("arial.ttf", 80)
        font_small = ImageFont.truetype("arial.ttf", 60)

    # Create three different layouts
    layouts = ['center', 'left', 'right']
    
    for layout in layouts:
        image = Image.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        # Set image and text positions based on layout
        if layout == 'center':
            img_x = (width - product_img.width) // 2
            img_y = height - product_img.height - 50
            text_y = 50
        elif layout == 'left':
            img_x = 50
            img_y = (height - product_img.height) // 2
            text_y = 50
        else:  # right
            img_x = width - product_img.width - 50
            img_y = (height - product_img.height) // 2
            text_y = 50
        
        # Paste product image
        image.paste(product_img, (img_x, img_y), product_img)
        
        # Add discount text
        y_text = text_y
        # discount_lines = textwrap.wrap(discount_text, width=15)
        # for line in discount_lines:
        #     bbox = draw.textbbox((0, 0), line, font=font_large)
        #     text_width = bbox[2] - bbox[0]
        #     if layout == 'left':
        #         x_text = width - text_width - 50
        #     elif layout == 'right':
        #         x_text = 50
        #     else:  # center
        #         x_text = (width - text_width) // 2
        #     draw.text((x_text, y_text), line, font=font_large, fill=(0, 0, 0))
        #     y_text += bbox[3] - bbox[1]
        
        # Add deal text
        deal_lines = textwrap.wrap(deal_text, width=20)
        for line in deal_lines:
            bbox = draw.textbbox((0, 0), line, font=font_small)
            text_width = bbox[2] - bbox[0]
            if layout == 'left':
                x_text = width - text_width - 50
            elif layout == 'right':
                x_text = 50
            else:  # center
                x_text = (width - text_width) // 2
            draw.text((x_text, y_text), line, font=font_small, fill=(0, 0, 0))
            y_text += bbox[3] - bbox[1]
        
        # Save the image
        image.save(f"{output_path_prefix}_{layout}.jpg", quality=95)

# Example usage
dealtext=input('enter the text')
create_promo_images('product.png', dealtext, 'promo_image')