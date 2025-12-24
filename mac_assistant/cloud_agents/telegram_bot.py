"""
Telegram Bot Agent
Control your Mac from anywhere via Telegram
"""

import os
import threading
from typing import Optional, Callable


class TelegramBotAgent:
    """Telegram bot for remote control"""

    def __init__(self, core, token: Optional[str] = None):
        self.core = core
        self.token = token or os.getenv('TELEGRAM_BOT_TOKEN')

        self.bot = None
        self.running = False

        if not self.token:
            print("⚠️  TELEGRAM_BOT_TOKEN not set. Bot disabled.")
            return

        self._init_bot()

    def _init_bot(self):
        """Initialize Telegram bot"""
        try:
            # Try to import python-telegram-bot
            import telegram
            from telegram.ext import Application, CommandHandler, MessageHandler, filters

            self.telegram = telegram
            self.Application = Application
            self.CommandHandler = CommandHandler
            self.MessageHandler = MessageHandler
            self.filters = filters
            self.available = True

            print("✓ Telegram bot initialized")

        except ImportError:
            print("⚠️  python-telegram-bot not installed.")
            print("   Run: pip install python-telegram-bot")
            self.available = False

    def start(self):
        """Start the Telegram bot"""
        if not self.available:
            return False

        if self.running:
            return True

        print("🤖 Starting Telegram bot...")

        # Start bot in background thread
        threading.Thread(target=self._run_bot, daemon=True).start()
        self.running = True

        return True

    def stop(self):
        """Stop the Telegram bot"""
        self.running = False
        print("🤖 Telegram bot stopped")

    def _run_bot(self):
        """Run bot (in thread)"""
        try:
            # Create application
            app = self.Application.builder().token(self.token).build()

            # Register handlers
            app.add_handler(self.CommandHandler("start", self._cmd_start))
            app.add_handler(self.CommandHandler("help", self._cmd_help))
            app.add_handler(self.CommandHandler("status", self._cmd_status))
            app.add_handler(self.CommandHandler("email", self._cmd_email))
            app.add_handler(self.CommandHandler("messages", self._cmd_messages))
            app.add_handler(self.CommandHandler("photos", self._cmd_photos))
            app.add_handler(self.CommandHandler("tasks", self._cmd_tasks))

            # Message handler for natural language
            app.add_handler(self.MessageHandler(
                self.filters.TEXT & ~self.filters.COMMAND,
                self._handle_message
            ))

            # Run bot
            app.run_polling()

        except Exception as e:
            print(f"Error running Telegram bot: {e}")

    # ===== Command Handlers =====

    async def _cmd_start(self, update, context):
        """Handle /start command"""
        welcome = """
🤖 **Mac Remote Assistant Bot**

Willkommen! Steuere deinen Mac von überall!

**Befehle:**
/status - System-Status
/email - E-Mails prüfen
/messages - Nachrichten
/photos - Fotos suchen
/tasks - Aufgaben ausführen
/help - Hilfe

**Oder schreib einfach was du willst:**
"Was habe ich heute gemacht?"
"Sende E-Mail an Max"
"Zeige Fotos von heute"
        """
        await update.message.reply_text(welcome, parse_mode='Markdown')

    async def _cmd_help(self, update, context):
        """Handle /help command"""
        help_text = """
📚 **Hilfe**

**Befehle:**
• `/status` - System-Status & Plugins
• `/email` - Ungelesene E-Mails
• `/messages` - Neue Nachrichten
• `/photos [suche]` - Fotos suchen
• `/tasks [befehl]` - Task ausführen

**Natural Language:**
Schreib einfach was du willst!

Beispiele:
• "Was habe ich heute gemacht?"
• "Sende E-Mail an max@example.com"
• "Suche Fotos vom Strand"
• "Status"
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def _cmd_status(self, update, context):
        """Handle /status command"""
        try:
            plugins = len(self.core.plugin_manager.get_available_plugins())
            ai_status = "✅ Aktiv" if self.core.ai_enabled else "❌ Inaktiv"

            status = f"""
📊 **System-Status**

