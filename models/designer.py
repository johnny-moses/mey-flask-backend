from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Designer(Base):
    __tablename__ = 'designers'
    id = Column(Integer, primary_key=True)
    company = Column(String(56))
    abbreviation = Column(String(12))
    designer_name = Column(String(36), unique=True)
    email = Column(String(255))
    secondary_email = Column(String(255))
    phone = Column(String(50))
    workorders = relationship("Workorder", back_populates="designer")
    inventories = relationship("Inventory", back_populates="designer")

    def to_dict(self):
        return {
            'id': self.id,
            'designer_name': self.designer_name,
            'company': self.company,
            'abbreviation': self.abbreviation,
            'email': self.email,
            'phone': self.phone
        }


class Sidemark(Base):
    __tablename__ = 'sidemarks'
    id = Column(Integer, primary_key=True)
    designer_id = Column(Integer, ForeignKey('designers.id'))
    name = Column(String(255))
    designer = relationship('Designer')
    workorders = relationship("Workorder", back_populates="sidemark")
