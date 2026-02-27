"""
Speech Emotion Detection Model Wrapper
"""
import numpy as np
from typing import Dict
import os

try:
    from tensorflow import keras
except ImportError:
    import keras

from app.core.config import settings
from app.utils.preprocessing import extract_audio_features


class SpeechEmotionModel:
    """
    Wrapper for speech emotion detection CNN model
    """
    
    def __init__(self):
        self.model = None
        self.emotions = settings.speech_emotions
        self.model_loaded = False
    
    def load_model(self) -> bool:
        """
        Load the pre-trained speech emotion model
        
        Returns:
            True if model loaded successfully, False otherwise
        """
        try:
            if not os.path.exists(settings.speech_model_path):
                print(f"Warning: Model file not found at {settings.speech_model_path}")
                print("Please place your trained speech emotion model in backend/models/speech_model.h5")
                return False
            
            # Rebuild architecture (from SpeechTrain.py via rebuild_models.py)
            from tensorflow.keras.models import Sequential
            from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
            
            self.model = Sequential()
            # Speech model weights are in channels_last format (1, 1, 1, 32)
            self.model.add(Conv2D(32, (1, 1), input_shape=(180, 1, 1), activation='relu'))
            self.model.add(MaxPooling2D(pool_size=(1, 1)))
            self.model.add(Conv2D(32, (1, 1), activation='relu'))
            self.model.add(MaxPooling2D(pool_size=(1, 1)))
            self.model.add(Flatten())
            self.model.add(Dense(units=256, activation='relu'))
            self.model.add(Dense(units=9, activation='softmax'))  # 9 classes found in weights
            
            # Compile model
            self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
            
            # Load weights
            self.model.load_weights(settings.speech_model_path)
            
            self.model_loaded = True
            print("✓ Speech emotion model loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading speech emotion model: {str(e)}")
            self.model_loaded = False
            return False
    
    def predict(self, audio_path: str) -> Dict:
        """
        Predict emotion from audio file
        
        Args:
            audio_path: Path to audio file
        
        Returns:
            Dictionary with emotion predictions and confidence scores
        """
        if not self.model_loaded:
            return {
                "error": "Model not loaded. Please add your trained model to backend/models/",
                "emotion": "Unknown",
                "confidence": 0.0,
                "probabilities": {}
            }
        
        try:
            # Extract audio features
            features = extract_audio_features(audio_path)
            
            # Make prediction
            predictions = self.model.predict(features, verbose=0)[0]
            
            # Get top emotion
            top_emotion_idx = np.argmax(predictions)
            top_emotion = self.emotions[top_emotion_idx]
            confidence = float(predictions[top_emotion_idx])
            
            # Create probabilities dictionary
            probabilities = {
                emotion: float(prob)
                for emotion, prob in zip(self.emotions, predictions)
            }
            
            return {
                "emotion": top_emotion,
                "confidence": confidence,
                "probabilities": probabilities,
                "all_emotions": self.emotions
            }
        
        except Exception as e:
            return {
                "error": f"Prediction error: {str(e)}",
                "emotion": "Unknown",
                "confidence": 0.0,
                "probabilities": {}
            }


# Singleton instance
speech_model = SpeechEmotionModel()
