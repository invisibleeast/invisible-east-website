"""
This script is used to process codex images
(e.g. compresses main images and generates a thumbnail for each)

Steps:
1.  From django dir, run the command `python corpus/codex_images_process.py`
2.  Provide the full path to the directory of images to be processed when prompted
3.  Manually copy the output file to the correct location (e.g. django/media/corpus/codex/)
    either locally on the dev machine during development or the live VM with live data
4.  Delete the original source images when no longer needed
"""

from PIL import Image
from pathlib import Path
import shutil
import os

# Set source image directory
source_image_dir = input("Input source image directory full path: ")
source_image_dir = source_image_dir[:-1] if source_image_dir.endswith('/') else source_image_dir

# Set output image directories
output_image_dir = Path(source_image_dir) / source_image_dir.rsplit('/', 1)[-1]
output_image_thumbnail_dir = Path(output_image_dir) / 'thumbnails'

# Delete output directories, if they exist
if output_image_dir.exists() and output_image_dir.is_dir():
    shutil.rmtree(output_image_dir)
# Create output directories
output_image_thumbnail_dir.mkdir(parents=True, exist_ok=True)

# Loop through images and process them
for source_image in os.listdir(source_image_dir):
    if source_image.rsplit('.', 1)[-1].lower() in ['jpg', 'jpeg', 'png']:
        source_image_path = Path(source_image_dir) / Path(source_image)

        # Compress main image
        image = Image.open(source_image_path)
        image.thumbnail((2000, 2000), Image.LANCZOS)
        output_image_path = output_image_dir / Path(source_image)
        image.save(output_image_path, "JPEG", optimize=True, quality=80)

        # Create thumbnail image
        image = Image.open(source_image_path)
        image.thumbnail((400, 400), Image.LANCZOS)
        output_image_thumbnail_path = output_image_thumbnail_dir / Path(source_image)
        image.save(output_image_thumbnail_path, "JPEG", optimize=True, quality=80)
