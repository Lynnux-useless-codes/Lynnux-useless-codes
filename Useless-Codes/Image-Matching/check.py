import json
import os
import cv2
from skimage.metrics import structural_similarity as ssim
import logging
import numpy as np
import gc

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration from the config file
def load_config(config_path):
    logging.info(f"Loading config from {config_path}")
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config

# Resize image for comparison
def resize_image(image, target_size=(500, 500)):
    if image is None:
        raise ValueError("Image not found or cannot be loaded.")
    return cv2.resize(image, target_size)

# Exact match comparison
def exact_match(img1, img2):
    return np.array_equal(img1, img2)

# SSIM similarity comparison
def calculate_ssim(img1, img2):
    # Minimum size for SSIM window
    min_size = 7  
    
    # Get the smaller side of the images
    img1_height, img1_width = img1.shape[:2]
    img2_height, img2_width = img2.shape[:2]
    
    # Check if either image is smaller than 7x7 pixels
    if img1_height < min_size or img1_width < min_size or img2_height < min_size or img2_width < min_size:
        raise ValueError("One or both images are too small for SSIM calculation. Images must be at least 7x7 pixels.")
    
    # Calculate the window size based on the smallest dimension of both images
    min_side = min(img1_height, img1_width, img2_height, img2_width)
    win_size = min(min_side, min_size)  # Ensure window size is within limits
    
    # Ensure that the window size is odd
    if win_size % 2 == 0:
        win_size -= 1
    
    # Log the details for debugging
    logging.info(f"Image 1 size: {img1_height}x{img1_width}")
    logging.info(f"Image 2 size: {img2_height}x{img2_width}")
    logging.info(f"Using window size: {win_size}")

    # Check that win_size is valid for both images
    if win_size <= 1:
        raise ValueError(f"Invalid window size {win_size} for SSIM. Image dimensions are too small.")
    
    try:
        # Check if the images are multichannel (e.g., RGB, RGBA)
        channel_axis = -1 if len(img1.shape) == 3 else None
        
        # Pass win_size explicitly in the SSIM call, and set channel_axis if the image has multiple channels
        return ssim(img1, img2, multichannel=True, win_size=win_size, channel_axis=channel_axis)
    except ValueError as e:
        # Log the error and return a default value
        logging.error(f"Error calculating SSIM with win_size={win_size}: {e}")
        return 0  # Returning a default similarity value of 0 for the error case

# Match images in the directory
def match_images_in_directory(input_image_path, image_directory):
    # Check if input image path exists
    if not os.path.exists(input_image_path):
        logging.error(f"Input image not found: {input_image_path}")
        return [], [], []

    # Read the input image
    img_to_match = cv2.imread(input_image_path)
    img_to_match_resized = resize_image(img_to_match)  # Resize input image for comparison

    # Lists to store the matches
    matched_images = []
    ssim_matches = []
    exact_matches = []

    # Traverse through all subdirectories and files
    for root, dirs, files in os.walk(image_directory):
        for filename in files:
            img_path = os.path.join(root, filename)
            if os.path.isfile(img_path):
                img = cv2.imread(img_path)
                if img is None:
                    logging.warning(f"Failed to load image: {img_path}")
                    continue

                img_resized = resize_image(img)  # Resize current image for comparison

                # Exact matching
                if exact_match(img_resized, img_to_match_resized):
                    exact_matches.append(img_path)

                # SSIM matching
                similarity = calculate_ssim(img_resized, img_to_match_resized)
                if similarity > 0.9:  # Adjust threshold as needed
                    ssim_matches.append((img_path, similarity))

                # Feature matching or other comparisons can be added here

    return matched_images, ssim_matches, exact_matches

# Main function
def main():
    # Load config from the JSON file
    config = load_config("./config.json")
    
    # Get the image paths from the config
    input_image_path = config.get("input_image")  # Path to the image you want to match
    image_directory = config.get("image_directory")  # Path to the directory containing images to compare

    # Log the paths for debugging
    logging.info(f"Loaded config: input_image={input_image_path}, image_directory={image_directory}")

    # Check if the input image path and directory are valid
    if not input_image_path:
        logging.error("Error: input_image path is missing or invalid in the config.")
        return

    if not image_directory:
        logging.error("Error: image_directory path is missing or invalid in the config.")
        return

    if not os.path.exists(input_image_path):
        logging.error(f"Error: Input image path does not exist: {input_image_path}")
        return

    if not os.path.exists(image_directory):
        logging.error(f"Error: Image directory path does not exist: {image_directory}")
        return

    # Start garbage collection
    gc.collect()

    # Proceed with image matching
    logging.info("Starting image matching process...")
    matched_images, ssim_matches, exact_matches = match_images_in_directory(input_image_path, image_directory)

    # Output results
    logging.info(f"Checked images in {image_directory}, found {len(matched_images)} matches")
    if matched_images:
        logging.info("Matches found:")
        for match in matched_images:
            logging.info(f" - {match}")
    
    # Display SSIM matches
    if ssim_matches:
        logging.info("SSIM Matches found:")
        for match in ssim_matches:
            logging.info(f" - {match[0]} with similarity: {match[1]:.4f}")

    # Display Exact matches
    if exact_matches:
        logging.info("Exact Matches found:")
        for match in exact_matches:
            logging.info(f" - {match}")

    # Run garbage collection again after processing
    gc.collect()


if __name__ == "__main__":
    main()
