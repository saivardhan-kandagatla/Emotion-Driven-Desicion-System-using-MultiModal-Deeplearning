/**
 * Main Application Logic
 */

// State
let currentTab = 'facial';
let multiImageFile = null;
let multiAudioFile = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
    initializeText();
    initializeMultimodal();
    checkBackendStatus();
});

/**
 * Initialize tab navigation
 */
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.dataset.tab;

            // Update active states
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            button.classList.add('active');
            document.getElementById(`${tabName}Content`).classList.add('active');

            currentTab = tabName;
        });
    });
}

/**
 * Initialize text modal inputs
 */
function initializeText() {
    const analyzeTextBtn = document.getElementById('analyzeText');
    const textInput = document.getElementById('textInput');

    if (analyzeTextBtn && textInput) {
        analyzeTextBtn.addEventListener('click', async () => {
            const text = textInput.value.trim();
            if (!text) {
                alert('Please enter some text to analyze');
                return;
            }

            showLoading();
            try {
                const result = await apiService.analyzeTextEmotion(text);
                displayEmotionResult(result);

                const recommendation = await apiService.getRecommendation(
                    result.emotion,
                    result.confidence
                );
                displayDecisionResult(recommendation);
            } catch (error) {
                alert('Error analyzing text emotion: ' + error.message);
            } finally {
                hideLoading();
            }
        });
    }
}

/**
 * Initialize multimodal inputs
 */
function initializeMultimodal() {
    // Image upload
    document.getElementById('multiImageUpload').addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            multiImageFile = file;
            document.getElementById('multiImagePreview').innerHTML =
                `<small style="color: var(--success-color);">✓ ${file.name}</small>`;
        }
    });

    // Audio upload
    document.getElementById('multiAudioUpload').addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            multiAudioFile = file;
            document.getElementById('multiAudioPreview').innerHTML =
                `<small style="color: var(--success-color);">✓ ${file.name}</small>`;
        }
    });

    // Analyze button
    document.getElementById('analyzeMultimodal').addEventListener('click', async () => {
        const textInput = document.getElementById('multiTextInput');
        const text = textInput ? textInput.value.trim() : null;

        if (!multiImageFile && !multiAudioFile && !text) {
            alert('Please provide at least one input (image, audio, or text)');
            return;
        }

        showLoading();
        try {
            // Get multimodal analysis
            const result = await apiService.analyzeMultimodalEmotion(
                multiImageFile,
                multiAudioFile,
                text
            );

            // Display emotion result
            displayEmotionResult(result);

            // Get multimodal recommendation
            const recommendationData = {
                fused_emotion: result.emotion,
                fused_confidence: result.confidence
            };

            // Add individual emotions if available
            if (result.facial_analysis) {
                recommendationData.facial_emotion = result.facial_analysis.emotion;
                recommendationData.facial_confidence = result.facial_analysis.confidence;
            }
            if (result.speech_analysis) {
                recommendationData.speech_emotion = result.speech_analysis.emotion;
                recommendationData.speech_confidence = result.speech_analysis.confidence;
            }
            if (result.text_analysis) {
                recommendationData.text_emotion = result.text_analysis.emotion;
                recommendationData.text_confidence = result.text_analysis.confidence;
            }

            const recommendation = await apiService.getMultimodalRecommendation(
                recommendationData
            );
            displayDecisionResult(recommendation);

        } catch (error) {
            alert('Error analyzing multimodal emotion: ' + error.message);
        } finally {
            hideLoading();
        }
    });
}

/**
 * Check backend status
 */
async function checkBackendStatus() {
    try {
        const health = await apiService.checkHealth();
        console.log('Backend status:', health);

        if (health.status === 'offline') {
            showBackendWarning();
        } else if (!health.facial_model_loaded || !health.speech_model_loaded || !health.text_model_loaded) {
            showModelWarning(health);
        }
    } catch (error) {
        console.error('Backend check failed:', error);
        showBackendWarning();
    }
}

/**
 * Show backend offline warning
 */
function showBackendWarning() {
    const warning = document.createElement('div');
    warning.style.cssText = `
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(239, 68, 68, 0.9);
        color: white;
        padding: 1rem 2rem;
        border-radius: 8px;
        z-index: 9999;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    `;
    warning.innerHTML = `
        ⚠️ Backend server is not running. Please start the server with: 
        <code style="background: rgba(0,0,0,0.3); padding: 0.2rem 0.5rem; 
        border-radius: 4px; display: inline-block; margin-top: 0.5rem;">
        uvicorn app.main:app --reload
        </code>
    `;
    document.body.appendChild(warning);
}

/**
 * Show model loading warning
 */
function showModelWarning(health) {
    const warning = document.createElement('div');
    warning.style.cssText = `
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(245, 158, 11, 0.9);
        color: white;
        padding: 1rem 2rem;
        border-radius: 8px;
        z-index: 9999;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        max-width: 500px;
        text-align: center;
    `;

    let message = '⚠️ Models not loaded: ';
    if (!health.facial_model_loaded) message += 'Facial ';
    if (!health.speech_model_loaded) message += 'Speech ';
    if (!health.text_model_loaded) message += 'Text ';
    message += '<br><small>Please add your trained models to backend/models/</small>';

    warning.innerHTML = message;
    document.body.appendChild(warning);

    // Auto-hide after 10 seconds
    setTimeout(() => {
        warning.style.opacity = '0';
        warning.style.transition = 'opacity 0.5s';
        setTimeout(() => warning.remove(), 500);
    }, 10000);
}
