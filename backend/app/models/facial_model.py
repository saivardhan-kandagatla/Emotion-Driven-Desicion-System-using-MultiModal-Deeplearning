"""
Facial Emotion Detection Model Wrapper
"""
import cv2
import numpy as np
from typing import Dict, Tuple, Optional
import os

try:
    from tensorflow import keras
except ImportError:
    import keras

from app.core.config import settings
from app.utils.preprocessing import preprocess_image, extract_face


class FacialEmotionModel:
    """
    Wrapper for facial emotion detection CNN model
    """
    
    def __init__(self):
        self.model = None
        self.emotions = settings.facial_emotions
        self.input_shape = settings.facial_input_shape
        self.model_loaded = False
    
    def load_model(self) -> bool:
        """
        Load the pre-trained facial emotion model by rebuilding architecture and loading weights
        
        Returns:
            True if model loaded successfully, False otherwise
        """
        try:
            if not os.path.exists(settings.facial_model_path):
                print(f"Warning: Model file not found at {settings.facial_model_path}")
                print("Please place your trained facial emotion model in backend/models/facial_model.h5")
                return False
            
            # Rebuild model architecture (exactly matching shapes in facial_model.h5)
            from tensorflow.keras.models import Sequential
            from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
            
            self.model = Sequential()
            # Note: Weights are in channels_first format (32, 3, 3, 3)
            self.model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(3, 32, 32), data_format='channels_first'))
            self.model.add(MaxPooling2D(pool_size=(2, 2), data_format='channels_first'))
            self.model.add(Dropout(0.25))
            self.model.add(Conv2D(32, (3, 3), activation='relu', data_format='channels_first'))
            self.model.add(MaxPooling2D(pool_size=(2, 2), data_format='channels_first'))
            self.model.add(Dropout(0.25))
            self.model.add(Flatten())
            self.model.add(Dense(256, activation='relu'))
            self.model.add(Dropout(0.5))
            self.model.add(Dense(7, activation='softmax'))  # 7 emotions
            
            # Compile model
            self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
            
            # Load weights
            self.model.load_weights(settings.facial_model_path)
            
            self.model_loaded = True
            print("✓ Facial emotion model loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading facial emotion model: {str(e)}")
            self.model_loaded = False
            return False
    
    def predict(self, image_data: np.ndarray) -> Dict:
        """
        Predict emotion from image
        
        Args:
            image_data: Input image as numpy array (BGR format from OpenCV)
        
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
            # Extract face region
            face = extract_face(image_data)
            
            # Preprocess image for RGB input (32x32x3)
            processed = self._preprocess_for_rgb(face)
            
            # Make prediction
            predictions = self.model.predict(processed, verbose=0)[0]
            
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
    
    def _preprocess_for_rgb(self, image_data: np.ndarray) -> np.ndarray:
        """
        Preprocess image for RGB model (32x32x3)
        """
        # Ensure RGB format
        if len(image_data.shape) == 2:
            # Grayscale to RGB
            image_rgb = cv2.cvtColor(image_data, cv2.COLOR_GRAY2RGB)
        elif image_data.shape[2] == 4:
            # RGBA to RGB
            image_rgb = cv2.cvtColor(image_data, cv2.COLOR_BGRA2RGB)
        else:
            # Already BGR, convert to RGB
            image_rgb = cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)
        
        # Resize to 32x32
        resized = cv2.resize(image_rgb, (32, 32))
        
        # Normalize
        normalized = resized / 255.0
        
        # Transpose to channels_first (C, H, W)
        transposed = normalized.transpose(2, 0, 1)
        
        # Add batch dimension
        preprocessed = np.expand_dims(transposed, axis=0)
        
        return preprocessed
    
    
    def predict_from_file(self, image_path: str) -> Dict:
        """
        Predict emotion from image file
        
        Args:
            image_path: Path to image file
        
        Returns:
            Dictionary with emotion predictions
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                return {
                    "error": "Could not read image file",
                    "emotion": "Unknown",
                    "confidence": 0.0
                }
            
            return self.predict(image)
        
        except Exception as e:
            return {
                "error": f"File reading error: {str(e)}",
                "emotion": "Unknown",
                "confidence": 0.0
            }


# Singleton instance
facial_model = FacialEmotionModel()
