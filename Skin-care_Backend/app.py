import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
import torch
import json

app = Flask(__name__)
CORS(app)

# Initialize PyTorch device
torch_device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"\n{'='*70}")
print(f" Using PyTorch device: {torch_device}")
print(f"{'='*70}\n")


# LOAD ENSEMBLE DISEASE MODEL



print("LOADING ENSEMBLE DISEASE MODEL")


import timm
from torchvision import models
import torch.nn as nn

# Load ensemble checkpoint
checkpoint = torch.load('models/final_ensemble_model_v2.pth', map_location=torch_device)

disease_classes = checkpoint['classes']
num_disease_classes = len(disease_classes)

print(f" Loaded {num_disease_classes} classes")

# EfficientNet-B3
model1 = timm.create_model('efficientnet_b3', pretrained=False, num_classes=num_disease_classes)
model1.load_state_dict(checkpoint['efficientnet'])

# ResNet18
model2 = models.resnet18(weights=None)
model2.fc = nn.Linear(model2.fc.in_features, num_disease_classes)
model2.load_state_dict(checkpoint['resnet'])

model1.to(torch_device).eval()
model2.to(torch_device).eval()

print(" Ensemble model ready (EfficientNet + ResNet)")

# Load Skin Type Model (EXISTING - PyTorch EfficientNet-B3)

from torchvision import models


print("LOADING SKIN TYPE MODEL")


skin_type_model = models.efficientnet_b0(weights=None)
skin_type_model.classifier[1] = torch.nn.Linear(
    skin_type_model.classifier[1].in_features, 
    len(Config.SKIN_TYPE_CLASSES)
)

checkpoint_st = torch.load(Config.SKIN_TYPE_MODEL_PATH, map_location=torch_device)
state_dict_st = checkpoint_st.get('model_state_dict', checkpoint_st)

# Handle wrapper architecture if present
first_key = list(state_dict_st.keys())[0]
if first_key.startswith('base_model.'):
    import torch.nn as nn
    
    class SkinTypeModel(nn.Module):
        def __init__(self, base_model):
            super().__init__()
            self.base_model = base_model
        
        def forward(self, x):
            return self.base_model(x)
    
    temp_model = models.efficientnet_b0(weights=None)
    temp_model.classifier[1] = torch.nn.Linear(temp_model.classifier[1].in_features, 3)
    wrapper = SkinTypeModel(temp_model)
    wrapper.load_state_dict(state_dict_st, strict=False)
    skin_type_model = wrapper.base_model
else:
    skin_type_model.load_state_dict(state_dict_st, strict=False)

skin_type_model.to(torch_device)
skin_type_model.eval()

print(f" Skin Type Model Ready")
print(f"   Classes: {Config.SKIN_TYPE_CLASSES}")
print(f"   Device: {torch_device}")


# Initialize Chatbot


print("INITIALIZING RAG CHATBOT")


from utils.chatbot import SkincareChatbot

try:
    chatbot = SkincareChatbot()
    print(" RAG Chatbot initialized successfully")
except Exception as e:
    print(f"  Chatbot initialization failed: {e}")
    print("   Chatbot features will be disabled")
    chatbot = None


# Initialize Routes



print("REGISTERING ROUTES")


from routes.disease import init_disease_route
from routes.skincare import init_skincare_route
from routes.chatbot_route import chatbot_bp, init_chatbot_route

# Initialize routes
disease_bp = init_disease_route(model1, model2, disease_classes, torch_device)
skincare_bp = init_skincare_route(skin_type_model, Config.SKIN_TYPE_CLASSES, torch_device, chatbot)

# Initialize chatbot route
init_chatbot_route(chatbot)

# Register blueprints
app.register_blueprint(disease_bp, url_prefix='/api/disease')
app.register_blueprint(skincare_bp, url_prefix='/api/skincare')
app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')

print(" Disease detection route: /api/disease/analyze")
print(" Skincare analysis route: /api/skincare/analyze")
print(" Chatbot route: /api/chatbot/chat")


# Home Route


@app.route('/')
def home():
    return jsonify({
        'message': 'Skincare AI API is running! ',
        'version': '2.0',
        'endpoints': {
            'disease_detection': '/api/disease/analyze',
            'skincare_analysis': '/api/skincare/analyze',
            'chatbot': '/api/chatbot/chat'
        },
        'models': {
            'disease_detection': {
                'model': 'EfficientNet-B3 (PyTorch)',
                'classes': disease_classes,
                'num_classes': len(disease_classes),
                'confidence_threshold': Config.CONFIDENCE_THRESHOLD,
                'device': str(torch_device)
            },
            'skin_type': {
                'model': 'EfficientNet-B0 (PyTorch)',
                'classes': Config.SKIN_TYPE_CLASSES,
                'num_classes': len(Config.SKIN_TYPE_CLASSES),
                'device': str(torch_device)
            }
        }
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'models_loaded': True,
        'device': str(torch_device)
    })


# Main


if __name__ == '__main__':

    print(" STARTING FLASK SERVER")

    print("   Server: http://localhost:5000")
    print("   Disease Detection: http://localhost:5000/api/disease/analyze")
    print("   Skincare Analysis: http://localhost:5000/api/skincare/analyze")
    print("   Chatbot: http://localhost:5000/api/chatbot/chat")

    
    app.run(debug=False, host='0.0.0.0', port=5000)