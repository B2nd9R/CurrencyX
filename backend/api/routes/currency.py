from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import requests
import os
import logging
from dotenv import load_dotenv

router = APIRouter()

# تحميل المتغيرات من المسار الصحيح
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(env_path)

class ConvertRequest(BaseModel):
    amount: float
    from_currency: str
    to_currency: str

@router.post("/convert")
async def convert_currency(request: Request, data: ConvertRequest):
    """Convert currency using external API"""
    API_KEY = os.getenv("EXCHANGE_API_KEY")
    
    if not API_KEY:
        logging.critical("Exchange API KEY is missing!")
        raise HTTPException(
            status_code=500,
            detail="Service configuration error - API KEY missing"
        )

    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{data.from_currency}/{data.to_currency}/{data.amount}"
    
    try:
        # إضافة معلومات الرأس للتعريف
        headers = {
            "User-Agent": "CurrencyX/1.0",
            "Accept": "application/json"
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        result = response.json()

        if result.get("result") != "success":
            error_type = result.get("error-type", "unknown_error")
            logging.error(f"API Error: {error_type}")
            raise HTTPException(
                status_code=400,
                detail=f"Exchange API error: {error_type}"
            )

        return {
            "status": "success",
            "data": {
                "original": data.amount,
                "converted": result["conversion_result"],
                "rate": result["conversion_rate"],
                "from_currency": data.from_currency,
                "to_currency": data.to_currency
            }
        }

    except requests.Timeout:
        logging.error("API request timeout")
        raise HTTPException(status_code=504, detail="API request timeout")
    except requests.RequestException as e:
        logging.error(f"API connection error: {str(e)}")
        raise HTTPException(status_code=502, detail=f"API connection error: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )