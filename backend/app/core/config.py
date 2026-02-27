"""
Configuration settings for the Emotion-Driven Decision System
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    app_name: str = "Emotion-Driven Decision System"
    version: str = "1.0.0"
    api_prefix: str = "/api"
    
    # CORS Settings
    allowed_origins: List[str] = [
        "http://localhost:8080",
        "http://localhost:3000",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:3000",
        "*"  # Allow all for development
    ]
    
    # Model Paths
    base_dir: str = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    facial_model_path: str = os.path.join(base_dir, "models", "facial_model.h5")
    speech_model_path: str = os.path.join(base_dir, "models", "speech_model.h5")
    
    # Emotion Labels (customize based on your models)
    facial_emotions: List[str] = [
        "Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"
    ]
    speech_emotions: List[str] = [
        "Neutral", "Calm", "Happy", "Sad", "Angry", "Fearful", "Disgust", "Surprised", "Excited"
    ]
    text_emotions: List[str] = [
        "Negative", "Neutral", "Positive"
    ]
    
    # Model Settings
    facial_input_shape: tuple = (32, 32, 3)  # RGB images (from original training)
    speech_input_shape: tuple = (180, 1, 1)  # Audio features (from original training)
    speech_feature_dim: int = 180  # MFCC + chroma + mel features
    
    # Fusion Settings
    fusion_weights: dict = {
        "facial": 0.4,
        "speech": 0.3,
        "text": 0.3
    }
    
    # Decision Engine Settings
    confidence_threshold: float = 0.6
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
