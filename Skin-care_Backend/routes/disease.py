from flask import Blueprint, request, jsonify
import torch
from PIL import Image
import io
import numpy as np
from torchvision import transforms
from config import Config
import re

# Globals
disease_model1 = None
disease_model2 = None
disease_classes = None
torch_device = None


# CLEAN LABEL FUNCTION
def clean_label(label):
    label = re.sub(r'^\d+\.\s*', '', label)
    label = re.sub(r'\s*[-]?\s*\d+(\.\d+)?k?', '', label)
    return label.strip()


def init_disease_route(model1, model2, classes, device):
    global disease_model1, disease_model2, disease_classes, torch_device

    disease_model1 = model1
    disease_model2 = model2
    disease_classes = classes
    torch_device = device

    blueprint = Blueprint('disease', __name__)

    @blueprint.route('/analyze', methods=['POST'])
    def analyze_disease():
        try:
            if 'image' not in request.files:
                return jsonify({'error': 'No image provided'}), 400

            image = request.files['image'].read()

            img = Image.open(io.BytesIO(image)).convert('RGB')

            transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(Config.IMAGE_MEAN, Config.IMAGE_STD)
            ])

            img_tensor = transform(img).unsqueeze(0).to(torch_device)

            # 🔥 ENSEMBLE
            with torch.no_grad():
                out1 = disease_model1(img_tensor)
                out2 = disease_model2(img_tensor)

                w1 = Config.ENSEMBLE_WEIGHTS["efficientnet"]
                w2 = Config.ENSEMBLE_WEIGHTS["resnet"]

                outputs = (w1 * out1 + w2 * out2)

                probs = torch.softmax(outputs, dim=1).cpu().numpy()[0]

            # Top-K
            top_k = np.argsort(probs)[-Config.TOP_K_PREDICTIONS:][::-1]

            results = []
            for i, idx in enumerate(top_k):
                raw = disease_classes[idx]
                clean = clean_label(raw)

                results.append({
                    "disease": clean,
                    "raw_label": raw,
                    "confidence": round(float(probs[idx] * 100), 2),
                    "rank": i + 1
                })

            top_conf = results[0]["confidence"]

            return jsonify({
                "status": "success" if top_conf >= Config.CONFIDENCE_THRESHOLD else "low_confidence",
                "model": Config.DISEASE_MODEL_NAME,
                "top_prediction": results[0],
                "all_predictions": results,
                "warning": top_conf < Config.CONFIDENCE_THRESHOLD
            })

        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({"error": str(e)}), 500

    return blueprint