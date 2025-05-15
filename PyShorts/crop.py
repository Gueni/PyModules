from PIL import Image
import os

def crop_images_in_folder(folder_path):
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file is a PNG image
        if filename.endswith(".png"):
            # Full path to the image file
            file_path = os.path.join(folder_path, filename)
            
            # Open the image
            with Image.open(file_path) as img:
                # Get image dimensions
                width, height = img.size
                
                # Define the cropping box (left, upper, right, lower)
                left = 0
                upper = 200
                right = width
                lower = height - 1000
                
                # Crop the image
                cropped_img = img.crop((left, upper, right, lower))
                
                # Save the cropped image (overwrite the original)
                cropped_img.save(file_path)

# Example usage
folder_path = ""
crop_images_in_folder(folder_path)
