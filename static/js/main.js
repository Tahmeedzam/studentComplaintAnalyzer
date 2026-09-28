/**
 * Smart Student Complaint Analyzer - Main UI Interactions
 */

document.addEventListener('DOMContentLoaded', () => {
    // Auto-dismiss Flash Alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000);
    });

    // Character Counter for Textareas
    const charCounterTextarea = document.getElementById('description');
    const charCounterDisplay = document.getElementById('char-count');
    if (charCounterTextarea && charCounterDisplay) {
        const updateCount = () => {
            const len = charCounterTextarea.value.length;
            charCounterDisplay.textContent = `${len} characters`;
        };
        charCounterTextarea.addEventListener('input', updateCount);
        updateCount();
    }
});

/**
 * Quick-fill login credentials on demo login page
 */
function fillDemoCredentials(role) {
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');

    if (!emailInput || !passwordInput) return;

    if (role === 'admin') {
        emailInput.value = 'admin@smartcampus.com';
        passwordInput.value = 'Admin@123';
    } else if (role === 'student') {
        emailInput.value = 'student@smartcampus.com';
        passwordInput.value = 'Student@123';
    }
}
