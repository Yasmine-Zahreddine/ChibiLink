from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os 
from dotenv import load_dotenv
import contextlib
load_dotenv()

DB_PASS = os.getenv("DB_PASS")
DB_URl = f"postgresql://postgres.beiomutcvymyddmivtjr:{DB_PASS}@aws-0-eu-central-1.pooler.supabase.com:5432/postgres"

engine = create_engine(DB_URl, pool_size=0)
Session = scoped_session(sessionmaker(bind=engine))
session = Session()

@contextlib.contextmanager
def session_manager(mainCall: bool = True):
    session = Session()
    try: 
        yield session
    except: 
        session.rollback()
        if not mainCall:
            raise
    finally:
        if mainCall:
            try: 
                session.commit()
            except:
                print("error in commit")
                app_logger.error("error in commit")


