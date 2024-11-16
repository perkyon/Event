from database.setup import session
from models import Employee, Inventory
import hashlib

# Добавление нового сотрудника
def add_employee(name, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    new_employee = Employee(name=name, password=hashed_password)
    session.add(new_employee)
    session.commit()
    print(f"Сотрудник {name} успешно добавлен.")

# Добавление инструмента сотруднику
def assign_tool(employee_name, tool_data):
    employee = session.query(Employee).filter_by(name=employee_name).first()
    if not employee:
        raise ValueError(f"Сотрудник с именем {employee_name} не найден.")

    new_tool = Inventory(
        inv_number=tool_data["inv_number"],
        name=tool_data["name"],
        quantity=tool_data["quantity"],
        employee_id=employee.id
    )
    session.add(new_tool)
    session.commit()
    print(f"Инструмент {tool_data['name']} успешно назначен сотруднику {employee_name}.")
