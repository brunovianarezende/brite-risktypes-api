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
    attributes = relationship("AttributeType", back_populates="risk_type")
    instances = relationship("RiskTypeInstance", back_populates="risk_type")

class AttributeDataType(enum.Enum):
    INT = 1
    TEXT = 2
    DATE = 3
    ENUM = 4

class AttributeType(Base):
    __tablename__ = 'risk_type_attribute'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    data_type = Column(Enum(AttributeDataType), nullable=False)
    risk_type_id = Column(Integer, ForeignKey('risk_type.id'), nullable=False)
    risk_type = relationship("RiskType", back_populates="attributes")
    instances = relationship("AttributeInstance", back_populates="attribute_type")

    __mapper_args__ = {
        'polymorphic_on': data_type,
    }

class AttributeTypeInt(AttributeType):
    __mapper_args__ = {
        'polymorphic_identity': AttributeDataType.INT
    }

class AttributeTypeText(AttributeType):
    __mapper_args__ = {
        'polymorphic_identity': AttributeDataType.TEXT
    }

class AttributeTypeDate(AttributeType):
    __mapper_args__ = {
        'polymorphic_identity': AttributeDataType.DATE
    }

class AttributeTypeEnum(AttributeType):
    allowed_values = relationship("AttributeTypeEnumValue", back_populates="enum_type")

    __mapper_args__ = {
        'polymorphic_identity': AttributeDataType.ENUM
    }

class AttributeTypeEnumValue(Base):
    __tablename__ = 'risk_type_attribute_enum_value'

    id = Column(Integer, primary_key=True)
    value = Column(String, nullable=False)
    enum_type_id = Column(Integer, ForeignKey('risk_type_attribute.id'), nullable=False)
    enum_type = relationship("AttributeTypeEnum", back_populates="allowed_values")

class RiskTypeInstance(Base):
    __tablename__ = 'risk_type_instance'

    id = Column(Integer, primary_key=True)
    risk_type_id = Column(Integer, ForeignKey('risk_type.id'), nullable=False)
    risk_type = relationship("RiskType", back_populates="instances")
    attributes_instances = relationship("AttributeInstance", back_populates="risk_type_instance")

class AttributeInstance(Base):
    __tablename__ = 'risk_type_attribute_instance'

    id = Column(Integer, primary_key=True)
    attribute_data_type = Column(Enum(AttributeDataType), nullable=False)
    attribute_type_id = Column(Integer, ForeignKey('risk_type_attribute.id'), nullable=False)
    attribute_type = relationship("AttributeType", back_populates="instances")
    risk_type_instance_id = Column(Integer, ForeignKey('risk_type_instance.id'), nullable=False)
    risk_type_instance = relationship("RiskTypeInstance", back_populates="attributes_instances")

    __mapper_args__ = {
        'polymorphic_on': attribute_data_type,
    }

class AttributeInstanceInt(AttributeInstance):
    int_value = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': AttributeDataType.INT
    }

class AttributeInstanceText(AttributeInstance):
    text_value = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': AttributeDataType.TEXT
    }

class AttributeInstanceDate(AttributeInstance):
    date_value = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': AttributeDataType.DATE
    }

class AttributeInstanceEnum(AttributeInstance):
    enum_value = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': AttributeDataType.ENUM
    }