# Thermal stress tests
from core.thermal_stress import (
    vapor_pressure_hpa,
    dew_point_c,
    natural_wet_bulb_stull,
    compute_wbgt,
    compute_utci,
    compute_heat_index,
    compute_physiological_strain,
    calculate_comprehensive_heat_stress
)

def test_vapor_pressure_and_dew_point():
    # At 40°C and 50% RH
    vp = vapor_pressure_hpa(40.0, 50.0)
    assert 35.0 < vp < 40.0
    
    dp = dew_point_c(40.0, 50.0)
    assert 26.0 < dp < 30.0

def test_wbgt_extreme_humidity_compounding():
    # Dry heat: 40°C at 20% RH
    res_dry = compute_wbgt(temperature_c=40.0, relative_humidity=20.0, wind_speed_ms=2.0, solar_radiation_wm2=600.0)
    # Humid heat: 40°C at 70% RH
    res_humid = compute_wbgt(temperature_c=40.0, relative_humidity=70.0, wind_speed_ms=2.0, solar_radiation_wm2=600.0)
    
    assert res_dry["wbgt_active"] < 30.0
    assert res_humid["wbgt_active"] > 34.0
    assert res_humid["flag"] in ["Red", "Purple"]

def test_utci_thermal_stress_bands():
    # Normal temperature
    normal_utci = compute_utci(22.0, 50.0, wind_speed_ms=2.0, solar_radiation_wm2=200.0)
    assert normal_utci["stress_category"] == "No Thermal Stress"
    
    # Extreme heatwave
    extreme_utci = compute_utci(45.0, 60.0, wind_speed_ms=1.0, solar_radiation_wm2=900.0)
    assert extreme_utci["utci_c"] > 46.0
    assert extreme_utci["stress_category"] == "Extreme Heat Stress"

def test_physiological_strain_limits():
    # Extreme WBGT > 32°C must stop work
    strain = compute_physiological_strain(temperature_c=44.0, relative_humidity=65.0, activity_level="heavy_labor")
    assert strain["max_safe_work_duration_minutes"] <= 15
    assert strain["rest_percentage"] >= 75
    assert strain["estimated_sweat_rate_l_hr"] >= 1.0

def test_comprehensive_heat_stress_unified():
    res = calculate_comprehensive_heat_stress(
        temperature_c=42.0,
        relative_humidity=50.0,
        wind_speed_kmh=8.0,
        solar_radiation_wm2=800.0
    )
    assert "wbgt" in res
    assert "utci" in res
    assert "heat_index" in res
    assert "physiological_strain" in res
    assert res["wbgt"]["wbgt_active"] > 28.0
