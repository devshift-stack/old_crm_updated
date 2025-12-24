# 📞 Vonage + ElevenLabs Voice AI Integration

## 🎯 Was ist möglich?

Mit **Vonage Voice API** + **ElevenLabs Conversational AI** kannst du:

- ✅ **Eingehende Anrufe** automatisch mit AI Voice Agent beantworten
- ✅ **Ausgehende Anrufe** mit AI Voice tätigen
- ✅ **Echtzeitgespräche** mit sub-second Latenz
- ✅ **Natural Language** Telefongespräche
- ✅ **CRM Integration** - Calls mit deinen Kontakten verbinden
- ✅ **Standalone Caller** - Unabhängiges Voice Agent System

---

## 🔧 Wie es funktioniert

### **Technische Architektur:**

```
┌─────────────────┐
│  Telefon-Anruf  │ (PSTN/SIP/VoIP)
└────────┬────────┘
         │
┌────────▼────────────────────────────┐
│     Vonage Voice API                │
│  - WebSocket Connection             │
│  - Audio Stream (L16, 16kHz)        │
└────────┬────────────────────────────┘
         │
┌────────▼────────────────────────────┐
│  WebSocket Connector (Node.js)      │
│  - Audio Format Conversion          │
│  - Bidirectional Streaming          │
│  - Event Handling                   │
└────────┬────────────────────────────┘
         │
┌────────▼────────────────────────────┐
│  ElevenLabs Conversational AI       │
│  - Speech-to-Text                   │
│  - AI Processing (LLM)              │
│  - Text-to-Speech (Natural Voice)   │
└────────┬────────────────────────────┘
         │
┌────────▼────────────────────────────┐
│  Optional: Mac Assistant CRM        │
│  - Kontakt-Lookup                   │
│  - Call Logging                     │
│  - Task Execution                   │
└─────────────────────────────────────┘
```

---

## 🚀 Setup-Optionen

### **Option 1: Standalone Voice Agent** 🤖

**Use Case:** Automatische Anrufbeantwortung, Telefon-Bot, Voice Assistant

**Was du brauchst:**
1. Vonage Account + Phone Number
2. ElevenLabs Account + API Key
3. WebSocket Connector (Node.js)
4. ngrok oder Cloud Hosting

**Setup:**
```bash
# 1. Clone Connector
git clone https://github.com/nexmo-se/elevenlabs-agent-ws-connector.git
cd elevenlabs-agent-ws-connector

# 2. Install Dependencies
npm install

# 3. Configure .env
ELEVENLABS_API_KEY=your-api-key
ELEVENLABS_AGENT_ID=your-agent-id

# 4. Start Connector
node elevenlabs-agent-ws-connector.cjs

# 5. Expose with ngrok
ngrok http 6000
```

**Vonage Setup:**
```json
// Answer URL returns this NCCO:
[
  {
    "action": "connect",
    "endpoint": [
      {
        "type": "websocket",
        "uri": "wss://YOUR-NGROK-URL/socket",
        "content-type": "audio/l16;rate=16000"
      }
    ]
  }
]
```

---

### **Option 2: CRM Integration** 📊

**Use Case:** Verbinde Calls mit Mac Assistant, Log Activities, Smart Routing

**Integration in Mac Assistant:**

**Neue Module:**
- `voice_ai/vonage_client.py` - Vonage Voice API Client
- `voice_ai/elevenlabs_connector.py` - WebSocket Connector
- `voice_ai/call_manager.py` - Call Management & Logging

**Funktionen:**
```python
from mac_assistant.voice_ai import VoiceAIManager

# Initialisieren
voice = VoiceAIManager(
    vonage_api_key='your-key',
    vonage_api_secret='your-secret',
    vonage_application_id='your-app-id',
    elevenlabs_api_key='your-key',
    elevenlabs_agent_id='your-agent-id'
)

# Ausgehender Anruf
call = voice.make_call(
    to='+491234567890',
    context="Kunde Max Mustermann, letztes Gespräch vor 3 Tagen"
)

# Call wird geloggt in Activity Database
# → CRM hat vollständige Call History

# Eingehender Anruf
@voice.on_incoming_call
def handle_call(call):
    # Lookup Kontakt in CRM
    contact = crm.find_contact(call.from_number)

    # AI Agent bekommt Kontext
    call.set_context(f"Anrufer: {contact.name}, Status: {contact.status}")

    # Anruf verbinden
    call.connect_to_agent()

    # Nach Anruf: Log Activity
    tracker.log_activity(
        app_name='Phone',
        activity_type='call_received',
        title=f'Call from {contact.name}',
        content=call.transcript
    )
```

