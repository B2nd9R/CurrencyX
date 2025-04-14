import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes.currency import router as currency_router


app = FastAPI(
    title="CurrencyX API",
    description="واجهة برمجية لتحويل العملات",
    version="v0.3.0",
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
    return {
        "status": "healthy",
        "port": os.environ.get("PORT", "default"),
        "version": app.version
    }