from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # Логин
    password = Column(String, nullable=False)  # Пароль
    telegram_id = Column(String, unique=True, nullable=True)  # Telegram ID

class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    inv_number = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(Integer, default=0)
    status = Column(String, default="На складе")
    employee_id = Column(Integer, ForeignKey('employees.id'))
