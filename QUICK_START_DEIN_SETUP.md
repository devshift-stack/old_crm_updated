# 🚀 Quick Start - Dein optimales Setup

**Status:** Alle Cloud Agents sind up-to-date und committed! ✅

**Dein Setup:** Linear User → Web Dashboard + Cloud Sync (kein Slack Bot)

---

## ⚡ Los geht's in 5 Minuten:

### 1️⃣ **Installation** (Einmalig)

```bash
cd mac_assistant

# Virtual Environment erstellen
python3 -m venv venv
source venv/bin/activate

# Dependencies installieren
pip install -r requirements.txt
```

**Installiert wird:**
- `anthropic` - Claude AI
- `openai` - ChatGPT/Grok
- `flask` - Web Server ✅
- `slack-bolt` - (nicht gebraucht, aber installiert)

---

### 2️⃣ **Konfiguration**

**Optimierte .env nutzen:**

```bash
# Kopiere optimierte Config
cp .env.optimized .env

# Oder manuell:
cp .env.example .env
nano .env
```

**Minimal-Konfiguration (MUSS gesetzt werden):**

```ini
# Dein Claude API Key
ANTHROPIC_API_KEY=sk-ant-DEIN-KEY-HIER

# Web Server (Dein Haupt-Interface)
ENABLE_WEB_SERVER=true
WEB_SERVER_PORT=5000

# Cloud Sync (Auto-Backup)
ENABLE_CLOUD_SYNC=true
CLOUD_SYNC_DIR=~/Dropbox/MacAssistant

# Slack Bot DISABLED (du nutzt Linear!)
ENABLE_SLACK_BOT=false
```

**API Key holen:**
1. Gehe zu: https://console.anthropic.com/
2. Account erstellen / Login
3. Settings → API Keys → Create Key
4. Key kopieren → in .env eintragen

---

### 3️⃣ **Starten**

```bash
# Virtual Environment aktivieren (falls noch nicht)
source venv/bin/activate

# App starten
python3 main.py
```

**Was passiert:**
```
✓ Core initialized with 5 available plugins
✓ Web server agent initialized
✓ Cloud sync agent initialized
✓ Web agent started
✓ Sync agent started

Dashboard: http://localhost:5000
```

---

### 4️⃣ **Nutzen**

#### **Web Dashboard** (Dein Haupt-Tool!)

```
http://localhost:5000
```

**Features:**
- 📊 Live System-Status
- 🤖 Natural Language Queries
- ⚡ Task Executor
- 📱 Plugin Overview
- 📈 Analytics

**Im Netzwerk erreichbar:**
```
# Mac IP finden:
ifconfig | grep "inet " | grep -v 127.0.0.1

# Dann von anderem Gerät:
http://DEINE-MAC-IP:5000
```

#### **API Endpoints** (Für eigene Tools!)

```bash
# System Status
curl http://localhost:5000/api/status

# Natural Language Query
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Was habe ich heute gemacht?"}'

# Task ausführen
curl -X POST http://localhost:5000/api/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "Sende E-Mail an Max"}'

# Plugin Liste
curl http://localhost:5000/api/plugins
```

#### **Cloud Sync** (Läuft automatisch!)

**Backup Location:**
```
~/Dropbox/MacAssistant/
  database/
    activities_latest.db
    activities_20250124_160000.db
  config/
    config.json
  logs/
    activities_2025-01-24.json
  manifest.json
```

**Manueller Sync:**
```python
# In Python:
from mac_assistant.core_v2 import MacAssistantCore

core = MacAssistantCore()
core.get_cloud_agent('sync').sync_now()

# Backups auflisten
backups = core.get_cloud_agent('sync').list_backups()
print(backups)

# Wiederherstellen
core.get_cloud_agent('sync').restore_from_cloud()
```

---

## 🎯 Dein optimales Workflow:

### **Szenario 1: Täglich nutzen**

```
1. Mac starten
2. Terminal: python3 main.py
3. Browser: http://localhost:5000
4. Dashboard nutzen den ganzen Tag
5. Cloud Sync läuft automatisch alle 60 Min
```

### **Szenario 2: Von anderem Gerät**

```
1. Mac läuft mit main.py
2. iPhone/iPad im gleichen WLAN
3. Browser öffnen: http://MAC-IP:5000
4. Dashboard nutzen (Mobile-optimiert)
```

### **Szenario 3: API Integration**

```
1. Mac läuft mit main.py
2. Eigene App/Script
3. API Calls zu http://localhost:5000/api/*
4. Automation!
```

---

## 📱 **Was du NICHT brauchst:**

❌ **Slack Bot** - Du nutzt Linear, kein Slack
❌ **Telegram Bot** - Optional, erstmal nicht nötig
❌ **Socket Mode** - Nur für Slack/Telegram
❌ **Public URL** - Web Server läuft lokal

---

## 🔧 **Troubleshooting:**

### **Web Server startet nicht:**

