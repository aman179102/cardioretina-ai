/* CardioRetina-AI Frontend Application */
(function () {
    'use strict';

    const elements = {
        uploadArea: document.getElementById('uploadArea'),
        uploadContent: document.getElementById('uploadContent'),
        fileInput: document.getElementById('fileInput'),
        imagePreview: document.getElementById('imagePreview'),
        clinicalForm: document.getElementById('clinicalForm'),
        predictBtn: document.getElementById('predictBtn'),
        gradcamCheck: document.getElementById('gradcamCheck'),
        resultsPlaceholder: document.getElementById('resultsPlaceholder'),
        resultsContainer: document.getElementById('resultsContainer'),
        errorContainer: document.getElementById('errorContainer'),
        errorMessage: document.getElementById('errorMessage'),
        riskGauge: document.getElementById('riskGauge'),
        gaugeFill: document.getElementById('gaugeFill'),
        riskLabel: document.getElementById('riskLabel'),
        riskProbability: document.getElementById('riskProbability'),
        confidence: document.getElementById('confidence'),
        modelVersion: document.getElementById('modelVersion'),
        clinicalFactors: document.getElementById('clinicalFactors'),
        topContributors: document.getElementById('topContributors'),
        contributorsList: document.getElementById('contributorsList'),
        gradcamCard: document.getElementById('gradcamCard'),
        gradcamImage: document.getElementById('gradcamImage'),
    };

    let selectedFile = null;

    // Upload handling
    elements.uploadArea.addEventListener('click', () => elements.fileInput.click());

    elements.uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        elements.uploadArea.classList.add('dragover');
    });

    elements.uploadArea.addEventListener('dragleave', () => {
        elements.uploadArea.classList.remove('dragover');
    });

    elements.uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        elements.uploadArea.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    elements.fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    function handleFile(file) {
        const validTypes = ['image/jpeg', 'image/png', 'image/bmp', 'image/tiff'];
        if (!validTypes.includes(file.type)) {
            showError('Please upload a valid image file (JPEG, PNG, BMP, or TIFF).');
            return;
        }
        if (file.size > 10 * 1024 * 1024) {
            showError('File is too large. Maximum size is 10MB.');
            return;
        }

        selectedFile = file;
        elements.predictBtn.disabled = false;

        const reader = new FileReader();
        reader.onload = (e) => {
            elements.imagePreview.src = e.target.result;
            elements.imagePreview.classList.remove('hidden');
            elements.uploadContent.classList.add('hidden');
        };
        reader.readAsDataURL(file);
    }

    // Form submission
    elements.clinicalForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!selectedFile) return;

        setLoading(true);
        hideError();

        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('age', document.getElementById('age').value);
        formData.append('systolic_bp', document.getElementById('systolic_bp').value);
        formData.append('diastolic_bp', document.getElementById('diastolic_bp').value);
        formData.append('cholesterol', document.getElementById('cholesterol').value);
        formData.append('bmi', document.getElementById('bmi').value);
        formData.append('smoking', document.getElementById('smoking').value);
        formData.append('diabetes', document.getElementById('diabetes').value);
        formData.append('physical_activity', document.getElementById('physical_activity').value);
        formData.append('generate_gradcam', elements.gradcamCheck.checked);

        try {
            const response = await fetch('/predict', { method: 'POST', body: formData });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || 'Prediction failed');
            }

            const result = await response.json();
            displayResults(result);
        } catch (error) {
            showError(error.message || 'An error occurred during prediction.');
        } finally {
            setLoading(false);
        }
    });

    function displayResults(data) {
        elements.resultsPlaceholder.classList.add('hidden');
        elements.resultsContainer.classList.remove('hidden');

        // Risk gauge
        const pct = data.risk_percentage;
        const color = data.risk_level === 'High' ? '#dc2626' :
                      data.risk_level === 'Moderate' ? '#f59e0b' : '#0d9488';

        elements.gaugeFill.style.background =
            `conic-gradient(${color} 0deg, ${color} ${pct * 3.6}deg, #e2e8f0 ${pct * 3.6}deg)`;

        elements.riskLabel.textContent = data.risk_level;
        elements.riskLabel.className = 'risk-label ' + data.risk_level.toLowerCase();

        elements.riskProbability.textContent = `${data.risk_percentage}%`;
        elements.confidence.textContent = `${(data.confidence * 100).toFixed(1)}%`;
        elements.modelVersion.textContent = data.model_version || 'v1.0.0';

        // Clinical factors
        elements.clinicalFactors.innerHTML = '';
        for (const [name, value] of Object.entries(data.clinical_factors)) {
            const item = document.createElement('div');
            item.className = 'factor-item';

            const statusClass = value.includes('High') || value.includes('Obese') ||
                                value.includes('Increased') || value.includes('Sedentary') ||
                                value.includes('Elderly') ? 'danger' :
                                value.includes('Elevated') || value.includes('Borderline') ||
                                value.includes('Overweight') || value.includes('Middle') ? 'warning' : 'normal';

            item.innerHTML = `
                <div class="factor-name">${name.replace(/_/g, ' ')}</div>
                <div class="factor-value ${statusClass}">${value}</div>
            `;
            elements.clinicalFactors.appendChild(item);
        }

        // Top contributors
        if (data.top_clinical_contributors && data.top_clinical_contributors.length > 0) {
            elements.topContributors.classList.remove('hidden');
            elements.contributorsList.innerHTML = '';
            data.top_clinical_contributors.forEach(c => {
                const li = document.createElement('li');
                li.textContent = c;
                elements.contributorsList.appendChild(li);
            });
        } else {
            elements.topContributors.classList.add('hidden');
        }

        // Grad-CAM
        if (data.gradcam_url) {
            elements.gradcamCard.classList.remove('hidden');
            elements.gradcamImage.src = data.gradcam_url;
        } else {
            elements.gradcamCard.classList.add('hidden');
        }
    }

    function setLoading(loading) {
        elements.predictBtn.disabled = loading;
        const btnText = elements.predictBtn.querySelector('.btn-text');
        const btnLoading = elements.predictBtn.querySelector('.btn-loading');
        if (loading) {
            btnText.classList.add('hidden');
            btnLoading.classList.remove('hidden');
        } else {
            btnText.classList.remove('hidden');
            btnLoading.classList.add('hidden');
        }
    }

    function showError(message) {
        elements.resultsPlaceholder.classList.add('hidden');
        elements.resultsContainer.classList.add('hidden');
        elements.errorContainer.classList.remove('hidden');
        elements.errorMessage.textContent = message;
    }

    function hideError() {
        elements.errorContainer.classList.add('hidden');
    }
})();
