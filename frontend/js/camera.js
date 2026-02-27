/**
 * Camera and Image Handling Module
 */

class CameraHandler {
    constructor() {
        this.stream = null;
        this.video = document.getElementById('cameraVideo');
        this.canvas = document.getElementById('cameraCanvas');
        this.isActive = false;
    }

    /**
     * Start camera stream
     */
    async startCamera() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 640 },
                    height: { ideal: 480 }
                }
            });

            this.video.srcObject = this.stream;
            this.isActive = true;

            // Show camera container
            document.getElementById('cameraContainer').style.display = 'block';
            document.getElementById('startCamera').style.display = 'none';
            document.getElementById('stopCamera').style.display = 'inline-block';

            return true;
        } catch (error) {
            console.error('Camera access error:', error);
            alert('Could not access camera. Please check permissions.');
            return false;
        }
    }

    /**
     * Stop camera stream
     */
    stopCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.video.srcObject = null;
            this.stream = null;
            this.isActive = false;

            // Hide camera container
            document.getElementById('cameraContainer').style.display = 'none';
            document.getElementById('startCamera').style.display = 'inline-block';
            document.getElementById('stopCamera').style.display = 'none';
        }
    }

    /**
     * Capture image from camera
     */
    captureImage() {
        if (!this.isActive) return null;

        // Set canvas size to match video
        this.canvas.width = this.video.videoWidth;
        this.canvas.height = this.video.videoHeight;

        // Draw video frame to canvas
        const ctx = this.canvas.getContext('2d');
        ctx.drawImage(this.video, 0, 0);

        // Convert to blob
        return new Promise((resolve) => {
            this.canvas.toBlob((blob) => {
                const file = new File([blob], 'capture.jpg', { type: 'image/jpeg' });
                resolve(file);
            }, 'image/jpeg', 0.95);
        });
    }

    /**
     * Display image preview
     */
    displayPreview(file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const previewImg = document.getElementById('previewImage');
            const previewContainer = document.getElementById('imagePreview');

            previewImg.src = e.target.result;
            previewContainer.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}

// Initialize camera handler
const cameraHandler = new CameraHandler();

// Event listeners for camera controls
document.getElementById('startCamera').addEventListener('click', () => {
    cameraHandler.startCamera();
});

document.getElementById('stopCamera').addEventListener('click', () => {
    cameraHandler.stopCamera();
});

document.getElementById('captureBtn').addEventListener('click', async () => {
    const imageFile = await cameraHandler.captureImage();
    if (imageFile) {
        cameraHandler.displayPreview(imageFile);
        cameraHandler.stopCamera();

        // Analyze emotion
        showLoading();
        try {
            const result = await apiService.analyzeFacialEmotion(imageFile);
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

document.getElementById('imageUpload').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (file) {
        cameraHandler.displayPreview(file);

        // Analyze emotion
        showLoading();
        try {
            const result = await apiService.analyzeFacialEmotion(file);
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
