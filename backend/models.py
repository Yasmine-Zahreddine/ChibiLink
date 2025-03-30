from sqlalchemy import create_engine, Column, String, Integer, JSON, TIMESTAMP, text, ForeignKey, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy import Enum as SQLEnum

Base = declarative_base()

class ChibiLinkURLS(Base):
    __tablename__ = "chibilink_urls"
    url_pk = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), onupdate=text("now()"))
    original_url = Column(String, nullable=False, unique=True)
    short_code = Column(String, nullable=False, unique=True)
    clicks = Column(Integer, default=0, nullable=False)
    one_time_click = Column(Boolean, default=False, nullable=False)
    expiration_date = Column(TIMESTAMP(timezone=True), nullable=True)
    new_url = Column(String, nullable=False)