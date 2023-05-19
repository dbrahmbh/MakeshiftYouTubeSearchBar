from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

#Creates an engine for the database using sqlite and stores it in a file named youtube.sqlite
engine = create_engine('sqlite:///youtube.sqlite')

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False))

Base = declarative_base()
Base.query = db_session.query_property()

# Creates database
def init_db():
    
    from youtube_classes import Settings, Search, Video

    initialSettings = Settings()

    # Imports YouTube classes that represent tables in the database and then creates all of the tables
    Base.metadata.create_all(bind=engine)

    # save the database
    db_session.commit()
