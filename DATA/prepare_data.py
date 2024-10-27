"""
prepare Dataset using EfficientNet Model with validation and testing dataset from IMAGENET
"""

import os
import json
import torch
from torchvision import models, transforms
from torchvision.models import EfficientNet_B3_Weights
from PIL import Image
from tqdm import tqdm


IMAGE_DIR = os.path.join(os.path.dirname(__file__), "raw_images")
OUTPUT = os.path.join(os.path.dirname(__file__), "output.json")


def process_image(image_path, preprocess, model):
    """
    preproces the image

    Args:
        image_path (str): path-like object to input image
        preprocess (torchvision.transforms.Compose): a set of rules for transforming the input image
        model (torchvision.models): pretrained model for image classification

    Returns:
        list: the image classification vector
    """
    img = Image.open(image_path).convert("RGB")
    img_tensor = preprocess(img).unsqueeze(0).to("cpu")

    with torch.no_grad():
        output = model(img_tensor)

    return output.squeeze().tolist()


def main():
    """
    Do all processing.
    """
    # LOAD MODEL
    weights = EfficientNet_B3_Weights.IMAGENET1K_V1
    model = models.efficientnet_b3(weights=weights)
    model.eval()
    model = model.to("cpu")

    # ADAPT IMAGE TO MODEL
    preprocess = transforms.Compose(
        [
            transforms.Resize(224),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=weights.transforms().mean, std=weights.transforms().std
            ),
        ]
    )

    result_dir = {}
    process_image_queue = []

    for root, _, file_names in os.walk(IMAGE_DIR):
        for image_name in file_names:
            image_path = os.path.join(root, image_name)
            if os.path.isfile(image_path) and image_path.lower().endswith(
                (".png", ".jpg", ".jpeg")
            ):
                process_image_queue.append(image_path)

    for image in tqdm(process_image_queue):
        result_dir[os.path.basename(image)] = process_image(image, preprocess, model)

    # ok, i know it's a bad idea, do not judge me
    with open(OUTPUT, "w", encoding="utf-8") as json_file:
        json.dump(result_dir, json_file)


if __name__ == "__main__":
    main()
