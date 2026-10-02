"""
Epidemiological AI & Heat-Induced Mortality / Hospitalization Surge Engine
-------------------------------------------------------------------------
Translates multi-dimensional thermal stress (WBGT, UTCI, Nighttime Tmin)
and localized demographic vulnerability (Elderly %, Slum %, Outdoor Workers %, UHI)
into:
1. Heat Mortality Risk Index (HMRI: 0 - 100)
2. Hospitalization Surge Rate (Emergency heatstroke & acute dehydration cases / day)
3. Projected Healthcare Resource Surge (Dedicated ICU beds, ORS sachets, IV fluid bags)
4. 3 to 5-Day Forward Mortality & Morbidity Projections
"""

import math
import numpy as np
from typing import Dict, Any, List, Optional
from core.thermal_stress import compute_wbgt, compute_utci, compute_heat_index

class HeatMortalityPredictor:
    """
    Non-linear epidemiological exposure-response model calibrated on
    Indian urban heatwave mortality cohorts (Ahmedabad, Delhi, Hyderabad, Nagpur).
    """

    def __init__(self):
        # Baseline epidemiological constants for Indian urban settings
        self.baseline_daily_mortality_rate_per_100k = 2.15  # Normal all-cause mortality rate
        self.baseline_daily_er_admissions_per_100k = 18.5   # Normal ER hospitalizations
        self.optimal_wbgt_threshold = 24.5                  # Minimum Mortality Temperature (MMT) equivalent WBGT
        self.optimal_utci_threshold = 24.0                  # MMT equivalent UTCI
        
    def calculate_hmri(
        self,
        wbgt_active: float,
        utci_c: float,
        t_max_c: float,
        t_min_c: float,
        humidity_pct: float,
        elderly_pct: float = 8.5,            # % of population aged > 60
        outdoor_worker_pct: float = 22.0,    # % informal/construction/street workers
        slum_density_pct: float = 30.0,      # % living in tin/asbestos/uninsulated housing
        uhi_intensity_c: float = 2.5,        # Urban Heat Island temperature anomaly (°C)
        tree_canopy_pct: float = 12.0        # Protective green canopy cover %
    ) -> Dict[str, Any]:
        """
        Calculates the Heat Mortality Risk Index (HMRI - scale 0 to 100)
        and relative risk multipliers.
        """
        # 1. Primary Thermal Hazard Metric (Combined WBGT & UTCI load)
        # Wet-bulb stress component (exponential risk above 28°C WBGT)
        wbgt_excess = max(0.0, wbgt_active - self.optimal_wbgt_threshold)
        utci_excess = max(0.0, utci_c - self.optimal_utci_threshold)
        
        # Exponential epidemiological thermal load curve
        base_thermal_load = (
            0.55 * (math.exp(wbgt_excess * 0.32) - 1.0) +
            0.45 * (math.exp(utci_excess * 0.14) - 1.0)
        )
        
        # 2. Nighttime Heat Retention Modifier (Loss of nocturnal physiological recovery)
        # If Tmin > 28°C, mortality jumps sharply due to sustained cardiovascular stress during sleep
        night_strain_factor = 1.0
        if t_min_c > 27.0:
            night_strain_factor += 0.25 * (t_min_c - 27.0) ** 1.35
            
        # 3. Demographic & Microclimate Vulnerability Score (V_index from 0.5 to 3.0)
        elderly_factor = (elderly_pct / 8.0) * 0.35
        worker_factor = (outdoor_worker_pct / 20.0) * 0.30
        slum_factor = (slum_density_pct / 25.0) * 0.25
        uhi_factor = (uhi_intensity_c / 2.0) * 0.15
        green_mitigation = (tree_canopy_pct / 20.0) * 0.15
        
        vulnerability_multiplier = 0.5 + elderly_factor + worker_factor + slum_factor + uhi_factor - green_mitigation
        vulnerability_multiplier = max(0.6, min(3.2, vulnerability_multiplier))
        
        # 4. Total Composite HMRI (0 - 100)
        raw_hmri = base_thermal_load * night_strain_factor * vulnerability_multiplier * 4.2
        hmri = max(0.0, min(100.0, raw_hmri))
        
        # Risk Tier Classification
        if hmri < 20.0:
            risk_tier = "Low Risk (Normal)"
            color = "#10b981"  # Green
            alert_level = 0
            public_health_summary = "Normal physiological baseline. Standard hydration advisory."
        elif hmri < 45.0:
            risk_tier = "Moderate Risk (Yellow Alert)"
            color = "#f59e0b"  # Yellow/Amber
            alert_level = 1
            public_health_summary = "Mild excess mortality risk among bedridden elderly and outdoor laborers."
        elif hmri < 70.0:
            risk_tier = "High Risk (Orange Alert)"
            color = "#f97316"  # Orange
            alert_level = 2
            public_health_summary = "Significant excess mortality spike. Surge in heat exhaustion & dehydration admissions."
        elif hmri < 88.0:
            risk_tier = "Severe Risk (Red Alert)"
            color = "#ef4444"  # Red
            alert_level = 3
            public_health_summary = "Critical public health emergency. Sharp rise in heatstroke fatalities and ER collapse risk."
        else:
            risk_tier = "Extreme Disaster (Flash Heat Emergency)"
            color = "#7c3aed"  # Purple
            alert_level = 4
            public_health_summary = "Lethal thermal threshold exceeded. Wet-bulb hazard threatening healthy populations."
            
        # Excess Mortality & Morbidity Percentage Multipliers
        excess_mortality_pct = max(0.0, (hmri / 100.0) ** 1.45 * 85.0)
        hospital_surge_pct = max(0.0, (hmri / 100.0) ** 1.30 * 160.0)
        
        return {
            "hmri_score": round(hmri, 1),
            "risk_tier": risk_tier,
            "color_code": color,
            "alert_level": alert_level,
            "public_health_summary": public_health_summary,
            "vulnerability_multiplier": round(vulnerability_multiplier, 2),
            "night_strain_factor": round(night_strain_factor, 2),
            "excess_mortality_pct": round(excess_mortality_pct, 1),
            "hospital_surge_pct": round(hospital_surge_pct, 1)
        }

    def predict_ward_impact(
        self,
        ward_name: str,
        population: int,
        weather_forecast: Dict[str, Any],
        demographics: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Generates ward-level impact predictions:
        - Absolute projected excess deaths / day
        - Daily emergency heatstroke & dehydration admissions
        - Healthcare resources required (ICU beds, ORS packets, IV fluid units)
        """
        t_max = weather_forecast.get("temp_max_c", 41.0)
        t_min = weather_forecast.get("temp_min_c", 29.0)
        rh = weather_forecast.get("humidity_pct", 55.0)
        wind = weather_forecast.get("wind_kmh", 6.0)
        solar = weather_forecast.get("solar_radiation_wm2", 750.0)
        
        # Thermal stress
        wbgt_info = compute_wbgt(t_max, rh, wind / 3.6, solar)
        utci_info = compute_utci(t_max, rh, wind / 3.6, solar)
        
        hmri_res = self.calculate_hmri(
            wbgt_active=wbgt_info["wbgt_active"],
            utci_c=utci_info["utci_c"],
            t_max_c=t_max,
            t_min_c=t_min,
            humidity_pct=rh,
            elderly_pct=demographics.get("elderly_pct", 9.0),
            outdoor_worker_pct=demographics.get("outdoor_worker_pct", 24.0),
            slum_density_pct=demographics.get("slum_density_pct", 35.0),
            uhi_intensity_c=demographics.get("uhi_intensity_c", 2.8),
            tree_canopy_pct=demographics.get("tree_canopy_pct", 10.0)
        )
        
        # Absolute population metrics
        pop_100k = population / 100000.0
        baseline_deaths = pop_100k * self.baseline_daily_mortality_rate_per_100k
        baseline_er = pop_100k * self.baseline_daily_er_admissions_per_100k
        
        excess_deaths_daily = baseline_deaths * (hmri_res["excess_mortality_pct"] / 100.0)
        total_er_admissions_daily = baseline_er * (1.0 + hmri_res["hospital_surge_pct"] / 100.0)
        heat_specific_admissions = total_er_admissions_daily - baseline_er
        
        # ICU beds demand (approx 12% of severe heatstroke cases require intensive cooling & ICU)
        projected_icu_beds_needed = max(1, int(heat_specific_admissions * 0.12))
        
        # ORS and IV fluid demand
        ors_packets_daily = int(population * (0.015 + (hmri_res["hmri_score"] / 100.0) * 0.08))
        iv_fluid_units_daily = int(heat_specific_admissions * 3.5)
        
        # Outdoor worker population at direct risk
        vulnerable_pop_count = int(population * (
            demographics.get("elderly_pct", 9.0) / 100.0 +
            demographics.get("outdoor_worker_pct", 24.0) / 100.0 * 0.8 +
            demographics.get("slum_density_pct", 35.0) / 100.0 * 0.5
        ))
        
        return {
            "ward_name": ward_name,
            "population": population,
            "vulnerable_population_count": vulnerable_pop_count,
            "hmri": hmri_res,
            "thermal_metrics": {
                "wbgt_c": wbgt_info["wbgt_active"],
                "utci_c": utci_info["utci_c"],
                "wet_bulb_c": wbgt_info["natural_wet_bulb"],
                "t_max_c": t_max,
                "t_min_c": t_min
            },
            "epidemiological_projections": {
                "baseline_daily_deaths": round(baseline_deaths, 2),
                "projected_excess_deaths_daily": round(excess_deaths_daily, 2),
                "total_projected_deaths_daily": round(baseline_deaths + excess_deaths_daily, 2),
                "heat_er_admissions_daily": int(heat_specific_admissions),
                "total_er_admissions_daily": int(total_er_admissions_daily),
                "projected_icu_beds_needed": projected_icu_beds_needed,
                "daily_ors_packets_needed": ors_packets_daily,
                "daily_iv_fluid_units_needed": iv_fluid_units_daily
            }
        }

    def generate_5_day_forecast_trajectory(
        self,
        ward_name: str,
        population: int,
        demographics: Dict[str, float],
        daily_weather_series: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generates 3 to 5-day predictive trajectory of heat stress, HMRI,
        and hospital load spikes.
        """
        trajectory = []
        for day_idx, day_weather in enumerate(daily_weather_series):
            impact = self.predict_ward_impact(
                ward_name=ward_name,
                population=population,
                weather_forecast=day_weather,
                demographics=demographics
            )
            impact["day_offset"] = day_idx
            impact["date_label"] = day_weather.get("date_label", f"Day +{day_idx + 1}")
            trajectory.append(impact)
            
        return trajectory


# Global Singleton Instance
mortality_predictor = HeatMortalityPredictor()
