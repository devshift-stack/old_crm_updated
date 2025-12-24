#!/usr/bin/env python3
"""
VAPI AI Configurator - Steuere Vapi mit natürlicher Sprache
Nutzt OpenAI/Claude um Befehle in API-Calls umzuwandeln
"""

import os
import json
import requests
from openai import OpenAI

# Konfiguration
VAPI_API_KEY = "74f51fc7-0b8a-47b0-bbe0-31aaab39bbf1"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-key")
PHONE_NUMBER_ID = "7f4cbf9a-3eb5-4f35-b5ae-ab8cdeb754c1"

VAPI_BASE = "https://api.vapi.ai"

# OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """Du bist ein Vapi-Konfigurations-Assistent.
Wenn der Nutzer einen Befehl gibt, antworte NUR mit einem JSON-Objekt.

Verfügbare Aktionen:
1. create_assistant - Neuen Agent erstellen
2. update_assistant - Agent aktualisieren
3. make_call - Anruf starten
4. get_calls - Anrufe abrufen
5. list_assistants - Alle Agents auflisten

Beispiel-Antworten:

Befehl: "Erstelle einen Sales Agent der Produkte verkauft"
{
  "action": "create_assistant",
  "params": {
    "name": "Sales Agent",
    "prompt": "Du bist ein freundlicher Verkäufer...",
    "first_message": "Hallo, hier ist Max von der Firma XY..."
  }
}

Befehl: "Rufe +49123456789 an"
{
  "action": "make_call",
  "params": {
    "phone_number": "+49123456789"
  }
}

Befehl: "Ändere den Prompt zu: Du bist ein Kundenberater"
{
  "action": "update_assistant",
  "params": {
    "prompt": "Du bist ein Kundenberater..."
  }
}

