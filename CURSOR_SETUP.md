# Cursor AI Agent Setup - Schritt für Schritt

Diese Anleitung führt dich durch die komplette Einrichtung der AI-Agenten in Cursor.

## 📋 Was du bekommst

Nach diesem Setup hast du 3 spezialisierte AI-Agenten:

- **🎯 Supervisor Agent** - Überwacht Code-Qualität & Architektur
- **💻 Code Agent** - Generiert production-ready Code
- **🤝 Assistant Agent** - Erklärt & hilft bei Problemen

## 🚀 Schnellstart (5 Minuten)

### Schritt 1: Cursor installieren

Falls noch nicht installiert:
```bash
# Download von https://cursor.sh
# Oder per Homebrew:
brew install --cask cursor
```

### Schritt 2: Projekt öffnen

```bash
# Terminal:
cd /home/user/research-agent
cursor .

# Oder per GUI:
# Cursor öffnen > Open Folder > research-agent wählen
```

### Schritt 3: API Keys konfigurieren

**Option A: Cursor Pro nutzen (Empfohlen)**
```
1. Cursor > Settings > Cursor Settings
2. Wähle dein Subscription-Plan
3. Model Selection: "claude-3.5-sonnet"
4. Fertig! ✅
```

**Option B: Eigene API Keys**
```
1. Cursor > Settings > Models > API Keys
2. Klicke "Add API Key"
3. Wähle Provider: "Anthropic" (für Claude)
4. Füge deinen Key ein: sk-ant-...
5. Optional: Füge weitere Keys hinzu (OpenAI, etc.)
```

### Schritt 4: Cursor Settings aktivieren

Die Settings wurden bereits in `.cursor/settings.json` konfiguriert.

Cursor lädt diese automatisch beim Öffnen des Projekts!

**Verifiziere:**
```
Cursor > Settings > Workspace
→ Sollte "Using workspace settings" anzeigen
```

### Schritt 5: Agent-Regeln aktivieren

Die `.cursorrules` Datei ist bereits vorhanden!

**Verifiziere:**
```bash
# Prüfe ob Datei existiert
ls -la .cursorrules

# Sollte anzeigen:
# -rw------- .cursorrules
```

Cursor lädt die Regeln automatisch! ✅

## 🎯 Die 3 Agent-Modi verwenden

### 1. Chat Mode - Assistant Agent (Cmd+L)

**Wofür:**
- Fragen stellen
- Code erklären lassen
- Konzepte verstehen
- Probleme debuggen

**Beispiele:**
```
"Erkläre mir wie der AI Provider Manager funktioniert"
"Warum verwenden wir strikte TypeScript Typisierung?"
"Wo finde ich den Code für die Dateisuche?"
"Wie füge ich einen neuen AI Provider hinzu?"
```

**Agent-Verhalten:**
- Antwortet auf Deutsch
- Gibt Datei-Referenzen mit Zeilennummern
- Zeigt Beispiele
- Erklärt Schritt-für-Schritt

### 2. Composer Mode - Code Agent (Cmd+I)

**Wofür:**
- Größere Code-Änderungen
- Multi-file editing
- Feature-Implementierung
- Refactoring

**Beispiele:**
```
"Füge einen neuen AI Provider 'Gemini' hinzu"
"Implementiere eine Export-Funktion für Suchergebnisse"
"Refactore die Search Engine für bessere Performance"
"Füge Error-Logging mit Winston hinzu"
```

**Agent-Verhalten:**
- Generiert production-ready Code
- Ändert mehrere Dateien gleichzeitig
- Folgt allen Coding Standards
- Fügt JSDoc hinzu
- Implementiert Error-Handling

### 3. Inline Edit - Code Agent (Cmd+K)

**Wofür:**
- Schnelle Code-Fixes
- Einzelne Funktionen ändern
- Code-Generation
- Direktes Editing

**Beispiele:**
```
"Füge Error-Handling hinzu"
"Konvertiere zu async/await"
"Füge JSDoc Kommentar hinzu"
"Optimiere diese Funktion"
```

