from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///orm.sqlite', echo=False)

Base = declarative_base()


class Region(Base):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    number = Column(Integer, nullable=True)

    # note = Column(String, nullable=True)

    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __str__(self):
        return f'{self.id}) {self.name}: {self.number}'


# Создание таблицы
Base.metadata.create_all(engine)

# Создание сессии
# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()

# region = Region('Москва', 1)
#
# # Добавление данных
# session.add(region)
#
# region = Region('Питер', 78)
#
# # Добавление данных
# session.add(region)
#
# session.commit()
#
#
# # Изменение данных
# region.name = 'Тула'
#
# session.commit()
#
# # Удаление данных
# session.delete(region)
# session.commit()
#
# for i in range(10):
#     region = Region(f'region {i}', i)
#     session.add(region)
#
# session.commit()
#

# Выборка данных
# 1. Все регионы, которые есть в базе
regions = session.query(Region).all()
# Класс запроса
print(type(regions))

for region in regions:
    print(region)


# Запрос с условием
regions = session.query(Region).filter(Region.name == 'Москва' and Region.id > 0).all()
print(type(regions))

for region in regions:
    print(region)
