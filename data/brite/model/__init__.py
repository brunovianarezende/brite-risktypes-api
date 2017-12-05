import enum

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

Base = declarative_base()

class RiskType(Base):
    __tablename__ = 'risk_type'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    attributes = relationship("RiskTypeAttribute", back_populates="risk_type")
    instances = relationship("RiskTypeInstance", back_populates="risk_type")

class RiskTypeAttributeDataType(enum.Enum):
    INT = 1
    TEXT = 2
    DATE = 3
    ENUM = 4

class RiskTypeAttribute(Base):
    __tablename__ = 'risk_type_attribute'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    data_type = Column(Enum(RiskTypeAttributeDataType), nullable=False)
    risk_type_id = Column(Integer, ForeignKey('risk_type.id'), nullable=False)
    risk_type = relationship("RiskType", back_populates="attributes")
    instances = relationship("RiskTypeAttributeInstance", back_populates="attribute_type")

class RiskTypeInstance(Base):
    __tablename__ = 'risk_type_instance'

    id = Column(Integer, primary_key=True)
    risk_type_id = Column(Integer, ForeignKey('risk_type.id'), nullable=False)
    risk_type = relationship("RiskType", back_populates="instances")
    attributes_instances = relationship("RiskTypeAttributeInstance", back_populates="risk_type_instance")

class RiskTypeAttributeInstance(Base):
    __tablename__ = 'risk_type_attribute_instance'

    id = Column(Integer, primary_key=True)
    attribute_type_id = Column(Integer, ForeignKey('risk_type_attribute.id'), nullable=False)
    attribute_type = relationship("RiskTypeAttribute", back_populates="instances")
    risk_type_instance_id = Column(Integer, ForeignKey('risk_type_instance.id'), nullable=False)
    risk_type_instance = relationship("RiskTypeInstance", back_populates="attributes_instances")
    value = Column(Integer)
