/**
 * BetterPrompt Application JavaScript
 * Handles form submission and UI interactions
 */

class BetterPromptApp {
    constructor() {
        this.form = document.getElementById('promptForm');
        this.resultDiv = document.getElementById('result');
        this.errorDiv = document.getElementById('error');
        this.submitBtn = document.getElementById('submitBtn');
        this.copyBtn = document.getElementById('copyBtn');
        this.originalResultText = ''; // Store the original formatted text
        
        this.init();
    }
    
    init() {
        if (!this.form || !this.submitBtn) {
            console.error('Required elements not found');
            return;
        }
        
        this.attachEventListeners();
        this.setupFormValidation();
    }
    
    attachEventListeners() {
        this.form.addEventListener('submit', this.handleFormSubmit.bind(this));
        
        if (this.copyBtn) {
            this.copyBtn.addEventListener('click', this.handleCopyClick.bind(this));
        }
        
        // Add keyboard shortcuts
        document.addEventListener('keydown', this.handleKeydown.bind(this));
    }
    
    setupFormValidation() {
        const promptTextarea = document.getElementById('prompt');
        if (promptTextarea) {
            promptTextarea.addEventListener('input', this.validateForm.bind(this));
        }
    }
    
    validateForm() {
        const promptTextarea = document.getElementById('prompt');
        const isValid = promptTextarea && promptTextarea.value.trim().length > 0;
        
        this.submitBtn.disabled = !isValid;
        return isValid;
    }
    
    async handleFormSubmit(event) {
        event.preventDefault();
        
        if (!this.validateForm()) {
            this.showError('Please enter a prompt to improve.');
            return;
        }
        
        this.hideMessages();
        this.setLoading(true);
        
        const promptTextarea = document.getElementById('prompt');
        const prompt = promptTextarea.value.trim();
        
        try {
            const response = await this.submitPrompt(prompt);
            
            if (response.ok) {
                const data = await response.json();
                this.showResult(data.improved_prompt);
            } else {
                const errorData = await response.json().catch(() => ({}));
                this.showError(errorData.error || `Server error: ${response.status}`);
            }
        } catch (error) {
            console.error('Network error:', error);
            this.showError('Network error: Please check your connection and try again.');
        } finally {
            this.setLoading(false);
        }
    }
    
    async submitPrompt(prompt) {
        return fetch('/api/fix-prompt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt }),
        });
    }
    
    setLoading(isLoading) {
        this.submitBtn.disabled = isLoading;
        this.submitBtn.textContent = isLoading ? 'Generating...' : 'Generate Better Prompt';
        
        const container = document.querySelector('.container');
        if (container) {
            container.classList.toggle('loading', isLoading);
        }
    }
      showResult(improvedPrompt) {
        // Store the original formatted text
        this.originalResultText = improvedPrompt;
        
        const resultText = document.getElementById('resultText');
        if (resultText) {
            // Preserve line breaks and formatting when displaying
            resultText.style.whiteSpace = 'pre-wrap';
            resultText.textContent = improvedPrompt;
        }
        
        if (this.resultDiv) {
            this.resultDiv.style.display = 'block';
            this.resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }
    
    showError(message) {
        if (this.errorDiv) {
            this.errorDiv.textContent = message;
            this.errorDiv.style.display = 'block';
            this.errorDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }
      hideMessages() {
        if (this.resultDiv) {
            this.resultDiv.style.display = 'none';
        }
        if (this.errorDiv) {
            this.errorDiv.style.display = 'none';
        }
        // Clear the stored original text when hiding messages
        this.originalResultText = '';
    }
      async handleCopyClick() {
        const resultText = document.getElementById('resultText');
        if (!resultText) {
            console.error('Result text element not found');
            return;
        }
        
        // Use the stored original formatted text instead of textContent
        const text = this.originalResultText || resultText.textContent;
        if (!text) {
            this.showError('No text to copy');
            return;
        }
        
        try {
            await navigator.clipboard.writeText(text);
            this.showCopySuccess();
        } catch (error) {
            console.error('Copy failed:', error);
            this.fallbackCopy(text);
        }
    }
    
    showCopySuccess() {
        if (!this.copyBtn) return;
        
        const originalText = this.copyBtn.textContent;
        const originalClass = this.copyBtn.className;
        
        this.copyBtn.textContent = 'Copied!';
        this.copyBtn.classList.add('copied');
        
        setTimeout(() => {
            this.copyBtn.textContent = originalText;
            this.copyBtn.className = originalClass;
        }, 2000);
    }
    
    fallbackCopy(text) {
        // Fallback for browsers that don't support clipboard API
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.opacity = '0';
        document.body.appendChild(textArea);
        textArea.select();
        
        try {
            document.execCommand('copy');
            this.showCopySuccess();
        } catch (error) {
            console.error('Fallback copy failed:', error);
            this.showError('Copy failed. Please manually select and copy the text.');
        } finally {
            document.body.removeChild(textArea);
        }
    }
    
    handleKeydown(event) {
        // Ctrl+Enter or Cmd+Enter to submit form
        if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
            event.preventDefault();
            if (!this.submitBtn.disabled) {
                this.form.dispatchEvent(new Event('submit'));
            }
        }
        
        // Ctrl+C or Cmd+C when result is visible to copy
        if ((event.ctrlKey || event.metaKey) && event.key === 'c' && 
            this.resultDiv && this.resultDiv.style.display === 'block' &&
            window.getSelection().toString() === '') {
            event.preventDefault();
            this.handleCopyClick();
        }
    }
    
    // Utility method for analytics or monitoring
    trackEvent(eventName, properties = {}) {
        console.log(`Event: ${eventName}`, properties);
        // Add analytics tracking here if needed
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new BetterPromptApp();
});

// Export for testing purposes
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BetterPromptApp;
}
