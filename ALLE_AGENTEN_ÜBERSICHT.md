# 🤖 Alle Agenten - Schnellübersicht

## Research Agent Multi-Agent Development Team

**9 spezialisierte AI-Agenten für professionelle Software-Entwicklung**

---

## 📋 Alle Agenten auf einen Blick

| Agent | @Mention | Hauptaufgabe | Wann nutzen |
|-------|----------|--------------|-------------|
| 🎯 **Planner** | `@planner-agent` | Feature-Planung | Vor neuen Features |
| 👔 **Supervisor** | `@supervisor-agent` | Code Review & Leitung | Vor Commits, bei Reviews |
| 💻 **Coder** | `@code-agent` | Code-Implementation | Wenn Production Code gebraucht wird |
| 🧪 **Tester** | `@tester-agent` | Bug-Hunting & QA | Parallel zum Coden, vor Commits |
| 🎨 **Designer** | `@designer-agent` | UI/UX & Figma | Für Design-Aufgaben |
| 📝 **Docs Writer** | `@docs-writer-agent` | Dokumentation | README, Guides, API Docs |
| 🔧 **Problem Solver** | `@problem-solver-agent` | Problem-Analyse | Bei komplexen Problemen |
| 🛠️ **Repair** | `@repair-agent` | Code-Modernisierung | Legacy Code upgraden |
| 🔒 **Security** | `@security-agent` | Security-Scanning | Security Reviews, Monitoring |

---

## 🎯 Agent 1: PLANNER

**@mention:** `@planner-agent`

**Prompt-Datei:** `.cursor/prompts/planner-agent.md`

### Wann nutzen:
- ✅ Bevor du ein neues Feature startest
- ✅ Bei komplexen Architektur-Entscheidungen
- ✅ Wenn du einen strukturierten Plan brauchst

### Was er liefert:
```markdown
## Feature: [Name]

### Requirements
- Funktionale Requirements
- Non-funktionale Requirements (Performance, Security)

### Implementation Plan
1. Schritt 1 - Dateien - Aufwand
2. Schritt 2 - Dateien - Aufwand
...

### Risks & Mitigation
### Dependencies
### Testing Strategy
### Success Criteria
```

### Beispiel:
```
@planner-agent Plane Feature: Gemini AI Provider Integration
```

---

## 👔 Agent 2: SUPERVISOR (Team Lead)

**@mention:** `@supervisor-agent`

**Prompt-Datei:** `.cursor/prompts/supervisor-agent.md`

### Wann nutzen:
- ✅ Code Review vor dem Commit
- ✅ Architektur-Entscheidungen validieren
- ✅ Standards durchsetzen
- ✅ Bei Unsicherheiten zur Code-Qualität

### Was er prüft:
- ✅ **Type Safety** - Keine `any` Types, explizite Return Types
- ✅ **Error Handling** - Try-catch überall
- ✅ **Documentation** - JSDoc für alle exports
- ✅ **Architecture** - Richtige File-Lokation, Single Responsibility
- ✅ **Security** - Input validiert, keine Secrets im Code

### Review-Ergebnis:
```
✅ Code genehmigt - Gut gemacht!
❌ Code abgelehnt - Probleme: [Liste mit Fixes]
```

### Beispiel:
```
@supervisor-agent Reviewe meinen Gemini Provider Code
```

---

## 💻 Agent 3: CODER (Implementation)

**@mention:** `@code-agent`

**Prompt-Datei:** `.cursor/prompts/code-agent.md`

### Wann nutzen:
- ✅ Production-Ready Code generieren
- ✅ Neue Components/Services/Hooks erstellen
- ✅ Code-Templates anwenden
- ✅ Komplexe Business-Logic implementieren

### Code-Qualität:
```typescript
// ✅ Generiert immer so:
/**
 * Function description
 * @param input Parameter description
 * @returns Return value description
 */
export async function functionName(
  input: InputType
): Promise<ReturnType> {
  try {
    // Validation
    if (!input) throw new Error('Input required');

    // Implementation
    const result = await doSomething(input);
    return result;
  } catch (error) {
    throw new Error(`Failed: ${error.message}`);
  }
}
```

