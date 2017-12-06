import unittest
from copy import deepcopy

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from brite.model import Base
from brite.model import RiskType
from brite.model import AttributeDataType
from brite.model.service import DbService, str2enum

full_insurance = {
    'name': 'Stolen car',
    'description': 'Insurance for when a car is stolen',
    'attributes': [
        {
            'name': 'Customer name',
            'type': 'text',
        },
        {
            'name': 'Start date',
            'description': 'When the insurance begins to take effect',
            'type': 'date',
        },
        {
            'name': 'End date',
            'description': 'When the insurance finishes',
            'type': 'date',
        },
        {
            'name': 'Value',
            'description': 'How much to pay in the case of the car is stolen',
            'type': 'numeric',
        },
        {
            'name': 'Communication days',
            'description': 'The maximal number of days the client has to communicate the theft',
            'type': 'int',
        },
        {
            'name': 'Customer history',
            'description': 'Has the client being stolen before?',
            'type': 'enum',
            'allowed_values': ['Never stolen', 'Stolen once', 'Stolen multiple times'],
        },
    ]
}


class TestDbService(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(self.engine)
        self.db_service = DbService(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def test_add_type(self):
        insurance_type = deepcopy(full_insurance)
        new_id = self.db_service.add_type(insurance_type)
        session = self.Session()
        added_type = session.query(RiskType).filter_by(name='Stolen car').first()
        assert added_type.id == new_id
        assert added_type.name == insurance_type['name']
        assert added_type.description == insurance_type['description']
        
        def assert_attribute(attribute, dict_repr):
            assert attribute.name == dict_repr['name']
            assert attribute.description == dict_repr.get('description')
            assert attribute.data_type == str2enum(dict_repr['type'])
            if attribute.data_type == AttributeDataType.ENUM:
                assert [v.value for v in attribute.allowed_values] == dict_repr.get('allowed_values')
        model_attributes = added_type.attributes
        dict_attributes = insurance_type['attributes']
        assert_attribute(model_attributes[0], dict_attributes[0])
        assert_attribute(model_attributes[1], dict_attributes[1])
        assert_attribute(model_attributes[2], dict_attributes[2])
        assert_attribute(model_attributes[3], dict_attributes[3])
        assert_attribute(model_attributes[4], dict_attributes[4])
        assert_attribute(model_attributes[5], dict_attributes[5])

    def test_get_type(self):
        insurance_type = deepcopy(full_insurance)
        new_id = self.db_service.add_type(insurance_type)
        insurance_type['id'] = new_id
        result_type = self.db_service.get_type(new_id)
        for attribute in result_type['attributes']:
            # if there is no id, we'll get an attribute error
            attribute.pop('id')
        assert result_type == insurance_type

    def test_get_type_invalid_id(self):
        assert self.db_service.get_type(12345) is None

    def test_get_types(self):
        insurance_type = deepcopy(full_insurance)
        self.db_service.add_type(insurance_type)
        self.db_service.add_type(insurance_type)
        result_types = self.db_service.get_types()
        assert len(result_types) == 2
        for result_type in result_types:
            result_type.pop('id')
            for attr in result_type['attributes']:
                attr.pop('id')
            assert result_type == insurance_type

    def test_get_types_ordered(self):
        def new_insurance(name):
            insurance_type = deepcopy(full_insurance)
            insurance_type['name'] = name
            return insurance_type

        self.db_service.add_type(new_insurance('c'))
        self.db_service.add_type(new_insurance('B'))
        self.db_service.add_type(new_insurance('a'))
        result_types = self.db_service.get_types(order_by_name=True)
        assert ['a', 'B', 'c'] == [r['name'] for r in result_types]
