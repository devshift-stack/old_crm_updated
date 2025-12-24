/**
 * {{COMPONENT_NAME}} Component
 * {{COMPONENT_DESCRIPTION}}
 */

import React, { useState, useCallback } from 'react';
import './{{COMPONENT_NAME}}.css';

/**
 * Component props
 */
interface {{COMPONENT_NAME}}Props {
  readonly title: string;
  readonly onAction?: (value: string) => Promise<void>;
}

/**
 * {{COMPONENT_DESCRIPTION}}
 */
export function {{COMPONENT_NAME}}({
  title,
  onAction
}: {{COMPONENT_NAME}}Props): JSX.Element {
  // State
  const [value, setValue] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Handle action with error handling
   */
  const handleAction = useCallback(async (): Promise<void> => {
    if (!onAction) return;

    try {
      setIsLoading(true);
      setError(null);
      await onAction(value);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  }, [value, onAction]);

  return (
    <div className="{{COMPONENT_NAME_KEBAB}}">
      <h2>{title}</h2>

      {error && (
        <div className="error">{error}</div>
      )}

      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        disabled={isLoading}
      />

      <button
        onClick={handleAction}
        disabled={isLoading || !value.trim()}
      >
        {isLoading ? 'Loading...' : 'Submit'}
      </button>
    </div>
  );
}
