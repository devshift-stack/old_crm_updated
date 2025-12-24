"""
Environment Configuration Loader
Loads settings from .env file
"""

import os
from pathlib import Path
from typing import Optional


class Config:
    """Configuration manager with .env support"""

    def __init__(self, env_file: str = '.env'):
        self.env_file = Path(env_file)
        self.config = {}
        self._load_env()

    def _load_env(self):
        """Load environment variables from .env file"""

        # Try to load from .env file
        if self.env_file.exists():
            print(f"✓ Loading config from {self.env_file}")
            self._parse_env_file(self.env_file)
        else:
            print(f"⚠️  No .env file found. Using environment variables.")
            print(f"💡 Copy .env.example to .env and fill in your API keys!")

        # Load from system environment (override .env)
        self._load_from_system_env()

    def _parse_env_file(self, file_path: Path):
        """Parse .env file"""
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()

                    # Skip comments and empty lines
                    if not line or line.startswith('#'):
                        continue

                    # Parse KEY=VALUE
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()

                        # Remove quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]

                        # Set in environment
                        os.environ[key] = value
                        self.config[key] = value

        except Exception as e:
            print(f"Error reading .env file: {e}")

    def _load_from_system_env(self):
        """Load from system environment variables (takes precedence)"""
        env_vars = [
            'ANTHROPIC_API_KEY',
            'OPENAI_API_KEY',
            'XAI_API_KEY',
            'GROK_API_KEY',
            'ENABLE_AUTONOMOUS_AGENT',
            'ENABLE_VOICE_CONTROL',
            'ENABLE_BACKGROUND_MONITOR',
            'ACTIVE_AI_PROVIDER',
        ]

        for var in env_vars:
            value = os.getenv(var)
            if value:
                self.config[var] = value

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get configuration value"""
        return self.config.get(key, os.getenv(key, default))

    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get boolean configuration value"""
        value = self.get(key)
        if value is None:
            return default
        return value.lower() in ('true', '1', 'yes', 'on')

    def get_int(self, key: str, default: int = 0) -> int:
        """Get integer configuration value"""
        value = self.get(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            return default

    # Convenience methods for common configs

    @property
    def anthropic_api_key(self) -> Optional[str]:
        """Get Anthropic API key"""
        return self.get('ANTHROPIC_API_KEY')

    @property
    def openai_api_key(self) -> Optional[str]:
        """Get OpenAI API key"""
        return self.get('OPENAI_API_KEY')

    @property
    def xai_api_key(self) -> Optional[str]:
        """Get xAI/Grok API key"""
        return self.get('XAI_API_KEY') or self.get('GROK_API_KEY')

    @property
    def autonomous_enabled(self) -> bool:
        """Check if autonomous agent is enabled"""
        return self.get_bool('ENABLE_AUTONOMOUS_AGENT', default=True)

    @property
    def voice_enabled(self) -> bool:
        """Check if voice control is enabled"""
        return self.get_bool('ENABLE_VOICE_CONTROL', default=False)

    @property
    def monitor_enabled(self) -> bool:
        """Check if background monitor is enabled"""
        return self.get_bool('ENABLE_BACKGROUND_MONITOR', default=True)

    @property
    def active_ai_provider(self) -> str:
        """Get active AI provider"""
        return self.get('ACTIVE_AI_PROVIDER', default='claude')

    def has_any_api_key(self) -> bool:
        """Check if any API key is configured"""
        return any([
            self.anthropic_api_key,
            self.openai_api_key,
            self.xai_api_key
        ])

    def get_available_providers(self) -> list:
        """Get list of available AI providers based on API keys"""
        providers = []
        if self.anthropic_api_key:
            providers.append('claude')
        if self.openai_api_key:
            providers.append('chatgpt')
        if self.xai_api_key:
            providers.append('grok')
        return providers


# Global config instance
_config = None

def load_config(env_file: str = '.env') -> Config:
    """Load configuration (singleton)"""
    global _config
    if _config is None:
        _config = Config(env_file)
    return _config

def get_config() -> Config:
    """Get configuration instance"""
    global _config
    if _config is None:
        _config = load_config()
    return _config
