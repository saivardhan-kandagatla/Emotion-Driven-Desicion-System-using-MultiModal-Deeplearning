/**
 * Audio Recording and Handling Module
 */

class AudioHandler {
    constructor() {
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.stream = null;
        this.isRecording = false;
        this.recordedBlob = null;
    }

    /**
     * Start audio recording
     */
    async startRecording() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.mediaRecorder = new MediaRecorder(this.stream);
            this.audioChunks = [];

            this.mediaRecorder.ondataavailable = (event) => {
                this.audioChunks.push(event.data);
            };

            this.mediaRecorder.onstop = () => {
                this.recordedBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
                this.displayAudioPreview(this.recordedBlob);
            };

            this.mediaRecorder.start();
            this.isRecording = true;

            // Update UI
            document.getElementById('startRecording').style.display = 'none';
            document.getElementById('stopRecording').style.display = 'inline-block';
            document.getElementById('recordingIndicator').style.display = 'flex';

            return true;
        } catch (error) {
            console.error('Microphone access error:', error);
            alert('Could not access microphone. Please check permissions.');
            return false;
        }
    }

    /**
     * Stop audio recording
     */
    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.stream.getTracks().forEach(track => track.stop());
            this.isRecording = false;

            // Update UI
            document.getElementById('startRecording').style.display = 'inline-block';
            document.getElementById('stopRecording').style.display = 'none';
            document.getElementById('recordingIndicator').style.display = 'none';

            // Analyze after a short delay to ensure blob is ready
            setTimeout(() => {
                this.analyzeRecording();
            }, 500);
        }
    }

    /**
     * Display audio preview
     */
    displayAudioPreview(blob) {
        const audioPreview = document.getElementById('audioPreview');
        const audioPreviewContainer = document.getElementById('audioPreviewContainer');

        const audioUrl = URL.createObjectURL(blob);
        audioPreview.src = audioUrl;
        audioPreviewContainer.style.display = 'block';
    }

    /**
     * Analyze recorded audio
     */
    async analyzeRecording() {
        if (!this.recordedBlob) return;

        const audioFile = new File([this.recordedBlob], 'recording.wav', { type: 'audio/wav' });

        showLoading();
        try {
            const result = await apiService.analyzeSpeechEmotion(audioFile);
            displayEmotionResult(result);

            // Get recommendation
            const recommendation = await apiService.getRecommendation(
                result.emotion,
                result.confidence
            );
            displayDecisionResult(recommendation);
        } catch (error) {
            alert('Error analyzing emotion: ' + error.message);
        } finally {
            hideLoading();
        }
    }
}

// Initialize audio handler
const audioHandler = new AudioHandler();

// Event listeners for audio controls
document.getElementById('startRecording').addEventListener('click', () => {
    audioHandler.startRecording();
});

document.getElementById('stopRecording').addEventListener('click', () => {
    audioHandler.stopRecording();
});

document.getElementById('audioUpload').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (file) {
        audioHandler.displayAudioPreview(file);

        // Analyze emotion
        showLoading();
        try {
            const result = await apiService.analyzeSpeechEmotion(file);
            displayEmotionResult(result);

            // Get recommendation
            const recommendation = await apiService.getRecommendation(
                result.emotion,
                result.confidence
            );
            displayDecisionResult(recommendation);
        } catch (error) {
            alert('Error analyzing emotion: ' + error.message);
        } finally {
            hideLoading();
        }
    }
});
