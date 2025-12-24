"""
Slack Bot Agent
Control your Mac from anywhere via Slack
"""

import os
import threading
from typing import Optional


class SlackBotAgent:
    """Slack bot for remote control"""

    def __init__(self, core, bot_token: Optional[str] = None, app_token: Optional[str] = None):
        self.core = core
        self.bot_token = bot_token or os.getenv('SLACK_BOT_TOKEN')
        self.app_token = app_token or os.getenv('SLACK_APP_TOKEN')

        self.app = None
        self.running = False

        if not self.bot_token:
            print("⚠️  SLACK_BOT_TOKEN not set. Bot disabled.")
            return

        if not self.app_token:
            print("⚠️  SLACK_APP_TOKEN not set. Socket mode disabled.")
            print("   Für Socket Mode: SLACK_APP_TOKEN erforderlich")
            return

        self._init_bot()

    def _init_bot(self):
        """Initialize Slack bot"""
        try:
            # Try to import slack_bolt
            from slack_bolt import App
            from slack_bolt.adapter.socket_mode import SocketModeHandler

            self.App = App
            self.SocketModeHandler = SocketModeHandler
            self.available = True

            print("✓ Slack bot initialized")

        except ImportError:
            print("⚠️  slack-bolt not installed.")
            print("   Run: pip install slack-bolt")
            self.available = False

    def start(self):
        """Start the Slack bot"""
        if not self.available:
            return False

        if self.running:
            return True

        print("🤖 Starting Slack bot...")

        # Start bot in background thread
        threading.Thread(target=self._run_bot, daemon=True).start()
        self.running = True

        return True

    def stop(self):
        """Stop the Slack bot"""
        self.running = False
        print("🤖 Slack bot stopped")

    def _run_bot(self):
        """Run bot (in thread)"""
        try:
            # Create app
            app = self.App(token=self.bot_token)

            # Register command handlers
            app.command("/status")(self._cmd_status)
            app.command("/email")(self._cmd_email)
            app.command("/messages")(self._cmd_messages)
            app.command("/photos")(self._cmd_photos)
            app.command("/tasks")(self._cmd_tasks)
            app.command("/help")(self._cmd_help)

            # Event handlers
            app.event("app_mention")(self._handle_mention)
            app.event("message")(self._handle_message)

            # Start Socket Mode handler
            handler = self.SocketModeHandler(app, self.app_token)
            handler.start()

        except Exception as e:
            print(f"Error running Slack bot: {e}")

    # ===== Command Handlers =====

    def _cmd_status(self, ack, command, say):
        """Handle /status command"""
        ack()

        try:
            plugins = len(self.core.plugin_manager.get_available_plugins())
            ai_status = "✅ Aktiv" if self.core.ai_enabled else "❌ Inaktiv"

            status = f"""
📊 *System-Status*

*Plugins:* {plugins} verfügbar
*KI:* {ai_status}
*Autonomer Agent:* {'✅ Läuft' if hasattr(self.core, 'autonomous_agent') else '❌ Aus'}

*Verfügbare Apps:*
{self._get_plugin_list()}
            """
            say(status)

        except Exception as e:
            say(f"❌ Fehler: {str(e)}")

    def _cmd_email(self, ack, command, say):
        """Handle /email command"""
        ack()
        say("📧 Prüfe E-Mails...")

        try:
            mail_plugin = self.core.get_plugin('Mail')
            if mail_plugin and mail_plugin.is_available():
                emails = mail_plugin.get_unread_emails(5)
                say(f"📧 *E-Mails:*\n\n{emails}")
            else:
                say("❌ Mail-Plugin nicht verfügbar")

        except Exception as e:
            say(f"❌ Fehler: {str(e)}")

    def _cmd_messages(self, ack, command, say):
        """Handle /messages command"""
        ack()
        say("💬 Prüfe Nachrichten...")

        try:
            all_messages = self.core.get_all_messages(limit=5)

            response = "💬 *Nachrichten:*\n\n"
            for app, messages in all_messages.items():
                response += f"*{app}:*\n{messages}\n\n"

            say(response)

        except Exception as e:
            say(f"❌ Fehler: {str(e)}")

    def _cmd_photos(self, ack, command, say):
        """Handle /photos command"""
        ack()

        # Parse arguments from command text
        search_term = command.get('text', '').strip() or 'recent'
        say(f"📸 Suche Fotos: {search_term}...")

        try:
            photos_plugin = self.core.get_plugin('Photos')
            if photos_plugin and photos_plugin.is_available():
                if search_term == 'recent':
                    photos = photos_plugin.get_recent_media(days=7)
                else:
                    photos = photos_plugin.search(search_term)

                say(f"📸 *Fotos:*\n\n{photos}")
            else:
                say("❌ Photos-Plugin nicht verfügbar")

        except Exception as e:
            say(f"❌ Fehler: {str(e)}")

    def _cmd_tasks(self, ack, command, say):
        """Handle /tasks command"""
        ack()

        task = command.get('text', '').strip()
        if not task:
            say("💡 Usage: `/tasks <befehl>`\nBeispiel: `/tasks Sende E-Mail an Max`")
            return

        say(f"⚡ Führe aus: {task}...")

        try:
            result = self.core.execute_task(task)

            if result.get('success'):
                say(f"✅ Erledigt!\n\n{result.get('result', '')}")
            else:
                say(f"❌ Fehler: {result.get('error', '')}")

        except Exception as e:
            say(f"❌ Fehler: {str(e)}")

    def _cmd_help(self, ack, command, say):
        """Handle /help command"""
        ack()

        help_text = """
📚 *Mac Remote Assistant - Hilfe*

*Slash Commands:*
• `/status` - System-Status & Plugins
• `/email` - Ungelesene E-Mails
• `/messages` - Neue Nachrichten
• `/photos [suche]` - Fotos suchen
• `/tasks [befehl]` - Task ausführen
• `/help` - Diese Hilfe

*Natural Language:*
Erwähne den Bot (@Mac Assistant) oder schreibe eine DM!

Beispiele:
• @Mac Assistant was habe ich heute gemacht?
• @Mac Assistant sende E-Mail an max@example.com
• @Mac Assistant suche Fotos vom Strand
        """
        say(help_text)

    # ===== Event Handlers =====

    def _handle_mention(self, event, say):
        """Handle app mentions"""
        try:
            # Get message text without mention
            text = event.get('text', '')
            # Remove bot mention
            import re
            text = re.sub(r'<@[A-Z0-9]+>', '', text).strip()

            if not text:
                say("👋 Hi! Wie kann ich dir helfen?\nNutze `/help` für Befehle.")
                return

            say("🤖 Verarbeite...")

            # Process with core
            response = self.core.process_user_query(text)
            say(response)

        except Exception as e:
            say(f"❌ Fehler: {str(e)}")

    def _handle_message(self, event, say):
        """Handle direct messages"""
        # Only handle DMs (channel_type is 'im')
        if event.get('channel_type') != 'im':
            return

        # Ignore bot messages
        if event.get('bot_id'):
            return

        try:
            text = event.get('text', '').strip()
            if not text:
                return

            say("🤖 Verarbeite...")

            # Process with core
            response = self.core.process_user_query(text)
            say(response)

        except Exception as e:
            say(f"❌ Fehler: {str(e)}")

    def _get_plugin_list(self) -> str:
        """Get formatted plugin list"""
        plugins = self.core.plugin_manager.get_all_plugins()

        lines = []
        for plugin in plugins:
            status = "✅" if plugin.is_available() else "❌"
            lines.append(f"{status} {plugin.name}")

        return '\n'.join(lines)

    # ===== Proactive Notifications =====

    def notify(self, channel: str, message: str):
        """Send proactive notification to channel"""
        if not self.app:
            return

        try:
            self.app.client.chat_postMessage(
                channel=channel,
                text=message
            )
        except Exception as e:
            print(f"Error sending notification: {e}")

    def notify_user(self, user_id: str, message: str):
        """Send DM to user"""
        if not self.app:
            return

        try:
            # Open DM channel
            response = self.app.client.conversations_open(users=[user_id])
            channel = response['channel']['id']

            # Send message
            self.app.client.chat_postMessage(
                channel=channel,
                text=message
            )
        except Exception as e:
            print(f"Error sending DM: {e}")
