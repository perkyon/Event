from telegram.ext import Application, CommandHandler
from config import TOKEN
from handlers.commands import login, my_inventory, start, add_employee_command, assign_tool_command

def main():
    app = Application.builder().token(TOKEN).build()

    # Регистрация обработчиков
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("login", login))
    app.add_handler(CommandHandler("my_inventory", my_inventory))
    app.add_handler(CommandHandler("add_employee", add_employee_command))  # Добавить сотрудника
    app.add_handler(CommandHandler("assign_tool", assign_tool_command))    # Назначить инструмент

    app.run_polling()

if __name__ == "__main__":
    main()
