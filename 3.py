from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

engine = create_engine('sqlite:///orm.sqlite', echo=False)

Base = declarative_base()

# Таблица-связка многие-ко-многим без собственного id
vacancyskill = Table('vacancyskill', Base.metadata,
                     Column('vacancy_id', Integer, ForeignKey('vacancy.id'), primary_key=True),
                     Column('skill_id', Integer, ForeignKey('skill.id'), primary_key=True)
                     )

class Skill(Base):
    __tablename__ = 'skill'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    vacancies = relationship('Vacancy', secondary=vacancyskill, back_populates='skills')

    def __repr__(self):
        return f"<Skill(id={self.id}, name='{self.name}')>"

class Region(Base):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    number = Column(Integer, nullable=True)

    vacancies = relationship('Vacancy', back_populates='region')

    def __repr__(self):
        return f"<Region(id={self.id}, name='{self.name}', number={self.number})>"

class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    region_id = Column(Integer, ForeignKey('region.id'))

    region = relationship('Region', back_populates='vacancies')
    skills = relationship('Skill', secondary=vacancyskill, back_populates='vacancies')

    def __repr__(self):
        return f"<Vacancy(id={self.id}, name='{self.name}', region_id={self.region_id})>"

# Создаем таблицы
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Добавляем регионы
session.add_all([Region(name='Москва', number=0), Region(name='Питер', number=78)])

# Добавляем скилы
session.add_all([Skill(name='python'), Skill(name='java')])

session.commit()

# Создаем вакансии в регионах
regions = session.query(Region).all()
for region in regions:
    vacancy = Vacancy(name='какое то название', region=region)
    session.add(vacancy)

session.commit()

# Пример выборки региона Москва
moscow = session.query(Region).filter_by(name='Москва').first()
print(moscow)

# Вакансии для Москвы
vacancies = session.query(Vacancy).filter_by(region_id=moscow.id).all()
print(len(vacancies))
print(vacancies[0])

# Пример добавления навыков к вакансии
vacancies[0].skills.append(session.query(Skill).filter_by(name='python').first())
session.commit()

print(vacancies[0].skills)  # Навыки вакансии
