import sys
from PIL import Image
import pytesseract

# Check if an argument was passed
if len(sys.argv) != 2:
    print("Usage: python file.py <image_path>")
    sys.exit(1)

# Get the image file path from the command-line argument
image_path = sys.argv[1]

# Open the image using Pillow
try:
    img = Image.open(image_path)
except Exception as e:
    print(f"Error opening image: {e}")
    sys.exit(1)

# Use pytesseract to extract text
text = pytesseract.image_to_string(img)

# Output the extracted text
print("Extracted Text:\n", text)
