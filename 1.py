from sqlalchemy.orm import sessionmaker

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Создаем новых пользователей
user1 = User('alice', 'Alice Wonderland', 'password123')
user2 = User('bob', 'Bob Builder', 'secure456')

# Добавляем пользователей в сессию
session.add(user1)
session.add(user2)

# Фиксируем изменения в базе
session.commit()

# Выбираем всех пользователей
users = session.query(User).all()
for user in users:
    print(user)
