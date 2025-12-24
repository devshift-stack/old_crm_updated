# 🚀 Installation auf Mac

## ⚡ Schnellinstallation (Empfohlen!)

**Eine Zeile - fertig!**

```bash
cd mac_assistant && chmod +x install.sh && ./install.sh
```

Das war's! Der Script macht alles automatisch:
- ✅ Erstellt Virtual Environment
- ✅ Installiert Dependencies
- ✅ Erstellt .env Konfiguration
- ✅ Fragt nach API Key
- ✅ Erstellt Cloud Sync Ordner
- ✅ Startet die App

**Dashboard:** http://localhost:5000

---

## 📋 Schritt-für-Schritt (Manuell)

Falls du es lieber manuell machen möchtest:

### 1. Python prüfen

```bash
python3 --version
# Sollte Python 3.8+ sein
```

Falls nicht installiert: https://www.python.org/downloads/

### 2. Installation

```bash
cd mac_assistant

# Virtual Environment
python3 -m venv venv
source venv/bin/activate

# Dependencies
pip install -r requirements.txt

# Konfiguration
cp .env.optimized .env
nano .env
# → Setze ANTHROPIC_API_KEY=sk-ant-DEIN-KEY

# Cloud Sync Ordner
mkdir -p ~/Dropbox/MacAssistant
```

### 3. Starten

```bash
python3 main.py
```

**Browser öffnen:** http://localhost:5000

---

## 🔑 API Key holen

1. Gehe zu: https://console.anthropic.com/
2. Account erstellen / Login
3. Settings → API Keys → Create Key
4. Key kopieren (fängt mit `sk-ant-` an)
5. In `.env` eintragen:
   ```
   ANTHROPIC_API_KEY=sk-ant-dein-key-hier
   ```

---

## 📂 Installations-Optionen

### Option A: Via GitHub Clone

```bash
# 1. Clone Repository
git clone https://github.com/DEIN-USERNAME/old_crm_updated.git
cd old_crm_updated

# 2. Checkout Branch
git checkout claude/mac-remote-access-app-qiKTl

# 3. Auto-Install
cd mac_assistant
./install.sh
```

### Option B: Via ZIP Download

```bash
# 1. Download von GitHub
# → Code → Download ZIP

# 2. Entpacken
unzip old_crm_updated-*.zip
cd old_crm_updated-*/mac_assistant

# 3. Auto-Install
./install.sh
```

### Option C: Via v5.0 ZIP Package

```bash
# 1. Download mac_assistant_v5.0_CLOUD_REMOTE_ACCESS.zip

# 2. Entpacken
unzip mac_assistant_v5.0_CLOUD_REMOTE_ACCESS.zip
cd mac_assistant

# 3. Auto-Install
./install.sh
```

---

## ✅ Nach Installation

### App starten

```bash
cd mac_assistant
source venv/bin/activate
python3 main.py
```

### Dashboard öffnen

```
http://localhost:5000
```

### Im Netzwerk nutzen

```bash
# Mac IP finden
ifconfig | grep "inet " | grep -v 127.0.0.1

# Von anderem Gerät:
http://DEINE-MAC-IP:5000
```

---

## 🔧 Troubleshooting

### Python nicht gefunden

```bash
# macOS: Install Homebrew Python
brew install python3

# Oder: Download von python.org
# https://www.python.org/downloads/
```

### pip install schlägt fehl

```bash
# Upgrade pip
pip install --upgrade pip

# Nochmal versuchen
pip install -r requirements.txt
```

### Port 5000 belegt

```bash
# Anderen Port nutzen
# In .env: WEB_SERVER_PORT=5001
```

### .env nicht gefunden

```bash
# Von .env.optimized kopieren
cp .env.optimized .env
```

### Cloud Sync Ordner fehlt

```bash
# Manuell erstellen
mkdir -p ~/Dropbox/MacAssistant

# Oder anderen Pfad in .env:
# CLOUD_SYNC_DIR=~/Google\ Drive/MacAssistant
```

---

## 📦 Was wird installiert?

**Python Packages:**
- `anthropic` - Claude AI API
- `openai` - ChatGPT/Grok API
- `flask` - Web Server
- `slack-bolt` - Slack Bot (optional)

**Größe:** ~50 MB (alle Dependencies)

---

## 🎯 Empfohlene Konfiguration

Deine `.env` sollte mindestens haben:

```ini
# AI Provider
ANTHROPIC_API_KEY=sk-ant-DEIN-KEY

# Web Server (Haupt-Interface)
ENABLE_WEB_SERVER=true
WEB_SERVER_PORT=5000

# Cloud Sync
ENABLE_CLOUD_SYNC=true
CLOUD_SYNC_DIR=~/Dropbox/MacAssistant

# Slack/Telegram (für dich nicht nötig)
ENABLE_SLACK_BOT=false
ENABLE_TELEGRAM_BOT=false
```

---

## 🚀 Nächste Schritte

Nach erfolgreicher Installation:

1. ✅ **Teste Web Dashboard**
   - Öffne http://localhost:5000
   - Probiere: "Was habe ich heute gemacht?"

2. ✅ **Prüfe Cloud Sync**
   - Check `~/Dropbox/MacAssistant/`
   - Sollte Backups erstellen

3. ✅ **Erkunde Features**
   - Plugin System
   - Natural Language Queries
   - Task Execution
   - Analytics

4. ✅ **Lies Dokumentation**
   - `QUICK_START_DEIN_SETUP.md` - Dein Guide
   - `CLOUD_AGENTS.md` - Remote Access
   - `DASHBOARD_FEATURES.md` - Dashboard

---

## 💡 Tipps

**Täglich nutzen:**
```bash
# Terminal alias erstellen
echo 'alias macassist="cd ~/mac_assistant && source venv/bin/activate && python3 main.py"' >> ~/.zshrc

# Dann einfach:
macassist
```

**Automatisch beim Start:**
```bash
# macOS Launch Agent erstellen (optional)
# Siehe: BUILD_NATIVE_APP.md
```

**Im Netzwerk nutzen:**
- Stelle sicher WEB_SERVER_HOST=0.0.0.0
- Firewall erlaubt Port 5000
- Verbinde von iPhone/iPad via http://MAC-IP:5000

---

## 🎉 Fertig!

Die App läuft jetzt auf deinem Mac! 🚀

**Dashboard:** http://localhost:5000

**Viel Spaß!**
