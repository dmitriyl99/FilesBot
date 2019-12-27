from filebot.models import BotUser
from typing import Optional, List


def add_user(telegram_id: int, first_name: str, last_name: str, username: str) -> BotUser:
    """
    Create a new user
    :param telegram_id: User Telegram Id
    :param first_name: User first name
    :param last_name: User last name
    :param username: User username
    """
    exist_user = get_user_by_telegram_id(telegram_id)
    if exist_user is None:
        exist_user = BotUser.objects.create(id=telegram_id, first_name=first_name, last_name=last_name, username=username)
    return exist_user


def get_user_by_telegram_id(telegram_id: int) -> Optional[BotUser]:
    try:
        return BotUser.objects.get(pk=telegram_id)
    except BotUser.DoesNotExist:
        return None


def get_all_users() -> List[BotUser]:
    return BotUser.objects.all()
