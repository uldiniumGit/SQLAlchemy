from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

engine = create_engine('sqlite:///orm.sqlite', echo=False)

Base = declarative_base()

class Tag(Base):
    __tablename__ = 'tags'  # обычно таблицы во множественном числе
    id = Column(Integer, primary_key=True)
    tag = Column(String, unique=True)

    # связь к новостям
    news = relationship('News', back_populates='tag')

    def __repr__(self):
        return f"<Tag(id={self.id}, tag='{self.tag}')>"


class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    news = Column(String)
    time = Column(String)
    link = Column(String)
    tag_id = Column(Integer, ForeignKey('tags.id'))

    tag = relationship('Tag', back_populates='news')

    def __repr__(self):
        return f"<News(id={self.id}, news='{self.news}', time='{self.time}', link='{self.link}', tag_id={self.tag_id})>"


# Создаем таблицы в базе
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Добавим теги
tag_life = Tag(tag='life')
tag_work = Tag(tag='work')

session.add_all([tag_life, tag_work])
session.commit()

# Добавим новость, связав с тегом
news_item = News(news='Упал ноль', time='14:01', link='vk.com', tag_id=tag_life.id)
session.add(news_item)
session.commit()

# Получаем все новости
all_news = session.query(News).all()
print(type(all_news))  # <class 'list'>

for news in all_news:
    print(news)
    print(f"Тег новости: {news.tag}")  # благодаря relationship можно получить объект тега
