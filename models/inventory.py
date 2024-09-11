from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship

from .base import Base
from .orders import WorkorderItem


class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    item_name = Column(String(255), nullable=False)
    sku = Column(String(255))
    manufacture = Column(String(255))
    quantity = Column(Integer, nullable=False)
    description = Column(String(1000))
    received_by_admin = Column(Boolean, default=False)
    length = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    active = Column(Boolean, default=True)
    workorder_items = relationship(WorkorderItem, back_populates="inventory_item")
    designer_id = Column(Integer, ForeignKey('designers.id'))
    designer = relationship("Designer", back_populates="inventories")
    cubic_sq_inches = Column(Float)
    cubic_sq_footage = Column(Float)
    in_storage = Column(Boolean, default=False)
    days_in_storage = Column(Integer, default=0)
    size = Column(String(255))
    weight = Column(Integer)
    ground_receive = Column(Integer)
    freight_receive = Column(Integer)
    assembled = Column(Integer, default=0)
    unpacked = Column(Integer, default=0)
    assembly_time = Column(Integer, default=0)
    photos = relationship('Photo', backref='inventory')

    def __init__(self, item_name, sku, manufacture, quantity, description, designer_id, length,
                 width, height, active, cubic_sq_inches, cubic_sq_footage, in_storage,
                 days_in_storage, size, weight, received_by_admin, ground_receive, freight_receive,
                 assembled, unpacked, assembly_time, photos=[]):
        self.item_name = item_name
        self.sku = sku
        self.manufacture = manufacture
        self.quantity = quantity
        self.description = description
        self.designer_id = designer_id
        self.length = length
        self.width = width
        self.height = height
        self.active = active
        self.cubic_sq_inches = cubic_sq_inches
        self.cubic_sq_footage = cubic_sq_footage
        self.in_storage = in_storage
        self.days_in_storage = days_in_storage
        self.size = size
        self.weight = weight
        self.received_by_admin = received_by_admin
        self.ground_receive = ground_receive
        self.freight_receive = freight_receive
        self.assembled = assembled
        self.unpacked = unpacked
        self.assembly_time = assembly_time
        self.photos = photos


class Photo(Base):
    __tablename__ = 'photo'
    id = Column(Integer, primary_key=True)
    url = Column(String(500))
    inventory_id = Column(Integer, ForeignKey('inventory.id'))
