import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips
from PIL import Image, ImageDraw, ImageFont
import os
import json
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def add_watermark_to_image(image, watermark_text, position, font, font_size, transparency, text_color, bg_color):
    """Add watermark to a single image frame."""
    original = image.convert("RGBA")

    # Make the image editable
    txt = Image.new('RGBA', original.size, (255, 255, 255, 0))

    # Initialize ImageDraw
    draw = ImageDraw.Draw(txt)

    # Calculate position
    text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    if position == "top-left":
        pos = (10, 10)
    elif position == "top-right":
        pos = (original.width - text_width - 10, 10)
    elif position == "bottom-left":
        pos = (10, original.height - text_height - 10)
    elif position == "bottom-right":
        pos = (original.width - text_width - 10, original.height - text_height - 10)
    else:
        pos = position  # Use as coordinates if not a predefined position

    # Add background rectangle
    draw.rectangle([pos[0] - 5, pos[1] - 5, pos[0] + text_width + 5, pos[1] + text_height + 5], fill=(bg_color[0], bg_color[1], bg_color[2], transparency))

    # Add text to image
    draw.text(pos, watermark_text, fill=(text_color[0], text_color[1], text_color[2], 255), font=font)

    # Combine original image with watermark
    watermarked = Image.alpha_composite(original, txt).convert("RGB")
    return watermarked

def process_image(input_image_path, output_image_path, watermark_text, position, font_path, font_size_ratio, transparency, text_color, bg_color):
    """Process image files and add watermark."""
    try:
        original = Image.open(input_image_path)
    except Exception as e:
        logging.error(f"Failed to open {input_image_path}: {e}")
        return

    width, height = original.size
    min_dimension = min(width, height)
    font_size = max(10, int(min_dimension * font_size_ratio))
    font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()

    watermarked = add_watermark_to_image(original, watermark_text, position, font, font_size, transparency, text_color, bg_color)
    watermarked.save(output_image_path)
    logging.info(f"Watermark added to {input_image_path}, saved as {output_image_path}")

def process_video(input_video_path, output_video_path, watermark_text, position, font_path, font_size_ratio, transparency, text_color, bg_color):
    """Process video files and add watermark to each frame."""
    try:
        video = VideoFileClip(input_video_path)
    except Exception as e:
        logging.error(f"Failed to open video {input_video_path}: {e}")
        return

    width, height = video.size
    min_dimension = min(width, height)
    font_size = max(10, int(min_dimension * font_size_ratio))
    font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()

    def add_watermark_to_frame(get_frame, t):
        frame = Image.fromarray(get_frame(t))
        watermarked_frame = add_watermark_to_image(frame, watermark_text, position, font, font_size, transparency, text_color, bg_color)
        return np.array(watermarked_frame)

    watermarked_video = video.fl(add_watermark_to_frame)
    watermarked_video.write_videofile(output_video_path, codec='libx264', audio_codec='aac')
    logging.info(f"Watermark added to video {input_video_path}, saved as {output_video_path}")

def process_gif(input_gif_path, output_gif_path, watermark_text, position, font_path, font_size_ratio, transparency, text_color, bg_color):
    """Process GIF files and add watermark to each frame."""
    try:
        gif = Image.open(input_gif_path)
    except Exception as e:
        logging.error(f"Failed to open GIF {input_gif_path}: {e}")
        return

    frames = []
    try:
        while True:
            frame = gif.copy().convert("RGBA")
            width, height = frame.size
            min_dimension = min(width, height)
            font_size = max(10, int(min_dimension * font_size_ratio))
            font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()

            watermarked_frame = add_watermark_to_image(frame, watermark_text, position, font, font_size, transparency, text_color, bg_color)
            frames.append(watermarked_frame)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    frames[0].save(output_gif_path, save_all=True, append_images=frames[1:], loop=0, duration=gif.info['duration'])
    logging.info(f"Watermark added to GIF {input_gif_path}, saved as {output_gif_path}")

def load_config(config_path):
    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            return config
    except Exception as e:
        logging.error(f"Failed to load configuration file {config_path}: {e}")
        return {}

def parse_args():
    parser = argparse.ArgumentParser(description="Add watermark to images and videos.")
    parser.add_argument('--config', type=str, default='config.json', help='Path to the configuration file.')
    return parser.parse_args()

def main():
    args = parse_args()
    config = load_config(args.config)

    watermark_text = config.get("watermark_text", "Sample Watermark")
    position = config.get("position", "bottom-right")
    font_path = config.get("font_path", None)
    font_size_ratio = config.get("font_size_ratio", 0.05)
    input_folder = config.get("input_folder", "media")
    output_folder = config.get("output_folder", "watermarked_media")
    transparency = config.get("transparency", 128)
    text_color = tuple(config.get("text_color", [255, 255, 255]))
    bg_color = tuple(config.get("bg_color", [0, 0, 0]))

    os.makedirs(output_folder, exist_ok=True)

    for media_file in os.listdir(input_folder):
        input_media_path = os.path.join(input_folder, media_file)
        output_media_path = os.path.join(output_folder, f"watermarked_{media_file}")

        if media_file.lower().endswith(('png', 'jpg', 'jpeg')):
            process_image(input_media_path, output_media_path, watermark_text, position, font_path, font_size_ratio, transparency, text_color, bg_color)
        elif media_file.lower().endswith(('mp4', 'avi', 'mov', 'mkv')):
            process_video(input_media_path, output_media_path, watermark_text, position, font_path, font_size_ratio, transparency, text_color, bg_color)
        elif media_file.lower().endswith(('gif',)):
            process_gif(input_media_path, output_media_path, watermark_text, position, font_path, font_size_ratio, transparency, text_color, bg_color)
        else:
            logging.warning(f"Unsupported file format: {media_file}")

if __name__ == "__main__":
    main()
