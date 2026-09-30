"""
Общие настройки, которые нужны и боту, и API (чтобы не дублировать списки).
Всё, что можно менять без правки кода, берётся из переменных окружения.
"""
import os

# Админы бота (доступ к /admin и обход проверки подписки). Во время техработ в мини-апп они НЕ проходят — см. MAINTENANCE_WHITELIST.
ADMIN_USERNAMES = ["Richie", "boros", "onewino"]

# Кто может заходить в мини-апп, когда включены технические работы. ТОЛЬКО эти двое —
# остальные (включая других админов бота) видят экран «Технические работы».
# Список зашит в код намеренно: от переменных окружения на хостинге он не зависит.
MAINTENANCE_WHITELIST = ["Richie", "Boros"]

# Обязательная подписка на канал.
# REQUIRED_CHANNEL — @username канала или числовой id (-100...). Бот должен быть АДМИНОМ канала,
# иначе Telegram не даст проверить подписчиков. Пока переменная пуста — проверка выключена.
REQUIRED_CHANNEL = os.getenv("REQUIRED_CHANNEL", "").strip()
CHANNEL_SUB_URL = os.getenv("CHANNEL_SUB_URL", "https://catup.lol/casino").strip()
# Как канал назван на экране «НЕОБХОДИМО ПОДПИСАТЬСЯ НА КАНАЛ …!» в мини-аппе.
CHANNEL_LABEL = os.getenv("CHANNEL_LABEL", "@casino").strip() or "@casino"
# Как часто (сек) бот сверяет подписчиков, если Telegram не прислал событие об отписке.
SUB_WATCH_INTERVAL = int(os.getenv("SUB_WATCH_INTERVAL", "300") or 300)

# Адрес Bot API (бот работает через свой сервер bot.catup.lol)
TELEGRAM_API_BASE = os.getenv("TELEGRAM_API_BASE", "https://bot.catup.lol").rstrip("/")


def _norm(username) -> str:
    return (username or "").strip().lstrip("@").lower()


def is_admin_username(username) -> bool:
    return _norm(username) in {_norm(u) for u in ADMIN_USERNAMES}


def is_maintenance_whitelisted(username) -> bool:
    return _norm(username) in {_norm(u) for u in MAINTENANCE_WHITELIST}
