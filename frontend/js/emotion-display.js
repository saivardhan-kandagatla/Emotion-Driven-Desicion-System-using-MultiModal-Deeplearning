/**
 * Emotion Display and Visualization Module
 */

/**
 * Display emotion detection results
 */
function displayEmotionResult(result) {
    const emotionDisplay = document.getElementById('emotionDisplay');
    const resultsSection = document.getElementById('resultsSection');

    if (result.error) {
        emotionDisplay.innerHTML = `
            <div class="error-message">
                <p>❌ ${result.error}</p>
            </div>
        `;
        resultsSection.style.display = 'grid';
        return;
    }

    const { emotion, confidence, probabilities } = result;
    const confidencePercent = (confidence * 100).toFixed(1);

    // Create emotion display HTML
    let html = `
        <div class="emotion-display">
            <div class="emotion-icon">${getEmotionEmoji(emotion)}</div>
            <div class="emotion-label">${emotion}</div>
            <div class="emotion-confidence">Confidence: ${confidencePercent}%</div>
        </div>
    `;

    // Add probability chart if available
    if (probabilities) {
        html += '<div class="emotion-chart">';

        // Sort emotions by probability
        const sortedEmotions = Object.entries(probabilities)
            .sort((a, b) => b[1] - a[1]);

        for (const [emotionName, probability] of sortedEmotions) {
            const percent = (probability * 100).toFixed(1);
            html += `
                <div class="emotion-bar">
                    <div class="emotion-bar-label">
                        <span>${emotionName}</span>
                        <span>${percent}%</span>
                    </div>
                    <div class="emotion-bar-bg">
                        <div class="emotion-bar-fill" style="width: ${percent}%"></div>
                    </div>
                </div>
            `;
        }
        html += '</div>';
    }

    emotionDisplay.innerHTML = html;
    resultsSection.style.display = 'grid';

    // Animate bars
    setTimeout(() => {
        document.querySelectorAll('.emotion-bar-fill').forEach(bar => {
            const width = bar.style.width;
            bar.style.width = '0';
            setTimeout(() => {
                bar.style.width = width;
            }, 100);
        });
    }, 100);
}

/**
 * Display decision recommendations
 */
function displayDecisionResult(recommendation) {
    const decisionPanel = document.getElementById('decisionPanel');

    if (!recommendation || recommendation.error) {
        decisionPanel.innerHTML = '<p>Could not generate recommendations</p>';
        return;
    }

    const {
        emotion,
        confidence,
        recommendations,
        color,
        icon,
        confidence_level,
        note,
        modal_analysis
    } = recommendation;

    let html = `
        <div class="decision-header">
            <div class="decision-icon">${icon}</div>
            <div class="decision-emotion">${emotion}</div>
            <span class="confidence-badge">Confidence: ${confidence_level}</span>
        </div>

        <ul class="recommendations-list">
    `;

    for (const rec of recommendations) {
        html += `<li class="recommendation-item">${rec}</li>`;
    }

    html += '</ul>';

    // Add note if present
    if (note) {
        html += `<div class="alert-note">${note}</div>`;
    }

    // Add modal analysis if present
    if (modal_analysis) {
        html += '<div class="modal-analysis">';

        if (modal_analysis.facial && modal_analysis.facial.emotion) {
            html += `
                <div class="modal-item">
                    <div class="modal-item-label">Facial</div>
                    <div class="modal-item-value">${modal_analysis.facial.emotion}</div>
                </div>
            `;
        }

        if (modal_analysis.speech && modal_analysis.speech.emotion) {
            html += `
                <div class="modal-item">
                    <div class="modal-item-label">Speech</div>
                    <div class="modal-item-value">${modal_analysis.speech.emotion}</div>
                </div>
            `;
        }

        if (modal_analysis.text && modal_analysis.text.emotion) {
            html += `
                <div class="modal-item">
                    <div class="modal-item-label">Text</div>
                    <div class="modal-item-value">${modal_analysis.text.emotion}</div>
                </div>
            `;
        }

        html += `
                <div class="modal-item">
                    <div class="modal-item-label">Combined</div>
                    <div class="modal-item-value">${modal_analysis.fused.emotion}</div>
                </div>
            </div>
        `;
    }

    decisionPanel.innerHTML = html;
}

/**
 * Get emoji for emotion
 */
function getEmotionEmoji(emotion) {
    const emojiMap = {
        'Happy': '😊',
        'Sad': '😔',
        'Angry': '😠',
        'Neutral': '😐',
        'Fear': '😰',
        'Surprise': '😲',
        'Disgust': '🤢'
    };
    return emojiMap[emotion] || '😐';
}

/**
 * Show loading overlay
 */
function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'flex';
}

/**
 * Hide loading overlay
 */
function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}
