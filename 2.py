from sqlalchemy import Column, Integer, String, create_engine, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///orm.sqlite', echo=False)
Base = declarative_base()

class Region(Base):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    number = Column(Integer, nullable=True)

    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __str__(self):
        return f'{self.id}) {self.name}: {self.number}'

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Пример выборки с условием
regions = session.query(Region).filter(
    and_(Region.name == 'Москва', Region.id > 0)
).all()

print(type(regions))
for region in regions:
    print(region)

