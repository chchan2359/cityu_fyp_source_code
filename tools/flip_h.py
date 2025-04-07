# Author        : CHAN Cheuk Hei
# Student Name  : CHAN Cheuk Hei
# Student ID    : 57270778
# Usage         : Tool - Data Augmentation [Flipping Image Horinzontal]

from PIL import Image
import os

def horizontal_flip_in_folder(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} does not exist!")
        return
    
    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        # Build the full path of the file
        file_path = os.path.join(folder_path, filename)
        
        # Check if the file is an image (e.g., has jpg, jpeg, or png extension)
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            try:
                # Open the image
                img = Image.open(file_path)
                
                # Perform horizontal flip
                flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
                
                # Create the new file name
                base, ext = os.path.splitext(filename)
                new_filename = f"{base}_fliph{ext}"
                new_file_path = os.path.join(folder_path, new_filename)
                
                # Save the flipped image
                flipped_img.save(new_file_path)
                print(f"Flipped image saved as {new_file_path}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Example usage
folder_path = "E:/FYP/dataset/disease_v3/leaf_wilting"
horizontal_flip_in_folder(folder_path)