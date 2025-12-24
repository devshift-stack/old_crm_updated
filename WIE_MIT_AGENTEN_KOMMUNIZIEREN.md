# 💬 Wie du mit deinen AI-Agenten kommunizierst

## Kompletter Kommunikations-Guide

---

## 🎯 Die 3 Wege mit Agenten zu sprechen

### 1️⃣ @ Mention (Empfohlen!)

**Am einfachsten und klarsten:**

```
@planner Feature: Export-Funktion hinzufügen
@designer Erstelle UI für Dark Mode
@coder Implementiere nach dem Plan
@tester Finde alle Bugs
@problem-solver App ist langsam, optimiere
@repair Modernisiere diese alte Codebase
@docs Dokumentiere das neue Feature
@supervisor Review den Code
```

**Vorteile:**
- ✅ Klar welcher Agent gemeint ist
- ✅ Agent weiß sofort: "Ich bin dran!"
- ✅ Funktioniert in Chat, Composer, überall

### 2️⃣ Direkt ansprechen (mit Namen)

**Freundlicher, persönlicher:**

```
"Hey Emir, plane mir die Export-Funktion"
"Emir, kannst du den Code reviewen?"
"Planner, erstelle einen detaillierten Plan"
"Tester, teste das neue Feature gründlich"
```

**Vorteile:**
- ✅ Natürlicher
- ✅ Wie echte Konversation
- ✅ Gut für Brainstorming

### 3️⃣ Kontext-basiert (implizit)

**Agent versteht aus dem Kontext:**

```
"Ich will Feature X bauen, wie gehen wir vor?"
→ Planner antwortet automatisch

"Der Code sieht noch nicht gut aus"
→ Designer gibt Feedback

"Die App crashed bei leerem Input"
→ Problem Solver analysiert
```

**Vorteile:**
- ✅ Schnell
- ✅ Natürlich
- ✅ Flexibel

---

## 🗣️ In Cursor IDE kommunizieren

### Chat Mode (Cmd+L)

**Für:** Fragen, Erklärungen, Diskussionen

```bash
# Öffnen
Cmd+L

# Dann schreiben:
"@planner Ich brauche einen Plan für Feature X"
"@problem-solver Warum ist die App so langsam?"
"Emir, erkläre mir wie der AI Provider funktioniert"
```

**Agent antwortet:**
- Auf Deutsch
- Ausführlich
- Mit Code-Beispielen
- Mit File-Referenzen

**Beispiel-Dialog:**
```
Du: "@planner Feature: Export Results to CSV"

Planner: "Alles klar! Ich erstelle einen detaillierten Plan...

### Feature: Export Search Results

#### Ziel
User können Suchergebnisse als CSV exportieren

#### Implementation Plan

Phase 1: Backend
Step 1: CSV Generator Service
- File: src/services/export/csv-generator.ts
- Why: CSV logic isolieren
...

Was denkst du? Soll ich detaillierter werden bei einem Step?"

Du: "Ja, erkläre Step 1 genauer"

Planner: "Gerne! Step 1 im Detail:
..."
```

### Composer Mode (Cmd+I)

**Für:** Code-Implementierung, Multi-file Änderungen

```bash
# Öffnen
Cmd+I

# Dann schreiben:
"@coder Implementiere den Export-Plan"
"@repair Update alle Dependencies"
"@coder + @designer Baue die SearchBar neu"
```

**Agent macht:**
- Generiert Code
- Ändert mehrere Files
- Zeigt Preview
- Du approved oder änderst

**Beispiel:**
```
Du: "@coder Implementiere Export Feature nach Plan"

Coder: "Okay, ich implementiere jetzt:

1. src/services/export/csv-generator.ts
2. src/main/ipc-handlers.ts (Zeile 145)
3. src/renderer/components/ExportButton.tsx

[Zeigt Code Preview...]

Sieht gut aus? Dann drücke Enter zum Apply."
```

### Inline Edit (Cmd+K)

**Für:** Schnelle Edits, einzelne Funktionen

```bash
# Cursor in Code-Zeile
Cmd+K

# Dann schreiben:
"Füge Error Handling hinzu"
"Konvertiere zu async/await"
"Optimiere diese Funktion"
```

---

## 🎭 Welcher Agent wann?

### 📋 Planner

**Wann rufen:**
```
✅ "Ich will Feature X bauen"
✅ "Wie soll ich das strukturieren?"
✅ "Erstelle einen Implementation Plan"
✅ "Was sind die Steps für...?"
```

**Agent antwortet mit:**
- Detailliertem Plan
- Step-by-Step Anleitung
- Architektur-Vorschlag
- Risiko-Analyse
- Timeline

### 🎯 Supervisor (Emir)

**Wann rufen:**
```
✅ "Review meinen Code"
✅ "Ist das so okay?"
✅ "Gibt es bessere Ansätze?"
✅ "@supervisor Schau dir das an"
```

**Agent antwortet mit:**
- Konstruktivem Feedback
- Code Quality Check
- Verbesserungsvorschlägen
- Go/No-Go Decision

