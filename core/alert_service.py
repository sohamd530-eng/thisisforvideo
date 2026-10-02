"""
Pune Municipal Corporation (PMC) - Regional Alert & Notification Engine
-----------------------------------------------------------------------
Generates localized, vernacular heatwave emergency alerts in Marathi (मराठी) and English
specifically tailored for Pune citizens, PMPML commuters, construction laborers, and PMC officials.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import uuid

# Multilingual Alert Templates for Pune PMC
PUNE_ALERT_TRANSLATIONS = {
    "mr": {
        "lang_name": "मराठी (Marathi)",
        "yellow": {
            "title": "⚠️ यलो अलर्ट: पुणे शहर उष्मा पूर्वसूचना (PMC Heat Watch)",
            "body": "पुणे मनपा कार्यक्षेत्र - {ward_name}: वातावरणात तापमान आणि आर्द्रतेचा ताण (WBGT: {wbgt}°C) वाढला आहे. नागरिकांनी, विशेषतः ज्येष्ठ नागरिकांनी भरपूर पाणी व लिंबू सरबत प्यावे.",
            "action": "दुपारी १२ ते ३ दरम्यान थेट उन्हात जाणे टाळा. जवळच्या मनपा शीतल जलकेंद्राचा लाभ घ्या."
        },
        "orange": {
            "title": "🚨 ऑरेंज अलर्ट: तीव्र उष्णतेची लाट इशारा! (PMC Heat Alert)",
            "body": "प्रभाग: {ward_name}। धोकादायक उष्मा निर्देशांक (UTCI: {utci}°C, हीट इंडेक्स: {hi}°C). बांधकाम कामगार व रस्त्यावरील विक्रेत्यांनी दुपारी ११:३० ते ३:३० दरम्यान जड शारीरिक श्रम थांबवावे.",
            "action": "उष्माघाताची लक्षणे (चक्कर, उलट्या, तीव्र ताप) आढळल्यास तात्काळ १०८ रुग्णवाहिका किंवा ससून/मनपा रुग्णालयात संपर्क साधा."
        },
        "red": {
            "title": "🛑 रेड अलर्ट: अति-गंभीर उष्मा आणीबाणी! (PMC Disaster Emergency)",
            "body": "पुणे जिल्हा आपत्ती व्यवस्थापन इशारा! {ward_name} मध्ये प्राणघातक उष्णता ताण (HMRI: {hmri}/100, WBGT: {wbgt}°C). घराबाहेर पडणे आरोग्यासाठी धोकादायक आहे. उघड्यावरील कामांवर पूर्ण बंदी.",
            "action": "मनपाचे वातानुकूलित कूलिंग सेंटर व समाजमंदिरे २४ तास खुली आहेत. विनामूल्य ओआरएस उपलब्ध."
        }
    },
    "en": {
        "lang_name": "English",
        "yellow": {
            "title": "⚠️ YELLOW ALERT: Pune Municipal Heat Watch",
            "body": "PMC Ward: {ward_name}. Elevated human thermal stress detected (WBGT: {wbgt}°C, Temp: {temp}°C, Humidity: {rh}%). Stay well hydrated with electrolytes/buttermilk and avoid prolonged midday sun exposure.",
            "action": "Rest in shaded zones. PMC drinking water stations are active across major transit halts."
        },
        "orange": {
            "title": "🚨 ORANGE ALERT: Severe Heat & Humidity Warning (PMC)",
            "body": "CRITICAL THERMAL LOAD in {ward_name} (UTCI: {utci}°C, Heat Index: {hi}°C). Compulsory 15-min rest every 45 min for outdoor construction workers. Direct physical labor prohibited from 11:30 AM to 3:30 PM.",
            "action": "If experiencing heat cramps or disorientation, contact 108 Emergency Ambulance or visit the nearest PMC UPHC."
        },
        "red": {
            "title": "🛑 RED ALERT / DISASTER EMERGENCY: Lethal Heatwave in Pune!",
            "body": "LIFE-THREATENING HEAT HAZARD in {ward_name} (HMRI: {hmri}/100, WBGT: {wbgt}°C). Evaporative sweat cooling has collapsed under high humidity. Section 30 Disaster Act protocols activated.",
            "action": "Take shelter immediately in designated AC Pune Metro stations or PMC Emergency Cooling Shelters."
        }
    }
}

class AlertDispatcher:
    """
    Manages multi-channel broadcasts across SMS, WhatsApp, and CAP for Pune PMC.
    """

    def __init__(self):
        self.broadcast_logs: List[Dict[str, Any]] = []

    def compose_alert(
        self,
        ward_name: str,
        marathi_name: str,
        alert_level: int,
        wbgt_c: float,
        utci_c: float,
        hi_c: float,
        temp_c: float,
        humidity_pct: float,
        hmri_score: float,
        lang: str = "mr",
        persona: str = "citizen"
    ) -> Dict[str, Any]:
        lang_dict = PUNE_ALERT_TRANSLATIONS.get(lang, PUNE_ALERT_TRANSLATIONS["mr"])
        tier_key = "yellow" if alert_level <= 1 else ("orange" if alert_level == 2 else "red")
        template = lang_dict.get(tier_key, lang_dict["yellow"])
        
        display_name = f"{marathi_name} ({ward_name})" if lang == "mr" else f"{ward_name}"
        title = template["title"]
        body = template["body"].format(
            ward_name=display_name,
            wbgt=wbgt_c,
            utci=utci_c,
            hi=hi_c,
            temp=temp_c,
            rh=humidity_pct,
            hmri=hmri_score
        )
        action = template["action"]
        
        persona_note = ""
        if persona == "laborer":
            persona_note = "\n\n[कामगार सूचना / Labor Mandate]: दर ४५ मिनिटांनी १५ मिनिटे सावलीत विश्रांती बंधनकारक. मालकाने थंड पाणी देणे सक्तीचे आहे."
        elif persona == "municipal_officer":
            persona_note = "\n\n[PMC Officer Trigger]: पत्र्यांच्या वस्त्यांमध्ये तातडीने पाण्याचे टँकर पाठवा आणि कूलिंग सेंटर सक्रिय करा."
        elif persona == "hospital_cmo":
            persona_note = f"\n\n[ससून/रुग्णालय अलर्ट]: अंदाजे {int(hmri_score * 0.7)} उष्माघात रुग्णांसाठी आयसीयू आणि ओआरएस कॉर्नर सज्ज ठेवा."
            
        full_message = f"{title}\n\n{body}\n\n💡 मार्गदर्शक सूचना / Action: {action}{persona_note}"
        
        return {
            "alert_id": f"PMC-ALT-{uuid.uuid4().hex[:6].upper()}",
            "language": lang,
            "language_name": lang_dict["lang_name"],
            "alert_level": alert_level,
            "tier": tier_key.upper(),
            "persona": persona,
            "ward_name": ward_name,
            "marathi_name": marathi_name,
            "headline": title,
            "message_body": full_message,
            "sms_length": len(full_message),
            "generated_at": datetime.now(timezone.utc).isoformat()
        }

    def dispatch_broadcast(
        self,
        ward_name: str,
        channel: str,
        alert_payload: Dict[str, Any],
        recipients_count: int = 2500
    ) -> Dict[str, Any]:
        dispatch_id = f"PMC-DISP-{uuid.uuid4().hex[:6].upper()}"
        timestamp = datetime.now(timezone.utc).isoformat()
        
        record = {
            "dispatch_id": dispatch_id,
            "timestamp": timestamp,
            "ward_name": ward_name,
            "channel": channel,
            "recipients_count": recipients_count,
            "delivered_count": int(recipients_count * 0.988),
            "status": "SUCCESS",
            "alert_level": alert_payload.get("alert_level", 1),
            "language": alert_payload.get("language", "mr"),
            "headline": alert_payload.get("headline", ""),
            "message_preview": alert_payload.get("message_body", "")[:120] + "..."
        }
        
        self.broadcast_logs.insert(0, record)
        if len(self.broadcast_logs) > 50:
            self.broadcast_logs = self.broadcast_logs[:50]
            
        return record

# Global Singleton
alert_dispatcher = AlertDispatcher()