### Templates:
- `@new-component` - React Component Template
- `@new-service` - Service Class Template
- `@new-hook` - Custom Hook Template

### Beispiel:
```
@code-agent Implementiere Gemini Provider basierend auf Plan
```

---

## 🧪 Agent 4: TESTER (Quality Assurance)

**@mention:** `@tester-agent`

**Prompt-Datei:** `.cursor/prompts/tester-agent.md`

### Wann nutzen:
- ✅ **PARALLEL** zum Coder während Entwicklung
- ✅ Vor jedem Commit
- ✅ Nach größeren Refactorings
- ✅ Bevor User den Code sieht

### Ziel:
🎯 **ZERO BUGS** bevor User den Code sieht!

### Bug Report:
```markdown
## Bug Report

### 🔴 CRITICAL (Blocker)
- API Key exposed in code - src/config.ts:12 - Move to .env
- Null pointer exception - src/search.ts:45 - Add null check

### 🟠 HIGH (Must-fix)
- Error not handled - src/api.ts:78 - Add try-catch

### 🟡 MEDIUM (Should-fix)
- Missing TypeScript type - src/utils.ts:23 - Add explicit type

### 🟢 LOW (Nice-to-have)
- Code duplication - Extract to function

### Test Coverage Recommendations
- Unit Tests: Test provider fallback logic
- Integration Tests: Test full search flow
- E2E Tests: Test UI search interaction
```

### Moderne Tools:
- ✅ Vitest (statt Jest)
- ✅ Playwright (statt Cypress)
- ✅ Testing Library

### Beispiel:
```
@tester-agent Teste Gemini Provider parallel zur Entwicklung
```

---

## 🎨 Agent 5: DESIGNER (UI/UX)

**@mention:** `@designer-agent`

**Prompt-Datei:** `.cursor/prompts/designer-agent.md`

### Wann nutzen:
- ✅ UI/UX Design für neue Features
- ✅ Figma Designs erstellen
- ✅ Design System definieren
- ✅ User Experience verbessern

### Design System:
```css
/* Colors */
--primary-blue: #60a5fa;
--primary-purple: #a78bfa;
--primary-gradient: linear-gradient(90deg, #60a5fa 0%, #a78bfa 100%);

/* Typography */
--font-primary: 'Inter', -apple-system, sans-serif;
--font-mono: 'JetBrains Mono', monospace;

/* Spacing */
--spacing-xs: 4px;
--spacing-sm: 8px;
--spacing-md: 16px;
--spacing-lg: 24px;
--spacing-xl: 32px;
```

### Liefert:
- 🎨 Figma Designs mit Measurements
- 📐 Component Specs (Größen, Abstände, States)
- 🎭 User Flows & Prototypes
- ♿ Accessibility Guidelines
- 📱 Responsive Breakpoints

### Figma Guide:
Siehe: `FIGMA_DESIGN_GUIDE.md` für detaillierte Anleitung

### Beispiel:
```
@designer-agent Design für Gemini Provider Selector UI
```

---

## 📝 Agent 6: DOCS WRITER (Documentation)

**@mention:** `@docs-writer-agent`

**Prompt-Datei:** `.cursor/prompts/docs-writer-agent.md`

### Wann nutzen:
- ✅ README aktualisieren
- ✅ API Dokumentation schreiben
- ✅ User Guides erstellen
- ✅ Architecture Docs

### Erstellt:
1. **JSDoc** - Vollständige Code-Dokumentation
2. **README** - Installation, Usage, Features
3. **API Docs** - Endpoints, Parameter, Responses
4. **User Guides** - How-To Schritt-für-Schritt
5. **Architecture Docs** - System-Übersichten, Diagramme

### Dokumentations-Standards:
- ✅ Markdown (GitHub-Flavor)
- ✅ Code-Beispiele überall
- ✅ Screenshots bei UI-Anleitungen
- ✅ Schritt-für-Schritt Listen
- ✅ Immer auf Deutsch (außer Code)

### Beispiel:
```
@docs-writer-agent Dokumentiere Gemini Provider Setup
```

