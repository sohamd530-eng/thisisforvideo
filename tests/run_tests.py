"""
Standalone test runner for Pune PMC Heatwave System
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_thermal_stress import (
    test_vapor_pressure_and_dew_point,
    test_wbgt_extreme_humidity_compounding,
    test_utci_thermal_stress_bands,
    test_physiological_strain_limits,
    test_comprehensive_heat_stress_unified
)
from tests.test_mortality import (
    test_hmri_monotonic_vulnerability_increase,
    test_ward_impact_projections
)
from tests.test_api import (
    test_health_endpoint,
    test_pune_metadata_endpoint,
    test_pune_wards_geojson_endpoint,
    test_calculate_stress_endpoint,
    test_trigger_hap_endpoint,
    test_compose_and_dispatch_alert
)

def run_all_tests():
    print("=" * 60)
    print("RUNNING SURAKSHATAAP PUNE (PMC) VERIFICATION SUITE")
    print("=" * 60)
    
    tests = [
        ("Vapor Pressure & Dew Point", test_vapor_pressure_and_dew_point),
        ("WBGT Humidity Compounding (ISO 7243)", test_wbgt_extreme_humidity_compounding),
        ("UTCI Thermal Stress Bands (Fiala Model)", test_utci_thermal_stress_bands),
        ("Physiological Strain & OSHA Safe Work Limits", test_physiological_strain_limits),
        ("Comprehensive Heat Stress Unified Endpoint", test_comprehensive_heat_stress_unified),
        ("HMRI Epidemiological Vulnerability Scaling", test_hmri_monotonic_vulnerability_increase),
        ("Ward Public Health & Casualty Projections", test_ward_impact_projections),
        ("FastAPI /health Endpoint", test_health_endpoint),
        ("FastAPI /api/pune/metadata Endpoint", test_pune_metadata_endpoint),
        ("FastAPI /api/pune/wards GeoJSON (12 PMC Wards)", test_pune_wards_geojson_endpoint),
        ("FastAPI /api/calculate-stress Endpoint", test_calculate_stress_endpoint),
        ("FastAPI /api/trigger-hap (PMC HAP Protocol)", test_trigger_hap_endpoint),
        ("FastAPI /api/compose-alert & /dispatch-alert (Marathi)", test_compose_and_dispatch_alert)
    ]
    
    passed = 0
    failed = 0
    
    for name, test_fn in tests:
        try:
            test_fn()
            print(f" [PASS] {name}")
        except Exception as e:
            print(f" [FAIL] {name}: {str(e)}")
            failed += 1
            
    print("=" * 60)
    print(f"TOTAL TESTS: {len(tests)} | PASSED: {passed} | FAILED: {failed}")
    print("=" * 60)
    
    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    run_all_tests()
