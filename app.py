"""
SurakshaTaap Pune - Pune Municipal Corporation (PMC) Heatwave & Thermal Stress Platform
Ministry of Earth Sciences (MoES) / NCMRWF - Problem Statement 26083
FastAPI Backend Server
"""

import os
from typing import Dict, Any, Optional
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Core modules
from core.thermal_stress import (
    calculate_comprehensive_heat_stress,
    compute_wbgt,
    compute_utci,
    compute_heat_index,
    compute_physiological_strain
)
from core.mortality_model import mortality_predictor
from core.gis_engine import (
    PUNE_METADATA,
    PUNE_PMC_WARDS,
    get_pune_geojson
)
from core.hap_engine import hap_engine
from core.alert_service import alert_dispatcher, PUNE_ALERT_TRANSLATIONS
from core.weather_service import weather_service, PUNE_HISTORICAL_BENCHMARKS

app = FastAPI(
    title="SurakshaTaap Pune - PMC Heatwave Decision Support System",
    description="Hyper-Local Human Thermal Stress & Mortality Risk Platform for Pune Municipal Corporation (PMC)",
    version="2.5.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schemas
class StressCalculationRequest(BaseModel):
    temperature_c: float = Field(..., example=41.5)
    relative_humidity: float = Field(..., example=48.0)
    wind_speed_kmh: float = Field(6.5, example=6.5)
    solar_radiation_wm2: float = Field(850.0, example=850.0)
    activity_level: str = Field("moderate_labor")

class TriggerHAPRequest(BaseModel):
    ward_id: str = Field(..., example="PMC-W01")
    ward_name: str = Field(..., example="Kasba - Budhwar Peth")
    marathi_name: str = Field("कसबा - बुधवार पेठ")
    alert_level: int = Field(2)
    wbgt_c: float = Field(31.2)
    utci_c: float = Field(42.5)
    hmri_score: float = Field(68.5)
    demographics: Optional[Dict[str, Any]] = Field(default_factory=dict)

class ComposeAlertRequest(BaseModel):
    ward_name: str = Field(..., example="Kasba - Budhwar Peth")
    marathi_name: str = Field("कसबा - बुधवार पेठ")
    alert_level: int = Field(2)
    wbgt_c: float = Field(31.2)
    utci_c: float = Field(42.5)
    hi_c: float = Field(46.0)
    temp_c: float = Field(43.0)
    humidity_pct: float = Field(50.0)
    hmri_score: float = Field(68.5)
    language: str = Field("mr", description="mr or en")
    persona: str = Field("citizen")

class DispatchAlertRequest(BaseModel):
    ward_name: str = Field(..., example="Kasba - Budhwar Peth")
    channel: str = Field("all")
    alert_payload: Dict[str, Any]
    recipients_count: int = Field(2500)

# Static files
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def root():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "SurakshaTaap Pune PMC Platform Active"}

@app.get("/health")
async def health_check():
    return {
        "status": "HEALTHY",
        "city": "Pune Municipal Corporation (PMC)",
        "observatories": ["IMD Shivajinagar", "IMD Pashan"],
        "wards_monitored": len(PUNE_PMC_WARDS),
        "system": "SurakshaTaap Pune - MoES / NCMRWF",
        "version": "2.5.0"
    }

@app.get("/api/pune/metadata")
async def get_metadata():
    """Returns Pune city metadata and IMD station positions."""
    return PUNE_METADATA

@app.get("/api/pune/wards")
async def get_wards_geojson(
    temp: Optional[float] = Query(None, description="Temp override (°C)"),
    humidity: Optional[float] = Query(None, description="Humidity override (%)"),
    wind: Optional[float] = Query(None, description="Wind speed override (km/h)"),
    solar: Optional[float] = Query(None, description="Solar radiation override (W/m²)")
):
    """
    Returns full GeoJSON FeatureCollection with live-computed WBGT, UTCI, HMRI,
    and casualty projections for all 12 Pune Municipal Corporation (PMC) wards.
    """
    weather_override = None
    if temp is not None or humidity is not None or wind is not None or solar is not None:
        weather_override = {
            "temp": temp if temp is not None else 41.2,
            "humidity": humidity if humidity is not None else 42.0,
            "wind": wind if wind is not None else 6.8,
            "solar": solar if solar is not None else 870.0
        }
        
    geojson = get_pune_geojson(weather_override)
    return geojson

@app.post("/api/calculate-stress")
async def calculate_stress(payload: StressCalculationRequest):
    """Unified thermal stress calculator for custom parameters."""
    res = calculate_comprehensive_heat_stress(
        temperature_c=payload.temperature_c,
        relative_humidity=payload.relative_humidity,
        wind_speed_kmh=payload.wind_speed_kmh,
        solar_radiation_wm2=payload.solar_radiation_wm2,
        activity_level=payload.activity_level
    )
    return res

@app.get("/api/pune/forecast")
async def get_forecast(live: bool = Query(True)):
    """5-day hourly predictive trajectory from IMD Pune / Open-Meteo."""
    return weather_service.get_live_or_synthetic_forecast(use_live_api=live)

@app.get("/api/pune/benchmarks")
async def get_benchmarks():
    """Historical Pune & Maharashtra heatwave benchmarks."""
    return list(PUNE_HISTORICAL_BENCHMARKS.values())

@app.post("/api/trigger-hap")
async def trigger_hap(payload: TriggerHAPRequest):
    """Generates official PMC & Sassoon Hospital emergency Heat Action Plan directives."""
    return hap_engine.generate_ward_hap(
        ward_id=payload.ward_id,
        ward_name=payload.ward_name,
        marathi_name=payload.marathi_name,
        alert_level=payload.alert_level,
        wbgt_c=payload.wbgt_c,
        utci_c=payload.utci_c,
        hmri_score=payload.hmri_score,
        demographics=payload.demographics or {}
    )

@app.post("/api/compose-alert")
async def compose_alert(payload: ComposeAlertRequest):
    """Generates localized bilingual Marathi/English alert."""
    return alert_dispatcher.compose_alert(
        ward_name=payload.ward_name,
        marathi_name=payload.marathi_name,
        alert_level=payload.alert_level,
        wbgt_c=payload.wbgt_c,
        utci_c=payload.utci_c,
        hi_c=payload.hi_c,
        temp_c=payload.temp_c,
        humidity_pct=payload.humidity_pct,
        hmri_score=payload.hmri_score,
        lang=payload.language,
        persona=payload.persona
    )

@app.post("/api/dispatch-alert")
async def dispatch_alert(payload: DispatchAlertRequest):
    """Dispatches simulated SMS / WhatsApp alert."""
    return alert_dispatcher.dispatch_broadcast(
        ward_name=payload.ward_name,
        channel=payload.channel,
        alert_payload=payload.alert_payload,
        recipients_count=payload.recipients_count
    )

@app.get("/api/broadcast-logs")
async def get_broadcast_logs():
    return alert_dispatcher.broadcast_logs

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
