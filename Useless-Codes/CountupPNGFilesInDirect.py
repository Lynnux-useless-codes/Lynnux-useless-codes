import os
import re

def rename_png_files(directory):
    # Get list of all png files in the directory
    files = os.listdir(directory)
    png_files = [file for file in files if file.lower().endswith('.png')]
    
    # Extract numbers from existing numbered files
    numbered_files = [file for file in png_files if re.match(r'^\d+\.png$', file)]
    numbered_files.sort(key=lambda x: int(x.split('.')[0]))
    
    # Find the next available number
    if numbered_files:
        last_number = int(numbered_files[-1].split('.')[0])
    else:
        last_number = 0
    # Filter files that are not numbered
    non_numbered_files = [file for file in png_files if not re.match(r'^\d+\.png$', file)]
    
    # Rename each non-numbered file
    for index, file in enumerate(non_numbered_files):
        new_number = last_number + index + 1
        new_name = f"{new_number}.png"
        old_path = os.path.join(directory, file)
        new_path = os.path.join(directory, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed {file} to {new_name}")

# Specify the directory
directory = '/media/lynnux/[E] Other/Images/Discord/Default-Avatars'

# Call the function
rename_png_files(directory)

print('Finished.')