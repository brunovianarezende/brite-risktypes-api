import unittest

from sqlalchemy import create_engine

from brite.model import Base
from brite.model.service import DbService
from brite.api.server import app

class TestServer(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=True)
        Base.metadata.create_all(engine)

        app.config['BACKEND'] = DbService(engine)
        self.app = app.test_client()

    def test_search_no_types(self):
        pass

    def test_search_with_types(self):
        pass

    def test_get_type(self):
        pass

    def test_get_type_not_available(self):
        pass