from database.setup import session
from models import Employee, Inventory, Shift
import hashlib
from datetime import datetime


# Добавить сотрудника
def add_employee(name, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    new_employee = Employee(name=name, password=hashed_password)
    session.add(new_employee)
    session.commit()


# Назначить инструмент сотруднику
def assign_tool(employee_name, tool_data):
    employee = session.query(Employee).filter_by(name=employee_name).first()
    if not employee:
        raise ValueError("Сотрудник не найден.")

    new_tool = Inventory(
        inv_number=tool_data["inv_number"],
        name=tool_data["name"],
        quantity=tool_data["quantity"],
        employee_id=employee.id,
    )
    session.add(new_tool)
    session.commit()


# Получить инвентарь сотрудника
def get_inventory(employee_id):
    return session.query(Inventory).filter_by(employee_id=employee_id).all()


# Добавить смену
def add_shift(employee_id):
    new_shift = Shift(employee_id=employee_id, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    session.add(new_shift)
    session.commit()


# Получить количество смен
def get_shift_count(employee_id):
    return session.query(Shift).filter_by(employee_id=employee_id).count()
