import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_multimodal_recommendation_with_text():
    print("Testing Multimodal Recommendation with Text...")
    
    # Simulate a scenario where there's a conflict between facial (Angry) and text (Positive)
    payload = {
        "facial_emotion": "Angry",
        "facial_confidence": 0.9,
        "speech_emotion": "Angry",
        "speech_confidence": 0.8,
        "text_emotion": "Positive",
        "text_confidence": 0.95,
        "fused_emotion": "Happy",
        "fused_confidence": 0.7
    }
    
    try:
        response = requests.post(f"{BASE_URL}/decision/recommend-multimodal", json=payload)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if "note" in result:
            print(f"\n✓ Found expected conflict note: {result['note']}")
        else:
            print("\n✗ Expected conflict note not found!")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_multimodal_recommendation_with_text()
