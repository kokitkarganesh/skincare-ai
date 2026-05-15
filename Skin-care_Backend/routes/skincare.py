"""
Skincare Analysis Routes - With Concern-Specific Advice
"""
from flask import Blueprint, request, jsonify
from utils.image_processing import preprocess_image_pytorch
from utils.image_processing import preprocess_image_pytorch as preprocess_for_skin_type
from utils.routine_generator import generate_skincare_routine
import torch
import json

skincare_bp = Blueprint('skincare', __name__)

# Will be set by app.py
skin_type_model = None
SKIN_TYPE_CLASSES = []
device = None
chatbot = None  # Add chatbot reference

def init_skincare_route(st_model, st_classes, torch_device, chatbot_instance=None):
    """Initialize route with skin type model and chatbot"""
    global skin_type_model, SKIN_TYPE_CLASSES, device, chatbot
    skin_type_model = st_model
    SKIN_TYPE_CLASSES = st_classes
    device = torch_device
    chatbot = chatbot_instance
    return skincare_bp

@skincare_bp.route('/analyze', methods=['POST'])
def analyze_skincare():
    """
    Skincare analysis: Skin Type + User Questionnaire + Personalized Routine + Concern Advice
    """
    try:
        # Validate image
        if 'image' not in request.files:
            return jsonify({
                "success": False,
                "error": "No image provided"
            }), 400
        
        image_file = request.files['image']
        image_data = image_file.read()
        
        # Get questionnaire data
        questionnaire = {}
        if 'questionnaire' in request.form:
            try:
                questionnaire = json.loads(request.form.get('questionnaire'))
            except json.JSONDecodeError:
                return jsonify({
                    "success": False,
                    "error": "Invalid questionnaire JSON"
                }), 400
        

        # AI: Skin Type Detection (PyTorch)

        
        img_tensor = preprocess_for_skin_type(image_data , target_size=(224, 224))
        img_tensor = img_tensor.to(device)
        
        with torch.no_grad():
            skin_type_model.eval()
            outputs = skin_type_model(img_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            skin_type_confidence, skin_type_idx = torch.max(probabilities, 1)
        
        skin_type = SKIN_TYPE_CLASSES[skin_type_idx.item()]
        skin_type_confidence = float(skin_type_confidence.item() * 100)
        
        print(f" Skin Type: {skin_type} ({skin_type_confidence:.2f}%)")
        

        # User Input

        
        concerns = questionnaire.get('concerns', [])
        lifestyle = {
            'sleep': questionnaire.get('sleep_hours', 'Not specified'),
            'water_intake': questionnaire.get('water_intake', 'Not specified'),
            'stress_level': questionnaire.get('stress_level', 'Not specified'),
            'sun_exposure': questionnaire.get('sun_exposure', 'Not specified'),
            'diet': questionnaire.get('diet', 'Not specified')
        }
        

        # Generate Personalized Routine

        
        routine = generate_skincare_routine(skin_type, concerns, lifestyle)
        

        # Get AI Advice for Each Concern (from chatbot)

        
        concern_advice = []
        
        if concerns and chatbot:
            print(f" Getting advice for concerns: {concerns}")
            
            for concern in concerns:
                # Query chatbot for each concern
                concern_query = f"how to treat {concern.lower()}"
                
                try:
                    chatbot_response = chatbot.get_response(
                        concern_query,
                        skin_type=skin_type
                    )
                    
                    concern_advice.append({
                        "concern": concern,
                        "advice": chatbot_response['answer'],
                        "source": chatbot_response['source'],
                        "confidence": chatbot_response.get('confidence', 'medium')
                    })
                    
                    print(f"    {concern}: {chatbot_response['source']}")
                
                except Exception as e:
                    print(f"     Failed to get advice for {concern}: {e}")
                    # Provide fallback advice
                    concern_advice.append({
                        "concern": concern,
                        "advice": f"For {concern}, please consult the chatbot at /api/chatbot/chat for detailed advice.",
                        "source": "fallback",
                        "confidence": "low"
                    })
        
        elif concerns and not chatbot:
            # Chatbot not available - provide basic advice
            print(f"  Chatbot not available for concern advice")
            for concern in concerns:
                concern_advice.append({
                    "concern": concern,
                    "advice": f"Chatbot unavailable. Your routine has been customized for {concern}. For detailed advice, try /api/chatbot/chat when available.",
                    "source": "unavailable",
                    "confidence": "low"
                })
        

        # Compile Response

        
        response = {
            "success": True,
            "ai_analysis": {
                "skin_type": skin_type,
                "confidence": skin_type_confidence,
                "detected_class_index": int(skin_type_idx.item()),
                "model_type": "PyTorch EfficientNet-B3"
            },
            "user_input": {
                "concerns": concerns,
                "lifestyle": lifestyle
            },
            "personalized_routine": routine,
            "concern_specific_advice": concern_advice if concern_advice else None,
            "note": "All routines include natural, commercial, and home remedy options!",
            "tip": " For skin disease detection, use /api/disease/analyze"
        }
        
        return jsonify(response)
    
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": f"Invalid image: {str(e)}"
        }), 400
    
    except Exception as e:
        print(f" Error in skincare analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    
