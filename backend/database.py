from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os 
from dotenv import load_dotenv
from logger import logger
import contextlib
from utils import generate_short_code, validate_url
from models import ChibiLinkURLS
from datetime import datetime
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
                logger.error("error in commit")


def get_shortened_url(url:str, base_url: str, expiration_date , one_time_click: bool = False, length: int = None, mainCall: bool = True):
    with session_manager(mainCall) as session:
        if validate_url(url): 
            existing_url = session.query(ChibiLinkURLS).filter(ChibiLinkURLS.original_url == url , ChibiLinkURLS.expiration_date > datetime.now()).first()
            if existing_url:
                logger.info(f"URL already exists: {url}")
                return existing_url.new_url
            short_code = generate_short_code(url, length)
            new_url = f"{base_url}/{short_code}"
            data = {
                "original_url": url,
                "short_code": short_code,
                "new_url": new_url,
                "clicks": 0,
                "one_time_click": one_time_click,
                "expiration_date": expiration_date, 
            }
            new_url_entry = ChibiLinkURLS.from_dict(data)
            session.add(new_url_entry)
            session.commit()
        return new_url
    

def get_original_url(short_code: str, mainCall: bool = True):
    with session_manager(mainCall) as session:
        url_entry = session.query(ChibiLinkURLS).filter(ChibiLinkURLS.short_code == short_code).first()
        if url_entry:
            if url_entry.one_time_click:
                session.delete(url_entry)
            return url_entry.original_url
        else:
            logger.info(f"Short code not found: {short_code}")
            return None

