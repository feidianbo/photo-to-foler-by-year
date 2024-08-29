import os
import shutil
import argparse
from PIL import Image
from PIL.ExifTags import TAGS

def get_exif_data(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data:
            exif = {
                TAGS.get(tag, tag): value
                for tag, value in exif_data.items()
            }
            return exif
    except Exception as e:
        print(f"Error reading EXIF data from {image_path}: {e}")
    return None

def get_photo_year(image_path):
    exif_data = get_exif_data(image_path)
    if exif_data:
        date_taken = exif_data.get("DateTimeOriginal") or exif_data.get("DateTime")
        if date_taken:
            return date_taken.split(":")[0]  # Year is the first part before the first ':'
    return None

def organize_photos_by_year(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f"Created destination directory {dest_dir}")
    
    print(f"Organizing photos in {src_dir} to {dest_dir}")
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff')):
                file_path = os.path.join(root, file)
                year = get_photo_year(file_path)
                
                if year:
                    target_dir = os.path.join(dest_dir, year)
                    if not os.path.exists(target_dir):
                        os.makedirs(target_dir)
                    
                    target_path = os.path.join(target_dir, file)
                    shutil.move(file_path, target_path)
                    print(f"Moved {file} to {target_dir}")
                else:
                    print(f"No EXIF year found for {file}")

def main():
    parser = argparse.ArgumentParser(description="Organize photos by year based on EXIF data.")
    parser.add_argument("source_directory", help="Directory containing the photos to organize.")
    parser.add_argument("destination_directory", help="Directory where organized photos will be stored.")
    args = parser.parse_args()

    print("传入的参数为：", args)

    organize_photos_by_year(args.source_directory, args.destination_directory)

if __name__ == "__main__":
    main()
