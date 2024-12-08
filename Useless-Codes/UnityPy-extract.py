import UnityPy
import os
import argparse
from PIL import Image

parser = argparse.ArgumentParser(description="Extract assets from a Unity .assets file.")
parser.add_argument('assets_path', type=str, help="Path to the Unity .assets file.")
parser.add_argument('output_dir', type=str, nargs='?', default="/home/lynnux/Documents/Codes/unityOutput/", help="Directory to save the extracted assets (default: /home/lynnux/Documents/Codes/unityOutput/).")
args = parser.parse_args()

assets_path = args.assets_path

output_dir = args.output_dir

env = UnityPy.load(assets_path)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

counter = 0

image_formats = ['png', 'jpg', 'jpeg', 'webp']

video_formats = ['mp4', 'webm', 'gif']

for obj in env.objects:
    try:
        if obj.type.name == "Texture2D":
            data = obj.read()
            texture = data.image

            texture_extension = 'png'
            if hasattr(data, 'name') and data.name:
                for ext in image_formats:
                    if data.name.lower().endswith(ext):
                        texture_extension = ext
                        break

            image_name = f"{data.name if hasattr(data, 'name') and data.name else f'image_{counter}'}.{texture_extension}"
            counter += 1

            image_path = os.path.join(output_dir, image_name)

            if texture.mode != 'RGB':
                texture = texture.convert('RGB')
            
            texture.save(image_path, texture_extension.upper())
            print(f"Extracted image: {image_path}")

        elif obj.type.name == "AudioClip":
            data = obj.read()
            audio_data = data.audio

            audio_format = '.ogg'

            audio_name = f"{data.name if hasattr(data, 'name') and data.name else f'audio_{counter}'}{audio_format}"
            counter += 1

            audio_path = os.path.join(output_dir, audio_name)
            with open(audio_path, 'wb') as f:
                f.write(audio_data)
            print(f"Extracted audio: {audio_path}")

        elif obj.type.name == "VideoClip":
            data = obj.read()
            video_data = data.bytes

            video_format = 'mp4'
            if hasattr(data, 'name') and data.name:
                for ext in video_formats:
                    if data.name.lower().endswith(ext):
                        video_format = ext
                        break

            video_name = f"{data.name if hasattr(data, 'name') and data.name else f'video_{counter}'}.{video_format}"
            counter += 1

            video_path = os.path.join(output_dir, video_name)
            with open(video_path, 'wb') as f:
                f.write(video_data)
            print(f"Extracted video: {video_path}")

    except Exception as e:
        print(f"Failed to extract or save asset for object {obj.id}: {e}")
