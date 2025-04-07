# Author        : CHAN Cheuk Hei
# Student Name  : CHAN Cheuk Hei
# Student ID    : 57270778
# Usage         : Tool - File Renamer

import os
from PIL import Image

def rename_and_convert_images(folder_path, new_name):
    # Ensure the target folder exists
    os.makedirs(folder_path, exist_ok=True)

    # Iterate through all files in the folder
    for count, filename in enumerate(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, filename)
        
        # Check if the file is an image
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', 'webp')):
            # Open the image
            with Image.open(file_path) as img:
                # Convert to RGB (if not already in RGB mode)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Define the new file name
                new_filename = f"{new_name}_{count}.jpg"
                new_file_path = os.path.join(folder_path, new_filename)
                
                # Save the image in JPG format
                img.save(new_file_path, 'JPEG')
                
                # Remove the original file
                os.remove(file_path)
                
                print(f"Processed: {new_filename}")
    
    print("--DONE--")

# Example usage
folder_path = "E:/FYP/dataset/plant/Trachelospermum_Asiaticum"
new_name = "trachelospermum_asiaticum"
rename_and_convert_images(folder_path, new_name)
