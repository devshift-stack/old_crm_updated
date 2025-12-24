# 🎨 Figma Design & UX Guide - Research Agent

## Komplette Schritt-für-Schritt Anleitung

Diese Anleitung zeigt dir **exakt** wie du mit Figma professionelle UI/UX Designs für deine Research Agent App erstellst.

---

## 📋 Inhaltsverzeichnis

1. [Figma Setup](#figma-setup)
2. [Design System erstellen](#design-system)
3. [Components designen](#components)
4. [Prototypes erstellen](#prototypes)
5. [Handoff an Developer](#handoff)
6. [Designer Agent nutzen](#designer-agent)

---

## 🚀 Figma Setup

### Schritt 1: Figma Account

```
1. Gehe zu https://figma.com
2. Klicke "Sign up"
3. Wähle "Free" Plan (ausreichend!)
4. Verifiziere Email
```

### Schritt 2: Neues Design File erstellen

```
1. Klicke "+ New design file"
2. Benenne: "Research Agent - UI Design"
3. ✅ Datei ist erstellt!
```

### Schritt 3: Workspace organisieren

```
Erstelle Pages:
1. "Design System" - Colors, Typography, Components
2. "Screens" - Actual app screens
3. "Prototypes" - Interactive flows
4. "Archive" - Old versions
```

---

## 🎨 Design System erstellen

### Schritt 1: Color Palette

**1. Erstelle Color Styles:**

```
1. Klicke auf den Kreis (Fill) oben rechts
2. Klicke auf "+" bei Styles
3. Erstelle folgende Colors:

Primary Colors:
├─ Primary/Blue (#60a5fa)
├─ Primary/Purple (#a78bfa)
└─ Primary/Gradient (gradient von Blue zu Purple)

Neutral Colors:
├─ BG/Dark (#1e1e1e)
├─ BG/Darker (#2d2d2d)
├─ Text/Primary (#e0e0e0)
├─ Text/Secondary (rgba(255, 255, 255, 0.7))
└─ Border (rgba(255, 255, 255, 0.1))

Semantic Colors:
├─ Success (#4caf50)
├─ Warning (#ff9800)
├─ Error (#ef4444)
└─ Info (#60a5fa)
```

**2. Apply Colors:**
```
Select ein Element → Fill → Wähle deine Color Style
```

### Schritt 2: Typography

**1. Erstelle Text Styles:**

```
1. Wähle Text Tool (T)
2. Schreibe "Heading 1"
3. Formatiere:
   - Font: -apple-system (oder SF Pro)
   - Size: 32px
   - Weight: 600
   - Color: Text/Primary

4. Klicke "Create text style"
5. Benenne: "H1"

Wiederhole für:
├─ H1 (32px, weight 600)
├─ H2 (24px, weight 600)
├─ H3 (20px, weight 600)
├─ Body (16px, weight 400)
├─ Body Bold (16px, weight 600)
├─ Small (14px, weight 400)
└─ Tiny (12px, weight 400)
```

### Schritt 3: Spacing System

**Erstelle Grid:**

```
1. View > Show Layout Grid
2. Settings:
   - Count: 12 columns
   - Gutter: 16px
   - Margin: 32px

3. Speichere als "12 Column Grid"
```

**Spacing Values (als Comment notieren):**
```
4px  = spacing-1
8px  = spacing-2
12px = spacing-3
16px = spacing-4
24px = spacing-6
32px = spacing-8
40px = spacing-10
```

### Schritt 4: Effects (Shadows & Glow)

**Erstelle Effect Styles:**

```
1. Wähle Element
2. Effects > + > Drop Shadow
3. Konfiguriere:

Shadow/SM:
- X: 0, Y: 1, Blur: 2, Spread: 0
- Color: #000000, Opacity: 5%

Shadow/MD:
- X: 0, Y: 4, Blur: 6, Spread: 0
- Color: #000000, Opacity: 10%

Shadow/LG:
- X: 0, Y: 10, Blur: 15, Spread: 0
- Color: #000000, Opacity: 15%

Glow/Blue:
- X: 0, Y: 0, Blur: 20, Spread: 0
- Color: #60a5fa, Opacity: 30%
```

---

## 🧩 Components designen

### Component 1: Button

**Schritt 1: Primary Button erstellen**

```
1. Rechteck Tool (R)
2. Zeichne: 200px × 48px
3. Border Radius: 8px
4. Fill: Primary/Gradient
5. Text: "Suchen"
   - Style: Body Bold
   - Color: White
   - Centered
```

**Schritt 2: Als Component speichern**

```
1. Select Button
2. Cmd+Opt+K (Create Component)
3. Name: "Button/Primary"
```

**Schritt 3: Variants erstellen**

```
1. Select Component
2. Rechts-Panel > "Add variant"
3. Erstelle Variants:

States:
├─ Default
├─ Hover (translateY: -2px, Shadow: LG)
├─ Active (translateY: 0)
└─ Disabled (Opacity: 50%)

Sizes:
├─ Small (height: 36px)
├─ Medium (height: 48px)
└─ Large (height: 56px)
```

**Schritt 4: Weitere Button Types**

```
Dupliziere und ändere:
├─ Button/Secondary (transparent, border)
├─ Button/Ghost (keine border, nur text)
└─ Button/Danger (red gradient)
```

### Component 2: Input Field

**Schritt 1: Input erstellen**

```
1. Rechteck: 400px × 48px
2. Border Radius: 12px
3. Fill: rgba(255, 255, 255, 0.05)
4. Stroke: 1px, Border color
5. Text: "Placeholder..."
   - Color: Text/Secondary
```

**Schritt 2: States**

```
Variants:
├─ Default (Border opacity 0.1)
├─ Focus (Border: Primary/Blue, Glow/Blue)
├─ Disabled (Opacity: 50%)
└─ Error (Border: Error)
```

### Component 3: Search Bar

**Vollständige Search Bar:**

```
1. Container: 800px × 60px
   - Border Radius: 12px
   - Fill: rgba(255, 255, 255, 0.05)
   - Stroke: Border

2. Input Field (links)
   - Width: 600px
   - Placeholder: "Beschreibe was du suchst..."

3. Search Button (rechts)
   - Width: 150px
   - Button/Primary Component
   - Text: "Suchen"

4. Gap zwischen Input & Button: 12px

5. Als Component speichern: "SearchBar"
```

### Component 4: Result Card

**Schritt 1: Card Structure**

```
1. Container: 100% × Auto
   - Border Radius: 8px
   - Fill: rgba(255, 255, 255, 0.03)
   - Stroke: Border
   - Padding: 16px

2. Header (Flex horizontal)
   ├─ File Name (Text/Primary, Body Bold)
   └─ Relevance Score (Text/Success, Small)

3. Path (Text/Secondary, Small, monospace)

4. Meta Info (Flex horizontal, gap 8px)
   ├─ Size
   ├─ •
   └─ Date

5. Match Reason (Text/Info, Tiny, italic)
```

**Schritt 2: States**

```
Variants:
├─ Default
└─ Hover (bg: rgba(255, 255, 255, 0.05), border: Primary)
```

**Schritt 3: Als Component**

```
Cmd+Opt+K
Name: "ResultCard"
```

### Component 5: Loading Spinner

**Schritt 1: Spinner erstellen**

```
1. Circle: 40px × 40px
2. No Fill
3. Stroke: 3px
4. Stroke Color:
   - Top: Primary/Blue
   - Rest: rgba(96, 165, 250, 0.2)
5. Rotation: 45° (for start position)
```

**Schritt 2: Animation (Prototype)**

```
1. Select Spinner
2. Prototype Tab
3. Add Interaction:
   - Trigger: After delay (0ms)
   - Action: Rotate 360°
   - Easing: Linear
   - Duration: 1000ms
   - Loop
```

---

## 🖼️ Screens designen

### Screen 1: Main View

**Frame erstellen:**

```
1. Frame Tool (F)
2. Wähle "Desktop" preset (1440 × 1024)
3. Name: "Main - Idle"
4. Fill: BG/Dark
5. Layout Grid: "12 Column Grid"
```

**Layout aufbauen:**

```
Structure:
├─ Header (sticky)
│  ├─ Logo/Title (left)
│  └─ Provider Selector (right)
│
├─ Search Section
│  └─ SearchBar (centered, width: 800px)
│
└─ Content Area
   └─ Empty State
      ├─ Icon 📂
      ├─ Heading "Research Agent"
      ├─ Description
      └─ Examples List
```

**Auto Layout nutzen:**

```
1. Select alle Elements in einer Section
2. Cmd+Opt+G (Frame)
3. Rechts-Panel > Auto Layout
4. Set:
   - Direction: Vertical
   - Gap: 24px
   - Padding: 32px
   - Alignment: Center
```

### Screen 2: Search Results

**Dupliziere Main:**

```
1. Main - Idle kopieren
2. Rename: "Main - Results"
3. Replace Empty State mit Results List
```

**Results List aufbauen:**

```
1. Header Section:
   ├─ "45 Ergebnisse gefunden"
   ├─ Meta (Suchzeit, AI Provider)
   └─ Intent-Beschreibung

2. Results Grid:
   - Nutze ResultCard Components
   - Stack vertical mit gap 12px
   - Zeige 5 Beispiel-Cards

3. Auto Layout:
   - Direction: Vertical
   - Gap: 12px
```

### Screen 3: Loading State

```
1. Dupliziere Main
2. Rename: "Main - Loading"
3. Replace Content mit:
   - Spinner Component (centered)
   - "Durchsuche Dateisystem..."
```

### Screen 4: Error State

```
1. Dupliziere Main
2. Rename: "Main - Error"
3. Replace Content mit:
   - Error Icon ⚠️
   - Heading "Fehler aufgetreten"
   - Error Message
   - "Erneut versuchen" Button
```

---

## 🔗 Prototypes erstellen

### Interactive Flow

**Schritt 1: Verbinde Screens**

```
1. Wechsle zu Prototype Tab
2. Select SearchBar auf "Main - Idle"
3. Click auf + neben Element
4. Ziehe Pfeil zu "Main - Loading"
5. Settings:
   - Trigger: On Click
   - Action: Navigate to
   - Animation: Instant (or Dissolve)
```

**Schritt 2: Loading → Results**

```
1. Select "Main - Loading" Frame
2. Add Interaction:
   - Trigger: After delay (2000ms)
   - Navigate to: Main - Results
   - Animation: Dissolve (300ms)
```

**Schritt 3: Error Flow**

```
Button "Erneut versuchen":
→ Navigate to Main - Loading
```

**Schritt 4: Test Prototype**

```
1. Klicke Play-Button (top right)
2. Teste alle Interactions
3. Prüfe Animations
```

---

## 📤 Handoff an Developer

### Schritt 1: Inspect Mode

```
1. Wähle Element
2. Rechts-Panel > Code
3. Siehst CSS Properties:
   - Width, Height
   - Border Radius
   - Colors
   - Spacing
```

### Schritt 2: Export Assets

**Icons exportieren:**

```
1. Select Icon
2. Export Settings:
   - Format: SVG
   - Resolution: 1x
3. Klicke "Export"
```

**Images exportieren:**

```
Format:
├─ PNG (for screenshots)
├─ SVG (for icons)
└─ WebP (for photos)

Resolutions:
├─ 1x (standard)
├─ 2x (retina)
└─ 3x (high-res)
```

### Schritt 3: Design Specs

**Erstelle Dev Specs Page:**

```
1. Neue Page: "Dev Handoff"
2. Copy Components
3. Annotate:
   - Dimensions
   - Spacing
   - Colors (mit hex codes)
   - Fonts

Beispiel:
┌─────────────────────┐
│  SearchBar          │
│                     │
│  Width: 800px       │
│  Height: 60px       │
│  Border Radius: 12px│
│  Padding: 8px       │
│  Gap: 12px          │
│  ────────────────   │
│  Input: 600px       │
│  Button: 150px      │
└─────────────────────┘
```

### Schritt 4: Share mit Developer

```
1. Klicke "Share" (top right)
2. Set Permission: "Can view"
3. Copy Link
4. Sende an @coder Agent mit:
   "@coder Implementiere dieses Design: [Figma Link]"
```

---

## 🤖 Designer Agent nutzen

### Mit Designer Agent arbeiten:

**Schritt 1: Design Request**

```
Du: "@designer Erstelle UI für Export Feature"

Designer Agent:
1. Analysiert bestehende UI
2. Erstellt Design Specs
3. Zeigt CSS Code
4. Empfiehlt Figma Structure
```

**Schritt 2: Figma Layout**

```
Designer gibt dir:
├─ Color codes
├─ Spacing values
├─ Typography specs
└─ Component structure

Du:
1. Erstellst in Figma
2. Nutzt die exakten Values
3. Components erstellen
```

**Schritt 3: Feedback Loop**

```
Du: "Design erstellt, schau dir an: [Figma Link]"

Designer Agent:
- Reviewed Design
- Gibt Feedback
- Schlägt Verbesserungen vor
- Check Accessibility

Du:
- Implementierst Feedback
- Finalisierst Design
```

**Schritt 4: Handoff**

```
Designer Agent gibt dir:
- CSS Code für Components
- React Component Structure
- Animations Code

Du: "@coder Implementiere Design mit diesem Code"
```

---

## 🎓 Figma Best Practices

### DO ✅

**Organisiere gut:**
```
✅ Benenne Layers sinnvoll
✅ Nutze Pages für verschiedene Bereiche
✅ Gruppiere related Elements
✅ Nutze Auto Layout wo möglich
```

**Nutze Design System:**
```
✅ Erstelle Color Styles
✅ Erstelle Text Styles
✅ Erstelle Components
✅ Verwende Variants
```

**Bleib konsistent:**
```
✅ Gleiche Spacing überall
✅ Gleiche Border Radius
✅ Gleiche Colors
✅ Gleiche Typography
```

### DON'T ❌

**Chaos vermeiden:**
```
❌ Layers "Rectangle 1", "Rectangle 2"
❌ Alles in einer Page
❌ Keine Components nutzen
❌ Verschiedene Spacings
```

---

## 📚 Figma Resources

### Tutorials
- Figma Official Tutorial: https://help.figma.com/
- YouTube: "Figma Tutorial for Beginners"

### Plugins (hilfreich)
- **Iconify** - Tausende Icons
- **Unsplash** - Stock Photos
- **Content Reel** - Dummy Content
- **Stark** - Accessibility Check

### Design Inspiration
- Dribbble.com
- Behance.net
- Mobbin (mobile app designs)

---

## 🎯 Quick Reference

### Shortcuts

```
T - Text Tool
R - Rectangle
O - Ellipse
L - Line
F - Frame
Cmd+G - Group
Cmd+Opt+G - Frame
Cmd+Opt+K - Create Component
Cmd+D - Duplicate
Opt+Drag - Duplicate while dragging
```

### Measurements

```
Colors: In Figma, nutze Color Styles
Spacing: 8px grid system (4, 8, 12, 16, 24, 32, 40)
Typography: System Font Stack
Border Radius: 8px (standard), 12px (large)
```

---

**Mit dieser Anleitung kannst du professionelle UI/UX Designs erstellen! 🎨**

Fragen? → `@designer Ich brauche Hilfe mit...`
