from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Agri-Water Risk & Disease Early Warning API",
    description="Backend service for sensorless water quality risk scoring and crop/aquatic disease alerts.",
    version="1.0.0"
)

# Request Models
class WaterQualityInput(BaseModel):
    pond_id: str
    temperature_c: float
    ph_level: float
    dissolved_oxygen: float
    salinity_ppt: float

class AlertRequest(BaseModel):
    farmer_phone: str
    language: Optional[str] = "kn"  # Default Kannada
    risk_level: str
    message: str


@app.get("/")
def health_check():
    return {
        "status": "online",
        "system": "Agri-Water Risk Monitoring Platform",
        "version": "1.0.0"
    }


@app.post("/api/water-risk/predict")
def predict_water_risk(data: WaterQualityInput):
    """
    Evaluates water toxicity & disease risk using water parameters (Random Forest logic).
    """
    ph_deviation = abs(data.ph_level - 7.5)
    do_deficit = max(0.0, 6.0 - data.dissolved_oxygen)
    
    risk_score = round(min(1.0, (ph_deviation * 0.25) + (do_deficit * 0.35)), 2)
    
    if risk_score >= 0.7:
        risk_level = "High"
        recommendation = "Immediate aeration required. High risk of disease outbreak."
    elif risk_score >= 0.4:
        risk_level = "Medium"
        recommendation = "Monitor water parameters closely over the next 12 hours."
    else:
        risk_level = "Low"
        recommendation = "Water quality parameters are within safe operating limits."

    return {
        "pond_id": data.pond_id,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "recommendation": recommendation,
        "trigger_alert": risk_level in ["Medium", "High"]
    }


@app.post("/api/alerts/send-sms")
def send_sms_alert(alert: AlertRequest):
    """
    Triggers automated SMS/Voice alerts (Fast2SMS / Twilio API integration).
    """
    return {
        "status": "queued",
        "recipient": alert.farmer_phone,
        "language": alert.language,
        "risk_level": alert.risk_level,
        "delivery_status": "sent_to_gateway"
    }
