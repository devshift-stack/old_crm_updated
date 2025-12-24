# 🔐 Environment Setup (.env)

## Übersicht

Alle API Keys und Einstellungen werden in einer `.env` Datei gespeichert - **sicher und einfach**!

---

## 🚀 Schnellstart

### 1. .env Datei erstellen:

```bash
cd mac_assistant
cp .env.example .env
```

### 2. .env bearbeiten:

```bash
# Mit beliebigem Editor:
nano .env
# oder
open -a TextEdit .env
# oder
code .env
```

### 3. API Keys eintragen:

```ini
# Mindestens einen API Key:
ANTHROPIC_API_KEY=sk-ant-dein-key-hier

# Optional:
OPENAI_API_KEY=sk-dein-openai-key
XAI_API_KEY=dein-grok-key
```

### 4. Speichern & App starten:

```bash
python3 main.py
```

**Fertig!** 🎉

---

## 📝 .env Datei - Vollständig

```ini
# ===== AI PROVIDERS =====

# Claude (Anthropic) - Standard
ANTHROPIC_API_KEY=sk-ant-api03-...

# ChatGPT (OpenAI) - Optional
OPENAI_API_KEY=sk-proj-...

# Grok (xAI) - Optional
XAI_API_KEY=xai-...

# ===== APP KONFIGURATION =====

# Autonomer Agent aktivieren?
ENABLE_AUTONOMOUS_AGENT=true

# Autonomie-Level (minimal, normal, maximum)
AUTONOMOUS_AGENT_LEVEL=normal

# Sprachsteuerung aktivieren?
ENABLE_VOICE_CONTROL=false

# Sprache für Voice
VOICE_LANGUAGE=de-DE
VOICE_NAME=Anna

# Background Monitor aktivieren?
ENABLE_BACKGROUND_MONITOR=true

# Intervalle in Sekunden
EMAIL_CHECK_INTERVAL=300     # 5 Minuten
MESSAGE_CHECK_INTERVAL=180   # 3 Minuten

# ===== PLUGINS =====

# Welche Plugins aktivieren?
PLUGIN_MAIL_ENABLED=true
PLUGIN_SLACK_ENABLED=true
PLUGIN_VIBER_ENABLED=true
PLUGIN_TELEGRAM_ENABLED=true
PLUGIN_PHOTOS_ENABLED=true

# ===== ADVANCED =====

# Datenbank-Pfad
DATABASE_PATH=~/.mac_assistant/activities.db

# Log-Level
LOG_LEVEL=INFO

# Aktiver AI-Provider (claude, chatgpt, grok)
ACTIVE_AI_PROVIDER=claude
```

---

## 🔑 API Keys bekommen

### Claude (Anthropic):
```
1. Gehe zu: https://console.anthropic.com
2. Registrieren / Einloggen
3. API Keys → Create Key
4. Key kopieren → in .env einfügen
```

### ChatGPT (OpenAI):
```
1. Gehe zu: https://platform.openai.com
2. Registrieren / Einloggen
3. API Keys → Create new secret key
4. Key kopieren → in .env einfügen
```

### Grok (xAI):
```
1. Gehe zu: https://console.x.ai
2. Registrieren / Einloggen
3. API Keys → Create
4. Key kopieren → in .env einfügen
```

---

## ⚠️ Sicherheit

### ✅ **DO:**
- `.env` Datei im `.gitignore` (ist bereits drin!)
- Niemals `.env` ins Git committen
- API Keys regelmäßig rotieren
- `.env` nur lokal speichern

### ❌ **DON'T:**
- `.env` öffentlich teilen
- API Keys in Code schreiben
- `.env` per E-Mail senden
- Screenshots mit Keys teilen

---

## 🎯 Konfiguration testen

### Im Code:

```python
from mac_assistant.utils.config import get_config

config = get_config()

# API Keys
print(config.anthropic_api_key)  # sk-ant-...
print(config.openai_api_key)     # sk-...

# Einstellungen
print(config.autonomous_enabled)  # True/False
print(config.voice_enabled)       # True/False

# Verfügbare Provider
print(config.get_available_providers())
# → ['claude', 'chatgpt', 'grok']
```

### Im Terminal:

```bash
# App starten - zeigt welche Keys gefunden wurden:
python3 main.py

# Ausgabe:
✓ API Keys gefunden für: claude, chatgpt, grok
```

---

## 🔄 .env aktualisieren

### Neue Keys hinzufügen:

```bash
# .env öffnen
nano .env

# Neue Zeile hinzufügen:
OPENAI_API_KEY=sk-neu-...

# Speichern & App neu starten
python3 main.py
```

### Keys ändern:

```bash
# Alte Zeile ersetzen:
ANTHROPIC_API_KEY=sk-alt-...
# Mit:
ANTHROPIC_API_KEY=sk-neu-...

# App neu starten
```

---

## 🚨 Troubleshooting

### "Keine API Keys gefunden"

```bash
# 1. Prüfe ob .env existiert:
ls -la .env

# 2. Prüfe Inhalt:
cat .env

# 3. Prüfe Syntax (kein Leerzeichen um =):
# RICHTIG:
ANTHROPIC_API_KEY=sk-ant-...

# FALSCH:
ANTHROPIC_API_KEY = sk-ant-...
```

### ".env wird nicht geladen"

```bash
# 1. Prüfe Dateiname (genau ".env"):
ls -la | grep env

# 2. Prüfe Pfad (muss im mac_assistant/ Ordner sein):
pwd
# Sollte sein: .../mac_assistant

# 3. Prüfe Berechtigung:
chmod 600 .env
```

### "API Key funktioniert nicht"

```bash
# 1. Prüfe Key-Format:
# Claude: sk-ant-api03-...
# OpenAI: sk-proj-...
# Grok: xai-...

# 2. Teste Key direkt:
export ANTHROPIC_API_KEY='sk-ant-...'
python3 main.py

# 3. Prüfe auf unsichtbare Zeichen:
cat -A .env
```

---

## 💡 Best Practices

### Mehrere Umgebungen:

```bash
# Development
.env.development

# Production
.env.production

# Laden:
python3 main.py --env .env.development
```

### Backup:

```bash
# Backup erstellen (ohne Keys!)
cp .env.example .env.backup

# In Backup nur Struktur, keine Secrets!
```

### Team-Setup:

```markdown
# README für Team:

1. Kopiere .env.example zu .env
2. Hole API Keys von Team-Admin
3. Trage Keys in .env ein
4. NICHT committen!
```

---

## 📦 In Native App

Bei Native .app:

```bash
# .env muss im Resources-Ordner sein:
Mac Remote Assistant.app/
  Contents/
    Resources/
      mac_assistant/
        .env          # ← Hier!
        .env.example
```

---

## 🎁 Vorteile

✅ **Sicher** - Keine Keys im Code
✅ **Einfach** - Eine Datei für alles
✅ **Versionierbar** - .env.example im Git
✅ **Flexibel** - Verschiedene Umgebungen
✅ **Standard** - Industry Best Practice

---

**Viel Spaß mit sicherer Konfiguration!** 🔐
