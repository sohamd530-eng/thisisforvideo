# Mortality tests
from core.mortality_model import mortality_predictor

def test_hmri_monotonic_vulnerability_increase():
    # Baseline normal ward
    res_base = mortality_predictor.calculate_hmri(
        wbgt_active=31.0,
        utci_c=42.0,
        t_max_c=42.0,
        t_min_c=28.0,
        humidity_pct=45.0,
        elderly_pct=5.0,
        outdoor_worker_pct=15.0,
        slum_density_pct=10.0,
        uhi_intensity_c=1.0,
        tree_canopy_pct=25.0
    )
    
    # Highly vulnerable slum ward with elderly population & high UHI
    res_vuln = mortality_predictor.calculate_hmri(
        wbgt_active=31.0,
        utci_c=42.0,
        t_max_c=42.0,
        t_min_c=33.0,  # Nocturnal heat retention
        humidity_pct=45.0,
        elderly_pct=14.0,
        outdoor_worker_pct=45.0,
        slum_density_pct=55.0,
        uhi_intensity_c=4.5,
        tree_canopy_pct=4.0
    )
    
    assert res_vuln["hmri_score"] > res_base["hmri_score"]
    assert res_vuln["excess_mortality_pct"] > res_base["excess_mortality_pct"]
    assert res_vuln["night_strain_factor"] > 1.0

def test_ward_impact_projections():
    impact = mortality_predictor.predict_ward_impact(
        ward_name="Test Slum Ward",
        population=200000,
        weather_forecast={
            "temp_max_c": 46.0,
            "temp_min_c": 34.0,
            "humidity_pct": 50.0,
            "wind_kmh": 5.0,
            "solar_radiation_wm2": 950.0
        },
        demographics={
            "elderly_pct": 10.0,
            "outdoor_worker_pct": 35.0,
            "slum_density_pct": 50.0,
            "uhi_intensity_c": 3.8,
            "tree_canopy_pct": 5.0
        }
    )
    
    assert impact["hmri"]["hmri_score"] > 60.0
    assert impact["epidemiological_projections"]["heat_er_admissions_daily"] > 10
    assert impact["epidemiological_projections"]["daily_ors_packets_needed"] > 2000
    assert impact["epidemiological_projections"]["projected_icu_beds_needed"] >= 1