**Agent-Verhalten:**
- Schnelle, fokussierte Änderungen
- Im Editor direkt
- Folgt Coding Standards

## 📚 Agent-Prompts nutzen

Die Agenten haben spezialisierte Prompts in `.cursor/prompts/`:

### Supervisor Agent aktivieren

```
@supervisor-agent Reviewe diese Änderungen
```

Der Agent prüft:
- ✅ Type Safety
- ✅ Error Handling
- ✅ Code-Qualität
- ✅ Architektur
- ✅ Sicherheit

### Code Agent aktivieren

```
@code-agent Implementiere Feature X
```

Der Agent:
- Generiert vollständigen Code
- Fügt Error-Handling hinzu
- Schreibt JSDoc
- Folgt Templates

### Assistant Agent aktivieren

```
@assistant-agent Erkläre wie Feature X funktioniert
```

Der Agent:
- Erklärt auf Deutsch
- Gibt Beispiele
- Zeigt Datei-Pfade
- Hilft Schritt-für-Schritt

## 🎨 Templates verwenden

Templates für häufige Patterns:

### Neue React Component
```
Cmd+I
"Erstelle eine neue Component basierend auf dem Template:
@new-component
Name: FeatureName
Description: Was die Component macht"
```

### Neue Service-Klasse
```
Cmd+I
"Erstelle einen neuen Service basierend auf dem Template:
@new-service
Name: ServiceName
Description: Was der Service macht"
```

### Custom Hook
```
Cmd+I
"Erstelle einen neuen Hook basierend auf dem Template:
@new-hook
Name: HookName
Description: Was der Hook macht"
```

## ⚙️ Erweiterte Konfiguration

### Model auswählen

```
Cursor > Settings > Models

Empfohlen für dieses Projekt:
- Chat: claude-3.5-sonnet (beste Erklärungen)
- Composer: claude-3.5-sonnet (beste Code-Qualität)
- Inline: claude-3.5-haiku (schnell & günstig)
```

### Codebase Indexing

Aktiviere für bessere Kontext-Awareness:

```
Cursor > Settings > Features
✅ Enable Codebase Indexing
✅ Index entire workspace
```

Cursor analysiert dann das gesamte Projekt und kann bessere Vorschläge machen.

### Git Context

Bereits aktiviert via Settings:

```json
"cursor.general.gitContext": true
```

Cursor sieht jetzt:
- Git History
- Commit Messages
- Branch Info
- Diff

## 🔍 Wie die Agenten zusammenarbeiten

### Typischer Workflow:

```
1. Du: "Ich brauche ein neues Feature X"
   ↓
2. Assistant Agent (Cmd+L): Erklärt wie man es am besten umsetzt
   ↓
3. Code Agent (Cmd+I): Implementiert das Feature
   ↓
4. Supervisor Agent: Reviewed automatisch (via .cursorrules)
   ↓
5. Code Agent: Korrigiert falls nötig
   ↓
6. ✅ Production-ready Code!
```

### Beispiel-Session:

```bash
# 1. Frage stellen
Cmd+L: "Wie füge ich einen neuen AI Provider hinzu?"

# Assistant erklärt Schritt-für-Schritt...

# 2. Code generieren
Cmd+I: "Implementiere Gemini Provider wie erklärt"

# Code Agent generiert:
# - src/services/ai-providers/gemini-provider.ts
# - Updates src/shared/types.ts
# - Updates src/services/ai-providers/provider-manager.ts
# - Alles mit Error-Handling, JSDoc, Types

# 3. Review
# Supervisor Agent prüft automatisch via .cursorrules

# 4. Testen
Cmd+L: "Wie teste ich den neuen Provider?"

# Assistant zeigt wie...
```

## 🛠️ Troubleshooting

### "Agent antwortet nicht auf Deutsch"

