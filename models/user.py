from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, func
from sqlalchemy.orm import relationship
from config.database import Base
from models.request import Request

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    role = Column(
        Enum('Buyer', 'Requestor', 'Admin', name='roles_enum'),
        nullable=False
    )
    commodity = Column(
        Enum('Spare Parts', 'Opex', 'Capex', name='commo_enum'),
        nullable=True
    )
    account_status = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    requests_made = relationship('Request', foreign_keys=Request.requestor_id, back_populates='requestor')
    requests_received = relationship('Request', foreign_keys=Request.buyer_id, back_populates='buyer')
    purchases = relationship('Purchase', back_populates='buyer')
