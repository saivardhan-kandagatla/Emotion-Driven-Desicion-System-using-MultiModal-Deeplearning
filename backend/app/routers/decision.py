"""
Decision Support API Endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional

from app.core import decision_engine

router = APIRouter(prefix="/decision", tags=["decision"])


class EmotionInput(BaseModel):
    """Input model for single emotion"""
    emotion: str
    confidence: float


class MultimodalEmotionInput(BaseModel):
    """Input model for multimodal emotion"""
    facial_emotion: Optional[str] = None
    facial_confidence: Optional[float] = 0.0
    speech_emotion: Optional[str] = None
    speech_confidence: Optional[float] = 0.0
    text_emotion: Optional[str] = None
    text_confidence: Optional[float] = None
    fused_emotion: str
    fused_confidence: float


@router.post("/recommend", response_model=Dict)
async def get_recommendation(emotion_input: EmotionInput):
    """
    Get decision recommendations based on detected emotion
    
    - **emotion**: Detected emotion label
    - **confidence**: Confidence score (0-1)
    
    Returns actionable recommendations
    """
    try:
        recommendation = decision_engine.get_recommendation(
            emotion_input.emotion,
            emotion_input.confidence
        )
        return recommendation
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendation: {str(e)}"
        )


@router.post("/recommend-multimodal", response_model=Dict)
async def get_multimodal_recommendation(emotion_input: MultimodalEmotionInput):
    """
    Get decision recommendations based on multimodal emotion analysis
    
    Returns recommendations considering both facial and speech emotions
    """
    try:
        recommendation = decision_engine.get_multimodal_recommendation(
            facial_emotion=emotion_input.facial_emotion,
            facial_confidence=emotion_input.facial_confidence,
            speech_emotion=emotion_input.speech_emotion,
            speech_confidence=emotion_input.speech_confidence,
            text_emotion=emotion_input.text_emotion,
            text_confidence=emotion_input.text_confidence,
            fused_emotion=emotion_input.fused_emotion,
            fused_confidence=emotion_input.fused_confidence
        )
        return recommendation
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendation: {str(e)}"
        )
