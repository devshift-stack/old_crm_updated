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
from mac_assistant.ui.main_window import MacAssistantGUI


def main():
    """Main entry point"""
    print("=== Mac Remote Assistant v2.0 ===")
    print("Mit Plugin-System und Task-Automation")
    print("")
    print("Starte Anwendung...")

    # Check for API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("\n⚠️  WARNUNG: ANTHROPIC_API_KEY nicht gesetzt!")
        print("KI-Funktionen werden nicht verfügbar sein.")
        print("Setze den API Key in den Einstellungen oder als Umgebungsvariable.")
        print("Beispiel: export ANTHROPIC_API_KEY='sk-ant-your-key-here'\n")

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

    # Launch GUI
    try:
        print("✓ Starte GUI...")
        gui = MacAssistantGUI(core)
        gui.run()
    except Exception as e:
        print(f"✗ Fehler beim Starten der GUI: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
