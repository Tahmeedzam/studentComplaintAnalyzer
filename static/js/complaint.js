/**
 * Smart Student Complaint Analyzer - Complaint & Live NLP AJAX Controller
 */

async function analyzeTextRealtime(text) {
    if (!text || text.trim().length < 5) {
        return null;
    }

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('NLP Analysis Fetch Error:', error);
        return null;
    }
}

function renderNLPResult(result, targetContainerId) {
    const container = document.getElementById(targetContainerId);
    if (!container) return;

    if (!result) {
        container.style.display = 'none';
        return;
    }

    // Priority badge class
    let priorityBadgeClass = 'badge-priority-low';
    if (result.priority === 'High') priorityBadgeClass = 'badge-priority-high';
    else if (result.priority === 'Medium') priorityBadgeClass = 'badge-priority-medium';

    // Sentiment badge class
    let sentimentBadgeClass = 'badge-sentiment-neu';
    if (result.sentiment === 'Positive') sentimentBadgeClass = 'badge-sentiment-pos';
    else if (result.sentiment === 'Negative') sentimentBadgeClass = 'badge-sentiment-neg';

    // Build keyword tags
    const keywordsHtml = (result.keywords && result.keywords.length > 0)
        ? result.keywords.map(kw => `<span class="keyword-tag"><i class="bi bi-tag-fill me-1"></i>${kw}</span>`).join('')
        : '<span class="text-muted small">No specific keywords extracted</span>';

    container.innerHTML = `
        <div class="card nlp-card shadow-sm p-3">
            <div class="d-flex justify-content-between align-items-center mb-3 border-bottom pb-2">
                <div class="d-flex align-items-center gap-2">
                    <span class="badge bg-primary text-white"><i class="bi bi-cpu me-1"></i>NLP Model Prediction</span>
                    <span class="text-muted small">Confidence: <strong>${result.confidence}%</strong></span>
                </div>
                <span class="badge ${priorityBadgeClass} px-3 py-2">
                    <i class="bi bi-exclamation-triangle-fill me-1"></i>Priority: ${result.priority}
                </span>
            </div>

            <div class="row g-3">
                <div class="col-md-6 col-12">
                    <div class="small text-muted mb-1">Predicted Category</div>
                    <div class="fw-bold text-dark fs-6">
                        <i class="bi bi-folder2-open text-primary me-2"></i>${result.category}
                    </div>
                </div>

                <div class="col-md-6 col-12">
                    <div class="small text-muted mb-1">Suggested Department</div>
                    <div class="fw-bold text-dark fs-6">
                        <i class="bi bi-building text-primary me-2"></i>${result.department}
                    </div>
                </div>

                <div class="col-md-6 col-12">
                    <div class="small text-muted mb-1">Sentiment & Polarity Score</div>
                    <div>
                        <span class="badge ${sentimentBadgeClass} me-2">${result.sentiment}</span>
                        <span class="small text-muted">Compound: <strong>${result.sentiment_score}</strong></span>
                    </div>
                </div>

                <div class="col-md-6 col-12">
                    <div class="small text-muted mb-1">Extracted Keywords</div>
                    <div class="d-flex flex-wrap">${keywordsHtml}</div>
                </div>
            </div>

            <div class="mt-3 pt-2 border-top">
                <a class="small text-decoration-none text-muted" data-bs-toggle="collapse" href="#vivaDetailsCollapse" role="button" aria-expanded="false">
                    <i class="bi bi-info-circle me-1"></i>How was this analyzed? (Viva / Technical Overview)
                </a>
                <div class="collapse mt-2" id="vivaDetailsCollapse">
                    <div class="p-2 bg-light rounded small text-muted">
                        <div class="mb-1"><strong>1. Preprocessing:</strong> Regex cleaning &rarr; Tokenization &rarr; Stopword Removal &rarr; WordNet Lemmatization.</div>
                        <div class="mb-1"><strong>2. Classification:</strong> TF-IDF Vectorizer (1-2 ngrams) &rarr; Logistic Regression Model (${result.confidence}% probability).</div>
                        <div class="mb-1"><strong>3. Sentiment:</strong> VADER Polarity Intensity Analyzer (Score: ${result.sentiment_score}).</div>
                        <div><strong>4. Priority:</strong> Rule-based heuristic weighing urgency keywords, negative sentiment intensity, and safety hazards.</div>
                    </div>
                </div>
            </div>
        </div>
    `;

    container.style.display = 'block';
}

// Attach live preview on submit complaint form
document.addEventListener('DOMContentLoaded', () => {
    const previewBtn = document.getElementById('btn-nlp-preview');
    const descInput = document.getElementById('description');
    const titleInput = document.getElementById('title');
    const previewContainer = document.getElementById('nlp-live-preview-container');
    const loadingIndicator = document.getElementById('nlp-loading-spinner');

    if (previewBtn && descInput) {
        previewBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            const text = `${titleInput ? titleInput.value : ''} ${descInput.value}`.trim();
            if (text.length < 5) {
                alert('Please enter at least a few words in the title or description to analyze.');
                return;
            }

            if (loadingIndicator) loadingIndicator.style.display = 'block';
            if (previewContainer) previewContainer.style.display = 'none';

            const result = await analyzeTextRealtime(text);

            if (loadingIndicator) loadingIndicator.style.display = 'none';
            if (result && previewContainer) {
                renderNLPResult(result, 'nlp-live-preview-container');
            }
        });
    }

    // Landing Page Live Demo Box
    const demoBtn = document.getElementById('btn-demo-analyze');
    const demoInput = document.getElementById('demo-complaint-text');
    const demoResultContainer = document.getElementById('demo-nlp-result');
    const demoSpinner = document.getElementById('demo-loading-spinner');

    if (demoBtn && demoInput && demoResultContainer) {
        demoBtn.addEventListener('click', async () => {
            const text = demoInput.value.trim();
            if (!text) {
                alert('Please type or pick a sample complaint.');
                return;
            }

            if (demoSpinner) demoSpinner.style.display = 'block';
            demoResultContainer.style.display = 'none';

            const result = await analyzeTextRealtime(text);

            if (demoSpinner) demoSpinner.style.display = 'none';
            if (result) {
                renderNLPResult(result, 'demo-nlp-result');
            }
        });

        // Sample suggestion chips
        const chips = document.querySelectorAll('.sample-chip');
        chips.forEach(chip => {
            chip.addEventListener('click', () => {
                demoInput.value = chip.getAttribute('data-sample');
                demoBtn.click();
            });
        });
    }
});
