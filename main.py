# python -m uvicorn main:app --reload

import os
import logging
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes.currency import router as currency_router

# إعدادات التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CurrencyX API",
    description="واجهة برمجية لتحويل العملات",
    version="v0.3.3",
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

@app.get("/health")
async def health_check():
    port = os.environ.get("PORT", "auto")
    return {
        "status": "healthy",
        "port": port,
        "version": app.version,
        "service": "CurrencyX Backend"
    }

@app.on_event("startup")
async def startup_event():
    port = os.environ.get("PORT", "غير محدد")
    logger.info(f"تم بدء التشغيل على المنفذ: {port}")
    logger.info(f"إصدار التطبيق: {app.version}")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        workers=1,
        log_level="info",
        timeout_keep_alive=60
    )

if __name__ == "__main__":
    run_server()