```bash
# Port 5000 bereits belegt?
lsof -i :5000

# Falls ja, anderen Port nutzen:
# In .env: WEB_SERVER_PORT=5001

# Flask installiert?
pip list | grep flask
# Falls nicht: pip install flask
```

### **Cloud Sync funktioniert nicht:**

```bash
# Dropbox Ordner existiert?
ls -la ~/Dropbox/MacAssistant

# Falls nicht:
mkdir -p ~/Dropbox/MacAssistant

# Oder anderen Ordner nutzen:
# .env: CLOUD_SYNC_DIR=~/Google\ Drive/MacAssistant
```

### **Claude API Fehler:**

```bash
# API Key testen:
python3 -c "
from mac_assistant.utils.config import load_config
config = load_config()
print('API Key:', config.anthropic_api_key[:20] + '...')
"

# Key sollte mit 'sk-ant-' anfangen
```

---

## 💡 **Nächste Schritte:**

### **Sofort:**
1. ✅ .env konfigurieren (ANTHROPIC_API_KEY setzen!)
2. ✅ App starten: `python3 main.py`
3. ✅ Dashboard öffnen: http://localhost:5000
4. ✅ Testen: "Was habe ich heute gemacht?"

### **Danach:**
1. 🔧 Cloud Sync testen (prüfe ~/Dropbox/MacAssistant/)
2. 📱 Von anderem Gerät zugreifen (WLAN)
3. 🎨 Dashboard customizen (siehe DASHBOARD_FEATURES.md)
4. 🔌 Linear Integration bauen (später!)

---

## 📊 **Deine aktuelle Architektur:**

```
┌─────────────────────────────────────┐
│     Mac Remote Assistant v5.0       │
└─────────────────────────────────────┘
              │
    ┌─────────┴─────────┐
    │                   │
┌───▼────┐       ┌──────▼─────┐
│  Web   │       │   Cloud    │
│ Server │       │   Sync     │
│ :5000  │       │  Dropbox   │
└────────┘       └────────────┘
    │                   │
    │            ┌──────┴──────┐
    │            │  Backup:    │
    │            │  - Database │
    │            │  - Config   │
    │            │  - Logs     │
    │            └─────────────┘
    │
┌───▼──────────────────────────────┐
│  Dashboard Features:             │
│  - System Status                 │
│  - Natural Language Queries      │
│  - Task Executor                 │
│  - Plugin Management             │
│  - Analytics                     │
│  - Activity Feed                 │
└──────────────────────────────────┘
```

---

## 🎁 **Was du hast:**

### **Aktive Features:**
✅ Web Dashboard (localhost:5000)
✅ Cloud Sync (Dropbox)
✅ Multi-AI (Claude, ChatGPT, Grok)
✅ Plugin System (Mail, Photos, Slack, Viber, Telegram)
✅ Autonomous Agent
✅ Analytics Engine
✅ Activity Tracking
✅ Natural Language Processing

### **Nicht aktiv (aber verfügbar):**
⭕ Slack Bot (ENABLE_SLACK_BOT=false)
⭕ Telegram Bot (ENABLE_TELEGRAM_BOT=false)
⭕ Voice Control (ENABLE_VOICE_CONTROL=false)

---

## 📚 **Dokumentation:**

- **Diese Datei** - Quick Start
- `START_HIER.txt` - Allgemeine Anleitung
- `CLOUD_AGENTS.md` - Cloud Agent Details
- `README_DE.md` - Vollständige Doku
- `DASHBOARD_FEATURES.md` - Dashboard Guide
- `.env.optimized` - Deine optimierte Config

---

## ✅ **Checklist:**

**Vor dem ersten Start:**
- [ ] Dependencies installiert (`pip install -r requirements.txt`)
- [ ] .env erstellt (von .env.optimized kopieren)
- [ ] ANTHROPIC_API_KEY gesetzt
- [ ] ENABLE_WEB_SERVER=true
- [ ] ENABLE_CLOUD_SYNC=true
- [ ] Cloud Sync Ordner existiert (~/Dropbox/MacAssistant)

**Nach dem Start:**
- [ ] App läuft ohne Errors
- [ ] Web Server erreichbar (http://localhost:5000)
- [ ] Dashboard zeigt System Status
- [ ] Cloud Sync erstellt Backups

**Testen:**
- [ ] Query: "Was habe ich heute gemacht?"
- [ ] Task: "Zeige meine E-Mails"
- [ ] Cloud Sync: Check ~/Dropbox/MacAssistant/
- [ ] Im Netzwerk: http://MAC-IP:5000

---

## 🚀 **Los geht's!**

```bash
cd mac_assistant
source venv/bin/activate
python3 main.py
```

**Dann Browser:** http://localhost:5000

**Viel Erfolg!** 🎉

---

**Fragen?**
- Dokumentation lesen (`CLOUD_AGENTS.md`)
- Troubleshooting oben checken
- Oder einfach fragen! 😊
