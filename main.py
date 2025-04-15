# python -m uvicorn main:app --reload

import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes.currency import router as currency_router

# إعداد التسجيل للمساعدة في تشخيص المشكلات
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CurrencyX API",
    description="واجهة برمجية لتحويل العملات",
    version="v3.1.0",  # تحديث الإصدار
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

# الرواتر
app.include_router(currency_router, prefix="/api", tags=["Currency"])

@app.get("/")
@app.head("/")
async def root():
    return {"status": "active", "service": "CurrencyX"}

@app.get("/api/health")
async def health_check():
    port = os.environ.get("PORT", "default")
    return {
        "status": "healthy",
        "port": port,
        "version": app.version
    }

# إضافة حدث بدء التشغيل لتسجيل المنفذ المستخدم
@app.on_event("startup")
async def startup_event():
    port = os.environ.get("PORT", "default")
    logger.info(f"بدء تشغيل التطبيق على المنفذ: {port}")
    logger.info(f"إصدار التطبيق: {app.version}")