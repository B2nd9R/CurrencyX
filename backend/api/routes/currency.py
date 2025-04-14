from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
import logging
import os  # هذه المكتبة ناقصة في ملفك الأصلي

logger = logging.getLogger(__name__)

# المسار الصحيح لملف .env يجب أن يكون نسبياً للموقع الحالي
load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))  # تصحيح المسار

router = APIRouter()

class ConvertRequest(BaseModel):
    amount: float
    from_currency: str
    to_currency: str

@router.post("/convert")
async def convert_currency(data: ConvertRequest):
    API_KEY = os.getenv("API_KEY")
    logger.debug(f"Using API Key: {API_KEY[:4]}...")  # تسجيل جزء من المفتاح للأمان
    
    if not API_KEY:
        logger.error("API_KEY is missing!")
        raise HTTPException(status_code=500, detail="API key not configured")

    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{data.from_currency}/{data.to_currency}"
    logger.debug(f"Requesting URL: {url.split('/')[2]}...")

    try:
        response = requests.get(url, timeout=10)  # أضف timeout لتجنب التجميد
        logger.debug(f"API Response: {response.status_code}")
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"API request failed with status {response.status_code}"
            )
            
        result = response.json()
        
        if result.get("result") == "error":
            error_detail = result.get("error-type", "Unknown error from exchange API")
            raise HTTPException(status_code=400, detail=error_detail)
            
        converted_amount = data.amount * result["conversion_rate"]
        return {
            "original": data.amount,
            "converted": round(converted_amount, 2),
            "rate": result["conversion_rate"],
            "currency": data.to_currency  # إضافة مفيدة للفرونت إند
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="Service temporarily unavailable"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )