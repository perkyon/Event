from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Укажите путь к базе данных SQLite
DATABASE_URL = "sqlite:///inventory.db"

# Создаем подключение к базе данных
engine = create_engine(DATABASE_URL)

# Создаем таблицы (если их еще нет)
Base.metadata.create_all(engine)

# Создаем сессию для взаимодействия с базой
Session = sessionmaker(bind=engine)
session = Session()