### 💻 Coder (Emir)

**Wann rufen:**
```
✅ "Implementiere Feature X"
✅ "Schreib den Code nach Plan"
✅ "Füge Feature Y hinzu"
✅ "@coder Baue das um"
```

**Agent macht:**
- Schreibt Code
- Folgt Plan
- Fügt Error-Handling hinzu
- Schreibt JSDoc
- Testet selbst

### 🧪 Tester

**Wann rufen:**
```
✅ "Teste das Feature"
✅ "Finde alle Bugs"
✅ "Run tests"
✅ "@tester Prüfe das gründlich"
```

**Agent antwortet mit:**
- Test Report
- Bug Liste
- Performance Metrics
- Action Items

### 🎨 Designer

**Wann rufen:**
```
✅ "Designe die UI für Feature X"
✅ "Verbessere das Layout"
✅ "Erstelle Figma Mockups"
✅ "@designer Wie soll das aussehen?"
```

**Agent antwortet mit:**
- Design Specs
- Figma Mockups (beschrieben)
- CSS Code
- Color Palette
- Typography

### 📚 Docs Writer

**Wann rufen:**
```
✅ "Dokumentiere Feature X"
✅ "Schreib User Guide"
✅ "Update README"
✅ "@docs Explain this code"
```

**Agent antwortet mit:**
- JSDoc Comments
- README Updates
- User Guides
- API Documentation

### 🔧 Problem Solver

**Wann rufen:**
```
✅ "Die App ist langsam, warum?"
✅ "Build schlägt fehl"
✅ "Gibt es eine moderne Alternative für X?"
✅ "@problem-solver Fix this"
```

**Agent antwortet mit:**
- Problem-Analyse
- Root Cause
- Lösungsvorschlägen
- Modernen Alternativen
- Implementation

### 🔨 Repair Agent

**Wann rufen:**
```
✅ "Analysiere diese alte Codebase"
✅ "Update Dependencies"
✅ "Modernisiere das Projekt"
✅ "@repair Fix all TypeScript errors"
```

**Agent antwortet mit:**
- Repair Report
- Upgrade Plan
- Modernization Strategy
- Step-by-Step Fixes

---

## 💡 Kommunikations-Patterns

### Pattern 1: Feature entwickeln

```
1. Du: "@planner Feature: Dark Mode"
   Planner: [Erstellt Plan]

2. Du: "Plan approved, go!"

3. Du: "@designer UI für Dark Mode"
   Designer: [Erstellt Design]

4. Du: "@coder Implementiere Design + Plan"
   Coder: [Schreibt Code]

5. @tester (arbeitet automatisch parallel!)
   Tester: [Findet 2 Bugs]

6. Du: "@coder Fix diese 2 Bugs"
   Coder: [Fixt]

7. Du: "@supervisor Review"
   Supervisor: [Approved ✅]

8. Du: "@docs Dokumentiere"
   Docs: [Schreibt Docs]

9. ✅ Feature DONE!
```

### Pattern 2: Problem lösen

```
1. Du: "Die Search ist sehr langsam"

2. @problem-solver (antwortet automatisch)
   "Ich analysiere...
   Problem: Sequentielle Verarbeitung
   Lösung: Parallel Processing"

3. Du: "@coder Implementiere die Lösung"
   Coder: [Implementiert]

4. @tester (testet parallel)
   "10x schneller! ✅"

5. ✅ Problem gelöst!
```

### Pattern 3: Code Review

```
1. Du: "@supervisor Review src/services/"

2. Supervisor: "Lass mich schauen...

   ✅ Gut:
   - Type Safety
   - Error Handling

   ⚠️ Issues:
   - Zeile 45: JSDoc fehlt
   - Zeile 67: Performance-Problem

   Soll ich das fixen lassen?"

3. Du: "Ja bitte"

4. Supervisor: "@coder Fix these issues"
   Coder: [Fixt]

5. Supervisor: "Jetzt gut ✅"
```

### Pattern 4: Brainstorming

```
Du: "Ich will Feature X bauen, aber bin unsicher"

Planner: "Ich sehe 2 Ansätze:
A) Schnell aber weniger flexibel
B) Komplexer aber zukunftssicher"

Problem Solver: "Moderne Alternative wäre:
Firebase statt eigene API"

Designer: "UI könnte so aussehen:
[Beschreibt Mockup]"

Du: "Lass uns Ansatz B mit Firebase machen"

Team: "Alles klar! Planner erstellt Plan..."
```

---

## 🎯 Tipps für gute Kommunikation

### ✅ DO

**Sei spezifisch:**
```
✅ "@planner Feature: Exportiere Results als CSV mit Dropdown"
❌ "@planner Mach Export"
```

**Gib Kontext:**
```
✅ "Die Search in src/services/search-engine.ts ist langsam bei 10.000+ Files"
❌ "Search ist langsam"
```

**Stelle Fragen:**
```
✅ "Warum nutzen wir Zustand statt Redux?"
✅ "Gibt es eine bessere Lösung?"
✅ "Was hältst du davon?"
```

