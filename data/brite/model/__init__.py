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

    def __repr__(self):
        return "<RiskType(name='%s', description='%s')>" % (
                            self.name, self.description)

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

    def __repr__(self):
        return "<RiskTypeAttribute(name='%s', data_type='%s')>" % (
                            self.name, self.data_type)