**Plugins:** {plugins} verfügbar
**KI:** {ai_status}
**Autonomer Agent:** {'✅ Läuft' if hasattr(self.core, 'autonomous_agent') else '❌ Aus'}

**Verfügbare Apps:**
{self._get_plugin_list()}
            """
            await update.message.reply_text(status, parse_mode='Markdown')

        except Exception as e:
            await update.message.reply_text(f"❌ Fehler: {str(e)}")

    async def _cmd_email(self, update, context):
        """Handle /email command"""
        await update.message.reply_text("📧 Prüfe E-Mails...")

        try:
            mail_plugin = self.core.get_plugin('Mail')
            if mail_plugin and mail_plugin.is_available():
                emails = mail_plugin.get_unread_emails(5)

                response = f"📧 **E-Mails:**\n\n{emails}"
                await update.message.reply_text(response)
            else:
                await update.message.reply_text("❌ Mail-Plugin nicht verfügbar")

        except Exception as e:
            await update.message.reply_text(f"❌ Fehler: {str(e)}")

    async def _cmd_messages(self, update, context):
        """Handle /messages command"""
        await update.message.reply_text("💬 Prüfe Nachrichten...")

        try:
            all_messages = self.core.get_all_messages(limit=5)

            response = "💬 **Nachrichten:**\n\n"
            for app, messages in all_messages.items():
                response += f"**{app}:**\n{messages}\n\n"

            await update.message.reply_text(response)

        except Exception as e:
            await update.message.reply_text(f"❌ Fehler: {str(e)}")

    async def _cmd_photos(self, update, context):
        """Handle /photos command"""
        search_term = ' '.join(context.args) if context.args else 'recent'

        await update.message.reply_text(f"📸 Suche Fotos: {search_term}...")

        try:
            photos_plugin = self.core.get_plugin('Photos')
            if photos_plugin and photos_plugin.is_available():
                if search_term == 'recent':
                    photos = photos_plugin.get_recent_media(days=7)
                else:
                    photos = photos_plugin.search(search_term)

                response = f"📸 **Fotos:**\n\n{photos}"
                await update.message.reply_text(response)
            else:
                await update.message.reply_text("❌ Photos-Plugin nicht verfügbar")

        except Exception as e:
            await update.message.reply_text(f"❌ Fehler: {str(e)}")

    async def _cmd_tasks(self, update, context):
        """Handle /tasks command"""
        if not context.args:
            await update.message.reply_text("💡 Usage: /tasks <befehl>\nBeispiel: /tasks Sende E-Mail an Max")
            return

        task = ' '.join(context.args)
        await update.message.reply_text(f"⚡ Führe aus: {task}...")

        try:
            result = self.core.execute_task(task)

            if result.get('success'):
                await update.message.reply_text(f"✅ Erledigt!\n\n{result.get('result', '')}")
            else:
                await update.message.reply_text(f"❌ Fehler: {result.get('error', '')}")

        except Exception as e:
            await update.message.reply_text(f"❌ Fehler: {str(e)}")

    async def _handle_message(self, update, context):
        """Handle natural language messages"""
        message = update.message.text

        await update.message.reply_text("🤖 Verarbeite...")

        try:
            # Process with core
            response = self.core.process_user_query(message)

            # Send response
            await update.message.reply_text(response)

        except Exception as e:
            await update.message.reply_text(f"❌ Fehler: {str(e)}")

    def _get_plugin_list(self) -> str:
        """Get formatted plugin list"""
        plugins = self.core.plugin_manager.get_all_plugins()

        lines = []
        for plugin in plugins:
            status = "✅" if plugin.is_available() else "❌"
            lines.append(f"{status} {plugin.name}")

        return '\n'.join(lines)

    # ===== Proactive Notifications =====

    async def notify(self, chat_id: int, message: str):
        """Send proactive notification to user"""
        if not self.bot:
            return

        try:
            await self.bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            print(f"Error sending notification: {e}")

    async def notify_all(self, message: str):
        """Send notification to all users"""
        # Would need to track user IDs
        pass
