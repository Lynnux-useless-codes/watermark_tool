from PIL import Image, ImageDraw, ImageFont
import os
import json
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def add_watermark(input_image_path, output_image_path, watermark_text, position, font_path=None, font_size_ratio=0.05, transparency=128, text_color=(255, 255, 255), bg_color=(0, 0, 0)):
    try:
        original = Image.open(input_image_path).convert("RGBA")
    except Exception as e:
        logging.error(f"Failed to open {input_image_path}: {e}")
        return

    # Make the image editable
    txt = Image.new('RGBA', original.size, (255, 255, 255, 0))

    # Calculate dynamic font size based on image dimensions
    width, height = original.size
    min_dimension = min(width, height)
    font_size = max(10, int(min_dimension * font_size_ratio))  # Ensure font size is at least 10

    # Load a font
    font = None
    if font_path:
        try:
            font = ImageFont.truetype(font_path, font_size)
        except Exception as e:
            logging.error(f"Failed to load font {font_path}: {e}")
            font = ImageFont.load_default()
    else:
        font = ImageFont.load_default()

    # Initialize ImageDraw
    draw = ImageDraw.Draw(txt)

    # Calculate position
    text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    if position == "top-left":
        pos = (10, 10)
    elif position == "top-right":
        pos = (width - text_width - 10, 10)
    elif position == "bottom-left":
        pos = (10, height - text_height - 10)
    elif position == "bottom-right":
        pos = (width - text_width - 10, height - text_height - 10)
    else:
        pos = position  # Use as coordinates if not a predefined position

    # Add background rectangle
    draw.rectangle([pos[0] - 5, pos[1] - 5, pos[0] + text_width + 5, pos[1] + text_height + 5], fill=(bg_color[0], bg_color[1], bg_color[2], transparency))

    # Add text to image
    draw.text(pos, watermark_text, fill=(text_color[0], text_color[1], text_color[2], 255), font=font)

    # Combine original image with watermark
    watermarked = Image.alpha_composite(original, txt)

    # Save the result
    watermarked = watermarked.convert("RGB")  # Remove alpha for saving in JPEG format
    try:
        watermarked.save(output_image_path)
        logging.info(f"Watermark added to {input_image_path}, saved as {output_image_path}")
    except Exception as e:
        logging.error(f"Failed to save {output_image_path}: {e}")

def load_config(config_path):
    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            return config
    except Exception as e:
        logging.error(f"Failed to load configuration file {config_path}: {e}")
        return {}

def parse_args():
    parser = argparse.ArgumentParser(description="Add watermark to images.")
    parser.add_argument('--config', type=str, default='config.json', help='Path to the configuration file.')
    return parser.parse_args()

def main():
    args = parse_args()
    config = load_config(args.config)

    watermark_text = config.get("watermark_text", "Sample Watermark")
    position = config.get("position", "bottom-right")
    font_path = config.get("font_path", None)
    font_size_ratio = config.get("font_size_ratio", 0.05)
    input_folder = config.get("input_folder", "images")
    output_folder = config.get("output_folder", "watermarked_images")
    transparency = config.get("transparency", 128)
    text_color = tuple(config.get("text_color", [255, 255, 255]))
    bg_color = tuple(config.get("bg_color", [0, 0, 0]))

    os.makedirs(output_folder, exist_ok=True)

    for image_file in os.listdir(input_folder):
        if image_file.lower().endswith(('png', 'jpg', 'jpeg')):
            input_image_path = os.path.join(input_folder, image_file)
            output_image_path = os.path.join(output_folder, f"watermarked_{image_file}")
            add_watermark(input_image_path, output_image_path, watermark_text, position, font_path, font_size_ratio, transparency, text_color, bg_color)

if __name__ == "__main__":
    main()
