import os
from PIL import Image

def get_image_size(image_path):
    """Returns the size (width, height) of an image."""
    with Image.open(image_path) as img:
        return img.size

def scale_image(image_path, size):
    """Scales an image to the specified size."""
    with Image.open(image_path) as img:
        img_resized = img.resize(size, Image.Resampling.LANCZOS)  # Use LANCZOS for quality resizing
        img_resized.save(image_path)  # Overwrite the original file

def scale_all_images_to_highest_resolution(directory):
    """Scales all images in a directory to the highest resolution."""
    image_files = [f for f in os.listdir(directory) if f.endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif', 'tiff'))]
    
    if not image_files:
        print("No images found in the directory.")
        return

    # Step 1: Find the highest resolution
    sizes = [get_image_size(os.path.join(directory, img)) for img in image_files]
    max_size = max(sizes, key=lambda size: size[0] * size[1])  # Find image with largest area
    
    # Step 2: Scale all images to the highest resolution
    for img_file in image_files:
        image_path = os.path.join(directory, img_file)
        scale_image(image_path, max_size)

    print(f"All images scaled to the highest resolution: {max_size}")



# Example usage:
directory_path = ""
scale_all_images_to_highest_resolution(directory_path)
