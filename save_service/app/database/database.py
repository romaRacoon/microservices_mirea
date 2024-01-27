from sqlalchemy import create_engine, String, UUID, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL = 'postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/query'

engine = create_engine(URL)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()


class DBDoc(Base):
    __tablename__ = 'documents_artemenkov'

    id = Column(UUID(as_uuid=True), primary_key=True)
    owner_id = Column(UUID)
    title = Column(String)
    body = Column(String)