"""
Emotion Detection API Endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict
import cv2
import numpy as np
import os
import tempfile

from app.models import facial_model, speech_model, text_model, fusion_model

router = APIRouter(prefix="/emotion", tags=["emotion"])


@router.post("/facial", response_model=Dict)
async def analyze_facial_emotion(
    image: UploadFile = File(..., description="Image file for facial emotion analysis")
):
    """
    Analyze facial emotion from uploaded image
    
    - **image**: Image file (jpg, png, etc.)
    
    Returns emotion prediction with confidence scores
    """
    try:
        # Read image file
        contents = await image.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Predict emotion
        result = facial_model.predict(img)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@router.post("/speech", response_model=Dict)
async def analyze_speech_emotion(
    audio: UploadFile = File(..., description="Audio file for speech emotion analysis")
):
    """
    Analyze speech emotion from uploaded audio file
    
    - **audio**: Audio file (wav, mp3, etc.)
    
    Returns emotion prediction with confidence scores
    """
    try:
        # Save audio to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio.filename)[1]) as tmp:
            contents = await audio.read()
            tmp.write(contents)
            tmp_path = tmp.name
        
        try:
            # Predict emotion
            result = speech_model.predict(tmp_path)
            
            if "error" in result:
                raise HTTPException(status_code=500, detail=result["error"])
            
            return result
        
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@router.post("/text", response_model=Dict)
async def analyze_text_emotion(
    text: str = File(..., description="Text for emotion analysis")
):
    """
    Analyze emotion from text
    
    - **text**: Text string
    
    Returns emotion prediction with confidence scores
    """
    try:
        # If text is sent as a file/multipart, it might be bytes
        if isinstance(text, bytes):
            text = text.decode("utf-8")
            
        result = text_model.predict(text)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@router.post("/multimodal", response_model=Dict)
async def analyze_multimodal_emotion(
    image: UploadFile = File(None, description="Image file for facial emotion analysis"),
    audio: UploadFile = File(None, description="Audio file for speech emotion analysis"),
    text: str = File(None, description="Text for emotion analysis")
):
    """
    Analyze emotion using multiple modalities (facial, speech, text)
    
    - **image**: Optional image file
    - **audio**: Optional audio file
    - **text**: Optional text string
    
    Returns fused emotion prediction combining available modalities
    """
    try:
        facial_result = None
        speech_result = None
        text_result = None
        
        # Process image if provided
        if image:
            image_contents = await image.read()
            if image_contents:
                nparr = np.frombuffer(image_contents, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                if img is not None:
                    facial_result = facial_model.predict(img)
        
        # Process audio if provided
        if audio:
            audio_contents = await audio.read()
            if audio_contents:
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio.filename)[1]) as tmp:
                    tmp.write(audio_contents)
                    tmp_path = tmp.name
                
                try:
                    speech_result = speech_model.predict(tmp_path)
                finally:
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
        
        # Process text if provided
        if text:
            if isinstance(text, bytes):
                text = text.decode("utf-8")
            text_result = text_model.predict(text)
        
        # Fuse predictions
        fused_result = fusion_model.fuse_predictions(
            facial_result=facial_result, 
            speech_result=speech_result,
            text_result=text_result
        )
        
        # Add individual results
        if facial_result:
            fused_result["facial_analysis"] = facial_result
        if speech_result:
            fused_result["speech_analysis"] = speech_result
        if text_result:
            fused_result["text_analysis"] = text_result
        
        return fused_result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
