import os
import shutil
import unittest
import tempfile
import json

from sqlalchemy import create_engine

from brite.model import Base
from brite.model.service import DbService
from brite.model.command_line.add_new_type import add_new_type

class TestNewType(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, 'mydb.db')

    def tearDown(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def _basic_add_type(self):
        insurance_type = {
            'name': 'Stolen car',
            'description': 'Insurance for when a car is stolen',
            'attributes': [
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

        json_path = os.path.join(self.temp_dir, 'insurance.json')
        with open(json_path, 'w') as f:
            json.dump(insurance_type, f)

        add_new_type(self.db_path, json_path)

        engine = create_engine('sqlite:///%s' % self.db_path, echo=False)
        service = DbService(engine)
        types = service.get_types()
        assert len(types) == 1
        result_type = types[0]
        result_type.pop('id')
        for attr in result_type['attributes']:
            attr.pop('id')
        assert result_type == insurance_type

    def test_add_type_db_exists(self):
        engine = create_engine('sqlite:///%s' % self.db_path, echo=False)
        Base.metadata.create_all(engine)
        self._basic_add_type()

    def test_add_type_db_doesnt_exist(self):
        self._basic_add_type()