---

## 🔧 Agent 7: PROBLEM SOLVER (Solution Architect)

**@mention:** `@problem-solver-agent`

**Prompt-Datei:** `.cursor/prompts/problem-solver-agent.md`

### Wann nutzen:
- ✅ Komplexe Probleme lösen
- ✅ Performance-Optimierung
- ✅ Architektur-Probleme
- ✅ Moderne Alternativen finden

### Kennt 2025 Best Practices:
```
❌ Alte Lösung → ✅ Moderne Alternative

Manual REST API → Firebase/Supabase
Webpack → Vite
Redux → Zustand
Jest → Vitest
Cypress → Playwright
Express → Fastify
MySQL → PostgreSQL/Supabase
Callbacks → Promises/Async-Await
Class Components → Function Components + Hooks
```

### Liefert:
1. **Root Cause Analyse** - Was ist das eigentliche Problem?
2. **Lösungsoptionen** - Min. 2-3 Ansätze mit Trade-offs
3. **Empfehlung** - Beste Lösung mit Begründung
4. **Implementation Guide** - Wie umsetzen?
5. **Performance Impact** - Vorher/Nachher Vergleich

### Beispiel:
```
@problem-solver-agent Analysiere warum Search langsam ist
@problem-solver-agent Moderne Alternative zu Express API?
```

---

## 🛠️ Agent 8: REPAIR (Modernization)

**@mention:** `@repair-agent`

**Prompt-Datei:** `.cursor/prompts/repair-agent.md`

### Wann nutzen:
- ✅ Legacy Code modernisieren
- ✅ Dependencies updaten
- ✅ Alte Patterns upgraden
- ✅ Codebase aufräumen

### Repair Report:
```markdown
## Repair Report: [Repo Name]

### Analyse
- Node Version: 14.x → 20.x (LTS)
- Dependencies: 23 veraltet, 5 mit Security Issues
- Code Patterns: 12 deprecated patterns gefunden

### Kritische Issues
🔴 CRITICAL: lodash@3.10.1 (CVE-2021-23337)
🟠 HIGH: React 16.8 → 18.3 (Breaking Changes)

### Modernisierungs-Plan
1. **Phase 1: Security** (1-2 Tage)
   - Update critical dependencies
   - Fix security vulnerabilities

2. **Phase 2: Node & Build** (2-3 Tage)
   - Node 14 → 20
   - Webpack → Vite
   - Jest → Vitest

3. **Phase 3: Code Patterns** (3-5 Tage)
   - Class Components → Function Components
   - Redux → Zustand
   - Callbacks → Async/Await

### Risks & Mitigation
### Breaking Changes Handling
### Estimated Effort: 6-10 Tage
```

### Beispiel:
```
@repair-agent Analysiere alten CRM Code und plane Modernisierung
@repair-agent Migriere von Webpack zu Vite
```

---

## 🔒 Agent 9: SECURITY (Security Specialist)

**@mention:** `@security-agent`

**Prompt-Datei:** `.cursor/prompts/security-agent.md`

### Wann nutzen:
- ✅ Code Security-Review
- ✅ Vor Production Deployment
- ✅ Nach Dependencies Updates
- ✅ 24/7 Monitoring (Synology NAS)

### Prüft:
1. **Code-Scanning**
   - XSS (Cross-Site Scripting)
   - SQL Injection
   - Command Injection
   - Path Traversal

2. **Dependencies**
   - npm audit
   - Known vulnerabilities
   - Outdated packages

3. **Secrets Detection**
   - API Keys im Code
   - Hardcoded Passwords
   - Private Keys
   - Database Credentials

4. **Input Validation**
   - User input sanitized
   - File uploads validated
   - Query parameters checked

5. **Configuration**
   - HTTPS enforced
   - CORS korrekt
   - CSP Headers
   - Rate Limiting

