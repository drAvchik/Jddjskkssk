from bot.database.connection import Base, engine

print("Создаю таблицы в базе данных...")
Base.metadata.create_all(bind=engine)
print("✅ Таблицы успешно созданы!")
