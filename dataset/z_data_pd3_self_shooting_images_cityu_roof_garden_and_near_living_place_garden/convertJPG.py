import os
from PIL import Image
import pillow_heif

def convert_heic_to_jpg(heic_folder, jpg_folder):
    if not os.path.exists(jpg_folder):
        os.makedirs(jpg_folder)

    for filename in os.listdir(heic_folder):
        if filename.lower().endswith(".heic"):
            heic_path = os.path.join(heic_folder, filename)
            jpg_path = os.path.join(jpg_folder, filename.rsplit('.', 1)[0] + ".jpg")

            # Open HEIC file
            heif_file = pillow_heif.open_heif(heic_path)
            image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data)
            
            # Save as JPG
            image.save(jpg_path, "JPEG")
            print(f"Converted {heic_path} to {jpg_path}")

def rename_jpg_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".JPG"):
            new_filename = filename[:-4] + ".jpg"
            os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
            print(f"Renamed {filename} to {new_filename}")

folder_path = './dataset_5_466'
rename_jpg_files(folder_path)


heic_folder = './dataset_5_466'
jpg_folder = './dataset_5_466_jpg'

#convert_heic_to_jpg(heic_folder, jpg_folder)