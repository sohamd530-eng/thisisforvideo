"""
Pune Municipal Corporation (PMC) - Automated Heat Action Plan (HAP) Engine
-------------------------------------------------------------------------
Translates predictive thermal stress (WBGT/UTCI) and ward vulnerability
into automated, legally actionable directives for PMC Administration,
PMPML, Sassoon Hospital, MSEDCL, and Pune District Disaster Management Authority.
"""

from typing import Dict, Any, List
from datetime import datetime, timezone

class HeatActionPlanEngine:
    """
    Generates sector-specific, hyper-local interventions for Pune Municipal Commissioner,
    Labor Officer, Sassoon Hospital Dean, and PMC Disaster Management Cell.
    """

    def generate_ward_hap(
        self,
        ward_id: str,
        ward_name: str,
        marathi_name: str,
        alert_level: int,       # 0: Green, 1: Yellow, 2: Orange, 3: Red, 4: Purple
        wbgt_c: float,
        utci_c: float,
        hmri_score: float,
        demographics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Synthesizes an immediate Heat Action Plan bulletin for the specified PMC ward.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        
        municipal_actions = []
        labor_actions = []
        health_actions = []
        power_water_actions = []
        
        if alert_level == 0:
            alert_tier = "GREEN (Normal Operations / सामान्य स्थिती)"
            alert_color = "#10b981"
            emergency_code = "PMC-HAP-LVL-0"
            summary = f"पुणे शहर - {marathi_name}: सामान्य तापमान व आर्द्रता. नियमित आरोग्य देखरेख सुरू आहे."
            
            municipal_actions.append({
                "id": "PMC-MUN-01",
                "action": "Routine inspection of PMPML bus station water coolers and garden fountains.",
                "action_mr": "पीएमपीएमएल बस स्थानकांवरील पिण्याच्या पाण्याच्या टाक्यांची नियमित तपासणी.",
                "dept": "PMC Water Supply Dept (पाणी पुरवठा विभाग)",
                "urgency": "Low"
            })
            labor_actions.append({
                "id": "PMC-LAB-01",
                "action": "Ensure basic shaded rest shelters at active construction sites.",
                "action_mr": "बांधकाम प्रकल्पांवर सावलीची सोय उपलब्ध असल्याची खात्री करणे.",
                "dept": "Labor Commissionerate Pune",
                "urgency": "Low"
            })
            health_actions.append({
                "id": "PMC-HLT-01",
                "action": "Maintain standard buffer stock of ORS at all PMC Urban Primary Health Centres (UPHCs).",
                "action_mr": "मनपा नागरी प्राथमिक आरोग्य केंद्रांमध्ये ओआरएसचा पुरेसा साठा ठेवणे.",
                "dept": "PMC Health Dept (आरोग्य विभाग)",
                "urgency": "Low"
            })
            
        elif alert_level == 1:
            alert_tier = "YELLOW (Heat Watch / उष्णता पूर्वसूचना)"
            alert_color = "#f59e0b"
            emergency_code = "PMC-HAP-LVL-1"
            summary = f"{marathi_name}: तापमान आणि उष्मा निर्देशांक (WBGT: {wbgt_c}°C) वाढला आहे. सावधगिरीच्या उपाययोजना लागू."
            
            municipal_actions.extend([
                {
                    "id": "PMC-MUN-11",
                    "action": "Open PMC public gardens (Sambhaji Park, Sarasbaug, PL Deshpande) and community halls for daytime public resting.",
                    "action_mr": "संभाजी पार्क, सारसबाग, पु. ल. देशपांडे उद्यान व मनपा समाजमंदिरे दुपारी विश्रांतीसाठी खुली ठेवणे.",
                    "dept": "PMC Garden & Estate Dept (उद्यान विभाग)",
                    "urgency": "Medium"
                },
                {
                    "id": "PMC-MUN-12",
                    "action": "Activate earthen pot (Matka) drinking water stations at high footfall PMPML transit halts (Swargate, Pune Station, Katraj).",
                    "action_mr": "स्वारगेट, पुणे स्टेशन, कात्रज पीएमपीएमएल थांब्यांवर मातीचे रांजण व शीतल पाण्याची सोय करणे.",
                    "dept": "PMPML & PMC Disaster Cell",
                    "urgency": "Medium"
                }
            ])
            labor_actions.extend([
                {
                    "id": "PMC-LAB-11",
                    "action": "Issue formal advisory to CREDAI Pune & builders to provide shaded electrolyte water stations.",
                    "action_mr": "क्रेडाई पुणे व बांधकाम व्यावसायिकांना कामगारांसाठी सावली व इलेक्ट्रोलाइट्स देण्याचे निर्देश.",
                    "dept": "Labor Welfare Board Pune",
                    "urgency": "Medium"
                }
            ])
            health_actions.extend([
                {
                    "id": "PMC-HLT-11",
                    "action": "Deploy ASHA and Anganwadi workers for door-to-door checkups of bedridden senior citizens in older Peths & Kothrud.",
                    "action_mr": "आशा व अंगणवाडी सेविकांमार्फत पेठांमधील व कोथरूडमधील ज्येष्ठ नागरिकांची आरोग्य तपासणी.",
                    "dept": "PMC Health Department",
                    "urgency": "Medium"
                }
            ])
            
        elif alert_level == 2:
            alert_tier = "ORANGE (Heat Alert / गंभीर उष्णता इशारा)"
            alert_color = "#f97316"
            emergency_code = "PMC-HAP-LVL-2"
            summary = f"तीव्र उष्माघात इशारा: {marathi_name} परिसरात घातक तापमान आणि आर्द्रता (UTCI: {utci_c}°C). दुपारच्या कामांवर निर्बंध लागू."
            
            municipal_actions.extend([
                {
                    "id": "PMC-MUN-21",
                    "action": f"Dispatch 4 emergency water tankers specifically to high-density tin-roof settlements in {ward_name} (Yerwada/Parvati/Janata Vasahat).",
                    "action_mr": f"{marathi_name} मधील पत्र्यांच्या वस्त्यांसाठी ४ तातडीचे मनपा पाण्याचे टँकर रवाना करणे.",
                    "dept": "PMC Water Tanker Cell",
                    "urgency": "High"
                },
                {
                    "id": "PMC-MUN-22",
                    "action": "Deploy Pune Fire Brigade mist-cannon sprayers at Alka Talkies, Shimla Office, and Swargate intersections (12 PM - 4 PM).",
                    "action_mr": "अलका टॉकीज, शिमला ऑफिस आणि स्वारगेट चौकात अग्निशामक दलाचे वॉटर मिस्ट कॅनन्स चालवणे.",
                    "dept": "Pune Fire & Disaster Services",
                    "urgency": "High"
                },
                {
                    "id": "PMC-MUN-23",
                    "action": "Designate AC Pune Metro stations (Vanaz to Ramwadi & PCMC to Swargate) as official daytime cooling shelters.",
                    "action_mr": "पुणे मेट्रोची वातानुकूलित स्थानके नागरिकांसाठी अधिकृत कूलिंग शेल्टर म्हणून खुली करणे.",
                    "dept": "MahaMetro & PMC Transit Cell",
                    "urgency": "High"
                }
            ])
            labor_actions.extend([
                {
                    "id": "PMC-LAB-21",
                    "action": "MANDATORY WORK REGIME: Compulsory 15 min rest every 45 min for outdoor construction/infrastructure laborers.",
                    "action_mr": "सक्तीचा नियम: उघड्यावर काम करणाऱ्या मजुरांसाठी दर ४५ मिनिटांनंतर १५ मिनिटे विश्रांती बंधनकारक.",
                    "dept": "Factory & Boilers Inspectorate",
                    "urgency": "Critical"
                },
                {
                    "id": "PMC-LAB-22",
                    "action": "Enforce work shift rescheduling: Prohibit heavy physical excavation/masonry between 11:30 AM and 3:30 PM.",
                    "action_mr": "दुपारी ११:३० ते ३:३० दरम्यान कडक उन्हात जड कामे करण्यास सक्त मनाई.",
                    "dept": "Department of Labor Maharashtra",
                    "urgency": "Critical"
                }
            ])
            health_actions.extend([
                {
                    "id": "PMC-HLT-21",
                    "action": "Activate Dedicated Heatstroke Stabilization Units at Sassoon General Hospital, Naidu Infectious Hospital, and Rajiv Gandhi Hospital.",
                    "action_mr": "ससून रुग्णालय, नायडू रुग्णालय व राजीव गांधी रुग्णालयात विशेष उष्माघात कक्ष (Ice-Bath Units) सुरू करणे.",
                    "dept": "Sassoon Hospital & PMC Health Dept",
                    "urgency": "High"
                },
                {
                    "id": "PMC-HLT-22",
                    "action": "Stage AC 108 Emergency Ambulances at Hadapsar Gadital, Katraj Chowk, and Yerwada.",
                    "action_mr": "हडपसर गाडीतळ, कात्रज चौक व येरवडा येथे १०८ रुग्णवाहिका सज्ज ठेवणे.",
                    "dept": "Maharashtra Emergency Medical Services (MEMS)",
                    "urgency": "High"
                }
            ])
            power_water_actions.extend([
                {
                    "id": "PMC-PWR-21",
                    "action": "MSEDCL Grid Alert: Anticipate +22% residential air cooler load surge; position mobile transformer replacement units in Peth areas.",
                    "action_mr": "महावितरण अलर्ट: वीज भार वाढल्याने ट्रान्सफॉर्मर जळू नये म्हणून फिरती दुरुस्ती पथके सज्ज ठेवणे.",
                    "dept": "MSEDCL Pune Circle (महावितरण)",
                    "urgency": "High"
                }
            ])
            
        else:  # Red or Purple Alert (alert_level >= 3)
            alert_tier = "RED / PURPLE (Disaster Emergency / अति-घातक उष्मा आणीबाणी)"
            alert_color = "#ef4444" if alert_level == 3 else "#7c3aed"
            emergency_code = "PMC-HAP-LVL-3-DISASTER"
            summary = f"पुणे जिल्हा आपत्ती व्यवस्थापन प्राधिकरण - धारा ३०/३४ नुसार आणीबाणी: {marathi_name} मध्ये प्राणघातक उष्णता निर्देशांक (HMRI: {hmri_score}/100)."
            
            municipal_actions.extend([
                {
                    "id": "PMC-MUN-31",
                    "action": f"FULL DISASTER MOBILIZATION: Continuous roving drinking water and ORS distribution across all slum pockets of {ward_name}.",
                    "action_mr": f"आपत्ती व्यवस्थापन आदेश: {marathi_name} मधील सर्व वस्त्यांमध्ये फिरत्या वाहनांद्वारे ओआरएस व पाण्याचे वाटप.",
                    "dept": "District Disaster Management Authority (DDMA Pune)",
                    "urgency": "Immediate / Emergency"
                },
                {
                    "id": "PMC-MUN-32",
                    "action": "Keep ALL PMC community halls, sports complexes, and AC libraries open 24x7 with free cold water and electrolytes.",
                    "action_mr": "मनपाची सर्व समाजमंदिरे व क्रीडा संकुले २४ तास नागरिकांच्या निवाऱ्यासाठी खुली ठेवणे.",
                    "dept": "Municipal Commissioner's Office, PMC",
                    "urgency": "Immediate / Emergency"
                }
            ])
            labor_actions.extend([
                {
                    "id": "PMC-LAB-31",
                    "action": "COMPLETE BAN ON OUTDOOR LABOR from 11:00 AM to 4:30 PM under Disaster Management Act. Violators face penal action.",
                    "action_mr": "आपत्ती कायद्यान्वये सकाळी ११:०० ते दुपारी ४:३० पर्यंत उघड्यावरील सर्व कामांवर पूर्ण बंदी.",
                    "dept": "Pune Police & Labor Commissioner",
                    "urgency": "Immediate / Emergency"
                },
                {
                    "id": "PMC-LAB-32",
                    "action": "Food & delivery aggregators (Swiggy, Zomato, Blinkit) mandated to provide shaded rest hubs and hydration stations.",
                    "action_mr": "डिलिव्हरी कंपन्यांनी रायडर्ससाठी सावलीचे विश्रांती केंद्र व पाणी देणे सक्तीचे.",
                    "dept": "RTO Pune & Police Commissionerate",
                    "urgency": "Immediate / Emergency"
                }
            ])
            health_actions.extend([
                {
                    "id": "PMC-HLT-31",
                    "action": "CODE HEAT RED AT SASSOON HOSPITAL: Cancel routine elective procedures; reserve 30% of ICU beds for acute core-cooling.",
                    "action_mr": "ससून व मनपा रुग्णालयांमध्ये 'कोड रेड': ३०% आयसीयू खाटा उष्माघात रुग्णांसाठी राखीव.",
                    "dept": "Dean, BJ Medical College & Sassoon Hospital",
                    "urgency": "Immediate / Emergency"
                }
            ])
            power_water_actions.extend([
                {
                    "id": "PMC-PWR-31",
                    "action": "ZERO-LOAD-SHEDDING PROTOCOL: Total protection of hospital feeders, water pumping stations (Parvati & Cantonment water works).",
                    "action_mr": "पर्वती व लष्कर जलकेंद्र आणि सर्व रुग्णालयांना अखंड वीज पुरवठा सुनिश्चित करणे.",
                    "dept": "MSEDCL Chief Engineer Pune",
                    "urgency": "Immediate / Emergency"
                }
            ])
            
        return {
            "ward_id": ward_id,
            "ward_name": ward_name,
            "marathi_name": marathi_name,
            "timestamp": timestamp,
            "emergency_code": emergency_code,
            "alert_tier": alert_tier,
            "alert_color": alert_color,
            "alert_level": alert_level,
            "metrics": {
                "wbgt_c": wbgt_c,
                "utci_c": utci_c,
                "hmri_score": hmri_score
            },
            "executive_summary": summary,
            "sectoral_action_plan": {
                "municipal_and_urban": municipal_actions,
                "labor_and_workplaces": labor_actions,
                "healthcare_and_hospitals": health_actions,
                "power_and_water_utilities": power_water_actions
            },
            "targeted_vulnerability_flags": {
                "elderly_alert": demographics.get("elderly_pct", 0) > 12.0,
                "slum_roofing_alert": demographics.get("slum_density_pct", 0) > 35.0,
                "outdoor_labor_hazard": demographics.get("outdoor_worker_pct", 0) > 25.0,
                "uhi_hotspot": demographics.get("uhi_intensity_c", 0) > 3.0
            }
        }

# Global Singleton
hap_engine = HeatActionPlanEngine()