### Security Report:
```markdown
## Security Scan Report

### 🔴 CRITICAL (Fix immediately!)
- API Key exposed - src/config.ts:12
  Fix: Move to .env file

- SQL Injection possible - src/db.ts:45
  Fix: Use parameterized queries

### 🟠 HIGH (Fix soon)
- Missing input validation - src/api.ts:78
  Fix: Add validation middleware

### 🟡 MEDIUM (Next update)
- lodash@4.17.15 has known vulnerability
  Fix: Update to 4.17.21

### 🟢 LOW (When convenient)
- Error messages too detailed
  Fix: Generic error messages for users

### 🔵 INFO (Best practices)
- Consider adding rate limiting
- Add CSP headers for XSS protection
```

### Alert Levels:
```
🔴 CRITICAL - Sofort fixen!
🟠 HIGH - Bald fixen
🟡 MEDIUM - Nächstes Update
🟢 LOW - Bei Gelegenheit
🔵 INFO - Best Practice Tip
```

### Synology NAS Deployment:
Siehe: `SYNOLOGY_INSTALLATION.md` für 24/7 Security Monitoring Setup

### Beispiel:
```
@security-agent Prüfe Code auf Sicherheitslücken
@security-agent Scan dependencies for vulnerabilities
```

---

## 🎭 Emir - Default Assistant Mode

**Kein @mention nötig** - Aktiv wenn kein spezifischer Agent angesprochen wird

### Emir ist:
- 🤝 **Gesprächig** - Redet wie ein Kollege, nicht wie ein Bot
- 🎯 **Hilfsbereit** - Denkt proaktiv mit
- 💡 **Erklärt** - Zeigt nicht nur WAS, sondern auch WARUM
- 🔍 **Detailliert** - Gibt File-Referenzen mit Zeilennummern

### Emir antwortet auf Deutsch:
```
✅ "Hey! Gute Frage. Der AI Provider Manager funktioniert so..."
✅ "Ich würde das anders machen, weil..."
✅ "Lass uns mal schauen... ah, in Zeile 45 sehe ich..."

❌ "Das steht in der Dokumentation."
❌ Roboter-hafte Antworten
```

### Code-Kommentare auf Englisch:
```typescript
/**
 * Process user query with AI provider
 * English documentation for code
 */
async function processQuery(query: string): Promise<Result> {
  // English inline comments
}
```

---

## 📋 Workflow-Beispiele

### Workflow 1: Neues Feature entwickeln

```bash
# 1️⃣ Planung
@planner-agent Plane Feature: Gemini AI Provider Integration

# 2️⃣ Design (parallel möglich)
@designer-agent Design für Gemini Provider Selector UI

# 3️⃣ Implementation
@code-agent Implementiere Gemini Provider basierend auf Plan

# 4️⃣ Testing (PARALLEL zum Coder!)
@tester-agent Teste Gemini Provider parallel zur Entwicklung

# 5️⃣ Review
@supervisor-agent Reviewe Gemini Provider Code

# 6️⃣ Security Check
@security-agent Prüfe Gemini Integration auf Sicherheitslücken

# 7️⃣ Dokumentation
@docs-writer-agent Dokumentiere Gemini Provider Setup

# ✅ Feature fertig!
```

### Workflow 2: Bug fixen

```bash
# 1️⃣ Problem analysieren
@problem-solver-agent Analysiere warum Search nicht funktioniert

# 2️⃣ Fix implementieren
@code-agent Fixe Search Bug basierend auf Analyse

# 3️⃣ Testen
@tester-agent Teste ob Search Bug wirklich gefixt ist

# 4️⃣ Review
@supervisor-agent Reviewe Bug-Fix

# ✅ Bug gefixt!
```

### Workflow 3: Legacy Code modernisieren

```bash
# 1️⃣ Analyse
@repair-agent Analysiere alten CRM Code und erstelle Modernisierungs-Plan

# 2️⃣ Migration
@repair-agent Migriere von Webpack zu Vite

# 3️⃣ Problem-Solving bei Breaking Changes
@problem-solver-agent Hilfe mit Breaking Changes bei Vite Migration

# 4️⃣ Testing
@tester-agent Teste ob alles nach Migration noch funktioniert

# 5️⃣ Security
@security-agent Prüfe ob Migration Sicherheitslücken eingeführt hat

# 6️⃣ Dokumentation
@docs-writer-agent Update README mit neuen Build-Instruktionen

# ✅ Code modernisiert!
```

