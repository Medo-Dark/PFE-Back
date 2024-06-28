from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, func
from sqlalchemy.orm import relationship
from config.database import Base

class PurchaseItem(Base):
    __tablename__ = 'purchase_items'
    purchase_id = Column(Integer, ForeignKey('purchases.id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)


    purchase = relationship('Purchase', back_populates='purchase_items')
    item = relationship('Item', back_populates='purchase_items')



class Purchase(Base):
    __tablename__ = 'purchases'
    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable=False)
    done = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

    supplier = relationship('Supplier', back_populates='purchases')
    buyer = relationship('User', back_populates='purchases')
    purchase_items = relationship('PurchaseItem', back_populates='purchase')
