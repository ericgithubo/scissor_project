from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base

class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, nullable=False)
    long_url = Column(String, nullable=False)
    short_url = Column(String, unique=True, nullable=False)
    clicks = Column(Integer, default=0)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )

    click = relationship("Click", back_populates="url")


class Click(Base):
    __tablename__ = "clicks"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )
    url_id = Column(Integer, ForeignKey("urls.id"))

    url = relationship("URL", back_populates="click")


class Users(Base):
    __tablename__ = "my_users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String,unique=True)
    username = Column(String,unique=True)
    hashed_password =Column(String)
