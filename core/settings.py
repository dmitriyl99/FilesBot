"""
Bot settings manager
"""

from filebot.models import Settings


def get_settings():
    """
    Get bot settings
    """
    return Settings.objects.first()


def set_settings(share_text: str, share_file,
                 contacts_text: str, contacts_file,
                 start_message_text: str, start_message_file):
    """
    Edit bot settings
    """
    bot_settings = get_settings()
    if bot_settings is None:
        bot_settings = Settings()
    bot_settings.start_message_text = start_message_text
    bot_settings.contacts_text = contacts_text
    bot_settings.share_text = share_text
    bot_settings.save()
