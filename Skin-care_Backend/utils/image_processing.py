"""
Image preprocessing utilities for PyTorch models
Updated for Ensemble (EfficientNet-B3 + ResNet18)
"""

import io
from PIL import Image
import torch
from torchvision import transforms
from config import Config


def preprocess_image_pytorch(image_data, target_size=224, mean=None, std=None):
    """
    Generic preprocessing for PyTorch models

    Args:
        image_data: Raw image bytes
        target_size: int or (H, W)
        mean: normalization mean
        std: normalization std

    Returns:
        torch.Tensor: [1, 3, H, W]
    """

    # Defaults (ImageNet)
    if mean is None:
        mean = Config.IMAGE_MEAN
    if std is None:
        std = Config.IMAGE_STD

    # Ensure tuple
    if isinstance(target_size, int):
        target_size = (target_size, target_size)

    # Load image
    img = Image.open(io.BytesIO(image_data)).convert('RGB')

    #  IMPORTANT: Use Resize (not crop) to match training
    transform = transforms.Compose([
        transforms.Resize(target_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=mean, std=std)
    ])

    img_tensor = transform(img).unsqueeze(0)

    return img_tensor



# ENSEMBLE MODEL PREPROCESSING (UPDATED)


def preprocess_for_disease_detection(image_data):
    """
    Preprocess for ENSEMBLE model

    Model expects:
    - Size: 224x224 (IMPORTANT CHANGE)
    - Normalization: ImageNet

    Returns:
        torch.Tensor: [1, 3, 224, 224]
    """
    return preprocess_image_pytorch(
        image_data,
        target_size=224   
    )


def preprocess_for_skin_type(image_data):
    """
    Skin type model preprocessing (unchanged)
    """
    return preprocess_image_pytorch(
        image_data,
        target_size=Config.SKIN_TYPE_IMAGE_SIZE
    )






def preprocess_for_ensemble(image_data):
    """
    Explicit function for ensemble usage (cleaner naming)
    """
    return preprocess_for_disease_detection(image_data)


# BACKWARD COMPATIBILITY


def preprocess_image_for_disease(image_data):
    return preprocess_for_disease_detection(image_data)


def preprocess_image_for_skintype(image_data):
    return preprocess_for_skin_type(image_data)