#!/bin/bash

# Argument check
if [ -z "$2" ]; then
  echo "Usage: $0 <path_to_video_directory> <X-z>"
  echo "Example: $0 ./video 4x10"
  exit 1
fi

# Use the path given in terminal.
VIDEO_DIR="$1"

# debug: current video dir
# echo "Processing videos in directory: $VIDEO_DIR"

# Activate the virtual environment
source /home/lynnux/Documents/Codes/Env/vcsi-env/bin/activate
if [ $? -ne 0 ]; then
  echo "Failed to activate virtual environment"
  exit 1
fi

# Ensure vcsi is available
if ! command -v vcsi &> /dev/null; then
  echo "vcsi command not found after activating virtual environment"
  exit 1
fi

# Confirm virtual environment activation
echo "Virtual environment activated"

# List of video file extensions
EXTENSIONS=("mp4" "mpv" "m4v" "mov" "avi" "wmv" "mkv" "avchd" "webm")

# Debug: List all found videos
# echo "Finding video files..."

# Find videos to be faster
find_command="find \"$VIDEO_DIR\" -type f \\( $(printf -- "-iname '*.%s' -o " "${EXTENSIONS[@]}" | sed 's/ -o $//') \\)"

# Run the find command and print the results
eval $find_command

# Function to process a single video file
process_video() {
  local video="$1"
  local ext="${video##*.}"
  local base_name=$(basename "$video" ".$ext")

  # echo "Processing video: $video"
  output_file="$VIDEO_DIR/${base_name}.$ext.jpg"
  vcsi_command="vcsi -g 4x10 -o \"$output_file\" \"$video\""
  # echo "Running command: $vcsi_command"
  eval $vcsi_command
  if [ $? -ne 0 ]; then
    echo "Failed to create contact sheet for $video"
  else
    if [ -f "$output_file" ]; then
      echo "Contact sheet created for $video"
    else
      echo "Contact sheet not found for $video"
    fi
  fi
}

export -f process_video

# Run the find command and process the files in parallel
eval $find_command | while read -r video; do
  process_video "$video"
done

# Print confirmation of completion
echo "Processing complete"

# Deactivate the virtual environment
deactivate
if [ $? -ne 0 ]; then
  echo "Failed to deactivate virtual environment"
else
  echo "Virtual environment deactivated"
fi
