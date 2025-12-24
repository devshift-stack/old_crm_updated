# Coding Standards - Für andere Chats

Diese Datei enthält die Coding Standards, die für dieses Projekt verwendet wurden.
**Kopiere den Inhalt unten in neue Chats, um konsistente Code-Qualität zu gewährleisten.**

---

## Globale Coding Standards

### Sprache
- Antworte immer auf **Deutsch**
- Code-Kommentare auf **Englisch**

### Coding Standards

#### TypeScript verwenden
- Strikte Typisierung (`strict: true`)
- Modulare Architektur mit klaren Schnittstellen
- Konsistente Namenskonventionen:
  - `camelCase` für Variablen und Funktionen
  - `PascalCase` für Komponenten und Klassen
  - `SCREAMING_SNAKE_CASE` für Konstanten
- Jede Funktion/Komponente mit JSDoc dokumentieren
- **Keine `any` Types** – immer explizite Typen definieren

#### Frontend-Backend-Integration
- API-Endpunkte immer explizit mit Frontend-Komponenten verknüpfen
- Bei Login/Auth: Backend-Route UND Frontend-Handler gemeinsam implementieren
- State-Management vor UI-Komponenten entwickeln
- Error-Handling für ALLE API-Aufrufe implementieren (try/catch, Loading-States, Error-States)
- API-Response-Types zwischen Frontend und Backend teilen (shared types)

#### Entwicklungsprozess
- Code in kleinen, testbaren Schritten generieren
- Nach jedem Schritt: Funktionalität verifizieren bevor weiter
- Bei Fehlern: Exakte Error-Message analysieren, Root Cause zuerst fixen
- Keine isolierten Snippets – immer Kontext zur Gesamtarchitektur beachten
- Abhängigkeiten zwischen Modulen explizit benennen

#### Sicherheit
- Input-Validierung auf Frontend UND Backend
- XSS/SQL-Injection Prevention beachten
- Secrets niemals im Code hardcoden – Environment Variables nutzen
- Authentication/Authorization bei jedem Endpoint prüfen

#### Code-Qualität
- **DRY-Prinzip**: Wiederholungen vermeiden, in Funktionen auslagern
- **Single Responsibility**: Eine Funktion = eine Aufgabe
- Früh returnen statt tiefe Verschachtelungen
- Aussagekräftige Variablen- und Funktionsnamen

---

## Verwendung in anderen Chats

**Kopiere diese Nachricht am Anfang eines neuen Chats:**

```
Bitte halte dich an folgende Coding Standards:

**Sprache:**
- Antworte auf Deutsch
- Code-Kommentare auf Englisch

**TypeScript:**
- Strikte Typisierung (strict: true)
- Keine any Types
- JSDoc für alle Funktionen
- Namenskonventionen:
  - camelCase (Variablen/Funktionen)
  - PascalCase (Komponenten/Klassen)
  - SCREAMING_SNAKE_CASE (Konstanten)

**Architektur:**
- Modulare Struktur
- Shared Types zwischen Frontend/Backend
- Single Responsibility Prinzip
- DRY-Prinzip

**Sicherheit:**
- Input-Validierung überall
- Keine Secrets im Code
- Environment Variables für Config

**Entwicklung:**
- Kleine, testbare Schritte
- Error-Handling überall (try/catch, States)
- Nach jedem Schritt verifizieren
```

---

## TypeScript Beispiel-Template

```typescript
/**
 * Example service class
 * Demonstrates coding standards
 */

/**
 * Configuration interface
 */
interface ServiceConfig {
  readonly apiKey: string;
  readonly timeout: number;
}

/**
 * Example service class
 * Follows single responsibility and DRY principles
 */
export class ExampleService {
  private readonly config: ServiceConfig;

  /**
   * Initialize the service
   * @param config Service configuration
   */
  constructor(config: ServiceConfig) {
    this.config = config;
  }

  /**
   * Execute a request with error handling
   * @param data Request data
   * @returns Promise with result
   */
  public async executeRequest(data: string): Promise<string> {
    try {
      // Validate input
      this.validateInput(data);

      // Execute request
      const result = await this.performRequest(data);

      return result;
    } catch (error) {
      // Handle error
      return this.handleError(error);
    }
  }

  /**
   * Validate input data
   * @param data Data to validate
   * @throws Error if validation fails
   */
  private validateInput(data: string): void {
    if (!data || data.trim().length === 0) {
      throw new Error('Input cannot be empty');
    }
  }

  /**
   * Perform the actual request
   * @param data Request data
   * @returns Promise with response
   */
  private async performRequest(data: string): Promise<string> {
    // Implementation here
    return data;
  }

  /**
   * Handle errors with proper typing
   * @param error Error object
   * @returns Error message
   */
  private handleError(error: unknown): string {
    if (error instanceof Error) {
      return error.message;
    }
    return 'Unknown error occurred';
  }
}
```

## React Component Beispiel

```typescript
/**
 * Example React component
 * Demonstrates component structure and typing
 */

import React, { useState, useCallback } from 'react';

/**
 * Component props interface
 */
interface ExampleProps {
  readonly title: string;
  readonly onSubmit: (value: string) => Promise<void>;
}

/**
 * Example component with proper TypeScript typing
 */
export function ExampleComponent({ title, onSubmit }: ExampleProps): JSX.Element {
  const [value, setValue] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Handle form submission with error handling
   */
  const handleSubmit = useCallback(async (): Promise<void> => {
    try {
      setIsLoading(true);
      setError(null);

      await onSubmit(value);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, [value, onSubmit]);

  return (
    <div>
      <h1>{title}</h1>

      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        disabled={isLoading}
      />

      <button onClick={handleSubmit} disabled={isLoading}>
        {isLoading ? 'Loading...' : 'Submit'}
      </button>

      {error && <div className="error">{error}</div>}
    </div>
  );
}
```

---

**Diese Standards wurden beim Research Agent Projekt zu 100% eingehalten!**
