from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///orm.sqlite', echo=False)

Base = declarative_base()


class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    news = Column(String)
    time = Column(String)
    link = Column(String)
    tag_id = Column(Integer, ForeignKey('tag.id'))

    def __init__(self, news, time, link, tag_id):
        self.news = news
        self.time = time
        self.link = link
        self.tag_id = tag_id

    def __str__(self):
        return f'{self.news} {self.time} {self.link} {self.tag_id}'


class Tags(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    tag = Column(String, unique=True)

    def __init__(self, tag):
        self.tag = tag

    def __str__(self):
        return self.tag


# Создание таблицы
Base.metadata.create_all(engine)

# Заполняем таблицы
Session = sessionmaker(bind=engine)

# create a Session
session = Session()

# Теги
session.add_all([Tags('life'), Tags('work')])

session.commit()


news = News('Упал ноль', '14:01', 'vk.com', 1)

# Добавление данных
session.add(news)

session.commit()

# Выборка данных
# 1. Все новости, которые есть в базе
news = session.query(News).all()
# Класс запроса
print(type(news))

for i in news:
    print(i)