---

## 💰 Kosten

### **Vonage Voice API:**
- **Eingehende Anrufe:** ~€0.0040/min (Deutschland)
- **Ausgehende Anrufe:** ~€0.0090/min (Deutschland)
- **Phone Number:** ~€0.90/Monat
- **Free Tier:** €2 Guthaben zum Testen

### **ElevenLabs:**
- **Free Tier:** 10,000 Zeichen/Monat
- **Starter:** $5/Monat - 30,000 Zeichen
- **Creator:** $22/Monat - 100,000 Zeichen
- **Conversational AI:** Extra Kosten pro Minute

**Total pro Anruf (1 Min):**
- Vonage: €0.0040 - €0.0090
- ElevenLabs: ~€0.01 - €0.05
- **~€0.02 - €0.06 pro Minute**

---

## 🎁 Features die möglich sind

### **Standalone Features:**
1. **Auto-Attendant** - "Danke für Ihren Anruf bei..."
2. **Voice Bot** - FAQ beantworten, Support
3. **Appointment Booking** - "Wann möchten Sie einen Termin?"
4. **Order Taking** - "Was möchten Sie bestellen?"
5. **Survey/Feedback** - Automatische Umfragen

### **CRM Integration Features:**
1. **Smart Routing** - Basierend auf Kontaktdaten
2. **Call Logging** - Automatische Activity Tracking
3. **Context-Aware Agent** - AI kennt Kundenhistorie
4. **Post-Call Tasks** - "Erstelle Follow-up E-Mail"
5. **Analytics** - Call-Statistiken im Dashboard
6. **Notifications** - "Wichtiger Kunde ruft an!"

---

## 🔑 API Keys & Credentials

### **Vonage:**
1. Account: https://dashboard.nexmo.com/
2. API Key + Secret (JWT Authentication)
3. Application ID (Voice App erstellen)
4. Phone Number (kaufen/zuweisen)

### **ElevenLabs:**
1. Account: https://elevenlabs.io/
2. API Key: My Account → API Keys
3. Agent ID: Agents Platform → Create Agent → Settings

---

## 📋 Setup-Guide

### **1. Vonage Account Setup**

```bash
# 1. Registrieren
https://dashboard.nexmo.com/sign-up

# 2. Voice Application erstellen
Name: Mac Assistant Voice AI
Answer URL: https://YOUR-SERVER/webhooks/answer
Event URL: https://YOUR-SERVER/webhooks/event

# 3. Phone Number kaufen
Numbers → Buy Numbers → Suche Deutschland
Link to Application: Mac Assistant Voice AI

# 4. Credentials notieren
API Key: abc123
API Secret: xyz789
Application ID: app-id-123
Phone Number: +4930123456
```

### **2. ElevenLabs Agent Setup**

```bash
# 1. Registrieren
https://elevenlabs.io/sign-up

# 2. Agent erstellen
Agents Platform → Create Agent
Name: Mac Assistant
Voice: Wähle deutsche Stimme
Model: Turbo v2.5 (schnellste)

# 3. Agent konfigurieren
System Prompt: "Du bist ein freundlicher Assistent..."
Knowledge Base: Optional CRM Infos
Tools: Optional API Calls

# 4. Credentials notieren
API Key: sk_abc123...
Agent ID: agent_xyz789...
```

### **3. Connector Deployment**

**Option A: Lokal mit ngrok (Testing)**
```bash
# WebSocket Connector starten
node elevenlabs-agent-ws-connector.cjs

# In anderem Terminal: ngrok
ngrok http 6000
# URL: https://abc123.ngrok.io

# In Vonage Answer URL:
wss://abc123.ngrok.io/socket
```

**Option B: Cloud Deployment (Production)**
```bash
# Heroku
heroku create mac-assistant-voice
git push heroku main

# Railway
railway init
railway up

# Fly.io
fly launch
fly deploy

# URL: https://mac-assistant-voice.fly.dev
# WebSocket: wss://mac-assistant-voice.fly.dev/socket
```

### **4. Mac Assistant Integration**

