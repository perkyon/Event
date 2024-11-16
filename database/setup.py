from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine("sqlite:///inventory.db")

# Создаём таблицы, если их ещё нет
Base.metadata.create_all(engine)

# Настройка сессии
Session = sessionmaker(bind=engine)
session = Session()
