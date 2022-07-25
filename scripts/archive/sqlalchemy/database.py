from datetime import datetime
from sqlalchemy.orm import declarative_base, session_maker
from sqlalchemy import Column, String, DateTime, Integer, create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(32),nullable=False,unique=False)
    email = Column(String(64),unique=True,nullable=False)
    regdate = Column(DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'User(name: {self.username}, id: {self.id})'

engine = create_engine('sqlite:///users.db',echo=True)
Base.metadata.create_all(bind=engine)
Session = session_maker(bind=engine)

with Session() as db:
    user = User()
    user.id = 12
    user.username = 'Checkmate'
    user.email = 'User@mail.com'

    db.add(user)