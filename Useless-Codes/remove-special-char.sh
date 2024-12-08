#!/bin/bash

# Directory containing files (default to current directory)
DIR=${1:-.}

# Loop through all files in the directory
for file in "$DIR"/*; do
    # Skip directories
    if [ -d "$file" ]; then
        continue
    fi

    # Extract the filename and extension
    base=$(basename "$file")
    name="${base%.*}"
    ext="${base##*.}"

    # Remove special characters from the filename (excluding spaces and the extension)
    clean_name=$(echo "$name" | tr -cd '[:alnum:] _-')

    # Form the new filename
    new_file="$DIR/$clean_name.$ext"

    # Rename the file
    mv "$file" "$new_file"
done
