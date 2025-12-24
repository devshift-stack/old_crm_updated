# ☁️ Cloud Agents - Remote Access Guide

## Übersicht

Mit **Cloud Agents** kannst du deinen Mac von **überall** steuern:

- 💬 **Slack Bot** - Steuere deinen Mac via Slack
- 🤖 **Telegram Bot** - Steuere deinen Mac via Telegram
- 🌐 **Web Server** - Browser-Zugriff auf deinen Mac
- 📦 **Cloud Sync** - Automatisches Backup in die Cloud

---

## 🚀 Schnellstart

### 1. Dependencies installieren:

```bash
cd mac_assistant
pip install -r requirements.txt
```

Dies installiert:
- `flask` - Web Server
- `slack-bolt` - Slack Bot

Optional für Telegram:
```bash
pip install python-telegram-bot
```

### 2. Cloud Agents in .env aktivieren:

```ini
# Slack Bot (Empfohlen!)
ENABLE_SLACK_BOT=true
SLACK_BOT_TOKEN=xoxb-dein-token
SLACK_APP_TOKEN=xapp-dein-app-token

# Web Server
ENABLE_WEB_SERVER=true
WEB_SERVER_PORT=5000

# Optional: Cloud Sync
ENABLE_CLOUD_SYNC=true
CLOUD_SYNC_DIR=~/Dropbox/MacAssistant
```

### 3. App starten:

```bash
python3 main.py
```

### 4. Cloud Agents starten:

Im Dashboard: **☁️ Cloud Agents** → **Agents starten**

Oder im Code:
```python
core.start_cloud_agents()
```

**Fertig!** 🎉

---

## 💬 Slack Bot Setup

### Warum Slack?

✅ **Einfach** - Schnelle Installation
✅ **Sicher** - Verschlüsselte Verbindung
✅ **Überall** - Desktop, Mobile, Web
✅ **Mächtig** - Slash Commands + Natural Language

### Setup Steps:

#### 1. Slack App erstellen:

```
1. Gehe zu: https://api.slack.com/apps
2. "Create New App" → "From scratch"
3. App Name: "Mac Remote Assistant"
4. Workspace wählen
```

#### 2. Bot Token Scopes:

Gehe zu **OAuth & Permissions**, füge hinzu:

```
app_mentions:read
channels:history
chat:write
im:history
im:read
im:write
users:read
```

#### 3. Event Subscriptions:

Aktiviere **Event Subscriptions** und subscribe zu:

```
app_mention
message.im
```

#### 4. Socket Mode aktivieren:

```
1. Gehe zu "Socket Mode"
2. Aktiviere Socket Mode
3. Kopiere App-Level Token → SLACK_APP_TOKEN
```

#### 5. Bot Token holen:

```
1. Gehe zu "OAuth & Permissions"
2. "Install to Workspace"
3. Kopiere "Bot User OAuth Token" → SLACK_BOT_TOKEN
```

#### 6. Slash Commands hinzufügen (optional):

Erstelle unter **Slash Commands**:

```
/status - System-Status
/email - E-Mails prüfen
/messages - Nachrichten
/photos [suche] - Fotos suchen
/tasks [befehl] - Task ausführen
```

#### 7. In .env eintragen:

```ini
ENABLE_SLACK_BOT=true
SLACK_BOT_TOKEN=xoxb-123456789-abcdefghijk
SLACK_APP_TOKEN=xapp-1-A0123456-123-abc
```

### Slack Bot benutzen:

#### Slash Commands:

```
/status
→ Zeigt System-Status

/email
→ Ungelesene E-Mails

/photos recent
→ Fotos der letzten 7 Tage

/tasks Sende E-Mail an Max
→ Führt Task aus
```

#### Natural Language:

Erwähne den Bot oder schreibe DM:

```
@Mac Assistant was habe ich heute gemacht?
@Mac Assistant sende E-Mail an max@example.com
@Mac Assistant suche Fotos vom Strand
```

Direct Messages:
```
Was habe ich vor 3 Tagen um 14 Uhr gemacht?
Zeige mir meine letzten Slack-Nachrichten
```

---

## 🤖 Telegram Bot Setup (Optional)

### Setup Steps:

#### 1. Bot erstellen:

```
1. Öffne Telegram
2. Suche @BotFather
3. /newbot
4. Name: Mac Remote Assistant
5. Username: deinname_mac_bot
6. Kopiere Token
```

