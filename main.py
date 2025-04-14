import os
from fastapi import FastAPI
from backend.api.routes.currency import router as currency_router
from fastapi.middleware.cors import CORSMiddleware
import logging

# إعدادات التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CurrencyX API",
    description="واجهة برمجية لتحويل العملات",
    version="v0.3.0",
    debug=False
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
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
    return {
        "status": "healthy",
        "port": os.environ.get("PORT", "default"),
        "version": app.version
    }

def run_server():
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        workers=4,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    run_server()