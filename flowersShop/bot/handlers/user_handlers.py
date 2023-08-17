from aiogram import Router
from aiogram.filters import CommandStart, Text
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text="Здравствуйте!\nК какому событию готовимся? "
             "Выберите один из вариантов, либо укажите свой."
    )
    
    
