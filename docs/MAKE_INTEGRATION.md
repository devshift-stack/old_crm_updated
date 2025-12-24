# Make.com Integration für Voice AI Agent

## Schritt 1: HTTP-Modul in Make.com

1. Erstelle neues Szenario in Make.com
2. Füge **HTTP > Make a request** Modul hinzu
3. Konfiguriere:

```
URL: https://api.vapi.ai/call/phone
Method: POST
Headers:
  - Authorization: Bearer 74f51fc7-0b8a-47b0-bbe0-31aaab39bbf1
  - Content-Type: application/json

Body (JSON):
{
  "phoneNumberId": "7f4cbf9a-3eb5-4f35-b5ae-ab8cdeb754c1",
  "assistantId": "dc7f394b-5118-4f84-bed9-13f8803b87ba",
  "customer": {
    "number": "{{phone}}",
    "name": "{{name}}"
  }
}
```

## Schritt 2: Trigger-Optionen

### Option A: Webhook (von externem System)
1. Füge **Webhooks > Custom webhook** als Trigger hinzu
2. Kopiere die Webhook-URL
3. Sende POST-Requests an diese URL:
```json
{
  "phone": "+49123456789",
  "name": "Max Mustermann"
}
```

### Option B: Google Sheets Trigger
1. **Google Sheets > Watch Rows** als Trigger
2. Bei neuer Zeile → Anruf starten
3. Mapping: `phone` = Spalte A, `name` = Spalte B

### Option C: CRM Trigger (HubSpot, Pipedrive, etc.)
1. **HubSpot > Watch Deals** oder **Watch Contacts**
2. Bei neuem Lead → Anruf starten

### Option D: Zeitplan
1. **Schedule** Trigger (z.B. täglich 9:00)
2. Hole Leads aus CRM/Datenbank
3. Für jeden Lead → Anruf starten

## Schritt 3: Webhook für Ergebnisse (Optional)

Wenn der Anruf beendet ist, kann Vapi ein Webhook senden:

1. In Vapi Dashboard → Assistant → Server URL eintragen
2. Oder in Make.com: Neues Szenario mit Webhook-Trigger
3. Webhook-URL in Vapi eintragen

### Webhook-Daten die du erhältst:
```json
{
  "message": {
    "type": "end-of-call-report",
    "call": {
      "id": "call-id",
      "status": "ended"
    },
    "transcript": "Gesamtes Transkript...",
    "summary": "Zusammenfassung...",
    "structuredData": {
      "interesse_vorhanden": true,
      "stimmung": "interessiert",
      "besichtigungstermin": "15.01.2025 14:00"
    }
  }
}
```

## Beispiel: Komplettes Make.com Szenario

```
[Google Sheets: Neue Zeile]
    → [HTTP: Vapi Anruf starten]
    → [Google Sheets: Status aktualisieren]

[Webhook: Vapi Ergebnis]
    → [Filter: Interesse vorhanden?]
    → [Google Sheets: Ergebnis eintragen]
    → [Email: Benachrichtigung senden]
```

## API-Referenz

### Anruf starten
```
POST https://api.vapi.ai/call/phone
```

### Anruf-Status abfragen
```
GET https://api.vapi.ai/call/{call_id}
```

### Alle Anrufe abrufen
```
GET https://api.vapi.ai/call
```
