#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <path_to_image_directory>"
  exit 1
fi

IMAGE_DIR="$1"

echo "Processing images in directory: $IMAGE_DIR"

EXTENSIONS=("jpg" "jpeg" "png" "gif" "bmp" "tiff")

# Debug
# echo "Finding image files..."

find_command="find \"$IMAGE_DIR\" -type f \\( $(printf -- "-iname '*.%s' -o " "${EXTENSIONS[@]}" | sed 's/ -o $//') \\)"
# Debug
#echo "Running command: $find_command"

image_files=()
while IFS= read -r -d '' file; do
  image_files+=("$file")
done < <(eval $find_command -print0)

if [ ${#image_files[@]} -eq 0 ]; then
  echo "No image files found in the directory."
  exit 1
fi

process_sub_batch() {
  local sub_batch_index=$1
  shift
  local sub_batch=("$@")
  echo "Processing sub-batch $sub_batch_index with ${#sub_batch[@]} images."

  montage "${sub_batch[@]}" -tile 10x5 -geometry 200x200+2+2 "$IMAGE_DIR/contact_sheet_sub_batch_${sub_batch_index}.jpg"

  if [ $? -ne 0 ]; then
    echo "Failed to create contact sheet for sub-batch $sub_batch_index"
  else
    echo "Contact sheet created for sub-batch $sub_batch_index"
  fi
}

process_batch() {
  local batch_index=$1
  shift
  local batch=("$@")
  echo "Processing batch $batch_index with ${#batch[@]} images."

  sub_batch_size=50
  total_sub_images=${#batch[@]}
  num_sub_batches=$(( (total_sub_images + sub_batch_size - 1) / sub_batch_size ))

  sub_batch_files=()
  for (( j=0; j<num_sub_batches; j++ )); do
    sub_start=$(( j * sub_batch_size ))
    sub_end=$(( sub_start + sub_batch_size ))
    if [ $sub_end -gt $total_sub_images ]; then
      sub_end=$total_sub_images
    fi
    sub_batch=("${batch[@]:sub_start:sub_end-sub_start}")
    process_sub_batch "$batch_index"_"$j" "${sub_batch[@]}"
    sub_batch_files+=("$IMAGE_DIR/contact_sheet_sub_batch_${batch_index}_${j}.jpg")
  done

  montage "${sub_batch_files[@]}" -tile 2x -geometry +2+2 "$IMAGE_DIR/contact_sheet_batch_${batch_index}.jpg"

  if [ $? -ne 0 ]; then
    echo "Failed to create final contact sheet for batch $batch_index"
  else
    echo "Final contact sheet created for batch $batch_index"
    rm "${sub_batch_files[@]}"
  fi
}

batch_size=200
total_images=${#image_files[@]}
num_batches=$(( (total_images + batch_size - 1) / batch_size ))

for (( i=0; i<num_batches; i++ )); do
  start=$(( i * batch_size ))
  end=$(( start + batch_size ))
  if [ $end -gt $total_images ]; then
    end=$total_images
  fi
  batch=("${image_files[@]:start:end-start}")
  process_batch "$i" "${batch[@]}"
done

echo "Processing complete"
