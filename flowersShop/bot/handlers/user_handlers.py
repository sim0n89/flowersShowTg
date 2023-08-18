from aiogram import Router
from aiogram.filters import CommandStart, Text
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states import User_state
from keyboards.user_keyboards import start_keyboard, summ_keyboard, buy_keyboard
from pathlib import Path

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(
        text="Здравствуйте!\nК какому событию готовимся? "
        "Выберите один из вариантов, либо укажите свой.",
        reply_markup=start_keyboard(),
    )
    await state.set_state(User_state.make_order)


@router.message(User_state.make_order)
async def order_start(message: Message, state: FSMContext):
    await message.answer(
        text="Введите пожалуйста имя:",
    )
    await state.set_state(User_state.make_order_adress)


@router.message(User_state.make_order_adress)
async def name_entered(message: Message, state: FSMContext):
    await state.update_data(order_name=message.text)
    await message.answer(
        text="Введите адрес доставки:",
    )
    await state.set_state(User_state.make_order_date)

@router.message(User_state.make_order_date)
async def adress_entered(message: Message, state: FSMContext):
    await state.update_data(order_address=message.text)
    await message.answer(
        text="Введите дату доставки:",
    )
    await state.set_state(User_state.make_order_time)

@router.message(User_state.make_order_time)
async def date_entered(message: Message, state: FSMContext):
    await state.update_data(order_date=message.text)
    await message.answer(
        text="Введите время доставки:",
    )
    await state.set_state(User_state.make_order_success)


@router.message(User_state.make_order_success)
async def time_entered(message: Message, state: FSMContext):
    await state.update_data(order_time=message.text)
    order_data = await state.get_data()
    await message.answer(
        text="Поздравляем, ваш заказ оформлен! Скоро с Вами свяжется менеджер",
    )
    text_order = f"""
НОВЫЙ ЗАКАЗ
Имя: {order_data['order_name']}
Адрес доставки: {order_data['order_address']}
Дата доставки: {order_data['order_date']}
Время доставки: {order_data['order_time']}
"""
    





