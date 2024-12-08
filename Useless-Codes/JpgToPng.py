import argparse
from PIL import Image
import os

def convert_jpg_to_png(jpg_path):
    # Determine the directory and base name of the input JPEG file
    input_dir = os.path.dirname(jpg_path)
    base_name = os.path.basename(jpg_path)
    base_name_without_ext = os.path.splitext(base_name)[0]
    
    # Define the output path with the same base name but with .png extension
    png_name = base_name_without_ext + '.png'
    png_path = os.path.join(input_dir, png_name)
    
    # Open the JPEG image
    with Image.open(jpg_path) as img:
        # Ensure the image is in RGB mode
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Save the image as a PNG
        img.save(png_path, 'PNG')
        print(f"Converted {jpg_path} to {png_path}")

def main():
    parser = argparse.ArgumentParser(description='Convert a JPEG image to a PNG image.')
    parser.add_argument('jpg_path', type=str, help='Path to the JPEG image file')
    
    args = parser.parse_args()
    
    convert_jpg_to_png(args.jpg_path)

if __name__ == "__main__":
    main()
