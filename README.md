# CurrencyX - محول العملات الذكي 💱

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68%2B-green)](https://fastapi.tiangolo.com)
[![GitHub release](https://img.shields.io/github/v/release/yourusername/CurrencyX)](https://github.com/yourusername/CurrencyX/releases)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

<img src="frontend/assets/logo.png" width="150" align="right">

أداة متكاملة لتحويل العملات بدقة عالية مع واجهة مستخدم جميلة تدعم الوضع المظلم/الفاتح.

## ✨ المميزات

✅ تحويل فوري بين 160+ عملة  
✅ واجهة مستخدم متجاوبة  
✅ دعم الوضع المظلم/الفاتح  
✅ معدلات صرف محدثة  
✅ تاريخ التحويلات السابقة  
✅ API سهل للدمج  

## 🚀 التنصيب

### المتطلبات
- Python 3.9+
- Node.js (لتطوير الفرونت إند)

### الخطوات
```bash
# 1. استنساخ المشروع
git clone https://github.com/b2nd9r/CurrencyX.git
cd CurrencyX

# 2. إعداد البيئة
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. تثبيت المتطلبات
pip install -r requirements.txt

# 4. تشغيل الخادم
python -m uvicorn main:app --reload
```
---
## 📚 الوثائق التقنية
## 📡 API Endpoints

| الطريقة | المسار         | الوصف              |
|--------|----------------|--------------------|
| POST   | `/api/convert` | تحويل بين العملات |

### 🧪 مثال طلب:

```json
{
  "amount": 100,
  "from_currency": "USD",
  "to_currency": "SAR"
}