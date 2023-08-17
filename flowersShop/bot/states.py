from aiogram.fsm.state import State, StatesGroup


class User_state(StatesGroup):
    choosing_category = State()  # выбор категории
    set_new_reason = State()  # новый повод
    check_summ = State()  # выбор суммы товара
    show_product = State()  # показать товар

    make_order = State()  # перейти к оформлению ввести имя имя
    make_order_adress = State()  # ввести адрес
    make_order_date = State()  # ввести дату
    make_order_time = State()  # ввести время
    make_order_success = State()  # заказ оформлен

    order_consult = State()  # заказ консультации,
    send_consult = State()  # ввод номера телефона, отправка сообщения менеджеру

