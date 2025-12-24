# Research Agent

Eine intelligente macOS Desktop-Applikation zum Durchsuchen deiner Festplatte mit natürlicher Sprache.

## Features

### 🤖 Multi-AI-Provider Support
- **Cloud-Provider** (Premium):
  - Claude (Anthropic) - Beste Reasoning-Fähigkeiten
  - ChatGPT (OpenAI) - Gute Allround-Performance
  - Grok (xAI) - Real-time Wissen

- **Lokale Provider** (Kostenlos/Offline):
  - Ollama - Komplett privat, läuft lokal
  - Automatischer Fallback wenn kein Internet

### 🔍 Intelligente Dateisuche
- Natürliche Sprachabfragen (z.B. "Finde alle WhatsApp Backups")
- KI-basierte Query-Interpretation
- Pattern-Matching und Fuzzy-Search
- Relevanz-Scoring für bessere Ergebnisse
- Optional: Indexierung für schnellere Suche

### 🎯 Moderne Architektur
- TypeScript mit strikter Typisierung
- Electron für Desktop-Integration
- React für moderne UI
- Zustand für State Management
- Modulare, testbare Struktur

## Installation

### Voraussetzungen

- Node.js 18+
- npm oder yarn
- macOS (Windows/Linux mit Anpassungen möglich)

### Optional: Ollama für lokale KI

```bash
# Ollama installieren (für Offline-Nutzung)
brew install ollama

# Modell herunterladen
ollama pull llama3.2
```

### Projekt Setup

```bash
# Repository klonen
cd research-agent

# Dependencies installieren
npm install

# Environment konfigurieren
cp .env.example .env

# API Keys eintragen (optional für Cloud-AI)
# ANTHROPIC_API_KEY=sk-...
# OPENAI_API_KEY=sk-...
# XAI_API_KEY=...
```

## Nutzung

### Development Mode

```bash
# Starte Development Server
npm run dev
```

Die App öffnet automatisch mit Hot-Reload.

### Production Build

```bash
# macOS App erstellen
npm run build:mac
```

Die fertige `.app` findest du im `dist` Ordner.

## Architektur

```
research-agent/
├── src/
│   ├── main/              # Electron Main Process
│   │   ├── main.ts        # Entry Point
│   │   ├── ipc-handlers.ts # IPC Communication
│   │   └── config-manager.ts
│   │
│   ├── renderer/          # React UI
│   │   ├── components/    # React Components
│   │   ├── hooks/         # Custom Hooks
│   │   └── store/         # Zustand Store
│   │
│   ├── services/          # Business Logic
│   │   ├── ai-providers/  # AI Provider Implementierungen
│   │   ├── file-search/   # File Search Engine
│   │   └── indexing/      # File Indexer
│   │
│   └── shared/            # Shared Types
│       ├── types.ts       # TypeScript Interfaces
│       └── constants.ts   # App Constants
```

## Verwendete Technologien

- **Electron**: Desktop App Framework
- **React**: UI Framework
- **TypeScript**: Typsichere Entwicklung
- **Zustand**: State Management
- **Fast-glob**: Schnelle Dateisuche
- **Fuse.js**: Fuzzy Search
- **Anthropic SDK**: Claude Integration
- **OpenAI SDK**: ChatGPT Integration
- **Vite**: Build Tool

## Coding Standards

### TypeScript
- Strikte Typisierung (`strict: true`)
- Keine `any` Types
- Alle Funktionen mit JSDoc dokumentiert

### Namenskonventionen
- `camelCase` für Variablen und Funktionen
- `PascalCase` für Komponenten und Klassen
- `SCREAMING_SNAKE_CASE` für Konstanten

### Code-Kommentare
- Alle Kommentare auf Englisch
- JSDoc für alle exportierten Funktionen

## Beispiel-Abfragen

```
"Finde alle WhatsApp Backups"
"Suche PDF-Dokumente vom letzten Monat"
"Zeige mir alle Bilder vom Urlaub 2024"
"Wo sind meine Python-Projekte?"
"Finde große Videodateien (> 1GB)"
```

## Konfiguration

### AI Provider wechseln

In der UI kannst du zwischen verfügbaren Providern wechseln. Die App zeigt nur verfügbare Provider an.

### Indexierung aktivieren

```typescript
// In .env
ENABLE_INDEXING=true
```

Indexierung beschleunigt Suchen, benötigt aber initialen Scan.

### Search Path ändern

Standardmäßig wird das Home-Verzeichnis durchsucht. Du kannst im UI einen anderen Pfad wählen.

## Sicherheit

- Input-Validierung auf Frontend und Backend
- Keine Secrets im Code
- Context Isolation in Electron
- Safe IPC-Kommunikation über Preload-Script

## Performance

- Lazy-Loading von Komponenten
- Virtuelle Listen für große Ergebnismengen
- Optimierte Glob-Patterns
- Optional: Indexierung für schnellere Suche

## Troubleshooting

### Ollama verbindet nicht
```bash
# Prüfe ob Ollama läuft
ollama list

# Starte Ollama Service
ollama serve
```

### AI Provider nicht verfügbar
- API Keys in `.env` prüfen
- Internet-Verbindung prüfen
- Fallback auf Ollama nutzen

### Keine Suchergebnisse
- Suchpfad prüfen
- Berechtigungen prüfen (macOS Sicherheitseinstellungen)
- Pattern in Query anpassen

## Lizenz

MIT

## Autor

Entwickelt nach strikten TypeScript Coding Standards
