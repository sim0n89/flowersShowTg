from aiogram import Bot, Router
from aiogram.filters import CommandStart, Text
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from handlers.states import UserStates
from keyboards import user_keyboards
from config_data.config import load_config
from database.database_sql_func import get_product, new_order
from pathlib import Path
import os
import datetime

router = Router()
config = load_config()
admin_ids = config.admins.ids

@router.message(UserStates.choose_category)
@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(
        text="Здравствуйте!\nК какому событию готовимся? "
        "Выберите один из вариантов, либо укажите свой.",
        reply_markup=user_keyboards.start_keyboard(),
    )

    user_id = int(message.from_user.id)
    await state.update_data(prods=[])
    await state.update_data(user_id=user_id)
    await state.set_state(UserStates.choosing_category)


@router.message(UserStates.choosing_category, Text(text=["Другой повод"]))
async def process_other_reason_category(message: Message, state: FSMContext):
    await message.answer(text="Напишите ваш повод, пожалуйста:")
    await state.set_state(UserStates.choosing_category)


@router.message(UserStates.choosing_category)
async def process_category_choosen(message: Message, state: FSMContext):
    category = message.text.strip()
    await state.update_data(choosen_category=category)
    await message.answer(
        text="На какую сумму расчитываете?",
        reply_markup=user_keyboards.amount_keyboard(),
    )
    await state.set_state(UserStates.choosing_amount)

@router.message(UserStates.show_bouquet , Text(text=["Посмотреть всю коллекцию"]))
@router.message(UserStates.choosing_amount)
async def process_choosen_amount(message: Message, state: FSMContext):
    if message.text.lower() != "посмотреть всю коллекцию":
        amount = message.text.lower().strip()
        await state.update_data(amount=amount)
    product_params = await state.get_data()
    choosen_category = product_params['choosen_category']
    showed_products = product_params['prods']
    amount = product_params['amount']
    product =  get_product(choosen_category, showed_products, amount)
    if (product):
        state_data = await state.get_data()
        state_data['prods'].append(product['id'])
        await state.update_data(prods=state_data['prods'])
        message_text = f"""
        <b>{product['name']}</b>
Цена: {product['price']}

{product['description']}
"""
        root_dir = Path(__file__).parent.parent.parent
        image_path = os.path.join(root_dir, product['image'])
        image = FSInputFile(image_path)
        print(image)
        await state.update_data(last_shown=product['id'])
        await state.update_data(last_shown_name=product['name'])
        await state.update_data(price=product['price'])
        await message.answer_photo(
            photo=image,
            caption=message_text,
            reply_markup=user_keyboards.buy_keyboard(),
            parse_mode="HTML"
        )
        await state.set_state(UserStates.show_bouquet)
        return
    else:
        await message.answer(
            text="Увы товаров по вашему запросу не нашлось, попробуйте изменить критерии поиска", reply_markup=user_keyboards.start_keyboard()
        )
        await state.set_state(UserStates.choosing_category)
        return


@router.message(UserStates.show_bouquet, Text(text=["Заказать букет"]))
async def order_start(message: Message, state: FSMContext):
    await message.answer(
        text="Введите пожалуйста имя:",
    )
    await state.set_state(UserStates.make_order_adress)


@router.message(UserStates.make_order_adress)
async def name_entered(message: Message, state: FSMContext):
    await state.update_data(order_name=message.text)
    await message.answer(
        text="Введите адрес доставки:",
    )
    await state.set_state(UserStates.make_order_date)


@router.message(UserStates.make_order_date)
async def adress_entered(message: Message, state: FSMContext):
    await state.update_data(order_address=message.text)
    await message.answer(
        text="Введите дату доставки:",
    )
    await state.set_state(UserStates.make_order_time)


@router.message(UserStates.make_order_time)
async def date_entered(message: Message, state: FSMContext):
    try:
        date = datetime.datetime.strptime(message.text, "%d.%m.%Y")
    except ValueError as e:
        await message.answer(text="Введите дату доставки в формате dd.mm.yy:")
        await state.set_state(UserStates.make_order_date)
        return
    
    await state.update_data(order_date=message.text)
    await message.answer(
        text="Введите время доставки:",
    )
    await state.set_state(UserStates.make_order_success)


@router.message(UserStates.make_order_success)
async def time_entered(message: Message, state: FSMContext, bot: Bot):
    try:
        date = datetime.datetime.strptime(message.text, "%H:%M")
    except ValueError as e:
        await message.answer(text="Введите время доставки в формате h:m")
        return
    await state.update_data(order_time=message.text)
    order_data = await state.get_data()
    await message.answer(
        text="Поздравляем, ваш заказ оформлен! Скоро с Вами свяжется менеджер",
    )
    text_order = f"""
НОВЫЙ ЗАКАЗ

Букет: {order_data['last_shown_name']}
Имя: {order_data['order_name']}
Адрес доставки: {order_data['order_address']}
Дата доставки: {order_data['order_date']}
Время доставки: {order_data['order_time']}
        """
    for id in admin_ids:
        await bot.send_message(chat_id=id, text=text_order)
    new_order(
        message.from_user.id, 
        order_data['last_shown'], 
        order_data['price'], 
        order_data['order_address'], 
        order_data['order_date'],
        order_data['order_time']
        )
    await state.clear()


@router.message(UserStates.show_bouquet, Text(text=["Заказать консультацию"]))
async def get_phone_consult(message: Message, state: FSMContext):
    await message.answer(
        text="Укажите ваш номер:",
    )
    await state.set_state(UserStates.send_consult)


@router.message(UserStates.send_consult)
async def time_entered(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(consult_phone=message.text)
    consult_data = await state.get_data()
    text = "В ближайшее время с вами свяжется наш флорист"
    await message.answer(
        text=text,
        reply_markup=user_keyboards.collection_keyboard()
    )
    text_consult = f"""
        Заявка на консультацию:

    Выбранная категория: {consult_data['choosen_category']}
    Стоимость: {consult_data['amount']}
    Номер для связи: {consult_data['consult_phone']}
    """

    for id in admin_ids:
        await bot.send_message(chat_id=id, text=text_consult)

    await state.set_state(UserStates.show_bouquet)
