# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SIGAXJhChyYe2IyL1qJTBIauDOG2U9Kt
"""

!pip install transformers huggingface_hub

from huggingface_hub import hf_hub_download

# Create a local folder in Colab
import os
os.makedirs("vit_model", exist_ok=True)

# Download files
hf_hub_download(repo_id="google/vit-base-patch16-224", filename="pytorch_model.bin", local_dir="vit_model")
hf_hub_download(repo_id="google/vit-base-patch16-224", filename="config.json", local_dir="vit_model")
hf_hub_download(repo_id="google/vit-base-patch16-224", filename="preprocessor_config.json", local_dir="vit_model")

!zip -r vit_model.zip vit_model

from google.colab import files
files.download("vit_model.zip")

# STEP 1: Install required libraries
!pip install transformers torchvision timm --quiet

# STEP 2: Import required packages
from transformers import ViTForImageClassification, ViTImageProcessor
from PIL import Image
import requests
import torch

# STEP 3: Load the pre-trained model and processor
model = ViTForImageClassification.from_pretrained("google/vit-base-patch16-224")
processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224")

# STEP 4: Load a sample image from the internet (cat image)
image_url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/cats.png"
image = Image.open(requests.get(image_url, stream=True).raw).convert("RGB")

# STEP 5: Preprocess the image
inputs = processor(images=image, return_tensors="pt")

# STEP 6: Run inference
with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()

# STEP 7: Print the result
print("Predicted class:", model.config.id2label[predicted_class_idx])

from transformers import DetrImageProcessor, DetrForObjectDetection

# Load detection model (DETR)
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

# Prepare inputs
inputs = processor(images=image, return_tensors="pt")

# Forward pass
outputs = model(**inputs)

# Let's only keep detections with confidence > 0.9
target_sizes = torch.tensor([image.size[::-1]])
results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

# Display with bounding boxes
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(1)
ax.imshow(image)

for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    box = [round(i, 2) for i in box.tolist()]
    ax.add_patch(patches.Rectangle((box[0], box[1]), box[2]-box[0], box[3]-box[1],
                                   linewidth=2, edgecolor="red", facecolor="none"))
    ax.text(box[0], box[1], f"{model.config.id2label[label.item()]}: {round(score.item(), 3)}",
            color="white", bbox=dict(facecolor="red", alpha=0.5))

plt.axis("off")
plt.show()

# STEP 2: Import libraries
from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from google.colab import files

# STEP 3: Upload your image
uploaded = files.upload()

# Load the uploaded image
image_path = list(uploaded.keys())[0]
image = Image.open(image_path).convert("RGB")

# STEP 4: Load pre-trained DETR model
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

# Preprocess and inference
inputs = processor(images=image, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)

# Post-process results
target_sizes = torch.tensor([image.size[::-1]])
results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

# STEP 5: Display image with bounding boxes
fig, ax = plt.subplots(1, figsize=(12, 8))
ax.imshow(image)

for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    box = [round(i, 2) for i in box.tolist()]
    ax.add_patch(patches.Rectangle(
        (box[0], box[1]), box[2] - box[0], box[3] - box[1],
        linewidth=2, edgecolor="red", facecolor="none"
    ))
    ax.text(
        box[0], box[1] - 10,
        f"{model.config.id2label[label.item()]}: {round(score.item(), 2)}",
        color="white", fontsize=12,
        bbox=dict(facecolor="red", alpha=0.7)
    )

plt.axis("off")
plt.show()

# STEP 2: Import libraries
from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from google.colab import files

# STEP 3: Upload your image
uploaded = files.upload()

# Load the uploaded image
image_path = list(uploaded.keys())[0]
image = Image.open(image_path).convert("RGB")

# STEP 4: Load pre-trained DETR model
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

# Preprocess and inference
inputs = processor(images=image, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)

# Post-process results
target_sizes = torch.tensor([image.size[::-1]])
results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

# STEP 5: Display image with bounding boxes
fig, ax = plt.subplots(1, figsize=(12, 8))
ax.imshow(image)

for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    box = [round(i, 2) for i in box.tolist()]
    ax.add_patch(patches.Rectangle(
        (box[0], box[1]), box[2] - box[0], box[3] - box[1],
        linewidth=2, edgecolor="red", facecolor="none"
    ))
    ax.text(
        box[0], box[1] - 10,
        f"{model.config.id2label[label.item()]}: {round(score.item(), 2)}",
        color="white", fontsize=12,
        bbox=dict(facecolor="red", alpha=0.7)
    )

plt.axis("off")
plt.show()