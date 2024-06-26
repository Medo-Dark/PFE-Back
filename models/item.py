# app/models/item.py
from sqlalchemy import Boolean, Column, Enum, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base


class SupplierItem(Base):
    __tablename__ = 'supplier_items'
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    price = Column(Integer)


    supplier = relationship('Supplier', back_populates='supplier_items')
    item = relationship('Item', back_populates='supplier_items')



class RequestItem(Base):
    __tablename__ = 'request_items'
    request_id = Column(Integer, ForeignKey('requests.id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    quantity = Column(Integer, nullable=False)
    Purchase_state =  Column(Boolean, nullable=False, default=False)

    request = relationship('Request', back_populates='request_items')
    item = relationship('Item', back_populates='requests')
    




class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    part_number = Column(String(255), nullable=False, unique=True)
    isDrg = Column(Boolean, nullable=False, default=False)
    image = Column(String(255), nullable=True)
    DwgTitle =  Column(String(255), nullable=False)
    DWG_REV = Column(
        Enum('A', 'B', 'C', name='Rev_enum'),
        nullable=False
    )



    requests = relationship('RequestItem', back_populates='item')
    supplier_items = relationship('SupplierItem', back_populates='item')
    purchase_items = relationship('PurchaseItem', back_populates='item')




