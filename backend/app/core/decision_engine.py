"""
Decision Engine - Maps emotions to actionable recommendations
"""
from typing import Dict, List
from app.core.config import settings


class DecisionEngine:
    """
    Core decision logic that provides recommendations based on detected emotions
    """
    
    def __init__(self):
        self.decision_rules = self._initialize_rules()
    
    def _initialize_rules(self) -> Dict:
        """
        Initialize decision rules mapping emotions to recommendations
        """
        return {
            "Happy": {
                "recommendations": [
                    "Great mood detected! This is an excellent time for creative work.",
                    "Consider tackling challenging tasks while you're feeling positive.",
                    "Share your positive energy with team collaborations."
                ],
                "color": "#4CAF50",
                "icon": "😊"
            },
            "Sad": {
                "recommendations": [
                    "Take a short break and practice self-care.",
                    "Consider lighter, routine tasks for now.",
                    "Reach out to someone you trust if you need support.",
                    "Remember: it's okay to not be okay. Take your time."
                ],
                "color": "#2196F3",
                "icon": "😔"
            },
            "Angry": {
                "recommendations": [
                    "Take deep breaths and step away for a moment.",
                    "Avoid making important decisions right now.",
                    "Try a brief walk or physical activity to release tension.",
                    "Address the source of frustration when you're calmer."
                ],
                "color": "#F44336",
                "icon": "😠"
            },
            "Neutral": {
                "recommendations": [
                    "Good baseline state for focused work.",
                    "Ideal time for analytical or detail-oriented tasks.",
                    "Consider planning and organizing activities."
                ],
                "color": "#9E9E9E",
                "icon": "😐"
            },
            "Fear": {
                "recommendations": [
                    "Acknowledge your concerns - they're valid.",
                    "Break down overwhelming tasks into smaller steps.",
                    "Seek support or guidance if needed.",
                    "Practice grounding techniques to reduce anxiety."
                ],
                "color": "#9C27B0",
                "icon": "😰"
            },
            "Surprise": {
                "recommendations": [
                    "Take a moment to process new information.",
                    "Unexpected situations can lead to opportunities.",
                    "Stay open-minded and adaptable."
                ],
                "color": "#FF9800",
                "icon": "😲"
            },
            "Disgust": {
                "recommendations": [
                    "Identify and address the source of discomfort.",
                    "Take a break from the current situation if possible.",
                    "Focus on tasks that feel more aligned with your values."
                ],
                "color": "#795548",
                "icon": "🤢"
            }
        }
    
    def get_recommendation(
        self, 
        emotion: str, 
        confidence: float
    ) -> Dict:
        """
        Get recommendation based on detected emotion
        
        Args:
            emotion: Detected emotion label
            confidence: Confidence score (0-1)
        
        Returns:
            Dictionary with recommendations and metadata
        """
        if emotion not in self.decision_rules:
            emotion = "Neutral"
        
        rule = self.decision_rules[emotion]
        
        return {
            "emotion": emotion,
            "confidence": confidence,
            "recommendations": rule["recommendations"],
            "color": rule["color"],
            "icon": rule["icon"],
            "confidence_level": self._get_confidence_level(confidence)
        }
    
    def get_multimodal_recommendation(
        self,
        facial_emotion: str,
        facial_confidence: float,
        speech_emotion: str,
        speech_confidence: float,
        fused_emotion: str,
        fused_confidence: float,
        text_emotion: str = None,
        text_confidence: float = 0.0
    ) -> Dict:
        """
        Get recommendation based on multimodal emotion analysis
        """
        # Use the fused emotion for primary recommendation
        primary_rec = self.get_recommendation(fused_emotion, fused_confidence)
        
        # Add context about individual modalities
        modal_analysis = {
            "facial": {
                "emotion": facial_emotion,
                "confidence": facial_confidence
            },
            "speech": {
                "emotion": speech_emotion,
                "confidence": speech_confidence
            }
        }
        
        if text_emotion:
            modal_analysis["text"] = {
                "emotion": text_emotion,
                "confidence": text_confidence
            }
        
        modal_analysis["fused"] = {
            "emotion": fused_emotion,
            "confidence": fused_confidence
        }
        
        # Check for emotional conflict
        conflicts = []
        if facial_emotion != speech_emotion:
            conflicts.append(f"facial ({facial_emotion}) vs speech ({speech_emotion})")
            
        if text_emotion:
            # Map text sentiments to core emotions for conflict detection
            # Note: This is a simplified mapping for conflict logic
            sentiment_map = {
                "Positive": ["Happy", "Surprise"],
                "Negative": ["Angry", "Sad", "Fear", "Disgust"],
                "Neutral": ["Neutral"]
            }
            
            # Check if facial emotion aligns with text sentiment
            if facial_emotion not in sentiment_map.get(text_emotion, []):
                conflicts.append(f"facial ({facial_emotion}) vs text ({text_emotion})")
        
        if conflicts:
            primary_rec["note"] = (
                f"Emotional divergence detected: {', '.join(conflicts)}. "
                f"This might suggest mixed emotions or nuanced context."
            )
        
        primary_rec["modal_analysis"] = modal_analysis
        return primary_rec
    
    def _get_confidence_level(self, confidence: float) -> str:
        """Convert confidence score to human-readable level"""
        if confidence >= 0.8:
            return "Very High"
        elif confidence >= 0.6:
            return "High"
        elif confidence >= 0.4:
            return "Medium"
        else:
            return "Low"


# Singleton instance
decision_engine = DecisionEngine()
