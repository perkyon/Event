from database.setup import session
from utils.helpers import add_employee, assign_tool
from models import Employee, Inventory
import hashlib
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Приветствие с кнопками
async def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Войти", callback_data="login")],
        [InlineKeyboardButton("Просмотр инвентаря", callback_data="my_inventory")],
        [InlineKeyboardButton("Добавить сотрудника", callback_data="add_employee")],
        [InlineKeyboardButton("Назначить инструмент", callback_data="assign_tool")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Добро пожаловать в систему управления инвентарем! Выберите действие:",
        reply_markup=reply_markup
    )

# Обработчик нажатий кнопок
async def button_handler(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "login":
        await query.edit_message_text("Введите команду /login <логин> <пароль>")
    elif query.data == "my_inventory":
        await query.edit_message_text("Введите команду /my_inventory")
    elif query.data == "add_employee":
        await query.edit_message_text("Введите команду /add_employee <имя> <пароль>")
    elif query.data == "assign_tool":
        await query.edit_message_text("Введите команду /assign_tool <имя> <номер_инвентаря> <название> <количество>")

# Вход в систему
async def login(update, context):
    args = context.args
    if len(args) != 2:
        await update.message.reply_text("Использование: /login <логин> <пароль>")
        return

    login, password = args[0], args[1]

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    employee = session.query(Employee).filter_by(name=login, password=hashed_password).first()

    if not employee:
        await update.message.reply_text("Неверный логин или пароль.")
        return

    existing_employee = session.query(Employee).filter_by(telegram_id=str(update.effective_user.id)).first()
    if existing_employee and existing_employee.id != employee.id:
        await update.message.reply_text("Этот Telegram ID уже используется другим сотрудником.")
        return

    employee.telegram_id = str(update.effective_user.id)
    session.commit()

    await update.message.reply_text(f"Добро пожаловать, {login}!")

# Просмотр инвентаря
async def my_inventory(update, context):
    telegram_id = str(update.effective_user.id)
    employee = session.query(Employee).filter_by(telegram_id=telegram_id).first()

    if not employee:
        await update.message.reply_text("Вы не авторизованы. Используйте /login для входа.")
        return

    tools = session.query(Inventory).filter_by(employee_id=employee.id).all()
    if not tools:
        await update.message.reply_text("У вас нет назначенных инструментов.")
        return

    inventory_list = "\n".join(
        [f"{tool.inv_number} - {tool.name} (количество: {tool.quantity})" for tool in tools]
    )
    await update.message.reply_text(f"Ваш инвентарь:\n{inventory_list}")

# Добавление сотрудника
async def add_employee_command(update, context):
    args = context.args
    if len(args) != 2:
        await update.message.reply_text("Использование: /add_employee <имя> <пароль>")
        return

    name, password = args
    try:
        add_employee(name, password)
        await update.message.reply_text(f"Сотрудник {name} успешно добавлен.")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

# Назначение инструмента
async def assign_tool_command(update, context):
    args = context.args
    if len(args) < 3:
        await update.message.reply_text("Использование: /assign_tool <имя> <номер_инвентаря> <название> <количество>")
        return

    employee_name, inv_number, name = args[0], args[1], args[2]
    quantity = int(args[3]) if len(args) > 3 else 1

    try:
        assign_tool(employee_name, {"inv_number": inv_number, "name": name, "quantity": quantity})
        await update.message.reply_text(f"Инструмент {name} успешно назначен сотруднику {employee_name}.")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

from database.setup import session
from utils.helpers import add_employee, assign_tool, get_inventory, add_shift, get_shift_count
from models import Employee, Inventory
import hashlib
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# Стартовое меню
async def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Информация", callback_data="info")],
        [InlineKeyboardButton("Войти в программу", callback_data="login")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Добро пожаловать в систему управления инвентарем! Выберите действие:",
        reply_markup=reply_markup,
    )


# Вход в систему
async def login(update, context):
    args = context.args
    if len(args) != 2:
        await update.message.reply_text("Использование: /login <логин> <пароль>")
        return

    login, password = args[0], args[1]
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    employee = session.query(Employee).filter_by(name=login, password=hashed_password).first()

    if not employee:
        await update.message.reply_text("Неверный логин или пароль.")
        return

    employee.telegram_id = str(update.effective_user.id)
    session.commit()

    await post_login_menu(update)


# Меню после входа
async def post_login_menu(update):
    keyboard = [
        [InlineKeyboardButton("Просмотр инвентаря", callback_data="my_inventory")],
        [InlineKeyboardButton("Просмотр кол-ва смен", callback_data="shifts")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Вы вошли в систему! Выберите действие:",
        reply_markup=reply_markup,
    )


# Просмотр инвентаря
async def show_inventory(query, employee):
    tools = get_inventory(employee.id)
    if not tools:
        await query.edit_message_text("У вас нет назначенных инструментов.")
        return

    inventory_list = "\n".join(
        [f"{tool.inv_number} - {tool.name} (количество: {tool.quantity})" for tool in tools]
    )
    await query.edit_message_text(f"Ваш инвентарь:\n{inventory_list}")


# Меню для смен
async def show_shifts_menu(query, employee):
    shift_count = get_shift_count(employee.id)
    keyboard = [
        [InlineKeyboardButton("Добавить выход в смену", callback_data="add_shift")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        f"Вы вышли {shift_count} смен. Выберите действие:",
        reply_markup=reply_markup,
    )


# Добавление смены
async def add_shift_handler(query, employee):
    add_shift(employee.id)
    await query.edit_message_text("Выход в смену добавлен!")
