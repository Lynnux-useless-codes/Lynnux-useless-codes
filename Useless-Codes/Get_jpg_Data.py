import sys
from PIL import Image, ExifTags

def get_exif_data(image_path):
    """
    Get EXIF data from a JPEG image.

    :param image_path: Path to the JPEG image.
    :return: Dictionary containing EXIF data.
    """
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        if exif_data:
            return {ExifTags.TAGS.get(tag, tag): value for tag, value in exif_data.items()}
        else:
            return None
    except Exception as e:
        print(f"Error getting EXIF data: {e}")
        return None

def print_exif_data(exif_data):
    """
    Print EXIF data in a readable format.

    :param exif_data: Dictionary containing EXIF data.
    """
    if exif_data is None:
        print("No EXIF data found.")
        return

    for tag, value in exif_data.items():
        print(f"{tag}: {value}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 ./get_exif.py <path_to_jpeg_image>")
        sys.exit(1)

    image_path = sys.argv[1]

    if not image_path.lower().endswith(('.jpg', '.jpeg')):
        print("Error: The input file must be a JPEG or JPG image.")
        sys.exit(1)

    exif_data = get_exif_data(image_path)
    print_exif_data(exif_data)
