// frontend/static/js/main.js
document.addEventListener('DOMContentLoaded', () => {
    // عناصر DOM
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    const amountInput = document.getElementById('amount');
    const fromCurrencySelect = document.getElementById('from-currency');
    const toCurrencySelect = document.getElementById('to-currency');
    const swapBtn = document.getElementById('swap-currencies');
    const convertBtn = document.getElementById('convert-btn');
    const resultContainer = document.querySelector('.result-container');
    const originalAmountSpan = document.getElementById('original-amount');
    const convertedAmountSpan = document.getElementById('converted-amount');
    const fromCurrencyText = document.getElementById('from-currency-text');
    const toCurrencyText = document.getElementById('to-currency-text');
    const rateValueSpan = document.getElementById('rate-value');
    const fromRateSpan = document.querySelector('.from-rate');
    const toRateSpan = document.querySelector('.to-rate');

    // إعداد رابط API (Render أو محلي)
    const API_URL = window.location.hostname === 'localhost' 
        ? 'http://localhost:8000' 
        : 'https://currencyx-backend.onrender.com';

    // تحميل الثيم
    const currentTheme = localStorage.getItem('theme') || 'light';
    body.classList.add(currentTheme + '-mode');
    updateThemeIcon(currentTheme);

    // تبديل الثيم
    themeToggle.addEventListener('click', () => {
        if (body.classList.contains('light-mode')) {
            body.classList.replace('light-mode', 'dark-mode');
            localStorage.setItem('theme', 'dark');
            updateThemeIcon('dark');
        } else {
            body.classList.replace('dark-mode', 'light-mode');
            localStorage.setItem('theme', 'light');
            updateThemeIcon('light');
        }
    });

    // تبديل العملات
    swapBtn.addEventListener('click', () => {
        const temp = fromCurrencySelect.value;
        fromCurrencySelect.value = toCurrencySelect.value;
        toCurrencySelect.value = temp;
        if (!resultContainer.classList.contains('hidden')) {
            convertCurrency();
        }
    });

    // تحويل العملات
    convertBtn.addEventListener('click', convertCurrency);

    // تحديث أيقونة الثيم
    function updateThemeIcon(theme) {
        const icon = themeToggle.querySelector('i');
        icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }

    // دالة تحويل العملات
    async function convertCurrency() {
        const amount = parseFloat(amountInput.value);
        const fromCurrency = fromCurrencySelect.value;
        const toCurrency = toCurrencySelect.value;

        if (isNaN(amount) || amount <= 0) {
            alert('الرجاء إدخال مبلغ صحيح');
            return;
        }

        try {
            convertBtn.disabled = true;
            convertBtn.textContent = 'جاري التحويل...';

            const response = await fetch(`${API_URL}/api/convert`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    amount: amount,
                    from_currency: fromCurrency,
                    to_currency: toCurrency
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'فشل في تحويل العملة');
            }

            const data = await response.json();

            // عرض النتيجة
            originalAmountSpan.textContent = amount;
            convertedAmountSpan.textContent = data.converted.toFixed(2);
            fromCurrencyText.textContent = fromCurrency;
            toCurrencyText.textContent = toCurrency;
            rateValueSpan.textContent = data.rate.toFixed(6);
            fromRateSpan.textContent = fromCurrency;
            toRateSpan.textContent = toCurrency;

            resultContainer.classList.remove('hidden');
        } catch (error) {
            console.error('Error:', error);
            alert('حدث خطأ أثناء تحويل العملة: ' + error.message);
        } finally {
            convertBtn.disabled = false;
            convertBtn.textContent = 'تحويل';
        }
    }
});