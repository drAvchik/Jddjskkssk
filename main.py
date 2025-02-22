import asyncio
import locale
import structlog
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config import load_config
from config.generator import TextGenerator
from bot.handlers import get_all_routers
from bot.database.connection import db_session as get_db_session, Base, engine
from bot.database.models import User  # Убедись, что у тебя есть модель User
from bot.api import SMSActivateAPI, CryptoBotAPI, check_all_payments_system
from keep_alive import keep_alive  # Импортируем keep_alive

# Класс для работы с базой данных
class GlobalDatabase:
    @staticmethod
    def create_tables():
        """Создает таблицы в базе данных, если их нет"""
        Base.metadata.create_all(bind=engine)

    @staticmethod
    def get_total_users():
        """Получает общее количество пользователей в базе"""
        with get_db_session() as session:
            return session.query(User).count()

async def default_info(bot: Bot):
    """Функция получения информации о боте и настройке БД"""
    me = await bot.get_me()
    GlobalDatabase.create_tables()  # Создаем таблицы, если их нет
    bot.bot_username = me.username

    bot.logger.info(f'⚙️ [v{bot.config.version}] created by t.me/awixa')
    bot.logger.info(f'Starting bot: @{me.username}')

    # Получаем количество пользователей
    total_users = GlobalDatabase.get_total_users()
    bot.logger.info(f'Всего пользователей в боте: {total_users}')

    # Проверяем платежные системы
    if await check_all_payments_system(bot.logger, bot.config, bot.sms_activate, bot.crypto_bot) == False:
        await bot.sms_activate.close()
        await bot.crypto_bot.close()
        await bot.session.close()
        sys.exit(1)

async def main():
    """Основная функция запуска бота"""
    locale.setlocale(locale.LC_TIME, "C")  # Использование стандартной локали

    _config = load_config()
    logger = structlog.get_logger()
    dp = Dispatcher()
    bot = Bot(token=_config.bot_token, default=DefaultBotProperties(parse_mode=_config.messages_parse_mode))

    bot.textgen = TextGenerator(_config.messages_path)
    bot.sms_activate = SMSActivateAPI(_config.sms_activate_api_token, logger, bot)
    bot.crypto_bot = CryptoBotAPI(bot, _config, logger)
    bot.logger = logger
    bot.config = _config

    await default_info(bot)
    dp.include_routers(*get_all_routers(logger))
    await dp.start_polling(bot)

if __name__ == '__main__':
    keep_alive()  # Запускаем Flask-сервер для поддержки бота
    asyncio.run(main())  # Запускаем бота