```bash
cd mac_assistant

# .env erweitern
ENABLE_VOICE_AI=true
VONAGE_API_KEY=abc123
VONAGE_API_SECRET=xyz789
VONAGE_APPLICATION_ID=app-id-123
VONAGE_PHONE_NUMBER=+4930123456
ELEVENLABS_API_KEY=sk_abc123
ELEVENLABS_AGENT_ID=agent_xyz789
VOICE_AI_CONNECTOR_URL=wss://your-connector.fly.dev/socket
```

---

## 🧪 Testing

### **Inbound Call Test:**
```bash
# 1. Connector läuft
# 2. Vonage Answer URL konfiguriert
# 3. Ruf deine Vonage Number an
# 4. AI Agent antwortet!
```

### **Outbound Call Test:**
```python
from mac_assistant.voice_ai import VoiceAIManager

voice = VoiceAIManager()
call = voice.make_call(
    to='+49123456789',
    message="Hallo, ich bin dein AI Assistant..."
)
print(f"Call ID: {call.id}")
```

---

## 🎯 Use Cases für dich

### **1. Personal Assistant Caller**
```
Szenario: "Ruf bei Restaurant an und reserviere Tisch für 4 Personen um 19 Uhr"

Mac Assistant:
→ Macht Anruf über Vonage
→ ElevenLabs Agent spricht mit Restaurant
→ Reservierung wird gemacht
→ Bestätigung in CRM geloggt
```

### **2. Incoming Call Handler**
```
Szenario: Jemand ruft deine Nummer an

Vonage:
→ Empfängt Anruf
→ Verbindet mit ElevenLabs AI Agent
→ Agent beantwortet Fragen
→ Optional: Durchstellen zu dir
→ Transcript wird in Mac Assistant gespeichert
```

### **3. CRM Phone Integration**
```
Szenario: Du siehst Kontakt in Linear, willst anrufen

Linear Integration:
→ Click to Call
→ Vonage macht Anruf
→ Optional: AI Agent als Assistent dabei
→ Call wird automatisch geloggt
→ Follow-up Tasks werden erstellt
```

---

## 💻 Code-Beispiel für Mac Assistant

**Neue Datei:** `mac_assistant/voice_ai/__init__.py`

```python
"""
Voice AI Module
Vonage + ElevenLabs Integration
"""

from .vonage_client import VonageClient
from .call_manager import CallManager
from .elevenlabs_connector import ElevenLabsConnector

__all__ = ['VonageClient', 'CallManager', 'ElevenLabsConnector']
```

**Neue Datei:** `mac_assistant/voice_ai/vonage_client.py`

```python
"""
Vonage Voice API Client
"""

import os
import jwt
import time
import requests
from typing import Optional, Dict

class VonageClient:
    """Vonage Voice API Client"""

    def __init__(self, api_key: str = None, api_secret: str = None,
                 application_id: str = None, private_key_path: str = None):
        self.api_key = api_key or os.getenv('VONAGE_API_KEY')
        self.api_secret = api_secret or os.getenv('VONAGE_API_SECRET')
        self.application_id = application_id or os.getenv('VONAGE_APPLICATION_ID')
        self.private_key_path = private_key_path or os.getenv('VONAGE_PRIVATE_KEY_PATH')

        self.base_url = 'https://api.nexmo.com'

    def _generate_jwt(self) -> str:
        """Generate JWT for authentication"""
        with open(self.private_key_path, 'r') as f:
            private_key = f.read()

        payload = {
            'application_id': self.application_id,
            'iat': int(time.time()),
            'exp': int(time.time()) + 3600,
            'jti': str(time.time())
        }

        return jwt.encode(payload, private_key, algorithm='RS256')

    def make_call(self, to: str, answer_url: str,
                  event_url: str = None, from_number: str = None) -> Dict:
        """
        Make outbound call

        Args:
            to: Phone number to call (E.164 format, e.g. +491234567890)
            answer_url: Webhook URL for call answer (NCCO)
            event_url: Webhook URL for call events
            from_number: Your Vonage number

        Returns:
            Call details
        """
        token = self._generate_jwt()

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        from_number = from_number or os.getenv('VONAGE_PHONE_NUMBER')

        data = {
            'to': [{'type': 'phone', 'number': to}],
            'from': {'type': 'phone', 'number': from_number},
            'answer_url': [answer_url],
            'event_url': [event_url] if event_url else []
        }

        response = requests.post(
            f'{self.base_url}/v1/calls',
            headers=headers,
            json=data
        )

        response.raise_for_status()
        return response.json()

    def get_call(self, call_id: str) -> Dict:
        """Get call details"""
        token = self._generate_jwt()

        headers = {
            'Authorization': f'Bearer {token}'
        }

        response = requests.get(
            f'{self.base_url}/v1/calls/{call_id}',
            headers=headers
        )

        response.raise_for_status()
        return response.json()

    def transfer_call(self, call_id: str, ncco: list) -> Dict:
        """Transfer or modify active call"""
        token = self._generate_jwt()

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        data = {'action': 'transfer', 'destination': {'type': 'ncco', 'ncco': ncco}}

        response = requests.put(
            f'{self.base_url}/v1/calls/{call_id}',
            headers=headers,
            json=data
        )

        response.raise_for_status()
        return response.json()

    def hangup_call(self, call_id: str) -> Dict:
        """Hangup active call"""
        token = self._generate_jwt()

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        data = {'action': 'hangup'}

        response = requests.put(
            f'{self.base_url}/v1/calls/{call_id}',
            headers=headers,
            json=data
        )

        response.raise_for_status()
        return response.json()
```

