/**
 * API Service Layer
 * Handles all backend communication
 */

const API_BASE_URL = 'http://localhost:8000/api';

class APIService {
    /**
     * Analyze facial emotion from image file
     */
    async analyzeFacialEmotion(imageFile) {
        const formData = new FormData();
        formData.append('image', imageFile);

        try {
            const response = await fetch(`${API_BASE_URL}/emotion/facial`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to analyze facial emotion');
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    /**
     * Analyze speech emotion from audio file
     */
    async analyzeSpeechEmotion(audioFile) {
        const formData = new FormData();
        formData.append('audio', audioFile);

        try {
            const response = await fetch(`${API_BASE_URL}/emotion/speech`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to analyze speech emotion');
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    /**
     * Analyze emotion from text
     */
    async analyzeTextEmotion(text) {
        const formData = new FormData();
        formData.append('text', text);

        try {
            const response = await fetch(`${API_BASE_URL}/emotion/text`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to analyze text emotion');
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    /**
     * Analyze multimodal emotion from image, audio, and text
     */
    async analyzeMultimodalEmotion(imageFile, audioFile, text = null) {
        const formData = new FormData();
        if (imageFile) formData.append('image', imageFile);
        if (audioFile) formData.append('audio', audioFile);
        if (text) formData.append('text', text);

        try {
            const response = await fetch(`${API_BASE_URL}/emotion/multimodal`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to analyze multimodal emotion');
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    /**
     * Get decision recommendation based on emotion
     */
    async getRecommendation(emotion, confidence) {
        try {
            const response = await fetch(`${API_BASE_URL}/decision/recommend`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ emotion, confidence })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to get recommendation');
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    /**
     * Get multimodal decision recommendation
     */
    async getMultimodalRecommendation(data) {
        try {
            const response = await fetch(`${API_BASE_URL}/decision/recommend-multimodal`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to get recommendation');
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    /**
     * Check backend health status
     */
    async checkHealth() {
        try {
            const response = await fetch('http://localhost:8000/health');
            return await response.json();
        } catch (error) {
            console.error('Health check failed:', error);
            return { status: 'offline' };
        }
    }
}

// Export singleton instance
const apiService = new APIService();
