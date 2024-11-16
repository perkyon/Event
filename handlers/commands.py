from database.setup import session
from utils.helpers import add_employee, assign_tool
from models import Employee, Inventory
import hashlib

# Приветствие
async def start(update, context):
    await update.message.reply_text(
        "Добро пожаловать! Используйте /login <логин> <пароль> для входа."
    )

# Вход в систему
async def login(update, context):
    args = context.args
    if len(args) != 2:
        await update.message.reply_text("Использование: /login <логин> <пароль>")
        return

    login, password = args[0], args[1]

    # Хэшируем пароль
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Проверяем пользователя в базе данных
    employee = session.query(Employee).filter_by(name=login, password=hashed_password).first()

    if not employee:
        await update.message.reply_text("Неверный логин или пароль.")
        return

    # Привязываем Telegram ID
    employee.telegram_id = str(update.effective_user.id)
    session.commit()

    await update.message.reply_text(f"Добро пожаловать, {login}!")

# Просмотр инвентаря
async def my_inventory(update, context):
    telegram_id = str(update.effective_user.id)
    employee = session.query(Employee).filter_by(telegram_id=telegram_id).first()

    if not employee:
        await update.message.reply_text("Вы не авторизованы.")
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
