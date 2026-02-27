"""
Multimodal Fusion Engine
"""
import numpy as np
from typing import Dict, List
from app.core.config import settings


class FusionModel:
    """
    Combines facial and speech emotion predictions using fusion techniques
    """
    
    def __init__(self):
        self.fusion_weights = settings.fusion_weights
        self.fusion_method = "weighted_average"  # Options: weighted_average, max_confidence, voting
    
    def fuse_predictions(
        self,
        facial_result: Dict = None,
        speech_result: Dict = None,
        text_result: Dict = None
    ) -> Dict:
        """
        Fuse facial, speech, and text emotion predictions
        
        Args:
            facial_result: Result from facial emotion model
            speech_result: Result from speech emotion model
            text_result: Result from text emotion model
        
        Returns:
            Fused emotion prediction
        """
        results = {
            "facial": facial_result if facial_result and "error" not in facial_result else None,
            "speech": speech_result if speech_result and "error" not in speech_result else None,
            "text": text_result if text_result and "error" not in text_result else None
        }
        
        # Filter out None results
        valid_results = {k: v for k, v in results.items() if v is not None}
        
        if not valid_results:
            return {
                "error": "All models failed to make predictions or no input provided",
                "emotion": "Unknown",
                "confidence": 0.0
            }
        
        # If only one valid result, return it
        if len(valid_results) == 1:
            modality = list(valid_results.keys())[0]
            result = valid_results[modality].copy()
            result["fused_from"] = [modality]
            return result
        
        # Perform fusion based on method
        if self.fusion_method == "weighted_average":
            return self._weighted_average_fusion(valid_results)
        elif self.fusion_method == "max_confidence":
            return self._max_confidence_fusion(valid_results)
        else:
            return self._weighted_average_fusion(valid_results)
    
    def _weighted_average_fusion(
        self,
        valid_results: Dict[str, Dict]
    ) -> Dict:
        """
        Fuse predictions using weighted average for any number of valid modalities
        """
        # Get Weights for valid modalities and normalize them
        active_weights = {k: self.fusion_weights.get(k, 0.0) for k in valid_results.keys()}
        total_weight = sum(active_weights.values())
        
        if total_weight > 0:
            normalized_weights = {k: v / total_weight for k, v in active_weights.items()}
        else:
            # Equal weight if all active weights are 0
            normalized_weights = {k: 1.0 / len(valid_results) for k in valid_results.keys()}
        
        # Get all unique emotions
        all_emotions = set()
        for res in valid_results.values():
            all_emotions.update(res.get("probabilities", {}).keys())
        
        # Calculate weighted average
        fused_probs = {}
        for emotion in all_emotions:
            fused_prob = 0.0
            for k, res in valid_results.items():
                prob = res.get("probabilities", {}).get(emotion, 0.0)
                fused_prob += normalized_weights[k] * prob
            fused_probs[emotion] = fused_prob
        
        # Get top emotion
        top_emotion = max(fused_probs, key=fused_probs.get)
        confidence = fused_probs[top_emotion]
        
        result = {
            "emotion": top_emotion,
            "confidence": float(confidence),
            "probabilities": {k: float(v) for k, v in fused_probs.items()},
            "fusion_method": "weighted_average",
            "fused_from": list(valid_results.keys()),
            "agreement": len(set(res.get("emotion") for res in valid_results.values())) == 1
        }
        
        # Add individual emotions
        for k, res in valid_results.items():
            result[f"{k}_emotion"] = res.get("emotion")
            
        return result
    
    def _max_confidence_fusion(
        self,
        valid_results: Dict[str, Dict]
    ) -> Dict:
        """
        Select prediction with highest confidence
        """
        best_modality = max(valid_results.keys(), key=lambda k: valid_results[k].get("confidence", 0.0))
        selected = valid_results[best_modality].copy()
        
        selected["fusion_method"] = "max_confidence"
        selected["selected_modality"] = best_modality
        selected["fused_from"] = list(valid_results.keys())
        selected["agreement"] = len(set(res.get("emotion") for res in valid_results.values())) == 1
        
        # Add individual emotions
        for k, res in valid_results.items():
            selected[f"{k}_emotion"] = res.get("emotion")
            
        return selected
    
    def set_fusion_method(self, method: str):
        """
        Set the fusion method
        
        Args:
            method: Fusion method name
        """
        valid_methods = ["weighted_average", "max_confidence"]
        if method in valid_methods:
            self.fusion_method = method
        else:
            raise ValueError(f"Invalid fusion method. Choose from: {valid_methods}")
    
    def set_weights(self, facial: float, speech: float):
        """
        Set fusion weights
        
        Args:
            facial: Weight for facial emotion (0-1)
            speech: Weight for speech emotion (0-1)
        """
        total = facial + speech
        self.fusion_weights = {
            "facial": facial / total,
            "speech": speech / total
        }


# Singleton instance
fusion_model = FusionModel()
