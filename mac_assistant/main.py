#!/usr/bin/env python3
"""
Mac Remote Assistant
Main entry point
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mac_assistant.core_v2 import MacAssistantCore
from mac_assistant.ui.dashboard import DashboardGUI  # New modern dashboard
# from mac_assistant.ui.main_window import MacAssistantGUI  # Legacy GUI


def main():
    """Main entry point"""
    print("=== Mac Remote Assistant v4.0 AUTONOMOUS ===")
    print("Mit KI, Sprachsteuerung & Autonomem Agent")
    print("🎨 Modern Dashboard Interface")
    print("")

    # Load configuration from .env
    from mac_assistant.utils.config import load_config
    config = load_config()

    print("Starte Anwendung...")

    # Check for API keys
    api_key = config.anthropic_api_key
    if not config.has_any_api_key():
        print("\n⚠️  WARNUNG: Keine API Keys gefunden!")
        print("📝 Erstelle eine .env Datei:")
        print("   cp .env.example .env")
        print("   # Dann fülle deine API Keys ein")
        print("")
        print("💡 Oder setze in der App unter ⚙️ Einstellungen")
        print("")
    else:
        providers = config.get_available_providers()
        print(f"✓ API Keys gefunden für: {', '.join(providers)}")
        print("")

    # Initialize core
    try:
        core = MacAssistantCore(api_key=api_key)
        print("✓ Core initialisiert")

        # Show plugin status
        print("\n=== Verfügbare Plugins ===")
        for plugin in core.plugin_manager.get_all_plugins():
            status = "✓" if plugin.is_available() else "✗"
            print(f"{status} {plugin.name}")
        print("")

    except Exception as e:
        print(f"✗ Fehler beim Initialisieren: {e}")
        import traceback
        traceback.print_exc()
        return

    # Launch Modern Dashboard GUI
    try:
        print("✓ Starte Dashboard GUI...")
        print("💡 Alle Funktionen sind jetzt per Mausklick verfügbar!")
        print("")
        gui = DashboardGUI(core)
        gui.run()
    except Exception as e:
        print(f"✗ Fehler beim Starten der GUI: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
