import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'

    #  ENSEMBLE MODEL
    DISEASE_MODEL_PATH = os.getenv(
        'DISEASE_MODEL_PATH',
        'models/final_ensemble_model_v2.pth'
    )

    DISEASE_IMAGE_SIZE = 224

    ENSEMBLE_WEIGHTS = {
        "efficientnet": 0.6,
        "resnet": 0.4
    }

    DISEASE_MODEL_NAME = "EfficientNet-B3 + ResNet18 Ensemble"
    
    KNOWLEDGE_BASE_PATH = 'data/skincare_knowledge.json'

    # Skin type
    SKIN_TYPE_MODEL_PATH = os.getenv('SKIN_TYPE_MODEL_PATH', 'models/skin_type_model.pth')
    SKIN_TYPE_IMAGE_SIZE = 224
    SKIN_TYPE_CLASSES = ['Dry', 'Normal', 'Oily']

    # ImageNet normalization
    IMAGE_MEAN = [0.485, 0.456, 0.406]
    IMAGE_STD = [0.229, 0.224, 0.225]

    CONFIDENCE_THRESHOLD = 50
    TOP_K_PREDICTIONS = 3