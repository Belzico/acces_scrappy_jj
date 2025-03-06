from PIL import Image, ImageDraw, ImageFont

def generate_text_image(output_path="downloaded_images/image_with_text.png"):
    """
    Genera una imagen con texto incrustado para probar OCR.
    """
    width, height = 400, 100
    image = Image.new("RGB", (width, height), color=(200, 200, 200))
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 24)  # Asegúrate de que Arial esté disponible
    except IOError:
        font = ImageFont.load_default()

    text = "Special Discount 50% OFF"
    
    # Usar textbbox() en lugar de textsize()
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2

    draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0))

    image.save(output_path)
    print(f"✅ Image saved: {output_path}")

# Ejecutar script
generate_text_image()
