from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.database.connection import db_session
from bot.database.models import User

router = Router()

# Состояние для FSM
class BroadcastState(StatesGroup):
    waiting_for_text = State()

@router.message(Command("broadcast"))
async def start_broadcast(message: types.Message, state: FSMContext):
    """Запрашивает у администратора текст для рассылки"""
    admin_id = 7064890315  # 🔹 Замени на свой Telegram ID
    if message.from_user.id != admin_id:
        return await message.answer("⛔ У вас нет доступа к этой команде!")

    await message.answer("📢 Отправьте текст для рассылки:")
    await state.set_state(BroadcastState.waiting_for_text)  # Устанавливаем состояние

@router.message(BroadcastState.waiting_for_text)
async def send_broadcast(message: types.Message, state: FSMContext):
    """Рассылает сообщение всем пользователям"""
    text = message.text

    with db_session() as session:
        users = session.query(User).all()

    count = 0
    for user in users:
        try:
            await message.bot.send_message(user.id, text)
            count += 1
        except Exception:
            pass  # Игнорируем ошибку, если пользователь заблокировал бота

    await message.answer(f"✅ Рассылка завершена! Сообщение отправлено {count} пользователям.")
    await state.clear()  # Сбрасываем состояние
