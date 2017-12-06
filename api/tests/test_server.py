import unittest
import json

from sqlalchemy import create_engine

from brite.model import Base
from brite.model.service import DbService
from brite.api.server import app
from copy import deepcopy

from_json = lambda r: json.loads(r.get_data(as_text=True))

_full_insurance = {
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

class TestServer(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)

        self._service = DbService(engine)

        app.config['BACKEND'] = self._service
        self.app = app.test_client()

    def test_search_no_types(self):
        response = self.app.get('/search/types/')
        self.assertEqual(response.status_code, 200)
        data = from_json(response)
        self.assertEqual(data, {
            'total': 0,
            'types': [],
        })

    def test_search_with_types(self):
        expected = []
        for i in range(3):
            risk_type = deepcopy(_full_insurance)
            # this will make sure names are not being inserted in order
            risk_type['name'] = '%s - %s' % (9-i, risk_type['name'])
            new_id = self._service.add_type(risk_type)
            expected.append(self._service.get_type(new_id))
        expected.sort(key=lambda x: x['name'])
        response = self.app.get('/search/types/')
        self.assertEqual(response.status_code, 200)
        data = from_json(response)
        self.assertEqual(data, {
            'total': 3,
            'types': expected,
        })

    def test_get_type(self):
        risk_type = deepcopy(_full_insurance)
        new_id = self._service.add_type(risk_type)
        expected = self._service.get_type(new_id)

        response = self.app.get('/types/%s/' % new_id)
        self.assertEqual(response.status_code, 200)
        data = from_json(response)
        self.assertEqual(data, expected)

    def test_get_type_not_available(self):
        for key in [1, 'a']:
            response = self.app.get('/types/%s/' % key)
            self.assertEqual(response.status_code, 404, '%s - should return error 400' % key)