Antworte NUR mit validem JSON, kein anderer Text!
"""

class VapiConfigurator:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {VAPI_API_KEY}",
            "Content-Type": "application/json"
        }
        self.current_assistant_id = "dc7f394b-5118-4f84-bed9-13f8803b87ba"

    def interpret_command(self, user_input: str) -> dict:
        """Nutze AI um den Befehl zu interpretieren"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            temperature=0.3
        )

        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {"error": "Konnte Befehl nicht interpretieren"}

    def execute_action(self, action_data: dict) -> dict:
        """Führe die Aktion aus"""
        action = action_data.get("action")
        params = action_data.get("params", {})

        if action == "create_assistant":
            return self.create_assistant(params)
        elif action == "update_assistant":
            return self.update_assistant(params)
        elif action == "make_call":
            return self.make_call(params)
        elif action == "get_calls":
            return self.get_calls()
        elif action == "list_assistants":
            return self.list_assistants()
        else:
            return {"error": f"Unbekannte Aktion: {action}"}

    def create_assistant(self, params: dict) -> dict:
        """Erstelle neuen Vapi Assistant"""
        data = {
            "name": params.get("name", "Neuer Agent"),
            "model": {
                "provider": "openai",
                "model": "gpt-4o-mini",
                "temperature": 0.7,
                "messages": [{
                    "role": "system",
                    "content": params.get("prompt", "Du bist ein hilfreicher Assistent.")
                }]
            },
            "firstMessage": params.get("first_message", "Hallo, wie kann ich Ihnen helfen?"),
            "voice": {
                "provider": "11labs",
                "voiceId": "pNInz6obpgDQGcFmaJgB",
                "stability": 0.45,
                "similarityBoost": 0.75
            },
            "transcriber": {
                "provider": "deepgram",
                "model": "nova-2",
                "language": "de"
            }
        }

        response = requests.post(
            f"{VAPI_BASE}/assistant",
            headers=self.headers,
            json=data
        )

        if response.status_code == 201:
            result = response.json()
            self.current_assistant_id = result["id"]
            return {"success": True, "assistant_id": result["id"], "name": result["name"]}
        return {"error": response.text}

    def update_assistant(self, params: dict) -> dict:
        """Aktualisiere bestehenden Assistant"""
        data = {}

        if "prompt" in params:
            data["model"] = {
                "provider": "openai",
                "model": "gpt-4o-mini",
                "messages": [{"role": "system", "content": params["prompt"]}]
            }

        if "first_message" in params:
            data["firstMessage"] = params["first_message"]

        if "name" in params:
            data["name"] = params["name"]

        if "voice_id" in params:
            data["voice"] = {
                "provider": "11labs",
                "voiceId": params["voice_id"]
            }

        response = requests.patch(
            f"{VAPI_BASE}/assistant/{self.current_assistant_id}",
            headers=self.headers,
            json=data
        )

        if response.status_code == 200:
            return {"success": True, "message": "Assistant aktualisiert"}
        return {"error": response.text}

    def make_call(self, params: dict) -> dict:
        """Starte einen Anruf"""
        data = {
            "phoneNumberId": PHONE_NUMBER_ID,
            "assistantId": params.get("assistant_id", self.current_assistant_id),
            "customer": {
                "number": params["phone_number"],
                "name": params.get("customer_name", "")
            }
        }

        response = requests.post(
            f"{VAPI_BASE}/call/phone",
            headers=self.headers,
            json=data
        )

        if response.status_code in [200, 201]:
            result = response.json()
            return {"success": True, "call_id": result["id"], "status": result["status"]}
        return {"error": response.text}

    def get_calls(self, limit: int = 10) -> dict:
        """Hole letzte Anrufe"""
        response = requests.get(
            f"{VAPI_BASE}/call?limit={limit}",
            headers=self.headers
        )

        if response.status_code == 200:
            calls = response.json()
            return {
                "success": True,
                "calls": [{
                    "id": c["id"],
                    "status": c["status"],
                    "duration": c.get("endedAt", "läuft noch"),
                    "summary": c.get("summary", "")[:100]
                } for c in calls[:limit]]
            }
        return {"error": response.text}

    def list_assistants(self) -> dict:
        """Liste alle Assistants"""
        response = requests.get(
            f"{VAPI_BASE}/assistant",
            headers=self.headers
        )

        if response.status_code == 200:
            assistants = response.json()
            return {
                "success": True,
                "assistants": [{
                    "id": a["id"],
                    "name": a["name"]
                } for a in assistants]
            }
        return {"error": response.text}

    def run(self, command: str) -> str:
        """Hauptfunktion: Interpretiere und führe aus"""
        print(f"\n🎯 Befehl: {command}")

        # 1. Interpretiere den Befehl
        action_data = self.interpret_command(command)
        print(f"📋 Interpretiert als: {json.dumps(action_data, indent=2)}")

        if "error" in action_data:
            return f"❌ Fehler: {action_data['error']}"

        # 2. Führe aus
        result = self.execute_action(action_data)
        print(f"✅ Ergebnis: {json.dumps(result, indent=2)}")

        return result


def main():
    """Interaktive CLI"""
    configurator = VapiConfigurator()

    print("=" * 50)
    print("🤖 VAPI AI Configurator")
    print("=" * 50)
    print("Sage mir was du möchtest, z.B.:")
    print("  - 'Erstelle einen Sales Agent'")
    print("  - 'Rufe +49123456789 an'")
    print("  - 'Zeig mir alle Anrufe'")
    print("  - 'exit' zum Beenden")
    print("=" * 50)

    while True:
        try:
            user_input = input("\n👤 Du: ").strip()

            if user_input.lower() in ["exit", "quit", "q"]:
                print("👋 Tschüss!")
                break

            if not user_input:
                continue

            result = configurator.run(user_input)

        except KeyboardInterrupt:
            print("\n👋 Tschüss!")
            break
        except Exception as e:
            print(f"❌ Fehler: {e}")


if __name__ == "__main__":
    main()
