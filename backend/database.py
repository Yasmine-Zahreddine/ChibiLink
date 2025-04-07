from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os 
from dotenv import load_dotenv
from logger import logger
import contextlib
import utils
import models 
from datetime import datetime
load_dotenv()

DB_PASS = os.getenv("DB_PASS")
DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")
DB_URl = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/postgres"

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
    try: 
        with session_manager(mainCall) as session:
            print("entering get_shortened_url")
            if utils.validate_url(url): 
                logger.info(f"Valid URL: {url}")
                existing_url = session.query(models.ChibiLinkURLS).filter(models.ChibiLinkURLS.original_url == url , models.ChibiLinkURLS.expiration_date > datetime.now()).first()
                if existing_url:
                    logger.info(f"URL already exists: {url}")
                    return existing_url.new_url
                short_code = utils.generate_short_code(url, length)
                new_url = f"{base_url}{short_code}"
                data = {
                    "original_url": url,
                    "short_code": short_code,
                    "new_url": new_url,
                    "clicks": 0,
                    "one_time_click": one_time_click,
                    "expiration_date": expiration_date, 
                }
                new_url_entry = models.ChibiLinkURLS.from_dict(data)
                logger.info(f"Creating new URL entry: {new_url}")
                try:
                    session.add(new_url_entry)
                    session.commit()
                except Exception as e:
                    logger.error(f"Error adding new URL entry: {e}")
                logger.info(f"New URL entry created: {new_url}")
                return new_url
            else:
                logger.error(f"Invalid URL: {url}")
                return None
    except Exception as e:
        logger.error(f"Error in get_shortened_url: {e}")
    

def get_original_url(short_code: str, mainCall: bool = True):
    with session_manager(mainCall) as session:
        url_entry = session.query(models.ChibiLinkURLS).filter(models.ChibiLinkURLS.short_code == short_code).first()
        if url_entry:
            if url_entry.one_time_click:
                session.delete(url_entry)
            return url_entry
        else:
            logger.info(f"Short code not found: {short_code}")
            return None


def delete_url_entry(url_pk:str):
    with session_manager() as session: 
        url_entry = session.query(models.ChibiLinkURLS).filter(models.ChibiLinkURLS.url_pk == url_pk).first()
        if url_entry: 
            session.delete(url_entry)
            session.commit()


def add_url_click(url_pk:str):
    with session_manager() as session: 
        url_entry = session.query(models.ChibiLinkURLS).filter(models.ChibiLinkURLS.url_pk == url_pk).first()
        if url_entry: 
            url_entry.clicks += 1
            session.commit()
            return url_entry
        return None