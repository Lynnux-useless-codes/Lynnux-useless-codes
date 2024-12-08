import sys
import os
from PIL import Image
import glob

def convert_to_webp(input_path, output_path):
    """
    Converts a PNG image to WEBP format.

    :param input_path: Path to the input PNG image.
    :param output_path: Path to save the converted WEBP image.
    :return: True if conversion was successful, False otherwise.
    """
    try:
        with Image.open(input_path) as img:
            img.save(output_path, 'WEBP')
        print(f"Image converted successfully: {output_path}")
        return True
    except Exception as e:
        print(f"Error converting image: {e}")
        return False

def convert_all_pngs(pattern):
    """
    Converts all PNG images matching the pattern to WEBP format.

    :param pattern: Glob pattern to match PNG files.
    """
    print(f"Looking for files with pattern: {pattern}")  # Debug output
    for input_path in glob.glob(pattern):
        if not input_path.lower().endswith('.png'):
            continue

        filename = os.path.basename(input_path).rsplit('.', 1)[0]
        output_path = os.path.join(os.path.dirname(input_path), f"{filename}.webp")

        if convert_to_webp(input_path, output_path):
            try:
                os.remove(input_path)
                print(f"Original image deleted successfully: {input_path}")
            except Exception as e:
                print(f"Error deleting the original image: {e}")
        else:
            print("Conversion failed, original image not deleted.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 ./png-webp.py <path_to_png_image_or_pattern>")
        sys.exit(1)

    pattern = sys.argv[1]

    # Debug output to show what pattern is received
    print(f"Pattern received: {pattern}")

    if not pattern.lower().endswith('.png') and '*' not in pattern:
        print("Error: The input must be a PNG image or a pattern matching PNG files.")
        sys.exit(1)

    convert_all_pngs(pattern)
