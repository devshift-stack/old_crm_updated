"""Cloud agents module"""
from .telegram_bot import TelegramBotAgent
from .slack_bot import SlackBotAgent
from .web_server import WebServerAgent
from .cloud_sync import CloudSyncAgent

__all__ = ['TelegramBotAgent', 'SlackBotAgent', 'WebServerAgent', 'CloudSyncAgent']