**Integration Beispiel:**

```python
# In core_v2.py

from mac_assistant.voice_ai import VonageClient, CallManager

class MacAssistantCore:
    def __init__(self, api_key: Optional[str] = None):
        # ... existing code ...

        # Voice AI (optional)
        if os.getenv('ENABLE_VOICE_AI', 'false').lower() == 'true':
            self.voice_ai = CallManager(
                vonage_client=VonageClient(),
                activity_tracker=self.tracker
            )
            print("✓ Voice AI initialized")

    def make_voice_call(self, to: str, message: str) -> Dict:
        """Make AI voice call"""
        if not hasattr(self, 'voice_ai'):
            return {'error': 'Voice AI not enabled'}

        return self.voice_ai.make_call(to, message)
```

---

## 📚 Dokumentation & Resources

### **Official Docs:**
- [Vonage Voice API](https://developer.vonage.com/en/voice/voice-api/overview)
- [ElevenLabs Vonage Integration](https://elevenlabs.io/docs/agents-platform/phone-numbers/telephony/vonage)
- [WebSocket Connector GitHub](https://github.com/nexmo-se/elevenlabs-agent-ws-connector)
- [Vonage WebSocket Guide](https://developer.vonage.com/en/voice/voice-api/concepts/websockets)

### **Example Projects:**
- [Televoice Proof of Concept](https://github.com/rhbuckley/televoice-proof)
- [Pipedream Integration](https://pipedream.com/apps/elevenlabs/integrations/vonage)

---

## 🎯 Empfehlung für dich

**Phase 1: Standalone Testing (1-2 Tage)**
1. ✅ Vonage + ElevenLabs Accounts erstellen
2. ✅ WebSocket Connector lokal mit ngrok testen
3. ✅ Ersten Test-Anruf machen
4. ✅ Voice Agent trainieren

**Phase 2: CRM Integration (3-5 Tage)**
1. ✅ `voice_ai` Modul in Mac Assistant erstellen
2. ✅ Vonage Client implementieren
3. ✅ Call Logging in Activity Tracker
4. ✅ Dashboard Integration

**Phase 3: Production (1 Woche)**
1. ✅ Connector auf Fly.io/Railway deployen
2. ✅ Produktive Phone Number kaufen
3. ✅ Advanced Features (Call Recording, etc.)
4. ✅ Linear Integration

---

## 💡 Next Steps

**Soll ich:**

1. **Standalone Prototype bauen?**
   - WebSocket Connector Setup
   - Vonage + ElevenLabs konfigurieren
   - Testing Guide

2. **CRM Integration bauen?**
   - `voice_ai` Module erstellen
   - Vonage Client Code
   - Call Manager mit Activity Logging
   - Dashboard Update

3. **Beide?** 😊

---

**Was möchtest du als Erstes testen?** 🚀

**Sources:**
- [ElevenLabs Vonage Integration](https://elevenlabs.io/agents/integrations/vonage)
- [ElevenLabs Vonage Documentation](https://elevenlabs.io/docs/agents-platform/phone-numbers/telephony/vonage)
- [WebSocket Connector GitHub](https://github.com/nexmo-se/elevenlabs-agent-ws-connector)
- [Vonage WebSocket Voice Guide](https://developer.vonage.com/en/voice/voice-api/concepts/websockets)
- [Televoice Proof of Concept](https://github.com/rhbuckley/televoice-proof)
