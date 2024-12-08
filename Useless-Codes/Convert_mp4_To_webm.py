import os
import argparse
import subprocess

def convert_mp4_to_webm(mp4_file_path, output_dir):
    # Get the input file name without extension
    file_name = os.path.splitext(os.path.basename(mp4_file_path))[0]
    
    # Set the output path (either provided or in the script's directory)
    output_file_path = os.path.join(output_dir, f"{file_name}.webm")
    
    # FFmpeg command to convert .mp4 to .webm
    convert_command = ['ffmpeg', '-i', mp4_file_path, output_file_path]
    subprocess.run(convert_command, check=True)
    print(f"Conversion complete: {output_file_path}")

if __name__ == "__main__":
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Convert MP4 to WebM")
    parser.add_argument("input_file", help="Path to the input .mp4 file")
    parser.add_argument("output_dir", nargs="?", default=".", help="Directory to save the output .webm file (optional, defaults to current directory)")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Ensure output directory exists
    output_dir = args.output_dir if os.path.isdir(args.output_dir) else "."
    
    # Convert the file
    convert_mp4_to_webm(args.input_file, output_dir)
