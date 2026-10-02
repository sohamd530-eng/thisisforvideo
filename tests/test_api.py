# API tests for Pune PMC System
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health_endpoint():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "HEALTHY"
    assert data["city"] == "Pune Municipal Corporation (PMC)"

def test_pune_metadata_endpoint():
    resp = client.get("/api/pune/metadata")
    assert resp.status_code == 200
    meta = resp.json()
    assert meta["id"] == "pune"
    assert len(meta["monitoring_stations"]) >= 2

def test_pune_wards_geojson_endpoint():
    resp = client.get("/api/pune/wards")
    assert resp.status_code == 200
    geojson = resp.json()
    assert geojson["type"] == "FeatureCollection"
    assert len(geojson["features"]) == 12
    first_feat = geojson["features"][0]
    assert "wbgt_c" in first_feat["properties"]
    assert "marathi_name" in first_feat["properties"]

def test_calculate_stress_endpoint():
    payload = {
        "temperature_c": 41.5,
        "relative_humidity": 45.0,
        "wind_speed_kmh": 6.5,
        "solar_radiation_wm2": 850.0,
        "activity_level": "moderate_labor"
    }
    resp = client.post("/api/calculate-stress", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "wbgt" in data
    assert "utci" in data
    assert data["wbgt"]["wbgt_active"] > 25.0

def test_trigger_hap_endpoint():
    payload = {
        "ward_id": "PMC-W01",
        "ward_name": "Kasba - Budhwar Peth",
        "marathi_name": "कसबा - बुधवार पेठ",
        "alert_level": 3,
        "wbgt_c": 32.5,
        "utci_c": 44.0,
        "hmri_score": 78.0,
        "demographics": {"elderly_pct": 14.8, "slum_density_pct": 38.0}
    }
    resp = client.post("/api/trigger-hap", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "sectoral_action_plan" in data
    assert len(data["sectoral_action_plan"]["municipal_and_urban"]) > 0

def test_compose_and_dispatch_alert():
    compose_payload = {
        "ward_name": "Kasba - Budhwar Peth",
        "marathi_name": "कसबा - बुधवार पेठ",
        "alert_level": 2,
        "wbgt_c": 31.0,
        "utci_c": 41.5,
        "hi_c": 45.0,
        "temp_c": 42.0,
        "humidity_pct": 52.0,
        "hmri_score": 65.0,
        "language": "mr",
        "persona": "citizen"
    }
    resp = client.post("/api/compose-alert", json=compose_payload)
    assert resp.status_code == 200
    alert_payload = resp.json()
    assert "message_body" in alert_payload
    
    dispatch_payload = {
        "ward_name": "Kasba - Budhwar Peth",
        "channel": "sms",
        "alert_payload": alert_payload,
        "recipients_count": 1500
    }
    resp2 = client.post("/api/dispatch-alert", json=dispatch_payload)
    assert resp2.status_code == 200
    res = resp2.json()
    assert res["status"] == "SUCCESS"
    assert res["delivered_count"] > 1400
