import json

from lem import db
from lem.models import Employee

from tests.base import BaseTestCase


class TestViewAPICase(BaseTestCase):

    def setUp(self):
        super(TestViewAPICase, self).setUp()

    def load_fixtures(self):
        employee = Employee(
            name='Arnaldo Pereira',
            email='arnalfo@luizalabs.com',
            department='Architecture'
        )

        db.session.add(employee)
        db.session.commit()

    def test_index(self):
        response = self.client.get("/api/")
        self.assertEqual(response.status_code, 200)
        r = json.loads(response.data.decode('utf-8'))
        self.assertIn(r['service'], "Luizalabs Employee Manager")

    def test_get_employees(self):
        response = self.client.get("/api/employee")
        self.assertEqual(response.status_code, 200)
        r = json.loads(response.data.decode('utf-8'))
        self.assertIn(r['employees'][0]['name'], "Arnaldo Pereira")
        self.assertIn(r['employees'][0]['email'], "arnalfo@luizalabs.com")
        self.assertIn(r['employees'][0]['department'], "Architecture")
