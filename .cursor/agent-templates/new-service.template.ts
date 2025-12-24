/**
 * {{SERVICE_NAME}}
 * {{SERVICE_DESCRIPTION}}
 */

/**
 * Service configuration
 */
interface {{SERVICE_NAME}}Config {
  readonly apiKey?: string;
  readonly timeout: number;
}

/**
 * {{SERVICE_DESCRIPTION}}
 */
export class {{SERVICE_NAME}} {
  private readonly config: {{SERVICE_NAME}}Config;
  private isInitialized = false;

  /**
   * Initialize the service
   * @param config Service configuration
   */
  constructor(config: {{SERVICE_NAME}}Config) {
    this.config = config;
  }

  /**
   * Initialize the service
   * @throws Error if initialization fails
   */
  public async initialize(): Promise<void> {
    try {
      // Initialization logic here
      this.isInitialized = true;
    } catch (error) {
      throw new Error(
        `Failed to initialize {{SERVICE_NAME}}: ${
          error instanceof Error ? error.message : 'Unknown error'
        }`
      );
    }
  }

  /**
   * Execute main operation
   * @param input Input data
   * @returns Promise with result
   */
  public async execute(input: string): Promise<Result> {
    if (!this.isInitialized) {
      throw new Error('{{SERVICE_NAME}} not initialized');
    }

    try {
      this.validate(input);
      return await this.process(input);
    } catch (error) {
      return this.handleError(error);
    }
  }

  /**
   * Validate input
   * @param input Input to validate
   * @throws Error if validation fails
   */
  private validate(input: string): void {
    if (!input || input.trim().length === 0) {
      throw new Error('Input cannot be empty');
    }
  }

  /**
   * Process input
   * @param input Validated input
   * @returns Promise with result
   */
  private async process(input: string): Promise<Result> {
    // Processing logic here
    return {
      success: true,
      data: input,
    };
  }

  /**
   * Handle errors
   * @param error Error object
   * @returns Error result
   */
  private handleError(error: unknown): Result {
    const message = error instanceof Error ? error.message : 'Unknown error';
    console.error(`[{{SERVICE_NAME}}] Error:`, message);

    return {
      success: false,
      error: message,
    };
  }

  /**
   * Cleanup resources
   */
  public async cleanup(): Promise<void> {
    this.isInitialized = false;
    // Cleanup logic here
  }
}

/**
 * Result interface
 */
interface Result {
  readonly success: boolean;
  readonly data?: string;
  readonly error?: string;
}
