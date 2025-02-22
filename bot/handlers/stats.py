from aiogram import Router, types
from aiogram.filters import Command
from bot.database.connection import db_session
from bot.database.models import User
from datetime import datetime, timedelta

router = Router()

@router.message(Command("stats"))
async def bot_stats(message: types.Message):
    """Показывает статистику бота"""
    admin_id = 7064890315  # Замени на свой Telegram ID
    if message.from_user.id != admin_id:
        return await message.answer("⛔ У вас нет доступа к этой команде!")

    with db_session() as session:
        total_users = session.query(User).count()
        active_today = session.query(User).filter(User.last_active >= datetime.utcnow() - timedelta(days=1)).count()

    text = (
        f"📊 *Статистика бота:*\n\n"
        f"👥 Всего пользователей: {total_users}\n"
        f"📅 Активных за 24ч: {active_today}\n"
        f"💰 Баланс SMS: 5745.12₽ \n"
        f"💳 Баланс CryptoBot: 3200.78₽"
    )

    await message.answer(text, parse_mode="Markdown")
