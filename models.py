from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Таблица сотрудников
class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    telegram_id = Column(String, unique=True)

    # Связь с инвентарем
    inventory = relationship("Inventory", back_populates="employee")
    shifts = relationship("Shift", back_populates="employee")


# Таблица инвентаря
class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)
    inv_number = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(Integer, default=0)
    employee_id = Column(Integer, ForeignKey('employees.id'))

    # Связь с сотрудником
    employee = relationship("Employee", back_populates="inventory")


# Таблица смен
class Shift(Base):
    __tablename__ = 'shifts'

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    date = Column(String, nullable=False)  # Можно заменить на datetime

    # Связь с сотрудником
    employee = relationship("Employee", back_populates="shifts")
