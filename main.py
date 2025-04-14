# python -m uvicorn main:app --reload

from fastapi import FastAPI
from backend.api.routes.currency import router as currency_router
import logging
from fastapi.middleware.cors import CORSMiddleware

# إعدادات التسجيل (Logging)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# تهيئة التطبيق مع تفعيل وضع التصحيح
app = FastAPI(
    title="CurrencyX API",
    description="واجهة برمجية لتحويل العملات",
    debug=True
)

# إعدادات CORS (السماح بطلبات من الفرونت إند)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # في الإنتاج استبدل "*" بالنطاق الخاص بك (مثال: ["https://yourdomain.com"])
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # أضف OPTIONS هنا
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

# تضمين الراوتر
app.include_router(
    currency_router,
    prefix="/api",
    tags=["Currency Conversion"]
)

# تشغيل الخادم (للاستخدام المحلي فقط)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug"
    )