#### 2. In .env eintragen:

```ini
ENABLE_TELEGRAM_BOT=true
TELEGRAM_BOT_TOKEN=123456:ABCdefGHIjklMNOpqrsTUVwxyz
```

#### 3. Requirements installieren:

```bash
pip install python-telegram-bot
```

### Telegram Bot benutzen:

```
/start - Willkommen
/status - System-Status
/email - E-Mails
/messages - Nachrichten
/photos [suche] - Fotos
/tasks [befehl] - Task

Oder Natural Language:
Was habe ich heute gemacht?
Sende E-Mail an Max
```

---

## 🌐 Web Server

### Setup:

In .env:

```ini
ENABLE_WEB_SERVER=true
WEB_SERVER_HOST=0.0.0.0  # Alle Interfaces
WEB_SERVER_PORT=5000
```

### Zugriff:

**Lokal:**
```
http://localhost:5000
```

**Im Netzwerk:**
```
http://deine-mac-ip:5000
```

**IP finden:**
```bash
ifconfig | grep "inet "
```

### Features:

- 📊 **System-Status** - Plugins, KI, Autonomer Agent
- 🤖 **KI-Assistent** - Natural Language Queries
- ⚡ **Task ausführen** - Befehle senden

### API Endpoints:

```
GET  /api/status    - System-Status
POST /api/query     - Query verarbeiten
POST /api/execute   - Task ausführen
GET  /api/plugins   - Plugin-Liste
```

Beispiel:
```bash
# Query
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Was habe ich heute gemacht?"}'

# Task
curl -X POST http://localhost:5000/api/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Sende E-Mail an Max"}'
```

### Sicherheit:

⚠️ **WICHTIG:**

- Web Server ist **NICHT** passwortgeschützt!
- Nur in **vertrautem Netzwerk** nutzen!
- **NIEMALS** öffentlich ins Internet!

Für öffentlichen Zugriff → Nutze Slack/Telegram Bot!

---

## 📦 Cloud Sync

### Setup:

```ini
ENABLE_CLOUD_SYNC=true
CLOUD_SYNC_DIR=~/Dropbox/MacAssistant
CLOUD_SYNC_INTERVAL=3600  # 1 Stunde
```

Unterstützt:
- Dropbox
- Google Drive
- iCloud Drive
- Jeden gemounteten Cloud-Ordner

### Was wird synchronisiert?

1. **Datenbank** - Activity Tracking
2. **Config** - Einstellungen (ohne API Keys!)
3. **Logs** - Activity Logs (letzte 30 Tage)

### Manueller Sync:

```python
# Sofort synchronisieren
core.get_cloud_agent('sync').sync_now()

# Backups auflisten
backups = core.get_cloud_agent('sync').list_backups()

# Wiederherstellen
core.get_cloud_agent('sync').restore_from_cloud()
```

### Backup-Struktur:

```
~/Dropbox/MacAssistant/
  database/
    activities_latest.db
    activities_20250101_120000.db
    activities_20250102_140000.db
  config/
    config.json
  logs/
    activities_2025-01-01.json
    activities_2025-01-02.json
  manifest.json
```

---

## 🎮 Cloud Agents im Code

### Core Integration:

```python
from mac_assistant.core_v2 import MacAssistantCore

core = MacAssistantCore(api_key='sk-ant-...')

# Alle Cloud Agents starten
core.start_cloud_agents()

# Status prüfen
status = core.get_cloud_agent_status()
print(status)
# {'slack': {'running': True, 'available': True},
#  'web': {'running': True, 'available': True}}

# Einzelnen Agent holen
slack_bot = core.get_cloud_agent('slack')
web_server = core.get_cloud_agent('web')

# Alle stoppen
core.stop_cloud_agents()
```

### Einzelne Agents:

```python
from mac_assistant.cloud_agents import SlackBotAgent, WebServerAgent

# Slack Bot
slack = SlackBotAgent(core)
slack.start()

# Notification senden
slack.notify_user('U12345', 'Hello from Mac!')

# Web Server
web = WebServerAgent(core, host='0.0.0.0', port=5000)
web.start()

# Cloud Sync
sync = CloudSyncAgent(core, sync_dir='~/Dropbox/MacAssistant')
sync.start()
sync.sync_now()
```

---

## 🔧 Troubleshooting

