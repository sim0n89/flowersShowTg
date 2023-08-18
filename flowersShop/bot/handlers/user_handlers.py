from aiogram import Router
from aiogram.filters import CommandStart, Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from handlers.states import UserStates
from keyboards import user_keyboards

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(
        text="Здравствуйте!\nК какому событию готовимся? "
        "Выберите один из вариантов, либо укажите свой.",
        reply_markup=user_keyboards.start_keyboard(),
    )
    user_id = int(message.from_user.id)
    await state.update_data(user_id=user_id)
    await state.set_state(UserStates.choosing_category)


@router.message(UserStates.choosing_category, Text(text=["Другой повод"]))
async def process_other_reason_category(message: Message, state: FSMContext):
    await message.answer(text="Напишите ваш повод, пожалуйста:")
    await state.set_state(UserStates.choosing_category)


@router.message(UserStates.choosing_category)
async def process_category_choosen(message: Message, state: FSMContext):
    category = message.text.lower().strip()
    await state.update_data(choosen_category=category)

    await message.answer(
        text="На какую сумму расчитываете?",
        reply_markup=user_keyboards.amount_keyboard(),
    )
    await state.set_state(UserStates.choosing_amount)


@router.message(UserStates.choosing_amount)
async def process_choosen_amount(message: Message, state: FSMContext):
    amount = message.text.lower().strip()
    await state.update_data(choosen_summ=amount)
    await message.answer(text="Фото букета в студию!")
    await state.set_state(UserStates.show_bouquet)


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
