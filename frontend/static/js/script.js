document.addEventListener('DOMContentLoaded', () => {
    // عناصر DOM
    const elements = {
        themeToggle: document.getElementById('theme-toggle'),
        body: document.body,
        amountInput: document.getElementById('amount'),
        fromCurrencySelect: document.getElementById('from-currency'),
        toCurrencySelect: document.getElementById('to-currency'),
        swapBtn: document.getElementById('swap-currencies'),
        convertBtn: document.getElementById('convert-btn'),
        resultContainer: document.querySelector('.result-container'),
        originalAmountSpan: document.getElementById('original-amount'),
        convertedAmountSpan: document.getElementById('converted-amount'),
        fromCurrencyText: document.getElementById('from-currency-text'),
        toCurrencyText: document.getElementById('to-currency-text'),
        rateValueSpan: document.getElementById('rate-value'),
        errorContainer: document.getElementById('error-container')
    };

    // إعداد رابط API
    const API_URL = window.location.hostname === 'localhost' 
        ? 'http://localhost:8000'
        : 'https://currencyx-backend.onrender.com';

    // الثيم الافتراضي
    initTheme();

    // الأحداث
    elements.themeToggle.addEventListener('click', toggleTheme);
    elements.swapBtn.addEventListener('click', swapCurrencies);
    elements.convertBtn.addEventListener('click', convertCurrency);

    // دالة تهيئة الثيم
    function initTheme() {
        const currentTheme = localStorage.getItem('theme') || 'light';
        elements.body.classList.add(`${currentTheme}-mode`);
        updateThemeIcon(currentTheme);
    }

    // دالة تبديل الثيم
    function toggleTheme() {
        if (elements.body.classList.contains('light-mode')) {
            elements.body.classList.replace('light-mode', 'dark-mode');
            localStorage.setItem('theme', 'dark');
            updateThemeIcon('dark');
        } else {
            elements.body.classList.replace('dark-mode', 'light-mode');
            localStorage.setItem('theme', 'light');
            updateThemeIcon('light');
        }
    }

    // دالة تحديث أيقونة الثيم
    function updateThemeIcon(theme) {
        const icon = elements.themeToggle.querySelector('i');
        icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }

    // دالة تبديل العملات
    function swapCurrencies() {
        const temp = elements.fromCurrencySelect.value;
        elements.fromCurrencySelect.value = elements.toCurrencySelect.value;
        elements.toCurrencySelect.value = temp;
        if (!elements.resultContainer.classList.contains('hidden')) {
            convertCurrency();
        }
    }

    // دالة تحويل العملات (محدثة)
    async function convertCurrency() {
        const amount = parseFloat(elements.amountInput.value);
        const fromCurrency = elements.fromCurrencySelect.value;
        const toCurrency = elements.toCurrencySelect.value;

        if (!validateInput(amount)) return;

        try {
            startLoading();
            
            const response = await fetch(`${API_URL}/api/convert`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    amount: amount,
                    from_currency: fromCurrency,
                    to_currency: toCurrency
                })
            });

            const data = await handleResponse(response);
            displayResult(data.data, amount, fromCurrency, toCurrency);
            hideError();
            
        } catch (error) {
            showError(error.message);
        } finally {
            stopLoading();
        }
    }

    // دوال مساعدة جديدة
    function validateInput(amount) {
        if (isNaN(amount) || amount <= 0) {
            showError('الرجاء إدخال مبلغ صحيح');
            return false;
        }
        return true;
    }

    async function handleResponse(response) {
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'فشل في تحويل العملة');
        }
        return response.json();
    }

    function displayResult(data, amount, from, to) {
        elements.originalAmountSpan.textContent = amount.toFixed(2);
        elements.convertedAmountSpan.textContent = data.converted.toFixed(2);
        elements.fromCurrencyText.textContent = from;
        elements.toCurrencyText.textContent = to;
        elements.rateValueSpan.textContent = data.rate.toFixed(6);
        elements.resultContainer.classList.remove('hidden');
    }

    function showError(message) {
        elements.errorContainer.textContent = message;
        elements.errorContainer.classList.remove('hidden');
        console.error('Conversion Error:', message);
    }

    function hideError() {
        elements.errorContainer.classList.add('hidden');
    }

    function startLoading() {
        elements.convertBtn.disabled = true;
        elements.convertBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> جاري التحويل...';
    }

    function stopLoading() {
        elements.convertBtn.disabled = false;
        elements.convertBtn.textContent = 'تحويل';
    }
});