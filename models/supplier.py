from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from config.database import Base


class Supplier(Base):
    __tablename__ = 'suppliers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    contact_info = Column(String(1024), nullable=True)
    supplier_items = relationship('SupplierItem', back_populates='supplier')
    purchases = relationship('Purchase', back_populates='supplier')


