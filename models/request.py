from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Enum, DateTime, func, text
from sqlalchemy.orm import relationship
from config.database import Base


class Request(Base):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True, index=True)
    status = Column(
        Enum('Pending', 'Accepted', 'Rejected', 'Completed', name='status_enum'),
        nullable=False,
        default='Pending'
    )
    requestor_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    buyer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    inflowDate = Column(DateTime, default=func.now())
    remark = Column(Boolean, default=False)
    delivery_date = Column(DateTime, default= func.dateadd(text('MONTH'), 1, func.getdate())
 )
    demand_PCS_not_DWG_related =Column(Integer, nullable=False)
    storageLocation = Column(String(255), nullable=False)
    departement =  Column(String(255), nullable=False)
    plant = Column(String(255), nullable=False)

    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    requestor = relationship('User', foreign_keys=[requestor_id], back_populates='requests_made')
    buyer = relationship('User', foreign_keys=[buyer_id], back_populates='requests_received')
    request_items = relationship('RequestItem', back_populates='request')
    


