from aiogram import Router
from aiogram.filters import CommandStart, Text
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from states import User_state
from keyboards.user_keyboards import start_keyboard, summ_keyboard, buy_keyboard
from pathlib import Path
from aiogram.types import InputFile
import os
router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(
        text="Здравствуйте!\nК какому событию готовимся? "
        "Выберите один из вариантов, либо укажите свой.",
        reply_markup=start_keyboard(),
    )
    await state.set_state(User_state.choosing_category)


@router.message(User_state.choosing_category)
async def category_choosen(message: Message, state: FSMContext):
    await state.update_data(choosen_category=message.text.lower())
   
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, выберите размер порции:",
        reply_markup=summ_keyboard()
    )
    await state.set_state(User_state.check_summ)


@router.message(User_state.check_summ) # не получается отправить фото
async def choosen_summ(message: Message, state: FSMContext):
    await state.update_data(choosen_summ=message.text.lower())
    root_dir = Path(__file__).parent.parent.parent
    image_path = os.path.join(root_dir, 'images', '101-gvozdika-jpg-1-1500x1500.jpg')
    with open (image_path, 'rb') as image:
        await message.answer_photo(
            photo=image,
            reply_markup=buy_keyboard()
        )
    data = await state.get_data()
    await state.set_state(User_state.check_summ)
    