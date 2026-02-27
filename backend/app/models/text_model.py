"""
Text Emotion Detection Model Wrapper
"""
from typing import Dict
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from app.core.config import settings


class TextEmotionModel:
    """
    Wrapper for text emotion detection using VADER sentiment analysis
    """
    
    def __init__(self):
        self.analyzer = None
        self.emotions = settings.text_emotions
        self.model_loaded = False
    
    def load_model(self) -> bool:
        """
        Initialize the VADER sentiment analyzer
        
        Returns:
            True if initialized successfully, False otherwise
        """
        try:
            self.analyzer = SentimentIntensityAnalyzer()
            self.model_loaded = True
            print("✓ Text emotion model (VADER) initialized successfully")
            return True
        except Exception as e:
            print(f"Error initializing text emotion model: {str(e)}")
            self.model_loaded = False
            return False
    
    def predict(self, text: str) -> Dict:
        """
        Predict emotion from text
        
        Args:
            text: Input text string
        
        Returns:
            Dictionary with emotion predictions and confidence scores
        """
        if not self.model_loaded:
            if not self.load_model():
                return {
                    "error": "Model not loaded",
                    "emotion": "Unknown",
                    "confidence": 0.0,
                    "probabilities": {}
                }
        
        try:
            # Get VADER scores
            scores = self.analyzer.polarity_scores(text)
            
            # Map VADER scores to our emotions: Negative, Neutral, Positive
            # compound score ranges from -1 (negative) to 1 (positive)
            compound = scores['compound']
            
            # Create probabilities based on the scores
            # VADER provides neg, neu, pos scores that sum to 1.0 (excluding compound)
            probabilities = {
                "Negative": float(scores['neg']),
                "Neutral": float(scores['neu']),
                "Positive": float(scores['pos'])
            }
            
            # Determine top emotion based on compound score for better accuracy
            if compound >= 0.05:
                top_emotion = "Positive"
                confidence = float(scores['pos'])
            elif compound <= -0.05:
                top_emotion = "Negative"
                confidence = float(scores['neg'])
            else:
                top_emotion = "Neutral"
                confidence = float(scores['neu'])
            
            return {
                "emotion": top_emotion,
                "confidence": confidence,
                "probabilities": probabilities,
                "all_emotions": self.emotions,
                "compound_score": float(compound)
            }
        
        except Exception as e:
            return {
                "error": f"Prediction error: {str(e)}",
                "emotion": "Unknown",
                "confidence": 0.0,
                "probabilities": {}
            }


# Singleton instance
text_model = TextEmotionModel()
