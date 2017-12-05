import unittest

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from brite.model import Base, RiskType, RiskTypeAttribute, RiskTypeAttributeDataType,\
    RiskTypeInstance, RiskTypeAttributeInstance

class TestRawRiskTypeModel(unittest.TestCase):
    def setUp(self):
        # make sure we always start from scratch
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
        prize_value = RiskTypeAttribute(name='Value', data_type=RiskTypeAttributeDataType.INT, risk_type=risk_type)
        session.add(prize_value)
        session.commit()
        found_risk_type = session.query(RiskType).filter_by(name='Golf prize').first()
        found_risk_type_attribute = session.query(RiskTypeAttribute).filter_by(name='Value').first()
        assert found_risk_type_attribute.risk_type == risk_type
        assert found_risk_type.attributes == [prize_value]

    def test_add_new_risk_type_instance(self):
        session = self.Session()
        risk_type = RiskType(name='Golf prize')
        session.add(risk_type)
        risk_type_instance = RiskTypeInstance(risk_type=risk_type)
        session.commit()
        found_risk_type_instance = session.query(RiskTypeInstance).filter_by(risk_type=risk_type).first()
        assert risk_type_instance == found_risk_type_instance
        assert found_risk_type_instance.id is not None

    def test_add_new_risk_type_attribute_instance(self):
        session = self.Session()
        risk_type = RiskType(name='Golf prize')
        session.add(risk_type)
        prize_value = RiskTypeAttribute(name='Value', data_type=RiskTypeAttributeDataType.INT, risk_type=risk_type)
        session.add(prize_value)

        risk_type_instance = RiskTypeInstance(risk_type=risk_type)
        session.add(risk_type_instance)

        risk_type_attribute_instance = RiskTypeAttributeInstance(risk_type_instance=risk_type_instance, attribute_type=prize_value, value=10)
        session.add(risk_type_attribute_instance)

        session.commit()

        found_risk_type_instance = session.query(RiskTypeInstance).filter_by(risk_type=risk_type).first()

        assert found_risk_type_instance.attributes_instances == [risk_type_attribute_instance]
