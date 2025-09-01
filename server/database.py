
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.models import Base


SQLITE_DATABASE_URL = "sqlite:///./test.db"

# check_same_thread - для SQLite в многопоточных приложениях
engine = create_engine(
    SQLITE_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def gget_db():
    
    #
    db = SessionLocal()
    try:
        
        yield db
    finally:
        
        db.close()


def create_tables():
   
    Base.metadata.create_all(bind=engine)