### Workflow 4: Performance-Optimierung

```bash
# 1️⃣ Problem identifizieren
@problem-solver-agent Analysiere Performance-Bottlenecks

# 2️⃣ Lösungen finden
@problem-solver-agent Moderne Alternativen für langsame Teile

# 3️⃣ Implementation
@code-agent Implementiere Performance-Optimierungen

# 4️⃣ Testing
@tester-agent Teste Performance vorher/nachher

# ✅ App schneller!
```

---

## 💡 Tipps zur Agent-Nutzung

### ✅ DO's:

1. **Paralleles Arbeiten nutzen**
   ```
   # Designer und Planner können parallel arbeiten
   @planner-agent + @designer-agent gleichzeitig starten
   ```

2. **Tester IMMER parallel zum Coder**
   ```
   @code-agent + @tester-agent = Zero Bugs!
   ```

3. **Spezifische Agenten für spezifische Tasks**
   ```
   ✅ @security-agent für Security
   ✅ @designer-agent für UI/UX
   ✅ @repair-agent für Legacy Code
   ```

4. **Supervisor am Ende**
   ```
   Immer @supervisor-agent vor dem Commit
   ```

### ❌ DON'Ts:

1. **Nicht alles mit einem Agent**
   ```
   ❌ @code-agent mach alles
   ✅ Verschiedene Agenten für verschiedene Tasks
   ```

2. **Tester nicht vergessen**
   ```
   ❌ Code schreiben ohne @tester-agent
   ✅ Immer parallel testen lassen
   ```

3. **Kein Review überspringen**
   ```
   ❌ Direkt committen ohne Review
   ✅ @supervisor-agent vor jedem Commit
   ```

---

## 📁 Alle Dateien & Guides

### Agent-Prompts:
```
.cursor/prompts/
├── planner-agent.md          # Planner
├── supervisor-agent.md        # Supervisor
├── code-agent.md              # Coder
├── tester-agent.md            # Tester
├── designer-agent.md          # Designer
├── docs-writer-agent.md       # Docs Writer
├── problem-solver-agent.md    # Problem Solver
├── repair-agent.md            # Repair Agent
└── security-agent.md          # Security
```

### Templates:
```
.cursor/agent-templates/
├── new-component.template.tsx  # React Component
├── new-service.template.ts     # Service Class
└── new-hook.template.ts        # Custom Hook
```

### Konfiguration:
```
.cursorrules                    # Haupt-Konfiguration (alle Agenten)
.cursor/settings.json           # Cursor IDE Settings
```

### Dokumentation:
```
CURSOR_SETUP.md                 # Cursor Installation & Setup
TEAM_WORKFLOW.md                # Team-Workflow Beispiele
FIGMA_DESIGN_GUIDE.md           # Figma Tutorial
SYNOLOGY_INSTALLATION.md        # Security Agent auf NAS
WIE_MIT_AGENTEN_KOMMUNIZIEREN.md # Kommunikations-Guide
ALLE_AGENTEN_ÜBERSICHT.md       # Diese Datei
```

---

## 🚀 Quick Start

### 1. Cursor öffnen
```bash
cursor /home/user/research-agent
```

### 2. Ersten Agent testen
```bash
# Chat öffnen (Cmd+L)
@planner-agent Erkläre wie du arbeitest
```

### 3. Feature entwickeln
```bash
@planner-agent Plane Feature: [Dein Feature]
@code-agent Implementiere [Feature]
@tester-agent Teste [Feature]
@supervisor-agent Reviewe [Feature]
```

### 4. Fertig! 🎉

---

## 📞 Support

Bei Fragen oder Problemen:
- 📖 Lies `CURSOR_SETUP.md` für Setup-Hilfe
- 💬 Frag Emir (default Assistant Mode)
- 🔧 `@problem-solver-agent` bei komplexen Problemen

---

**Dein komplettes AI Development Team - bereit zum Einsatz! 🚀**
