import unittest
import datetime
from decimal import Decimal

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from brite.model import Base
from brite.model import RiskType, RiskTypeInstance
from brite.model import AttributeType, AttributeDataType,\
    AttributeTypeInt, AttributeTypeText, AttributeTypeDate, AttributeTypeEnum,\
    AttributeTypeEnumValue, AttributeTypeNumeric
from brite.model import AttributeInstanceInt, AttributeInstanceText,\
    AttributeInstanceDate, AttributeInstanceEnum, AttributeInstanceNumeric

class TestRawRiskTypeModel(unittest.TestCase):
    def setUp(self):
        # make sure each test starts with a clean database
        engine = create_engine('sqlite:///:memory:', echo=True)
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

    def test_add_new_risk_type(self):
        session = self.Session()
        risk_type = RiskType(name='Golf prize')
        session.add(risk_type)
        session.commit()
        found_risk_type = session.query(RiskType).filter_by(name='Golf prize').first() 
        assert risk_type == found_risk_type
        assert found_risk_type.id is not None

    def test_add_new_risk_type_attribute(self):
        session = self.Session()
        risk_type = RiskType(name='Golf prize')
        session.add(risk_type)
        prize_value = AttributeType(name='Value', data_type=AttributeDataType.INT, risk_type=risk_type)
        session.add(prize_value)
        session.commit()
        found_risk_type = session.query(RiskType).filter_by(name='Golf prize').first()
        found_risk_type_attribute = session.query(AttributeType).filter_by(name='Value').first()
        assert found_risk_type_attribute.risk_type == risk_type
        assert found_risk_type.attributes == [prize_value]

    def test_add_new_risk_type_attribute_Int(self):
        session = self.Session()
        risk_type = RiskType(name='Golf prize')
        session.add(risk_type)
        prize_value = AttributeTypeInt(name='Value', risk_type=risk_type)
        session.add(prize_value)
        session.commit()
        found_risk_type = session.query(RiskType).filter_by(name='Golf prize').first()
        found_risk_type_attribute = session.query(AttributeType).filter_by(name='Value').first()
        assert found_risk_type_attribute.risk_type == risk_type
        assert found_risk_type.attributes == [prize_value]

    def test_add_new_risk_type_attribute_Numeric(self):
        session = self.Session()
        risk_type = RiskType(name='Golf prize')
        session.add(risk_type)
        prize_value = AttributeTypeNumeric(name='Value', risk_type=risk_type)
        session.add(prize_value)
        session.commit()
        found_risk_type = session.query(RiskType).filter_by(name='Golf prize').first()
        found_risk_type_attribute = session.query(AttributeType).filter_by(name='Value').first()
        assert found_risk_type_attribute.risk_type == risk_type
        assert found_risk_type.attributes == [prize_value]

    def test_add_new_risk_type_attribute_Text(self):
        session = self.Session()
        risk_type = RiskType(name='Golf prize')
        session.add(risk_type)
        attr_type = AttributeTypeText(name='Player', risk_type=risk_type)
        session.add(attr_type)
        session.commit()
        found_risk_type = session.query(RiskType).filter_by(name='Golf prize').first()
        found_risk_type_attribute = session.query(AttributeType).filter_by(name='Player').first()
        assert found_risk_type_attribute.risk_type == risk_type
        assert found_risk_type.attributes == [attr_type]

    def test_add_new_risk_type_attribute_Date(self):
        session = self.Session()
        risk_type = RiskType(name='Golf prize')
        session.add(risk_type)
        attr_type = AttributeTypeDate(name='When', risk_type=risk_type)
        session.add(attr_type)
        session.commit()
        found_risk_type = session.query(RiskType).filter_by(name='Golf prize').first()
        found_risk_type_attribute = session.query(AttributeType).filter_by(name='When').first()
        assert found_risk_type_attribute.risk_type == risk_type
        assert found_risk_type.attributes == [attr_type]

    def test_add_new_risk_type_attribute_Enum(self):
        session = self.Session()
        risk_type = RiskType(name='Golf prize')
        session.add(risk_type)
        allowed_values = [AttributeTypeEnumValue(value=v) for v in ['EASY', 'NORMAL', 'HARD']]
        attr_type = AttributeTypeEnum(name='level', risk_type=risk_type, allowed_values=allowed_values)
        session.add(attr_type)
        session.commit()
        found_risk_type = session.query(RiskType).filter_by(name='Golf prize').first()
        found_risk_type_attribute = session.query(AttributeType).filter_by(name='level').first()
        assert found_risk_type_attribute.risk_type == risk_type
        assert found_risk_type.attributes == [attr_type]

    def test_add_new_risk_type_instance(self):
        session = self.Session()
        risk_type = RiskType(name='Golf prize')
        session.add(risk_type)
        risk_type_instance = RiskTypeInstance(risk_type=risk_type)
        session.commit()
        found_risk_type_instance = session.query(RiskTypeInstance).filter_by(risk_type=risk_type).first()
        assert risk_type_instance == found_risk_type_instance
        assert found_risk_type_instance.id is not None

    def test_add_new_risk_type_attribute_instance_using_data_type(self):
        session = self.Session()
        risk_type = RiskType(name='Golf prize')
        session.add(risk_type)
        attr_type = AttributeType(name='Value', data_type=AttributeDataType.INT, risk_type=risk_type)
        session.add(attr_type)

        risk_type_instance = RiskTypeInstance(risk_type=risk_type)
        session.add(risk_type_instance)

        risk_type_attribute_instance = AttributeInstanceInt(risk_type_instance=risk_type_instance,
                                            attribute_type=attr_type, int_value=10)
        session.add(risk_type_attribute_instance)

        session.commit()

        found_risk_type_instance = session.query(RiskTypeInstance).filter_by(risk_type=risk_type).first()

        assert found_risk_type_instance.attributes_instances == [risk_type_attribute_instance]


    def test_add_new_risk_type_attribute_instance_IntAttribute(self):
        session = self.Session()
        risk_type = RiskType(name='Golf prize')
        session.add(risk_type)
        attr_type = AttributeTypeInt(name='Value', risk_type=risk_type)
        session.add(attr_type)

        risk_type_instance = RiskTypeInstance(risk_type=risk_type)
        session.add(risk_type_instance)

        risk_type_attribute_instance = AttributeInstanceInt(risk_type_instance=risk_type_instance,
                                            attribute_type=attr_type, int_value=10)
        session.add(risk_type_attribute_instance)

        session.commit()

        found_risk_type_instance = session.query(RiskTypeInstance).filter_by(risk_type=risk_type).first()

        assert found_risk_type_instance.attributes_instances == [risk_type_attribute_instance]

    def test_add_new_risk_type_attribute_instance_NumericAttribute(self):
        session = self.Session()
        risk_type = RiskType(name='Golf prize')
        session.add(risk_type)
        attr_type = AttributeTypeNumeric(name='Value', risk_type=risk_type)
        session.add(attr_type)

        risk_type_instance = RiskTypeInstance(risk_type=risk_type)
        session.add(risk_type_instance)

        risk_type_attribute_instance = AttributeInstanceNumeric(risk_type_instance=risk_type_instance,
                                            attribute_type=attr_type, numeric_value=Decimal('10.50'))
        session.add(risk_type_attribute_instance)

        session.commit()

        found_risk_type_instance = session.query(RiskTypeInstance).filter_by(risk_type=risk_type).first()

        assert found_risk_type_instance.attributes_instances == [risk_type_attribute_instance]

    def test_add_new_risk_type_attribute_instance_TextAttribute(self):
        session = self.Session()
        risk_type = RiskType(name='Golf prize')
        session.add(risk_type)
        attr_type = AttributeTypeText(name='Player', risk_type=risk_type)
        session.add(attr_type)

        risk_type_instance = RiskTypeInstance(risk_type=risk_type)
        session.add(risk_type_instance)

        risk_type_attribute_instance = AttributeInstanceText(risk_type_instance=risk_type_instance,
                                            attribute_type=attr_type, text_value='John')
        session.add(risk_type_attribute_instance)

        session.commit()

        found_risk_type_instance = session.query(RiskTypeInstance).filter_by(risk_type=risk_type).first()

        assert found_risk_type_instance.attributes_instances == [risk_type_attribute_instance]

    def test_add_new_risk_type_attribute_instance_DateAttribute(self):
        session = self.Session()
        risk_type = RiskType(name='Golf prize')
        session.add(risk_type)
        attr_type = AttributeTypeDate(name='When', risk_type=risk_type)
        session.add(attr_type)

        risk_type_instance = RiskTypeInstance(risk_type=risk_type)
        session.add(risk_type_instance)

        risk_type_attribute_instance = AttributeInstanceDate(risk_type_instance=risk_type_instance,
                                            attribute_type=attr_type, date_value=datetime.date(2017, 12, 15))
        session.add(risk_type_attribute_instance)

        session.commit()

        found_risk_type_instance = session.query(RiskTypeInstance).filter_by(risk_type=risk_type).first()

        assert found_risk_type_instance.attributes_instances == [risk_type_attribute_instance]

    def test_add_new_risk_type_attribute_instance_EnumAttribute(self):
        session = self.Session()
        risk_type = RiskType(name='Golf prize')
        session.add(risk_type)

        allowed_values = [AttributeTypeEnumValue(value=v) for v in ['EASY', 'NORMAL', 'HARD']]
        attr_type = AttributeTypeEnum(name='Level', risk_type=risk_type, allowed_values=allowed_values)
        session.add(attr_type)

        risk_type_instance = RiskTypeInstance(risk_type=risk_type)
        session.add(risk_type_instance)

        risk_type_attribute_instance = AttributeInstanceEnum(risk_type_instance=risk_type_instance,
                                            attribute_type=attr_type, enum_value='EASY')
        session.add(risk_type_attribute_instance)

        session.commit()

        found_risk_type_instance = session.query(RiskTypeInstance).filter_by(risk_type=risk_type).first()

        assert found_risk_type_instance.attributes_instances == [risk_type_attribute_instance]