### Slack Bot funktioniert nicht:

```bash
# 1. Prüfe Tokens:
echo $SLACK_BOT_TOKEN
echo $SLACK_APP_TOKEN

# 2. Prüfe Installation:
pip list | grep slack

# 3. Teste Import:
python3 -c "from slack_bolt import App; print('OK')"

# 4. Logs prüfen:
# Beim Start zeigt es Errors
```

### Web Server läuft nicht:

```bash
# 1. Port bereits belegt?
lsof -i :5000

# 2. Firewall?
# System Settings → Network → Firewall

# 3. Flask installiert?
pip list | grep flask
```

### Cloud Sync funktioniert nicht:

```bash
# 1. Ordner existiert?
ls -la ~/Dropbox/MacAssistant

# 2. Berechtigungen?
chmod 755 ~/Dropbox/MacAssistant

# 3. Cloud Ordner gemountet?
mount | grep Dropbox
```

---

## 🎯 Empfohlene Konfiguration

Für maximale Remote-Access-Power:

```ini
# .env

# Slack Bot (Haupt-Remote-Interface)
ENABLE_SLACK_BOT=true
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...

# Web Server (Lokales Netzwerk)
ENABLE_WEB_SERVER=true
WEB_SERVER_HOST=0.0.0.0
WEB_SERVER_PORT=5000

# Cloud Sync (Automatisches Backup)
ENABLE_CLOUD_SYNC=true
CLOUD_SYNC_DIR=~/Dropbox/MacAssistant
CLOUD_SYNC_INTERVAL=3600

# Telegram (Optional)
ENABLE_TELEGRAM_BOT=false
```

**Warum Slack?**

- ✅ Professionell und weit verbreitet
- ✅ Desktop + Mobile Apps
- ✅ Starke API und SDKs
- ✅ Socket Mode = keine öffentliche URL nötig
- ✅ Slash Commands + Natural Language

---

## 🌍 Von überall zugreifen

### Option 1: Slack/Telegram Bot (Empfohlen!)

```
✅ Von überall erreichbar
✅ Keine Router-Konfiguration
✅ Sicher und verschlüsselt
✅ Mobile + Desktop
```

### Option 2: VPN + Web Server

```
1. VPN zu deinem Heimnetzwerk
2. Zugriff auf http://mac-ip:5000
```

### Option 3: SSH Tunnel (Fortgeschritten)

```bash
# Von außen:
ssh -L 5000:localhost:5000 user@deine-mac-ip

# Dann: http://localhost:5000
```

---

## 📱 Use Cases

### Unterwegs:

```
[Du] @Mac Assistant was habe ich heute gemacht?
[Bot] Heute um 9 Uhr: E-Mail von Max gelesen
      Heute um 10 Uhr: Slack mit Team...

[Du] @Mac Assistant sende E-Mail an max@example.com
[Bot] ✅ E-Mail gesendet!
```

### Im Büro:

```
Browser → http://localhost:5000
→ Dashboard öffnen
→ System-Status sehen
→ Tasks ausführen
```

### Automatisches Backup:

```
Cloud Sync läuft im Hintergrund
→ Alle 1 Stunde
→ Datenbank zu Dropbox
→ Immer aktuell
```

---

## 🎁 Vorteile

✅ **Immer erreichbar** - Von überall auf der Welt
✅ **Mehrere Wege** - Slack, Web, Telegram
✅ **Sicher** - Verschlüsselte Verbindungen
✅ **Backup** - Automatisch in Cloud
✅ **Flexibel** - Einzeln ein/ausschaltbar
✅ **Einfach** - Setup in 5 Minuten

---

## 💡 Best Practices

### Sicherheit:

1. **Sichere Tokens** - In .env, NICHT in Git
2. **Netzwerk** - Web Server nur im vertrautem Netz
3. **Firewall** - Port 5000 nur intern
4. **Backup** - Cloud Sync ohne API Keys

### Performance:

1. **Slack/Telegram** - Für Remote (Internet)
2. **Web Server** - Für Lokal (Netzwerk)
3. **Sync Interval** - 1 Stunde reicht meist

### Workflow:

```
Unterwegs → Slack Bot
Zuhause → Web Dashboard
Automatisch → Cloud Sync
```

---

**Viel Spaß mit Remote Access!** 🚀

Fragen? Issues? → GitHub: https://github.com/your-repo/issues
