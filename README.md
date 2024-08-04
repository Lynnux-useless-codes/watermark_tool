# Watermark Tool

A Python script to add a watermark to images using the [PIL (Pillow)](https://pillow.readthedocs.io/en/stable/) library. Customize the watermark text, position, font, and colors via a configuration file.

## Project Structure

```tree
.
├── config.json
├── images
├── README.md
├── requirements.txt
└── src
    └── watermark.py
```

- `config.json`: Configuration file for watermark settings.
- `images`: Folder to place images you want to watermark.
- `requirements.txt`: List of Python dependencies.
- `src/watermark.py`: Main script to add watermarks to images.

## Requirements

- Python 3.x
- [Pillow](https://pillow.readthedocs.io/en/stable/) library

To install the required packages, run:

```bash
pip install -r requirements.txt
```

## Configurations

Create a config.json file in the root directory. Example configuration:

```json
{
    "watermark_text": "Your Watermark Text",
    "position": "bottom-right",
    "font_path": null,
    "font_size_ratio": 0.05,
    "input_folder": "images",
    "output_folder": "watermarked_images",
    "transparency": 128,
    "text_color": [255, 255, 255],
    "bg_color": [0, 0, 0]
}
```

## Usage

**Prepare Your Images:**
Place your images in the images folder.

**Run the Script**
The script will process all images in the images folder and save the watermarked images in a folder named watermarked_images as set by config.json.

```bash
python src/watermark.py --config config.json
```

## Configuration Options

- `watermark_text`: The text used as the watermark.
- `position`: Watermark position options include `top-left`, `top-right`, `bottom-left`, `bottom-right`, or custom coordinates.
- `font_path`: Path to the font file for the watermark text.
*Uses default font if not provided.*
- `font_size_ratio`: Ratio of the font size relative to the smallest dimension of the image.
- `input_folder`: Folder containing images to be watermarked.
- `output_folder`: Folder for saving watermarked images.
- `transparency`: Background transparency of the watermark rectangle (0-255).
- `text_color`: RGB values for the watermark text color.
- `bg_color`: RGB values for the background color behind the text.

## Logging

The script logs errors and information using Python's built-in logging module. Messages will appear in the console.

## License

This project is licensed under the MIT License - see the [LICENSE file](license.txt) for details.

## Contributing

Contributions are welcome! Please open issues or submit pull requests for bugs or enhancements

## Contact

For any questions or feedback, please contact me at discord @darl_lynn.
