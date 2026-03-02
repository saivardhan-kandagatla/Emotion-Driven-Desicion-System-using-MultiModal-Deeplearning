# Emotion-Driven Decision System 🧠🚀

> **Final Year Project** | **Focused on Multimodal Deep Learning**

A full-stack web application that uses multimodal deep learning to analyze emotions from facial expressions and speech, providing intelligent decision support based on detected emotional states.

## 🌟 Key Features

- **Facial Emotion Recognition**: Real-time analysis from images or live webcam feeds.
- **Speech Emotion Recognition**: High-precision detection from audio recordings or microphone input.
- **Multimodal Fusion**: Advanced engine that combines facial and speech emotions for higher decision accuracy.
- **Actionable Insights**: An intelligent decision engine that provides recommendations based on emotional context.
- **Modern UI/UX**: A sleek, responsive dashboard built with vanilla web technologies for speed and portability.

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Deep Learning**: TensorFlow/Keras
- **Audio Processing**: Librosa
- **Image Processing**: OpenCV

### Frontend
- **Languages**: HTML5, CSS3, JavaScript (ES6+)
- **Visuals**: Chart.js / Custom CSS Animations
- **Icons**: FontAwesome / Lucide

## 🏗️ Architecture

```mermaid
graph LR
    A[Frontend] --> B[FastAPI Gateway]
    B --> C[Facial CNN]
    B --> D[Speech CNN]
    C --> E[Fusion Engine]
    D --> E[Fusion Engine]
    E --> F[Decision Output]
```

## 🚀 Quick Start

### 1. Backend Setup
1. Navigate to `backend/`
2. Create virtual environment: `python -m venv venv`
3. Activate:
   - Windows: `.\venv\Scripts\activate`
   - Linux: `source venv/bin/activate`
4. Install: `pip install -r requirements.txt`
5. Place models in `backend/models/`:
   - `facial_model.h5`
   - `speech_model.h5`
6. Run: `uvicorn app.main:app --reload`

### 2. Frontend Setup
1. Navigate to `frontend/`
2. Option 1: Open `index.html` directly.
3. Option 2: Run `python -m http.server 8080`.

## 📁 Project Structure

```text
emotion-decision-system/
├── backend/
│   ├── app/                  # FastAPI logic
│   ├── models/               # Pre-trained .h5 models
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── index.html            # Main entry
│   ├── css/                  # Styling
│   └── js/                   # Interaction logic
├── .gitignore                # Git exclude rules
├── LICENSE                   # MIT License
└── README.md                 # Documentation
```
## Screenshots
<img width="712" height="369" alt="Screenshot 2026-02-25 084759" src="https://github.com/user-attachments/assets/f9b97bb0-c8b8-4c02-8703-f3509b6e71db" />
<img width="707" height="439" alt="Screenshot 2026-02-25 084713" src="https://github.com/user-attachments/assets/c1ba75b3-94f7-4971-bfd4-38c251d611dc" />
<img width="739" height="378" alt="Screenshot 2026-02-25 084613" src="https://github.com/user-attachments/assets/9d9d5564-c123-42a7-b68c-0734c59fa076" />
<img width="704" height="308" alt="Screenshot 2026-02-25 084558" src="https://github.com/user-attachments/assets/dbb73a12-2303-4400-a50a-8365c938acc8" />
<img width="748" height="440" alt="Screenshot 2026-02-25 084527" src="https://github.com/user-attachments/assets/baa5550e-e408-4283-ac0e-6f2d9e2b14f3" />
<img width="933" height="362" alt="Screenshot 2026-02-25 084505" src="https://github.com/user-attachments/assets/7df3dd72-ff12-411e-9afb-badb0233d62c" />
<img width="747" height="438" alt="Screenshot 2026-02-25 084246" src="https://github.com/user-attachments/assets/556a943c-0f6f-424c-a1fc-9cec0e05dfcd" />
<img width="942" height="433" alt="Screenshot 2026-02-25 084200" src="https://github.com/user-attachments/assets/5184fd76-63fa-468d-94e1-f2bc1c485143" />
<img width="940" height="326" alt="Screenshot 2026-02-25 084107" src="https://github.com/user-attachments/assets/768a13fa-8e7e-48a1-a290-efe62524efa0" />



## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---
*Created with ❤️ by Kandagatla Sai Vardhan*
