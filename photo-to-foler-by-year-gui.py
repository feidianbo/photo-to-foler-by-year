import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import font
from PIL import Image
from PIL.ExifTags import TAGS
import ctypes

# Enable High DPI Awareness
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass
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
    
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff')):
                file_path = os.path.join(root, file)
                year = get_photo_year(file_path)
                
                if year:
                    target_dir = os.path.join(dest_dir, year)
                    
                    if os.path.exists(target_dir):
                        response = messagebox.askyesno("Directory Exists",
                                                       f"The directory {target_dir} already exists. Do you want to overwrite it?")
                        if response:
                            shutil.rmtree(target_dir)  # Remove the existing directory and its contents
                        else:
                            continue
                    
                    os.makedirs(target_dir, exist_ok=True)
                    target_path = os.path.join(target_dir, file)
                    shutil.move(file_path, target_path)
                    print(f"Moved {file} to {target_dir}")
                else:
                    print(f"No EXIF year found for {file}")
    
    messagebox.showinfo("Success", "Photos have been organized successfully!")

def select_source_directory():
    source_dir = filedialog.askdirectory()
    if source_dir:
        source_dir_var.set(source_dir)

def select_destination_directory():
    dest_dir = filedialog.askdirectory()
    if dest_dir:
        dest_dir_var.set(dest_dir)

def start_organizing():
    src_dir = source_dir_var.get()
    dest_dir = dest_dir_var.get()
    if not src_dir or not dest_dir:
        messagebox.showwarning("Input Error", "Please select both source and destination directories.")
    else:
        organize_photos_by_year(src_dir, dest_dir)

# Create the main window
root = tk.Tk()
root.title("Photo Organizer by Year")

# Define a font for better clarity
# default_font = font.Font(family="Helvetica", size=10, weight="normal")
default_font = font.Font(family="", size=10)

# Create variables to hold directory paths
source_dir_var = tk.StringVar()
dest_dir_var = tk.StringVar()

# Create and place widgets with adjusted font
tk.Label(root, text="Source Directory:", font=default_font).grid(row=0, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=source_dir_var, width=50, font=default_font).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_source_directory, font=default_font).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Destination Directory:", font=default_font).grid(row=1, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=dest_dir_var, width=50, font=default_font).grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_destination_directory, font=default_font).grid(row=1, column=2, padx=10, pady=10)

tk.Button(root, text="Organize Photos", command=start_organizing, font=default_font).grid(row=2, column=1, pady=20)

# Start the Tkinter event loop
root.mainloop()
