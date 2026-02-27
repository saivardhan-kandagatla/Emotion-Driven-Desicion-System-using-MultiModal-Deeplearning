# Backend - Emotion-Driven Decision System

FastAPI backend for emotion detection and decision support.

## Setup

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Add Your Models

Copy your pre-trained models to the `models/` directory:
```
models/
├── facial_model.h5      # Your facial emotion CNN
└── speech_model.h5      # Your speech emotion CNN
```

## Run Server

```bash
uvicorn app.main:app --reload
```

Server will start at: http://localhost:8000
API Docs: http://localhost:8000/docs

## API Endpoints

- `POST /api/emotion/facial` - Upload image for facial emotion analysis
- `POST /api/emotion/speech` - Upload audio for speech emotion analysis
- `POST /api/emotion/multimodal` - Combined analysis (image + audio)
- `POST /api/decision/recommend` - Get decision recommendations
