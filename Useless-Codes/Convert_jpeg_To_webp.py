import sys
import os
from PIL import Image

def convert_to_webp(input_path, output_path):
    """
    Converts a JPEG/JPG image to WEBP format.

    :param input_path: Path to the input JPEG/JPG image.
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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 ./jpg-webp.py <path_to_jpeg_image>")
        sys.exit(1)

    input_path = sys.argv[1]

    if not input_path.lower().endswith(('.jpg', '.jpeg')):
        print("Error: The input file must be a JPEG or JPG image.")
        sys.exit(1)

    # Get the filename without the directory and extension
    filename = os.path.basename(input_path).rsplit('.', 1)[0]

    # Save the WEBP file in the current working directory
    output_path = os.path.join(os.getcwd(), f"{filename}.webp")

    if convert_to_webp(input_path, output_path):
        try:
            os.remove(input_path)
            print(f"Original image deleted successfully: {input_path}")
        except Exception as e:
            print(f"Error deleting the original image: {e}")
            sys.exit(1)
    else:
        print("Conversion failed, original image not deleted.")
        sys.exit(1)
