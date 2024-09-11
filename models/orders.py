from datetime import datetime

from sqlalchemy import Column, Integer, String, Enum, Float, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship

from .base import Base


class Workorder(Base):
    __tablename__ = 'workorders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    workorder_id = Column(String(255), unique=True)
    designer_id = Column(Integer, ForeignKey('designers.id'))
    sidemark_id = Column(Integer, ForeignKey('sidemarks.id'))
    workorder_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum('pending', 'processing', 'completed'), default='pending')
    shipments = relationship("Shipment", back_populates="workorder")
    services_recorded = Column(Boolean, default=False)
    designer = relationship("Designer", back_populates="workorders")
    sidemark = relationship("Sidemark", back_populates="workorders")
    workorder_items = relationship("WorkorderItem", back_populates="workorder")
    active = Column(Boolean, default=True)
    email_sent = Column(Boolean, default=False)
    tagged = Column(Boolean, default=False)


class WorkorderItem(Base):
    __tablename__ = 'workorder_items'
    id = Column(Integer, primary_key=True)
    workorder_id = Column(Integer, ForeignKey('workorders.id'))
    inventory_id = Column(Integer, ForeignKey('inventory.id'))
    quantity = Column(Integer, nullable=False)
    assembly_time = Column(Integer)
    unpacked = Column(Integer, default=0)
    assembled = Column(Integer, default=0)
    total_fee = Column(Float)
    shipment_id = Column(Integer, ForeignKey('shipments.id'))
    workorder = relationship("Workorder", back_populates="workorder_items")
    inventory_item = relationship("Inventory", back_populates="workorder_items")

    def __init__(self, workorder_id, inventory_id, quantity, assembly_time=None,
                 unpacked=0, assembled=0, total_fee=0, shipment_id=None, shipment=None):
        self.workorder_id = workorder_id
        self.inventory_id = inventory_id
        self.quantity = quantity
        self.assembly_time = assembly_time
        self.unpacked = unpacked
        self.assembled = assembled
        self.total_fee = total_fee
        self.shipment = shipment
        self.shipment_id = shipment_id


# Class for grouping inventory that was received together for proper fee calculations
class Shipment(Base):
    __tablename__ = 'shipments'

    id = Column(Integer, primary_key=True)
    workorder_id = Column(Integer, ForeignKey('workorders.id'))
    workorder = relationship("Workorder", back_populates="shipments")
    receipt_date = Column(DateTime, default=datetime.utcnow)