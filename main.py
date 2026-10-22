from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional

# Import local modules
from model import WaterRiskModel
from alert_service import AlertService
from vision_model import MobileNetDiseaseDetector

app = FastAPI(
    title="Agri-Water Risk & Disease Early Warning API",
    description="Backend service for sensorless water quality risk scoring and crop/aquatic disease alerts.",
    version="1.0.0"
)

# Initialize module engines
risk_engine = WaterRiskModel()
alert_engine = AlertService()
vision_engine = MobileNetDiseaseDetector()

# Input Models
class WaterQualityInput(BaseModel):
    pond_id: str
    temperature_c: float
    ph_level: float
    dissolved_oxygen: float
    salinity_ppt: float

class AlertRequest(BaseModel):
    farmer_phone: str
    risk_level: str


@app.get("/")
def health_check():
    return {
        "status": "online",
        "system": "Agri-Water Risk Monitoring Platform",
        "version": "1.0.0"
    }


@app.post("/api/water-risk/predict")
def predict_water_risk(data: WaterQualityInput):
    """Calculates risk using WaterRiskModel in model.py"""
    analysis = risk_engine.evaluate_risk(
        ph=data.ph_level,
        do=data.dissolved_oxygen,
        temp=data.temperature_c,
        salinity=data.salinity_ppt
    )
    return {
        "pond_id": data.pond_id,
        "risk_analysis": analysis
    }


@app.post("/api/alerts/send-sms")
def send_sms_alert(alert: AlertRequest):
    """Dispatches Kannada SMS using AlertService in alert_service.py"""
    return alert_engine.send_sms(
        phone_number=alert.farmer_phone,
        risk_level=alert.risk_level
    )


@app.post("/api/disease/detect")
async def detect_disease(file: UploadFile = File(...)):
    """Diagnoses disease using MobileNetDiseaseDetector in vision_model.py"""
    image_bytes = await file.read()
    return vision_engine.predict_disease(image_bytes)
