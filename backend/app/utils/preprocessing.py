"""
Preprocessing utilities for emotion detection
"""
import cv2
import numpy as np
import librosa
from typing import Tuple


def preprocess_image(image_data: np.ndarray, target_size: Tuple[int, int] = (48, 48)) -> np.ndarray:
    """
    Preprocess image for facial emotion detection
    
    Args:
        image_data: Input image as numpy array
        target_size: Target size for the model
    
    Returns:
        Preprocessed image ready for model input
    """
    # Convert to grayscale if needed
    if len(image_data.shape) == 3 and image_data.shape[2] == 3:
        gray = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
    else:
        gray = image_data
    
    # Resize to target size
    resized = cv2.resize(gray, target_size)
    
    # Normalize pixel values
    normalized = resized / 255.0
    
    # Add channel dimension
    preprocessed = np.expand_dims(normalized, axis=-1)
    
    # Add batch dimension
    preprocessed = np.expand_dims(preprocessed, axis=0)
    
    return preprocessed


def extract_face(image_data: np.ndarray) -> np.ndarray:
    """
    Extract face region from image using Haar Cascade
    
    Args:
        image_data: Input image as numpy array
    
    Returns:
        Cropped face region or original image if no face detected
    """
    # Load Haar Cascade for face detection
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    
    # Convert to grayscale for detection
    if len(image_data.shape) == 3:
        gray = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
    else:
        gray = image_data
    
    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    
    # Return first face if detected
    if len(faces) > 0:
        x, y, w, h = faces[0]
        return image_data[y:y+h, x:x+w]
    
    return image_data


def extract_audio_features(
    audio_path: str,
    sr: int = 22050,
    n_mfcc: int = 40,
    duration: float = 3.0
) -> np.ndarray:
    """
    Extract MFCC features from audio file
    
    Args:
        audio_path: Path to audio file
        sr: Sample rate
        n_mfcc: Number of MFCC coefficients
        duration: Maximum duration to process (seconds)
    
    Returns:
        Extracted features as numpy array
    """
    # Load audio file
    audio, sample_rate = librosa.load(audio_path, sr=sr, duration=duration)
    
    # Extract MFCC features
    mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=n_mfcc)
    
    # Calculate statistics across time
    mfccs_mean = np.mean(mfccs, axis=1)
    mfccs_std = np.std(mfccs, axis=1)
    
    # Combine mean and std
    features = np.concatenate([mfccs_mean, mfccs_std])
    
    # Add batch dimension
    features = np.expand_dims(features, axis=0)
    
    return features


def extract_audio_features_advanced(
    audio_path: str,
    sr: int = 22050,
    n_mfcc: int = 40
) -> np.ndarray:
    """
    Extract advanced audio features including MFCC, chroma, and spectral features
    
    Args:
        audio_path: Path to audio file
        sr: Sample rate
        n_mfcc: Number of MFCC coefficients
    
    Returns:
        Combined feature vector
    """
    # Load audio
    audio, sample_rate = librosa.load(audio_path, sr=sr)
    
    # MFCC
    mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=n_mfcc)
    mfcc_mean = np.mean(mfcc, axis=1)
    
    # Chroma
    chroma = librosa.feature.chroma_stft(y=audio, sr=sample_rate)
    chroma_mean = np.mean(chroma, axis=1)
    
    # Spectral features
    spectral_contrast = librosa.feature.spectral_contrast(y=audio, sr=sample_rate)
    spectral_contrast_mean = np.mean(spectral_contrast, axis=1)
    
    # Zero crossing rate
    zcr = librosa.feature.zero_crossing_rate(audio)
    zcr_mean = np.mean(zcr)
    
    # Combine all features
    features = np.concatenate([
        mfcc_mean,
        chroma_mean,
        spectral_contrast_mean,
        [zcr_mean]
    ])
    
    # Add batch dimension
    features = np.expand_dims(features, axis=0)
    
    return features
