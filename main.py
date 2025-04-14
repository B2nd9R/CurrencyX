# python -m uvicorn main:app --reload

from fastapi import FastAPI
from backend.api.routes.currency import router as currency_router
import logging
from fastapi.middleware.cors import CORSMiddleware
import os

# إعدادات التسجيل (Logging)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# تهيئة التطبيق
app = FastAPI(
    title="CurrencyX API",
    description="واجهة برمجية لتحويل العملات",
    # debug=False في الإنتاج! (يتم تعطيله تلقائياً عند استخدام gunicorn)
)

# إعدادات CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # في الإنتاج ضيق النطاق حسب الحاجة
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تضمين الراوتر
app.include_router(
    currency_router,
    prefix="/api",
    tags=["Currency Conversion"]
)

# نقطة فحص الصحة (مطلوبة لـ Render)
@app.get("/api/health")
async def health_check():
    return {
        "status": "active",
        "port": os.environ.get("PORT", "غير معين")
    }

# التشغيل المحلي vs الإنتاج
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=os.environ.get("DEV_MODE", "False") == "True",  # التحميل الحيوي في التطوير فقط
        log_level="info"
    )