import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_text_emotion():
    print("Testing Text Emotion Detection...")
    payload = {'text': 'I am absolutely thrilled and happy today!'}
    try:
        response = requests.post(f"{BASE_URL}/emotion/text", data=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

def test_multimodal_with_text():
    print("\nTesting Multimodal with Text Only...")
    payload = {'text': 'I am feeling very sad and disappointed.'}
    try:
        # multimodal endpoint now accepts optional fields
        response = requests.post(f"{BASE_URL}/emotion/multimodal", data=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Verification Script")
    print("Make sure the backend is running with 'uvicorn app.main:app --reload'")
    test_text_emotion()
    test_multimodal_with_text()
