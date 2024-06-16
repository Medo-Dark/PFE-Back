from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import relationship
from config.database import Base


class Request(Base):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=False)
    status = Column(
        Enum('Pending', 'Accepted', 'Rejected', 'Completed', name='status_enum'),
        nullable=False,
        default='Pending'
    )
    requestor_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    buyer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    requestor = relationship('User', foreign_keys=[requestor_id], back_populates='requests_made')
    buyer = relationship('User', foreign_keys=[buyer_id], back_populates='requests_received')
    items = relationship('Item', back_populates='request', cascade='all, delete-orphan')


