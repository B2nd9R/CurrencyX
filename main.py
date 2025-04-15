# python -m uvicorn main:app --reload

import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes.currency import router as currency_router

# إعدادات التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CurrencyX API",
    description="واجهة برمجية لتحويل العملات",
    version="v0.3.2",  # تم تحديث الإصدار
    docs_url="/docs",
    redoc_url=None,
    debug=False
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# تضمين الراوتر
app.include_router(currency_router, prefix="/api", tags=["Currency"])

@app.get("/")
@app.head("/")
async def root():
    return {"status": "active", "service": "CurrencyX"}

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "port": os.environ.get("PORT", "auto"),
        "version": app.version,
        "service": "CurrencyX Backend",
        "details": "Service is fully operational"
    }

@app.on_event("startup")
async def startup_event():
    port = os.environ.get("PORT", "غير محدد")
    logger.info(f"تم بدء التشغيل على المنفذ: {port}")
    logger.info(f"إصدار التطبيق: {app.version}")
    logger.info("التطبيق جاهز لاستقبال الطلبات")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)