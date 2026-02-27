"""
Script to rebuild complete Keras models from architecture JSON + weights
Run this once to create the complete model files
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TF warnings

from tensorflow.keras.models import model_from_json, Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
import json

# Paths
base_path = r"C:\Users\saiva\Downloads\FaceSpeechEmotion\model"
output_path = r"C:\Users\saiva\.gemini\antigravity\scratch\emotion-decision-system\backend\models"

print("=" * 70)
print("Model Rebuilding Script")
print("=" * 70)

# ===== 1. FACIAL EMOTION MODEL =====
print("\n[1/2] Building Facial Emotion Model...")

try:
    # Check if JSON architecture exists
    facial_json_path = os.path.join(base_path, "cnnmodel.json")
    facial_weights_path = os.path.join(base_path, "cnnmodel_weights.h5")
    
    if os.path.exists(facial_json_path):
        print(f"  ✓ Found architecture: {facial_json_path}")
        print(f"  ✓ Found weights: {facial_weights_path}")
        
        # Load  architecture
        with open(facial_json_path, 'r') as json_file:
            loaded_model_json = json_file.read()
        facial_model = model_from_json(loaded_model_json)
        
        # Load weights
        facial_model.load_weights(facial_weights_path)
        
        # Save complete model
        output_facial_path = os.path.join(output_path, "facial_model.h5")
        facial_model.save(output_facial_path)
        
        print(f"  ✓ Saved complete facial model to: {output_facial_path}")
        print(f"  Model input shape: {facial_model.input_shape}")
        print(f"  Model output shape: {facial_model.output_shape}")
    else:
        # Architecture file doesn't exist, rebuild from scratch
        print("  ⚠ JSON architecture not found. Rebuilding from training script...")
        
        # Rebuild the architecture based on FaceCNNTrain.py
        facial_model = Sequential()
        facial_model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
        facial_model.add(MaxPooling2D(pool_size=(2, 2)))
        facial_model.add(Dropout(0.25))
        facial_model.add(Conv2D(64, (3, 3), activation='relu'))
        facial_model.add(MaxPooling2D(pool_size=(2, 2)))
        facial_model.add(Dropout(0.25))
        facial_model.add(Flatten())
        facial_model.add(Dense(128, activation='relu'))
        facial_model.add(Dropout(0.5))
        facial_model.add(Dense(7, activation='softmax'))  # 7 emotions
        
        # Load weights
        facial_model.load_weights(facial_weights_path)
        
        # Save complete model
        output_facial_path = os.path.join(output_path, "facial_model.h5")
        facial_model.save(output_facial_path)
        
        print(f"  ✓ Rebuilt and saved facial model to: {output_facial_path}")
        print(f"  Model input shape: {facial_model.input_shape}")
        print(f"  Model output shape: {facial_model.output_shape}")
    
    print("  ✅ Facial model ready!")
    
except Exception as e:
    print(f"  ❌ Error with facial model: {str(e)}")

# ===== 2. SPEECH EMOTION MODEL =====
print("\n[2/2] Building Speech Emotion Model...")

try:
    speech_json_path = os.path.join(base_path, "speechmodel.json")
    speech_weights_path = os.path.join(base_path, "speech_weights.h5")
    
    if os.path.exists(speech_json_path):
        print(f"  ✓ Found architecture: {speech_json_path}")
        print(f"  ✓ Found weights: {speech_weights_path}")
        
        # Load architecture
        with open(speech_json_path, 'r') as json_file:
            loaded_model_json = json_file.read()
        speech_model = model_from_json(loaded_model_json)
        
        # Load weights
        speech_model.load_weights(speech_weights_path)
        
        # Save complete model
        output_speech_path = os.path.join(output_path, "speech_model.h5")
        speech_model.save(output_speech_path)
        
        print(f"  ✓ Saved complete speech model to: {output_speech_path}")
        print(f"  Model input shape: {speech_model.input_shape}")
        print(f"  Model output shape: {speech_model.output_shape}")
    else:
        # Architecture file doesn't exist, rebuild from scratch
        print("  ⚠ JSON architecture not found. Rebuilding from training script...")
        
        # Rebuild the architecture based on SpeechTrain.py
        speech_model = Sequential()
        speech_model.add(Conv2D(32, (1, 1), input_shape=(180, 1, 1), activation='relu'))
        speech_model.add(MaxPooling2D(pool_size=(1, 1)))
        speech_model.add(Conv2D(32, (1, 1), activation='relu'))
        speech_model.add(MaxPooling2D(pool_size=(1, 1)))
        speech_model.add(Flatten())
        speech_model.add(Dense(units=256, activation='relu'))
        speech_model.add(Dense(units=8, activation='softmax'))  # 8 classes from training
        
        # Load weights
        speech_model.load_weights(speech_weights_path)
        
        # Save complete model
        output_speech_path = os.path.join(output_path, "speech_model.h5")
        speech_model.save(output_speech_path)
        
        print(f"  ✓ Rebuilt and saved speech model to: {output_speech_path}")
        print(f"  Model input shape: {speech_model.input_shape}")
        print(f"  Model output shape: {speech_model.output_shape}")
    
    print("  ✅ Speech model ready!")
    
except Exception as e:
    print(f"  ❌ Error with speech model: {str(e)}")

print("\n" + "=" * 70)
print("✅ Model rebuilding complete!")
print("=" * 70)
print("\nNow you can restart your backend server:")
print("  cd backend")
print("  venv\\Scripts\\activate")
print("  uvicorn app.main:app --reload")
print("\nThe models should load successfully!")
