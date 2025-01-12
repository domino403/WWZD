import os
import json
from PIL import Image, ImageOps


def resize_and_pad_image(input_path, output_path, size=(150, 150)):
    with Image.open(input_path) as img:
        color = (0, 0, 0) if img.mode == "RGB" else 0
        img = ImageOps.pad(img, size, color=color, method=Image.Resampling.LANCZOS)
        img.save(output_path)


def process_images(source_folder, output_folder, json_file_path):
    os.makedirs(output_folder, exist_ok=True)
    image_data = {}

    for root, _, files in os.walk(source_folder):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                old_file_path = os.path.relpath(
                    os.path.join(root, file), start=source_folder
                )
                new_file_path = os.path.relpath(
                    os.path.join(output_folder, file), start=source_folder
                )

                resize_and_pad_image(
                    os.path.join(source_folder, old_file_path),
                    os.path.join(output_folder, file),
                    size=(150, 150),
                )

                image_data[file] = {
                    "old_file_path": old_file_path,
                    "new_file_path": new_file_path,
                }

    with open(json_file_path, "w") as json_file:
        json.dump(image_data, json_file, indent=4)


if __name__ == "__main__":
    process_images(
        source_folder=r"D:\programing\WWZD\data\raw_images",
        output_folder=r"D:\programing\WWZD\data\vis_images",
        json_file_path=r"D:\programing\WWZD\data\0_vis_images.json",
    )