**Gib Feedback:**
```
✅ "Das ist zu kompliziert, kannst du vereinfachen?"
✅ "Perfekt, genau so!"
✅ "Ich verstehe das nicht, erkläre nochmal anders"
```

### ❌ DON'T

**Sei nicht vage:**
```
❌ "Mach das besser"
❌ "Fix das"
❌ "Optimiere"
```

**Überlade nicht:**
```
❌ "Implementiere Features A, B, C, D, E gleichzeitig"
→ Besser: Ein Feature nach dem anderen
```

**Vergiss nicht zu testen:**
```
❌ Code schreiben → Fertig
→ Besser: Code schreiben → Testen → Review → Docs
```

---

## 🎨 Kommunikations-Beispiele

### Beispiel 1: Einfache Frage

```
Du: "Emir, wo finde ich den Code für die Dateisuche?"

Emir: "Hey! Der File Search Code ist hier:

Haupt-Engine:
src/services/file-search/search-engine.ts:45

Scanner:
src/services/file-search/file-scanner.ts:78

Die search() Funktion startet den Prozess.
Willst du dass ich dir den Flow erkläre?"
```

### Beispiel 2: Feature-Request

```
Du: "@planner Ich will dass User Ergebnisse filtern können"

Planner: "Cool! Lass mich einen Plan erstellen...

### Feature: Filter Results

#### Requirements
- Filter by file type
- Filter by date
- Filter by size
- Combine filters

#### Plan
[Detaillierter Plan...]

Passt das so oder soll ich was anpassen?"
```

### Beispiel 3: Bug Report

```
Du: "@problem-solver App crashed wenn ich auf Button klicke"

Problem Solver: "Okay, lass mich debuggen...

Fragen:
1. Welcher Button?
2. Console Error?
3. Passiert immer oder manchmal?

[Du antwortest...]

Problem Solver: "Ah ich sehe es!
Root Cause: onClick Handler fehlt in SearchBar.tsx:45

@coder kannst du das fixen?"
```

### Beispiel 4: Design-Feedback

```
Du: "@designer Die UI sieht langweilig aus"

Designer: "Verstehe! Lass mich Vorschläge machen:

1. Gradient statt Solid Colors
2. Glow Effects bei Hover
3. Smooth Animations
4. Micro-Interactions

Soll ich ein Mockup in Figma beschreiben?"

Du: "Ja, Mockup bitte"

Designer: "Okay! So würde ich das designen:
[Detaillierte Beschreibung...]"
```

---

## 📱 Shortcuts & Quick Commands

### Quick Reference

```bash
# Planung
@planner plan [feature]

# Implementierung
@coder implement [feature]
@designer design [component]

# Quality
@tester test [feature]
@supervisor review [code]

# Hilfe
@problem-solver fix [issue]
@repair upgrade [project]

# Dokumentation
@docs document [feature]

# Konversation
"Emir, [frage]"
"Hey [agent], [request]"
```

---

## 🎓 Lern-Kurve

### Anfänger (Tag 1-3)
```
- Nutze @ Mentions
- Stelle einfache Fragen
- Lass Agents Schritt-für-Schritt erklären
```

### Fortgeschritten (Woche 2-4)
```
- Kombiniere mehrere Agents
- Nutze Parallel Workflows
- Gib detaillierte Anfragen
```

### Profi (Monat 2+)
```
- Agents arbeiten automatisch zusammen
- Du orchestrierst nur noch
- Team läuft wie geschmiert
```

---

## 🚀 Pro-Tipps

### Tip 1: Parallel arbeiten lassen
```
@coder Implementiere Feature X
@tester Teste parallel

→ Schneller fertig!
```

### Tip 2: Agents diskutieren lassen
```
@planner + @designer + @problem-solver

"Wie sollen wir Feature X bauen?"

→ Verschiedene Perspektiven!
```

### Tip 3: Context geben
```
❌ "Optimiere das"
✅ "@problem-solver Optimiere Search in search-engine.ts
    Problem: Langsam bei 10.000+ Files
    Aktuell: Sequentielle Verarbeitung
    Goal: < 500ms"
```

### Tip 4: Feedback-Loop
```
Agent → Schlägt Lösung vor
Du → "Hmm, das ist zu kompliziert"
Agent → "Okay, einfachere Version:"
Du → "Perfekt!"
```

---

## ✅ Zusammenfassung

**Um mit Agenten zu kommunizieren:**

1. **@ Mention nutzen** für klare Zuordnung
2. **Spezifisch sein** was du willst
3. **Kontext geben** für bessere Antworten
4. **Fragen stellen** bei Unklarheiten
5. **Feedback geben** für bessere Ergebnisse

**Deine Agenten sind:**
- 👂 Gute Zuhörer
- 🧠 Intelligente Helfer
- 🤝 Team-Player
- 💬 Gesprächspartner

**Rede mit ihnen wie mit Kollegen!**

---

**Viel Erfolg mit deinem AI-Team! 🎉**
