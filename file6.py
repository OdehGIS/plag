from PIL import Image
from PIL.ExifTags import TAGS  
import os


image_path = r"C:\PythonFiles\project\images\image.jpg."
output_path = r"C:\PythonFiles\project\images\new_image.jpg."

def extract_exif(image_path):
    """
    This function extracts and prints EXIF data of a file.
    """
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()

        if exif_data:
            print("Extracted EXIF Data:")
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id) 
                print(f"{tag_name}: {value}")
        else:
            print("No EXIF data found.")

    except FileNotFoundError:
        print(f"Error: File not found at {image_path}")
    except Exception as e:
        print(f"Error reading EXIF data: {e}")

def remove_exif(image_path, output_path):
    """
    This function removes all EXIF metadata from an image and 
    creates a new image without EXIF data. 
    """
    try:
        img = Image.open(image_path)
        data = list(img.getdata()) 
        img_without_exif = Image.new(img.mode, img.size)  # Creating the new image
        img_without_exif.putdata(data)  # Paste pixel data
        img_without_exif.save(output_path)  # Saving the new image.

        print(f"\nEXIF data removed. Image saved as: {output_path}")

    except FileNotFoundError:
        print(f"Error: File not found at {image_path}")
    except Exception as e:
        print(f"Error removing EXIF data: {e}")


print("\nStudent ID: antchr2155")  

# Extracting and printing EXIF data
extract_exif(image_path)

# Removing EXIF data
#remove_exif(image_path, output_path)

"""
try:
    img_check = Image.open(output_path)
    if hasattr(img_check, "_getexif") and img_check._getexif() is not None:
        print("\nEXIF data may still be present (check manually).")
    else:
        print("\nEXIF data successfully removed.")
except Exception as e:
    print(f"Error checking EXIF data: {e}")"""