```
Lösung: In .cursorrules steht:
## Kommunikationsstil
Antworten auf Deutsch, Code auf Englisch

Falls es nicht klappt, explizit sagen:
"Bitte antworte auf Deutsch"
```

### "Code folgt nicht den Standards"

```
Lösung: Explizit auf .cursorrules verweisen:
"Bitte folge den Regeln in .cursorrules"

Oder direkter:
@supervisor-agent Reviewe diesen Code
```

### "API Limit erreicht"

```
Lösung:
1. Wechsel zu Haiku für einfache Tasks:
   Settings > Models > Inline: claude-3.5-haiku

2. Oder nutze lokale Modelle:
   - Ollama installieren
   - In Cursor Settings: Custom Model endpoint
```

### "Cursor lädt .cursorrules nicht"

```
Verifiziere:
1. Datei ist im Projekt-Root
2. Keine Syntax-Fehler (öffne .cursorrules)
3. Cursor neu starten
4. Projekt neu öffnen
```

## 📊 Erfolgskontrolle

Nach dem Setup solltest du:

### ✅ Chat Mode (Cmd+L)
- [ ] Fragen werden auf Deutsch beantwortet
- [ ] Code-Kommentare sind auf Englisch
- [ ] Datei-Referenzen werden gegeben
- [ ] Erklärungen sind klar & strukturiert

### ✅ Composer Mode (Cmd+I)
- [ ] Generierter Code ist typsicher (keine `any`)
- [ ] JSDoc ist vorhanden
- [ ] Error-Handling ist implementiert
- [ ] Code folgt Naming-Conventions

### ✅ Inline Edit (Cmd+K)
- [ ] Schnelle Edits funktionieren
- [ ] Code-Standards werden eingehalten
- [ ] Änderungen sind präzise

### ✅ Supervisor Agent
- [ ] Reviews sind streng
- [ ] Feedback ist konstruktiv
- [ ] Standards werden durchgesetzt

## 🎓 Best Practices

### DO:

```bash
✅ Spezifisch sein:
"Implementiere einen Gemini Provider in src/services/ai-providers/"

✅ Kontext geben:
"Basierend auf dem bestehenden Claude Provider..."

✅ Standards erwähnen:
"Bitte folge den .cursorrules Vorgaben"

✅ Templates nutzen:
"Nutze das @new-service Template"
```

### DON'T:

```bash
❌ Zu vage:
"Mach das Feature besser"

❌ Ohne Kontext:
"Schreib Code für X"

❌ Standards ignorieren:
"Schnell ohne Typen"
```

## 📖 Weitere Ressourcen

### Projekt-Dokumentation
- `README.md` - Projekt-Übersicht
- `ZUSAMMENFASSUNG.md` - Feature-Details
- `CODING_STANDARDS.md` - Standards für neue Chats

### Cursor Dokumentation
- [Cursor Docs](https://cursor.sh/docs)
- [.cursorrules Guide](https://cursor.sh/docs/cursorrules)
- [AI Models](https://cursor.sh/docs/models)

### TypeScript
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Strict Mode](https://www.typescriptlang.org/tsconfig#strict)

## 🎯 Nächste Schritte

1. **Teste die Agents:**
   ```bash
   Cmd+L: "Erkläre die Projekt-Architektur"
   Cmd+I: "Füge einen Kommentar zur main.ts hinzu"
   ```

2. **Implementiere ein Feature:**
   ```bash
   "Füge Export-Funktion für Suchergebnisse hinzu"
   ```

3. **Reviewe bestehenden Code:**
   ```bash
   "@supervisor-agent Reviewe src/services/ai-providers/"
   ```

4. **Experimentiere mit Templates:**
   ```bash
   "Erstelle neue Component mit @new-component Template"
   ```

---

## ✅ Setup Complete!

Du bist bereit! Die AI-Agenten helfen dir jetzt bei der Entwicklung.

**Viel Erfolg! 🚀**

Bei Fragen:
```
Cmd+L: "Ich habe eine Frage zu..."
```

Der Assistant Agent hilft dir weiter!
