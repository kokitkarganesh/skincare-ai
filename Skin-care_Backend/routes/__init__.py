"""
Routes initialization
"""

from .disease import init_disease_route
from .skincare import skincare_bp
from .chatbot_route import chatbot_bp


__all__ = ['init_disease_route', 'skincare_bp', 'chatbot_bp']