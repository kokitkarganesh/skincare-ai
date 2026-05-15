"""
Chatbot Routes
"""
from flask import Blueprint, request, jsonify

chatbot_bp = Blueprint('chatbot', __name__)

# Will be set by app.py
chatbot = None

def init_chatbot_route(chatbot_instance):
    """Initialize route with chatbot instance"""
    global chatbot
    chatbot = chatbot_instance

@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    """
    Hybrid chatbot endpoint
    
    Expected JSON:
    {
        "message": "how to treat acne",
        "skin_type": "Oily" (optional)
    }
    
    Returns: Chatbot response
    """
    try:
        data = request.json
        
        # Validate request
        if not data or 'message' not in data:
            return jsonify({
                "success": False,
                "error": "No message provided"
            }), 400
        
        user_message = data.get('message', '')
        user_skin_type = data.get('skin_type', None)
        
        # Validate message
        if not user_message or not user_message.strip():
            return jsonify({
                "success": False,
                "error": "Empty message"
            }), 400
        
        # Get chatbot response
        result = chatbot.get_response(user_message, user_skin_type)
        
        return jsonify({
            "success": True,
            "message": result['answer'],
            "source": result['source'],
            "similarity_score": result.get('similarity_score', 0),
            "matched_question": result.get('matched_question'),
            "confidence": result.get('confidence', 'medium'),
            "skin_type_context": user_skin_type
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500