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
        self.assertEqual(r['service'], "Luizalabs Employee Manager")

    def test_get_employees(self):
        response = self.client.get("/api/employee")
        self.assertEqual(response.status_code, 200)
        r = json.loads(response.data.decode('utf-8'))
        self.assertEqual(r['employees'][0]['name'], "Arnaldo Pereira")
        self.assertEqual(r['employees'][0]['email'], "arnalfo@luizalabs.com")
        self.assertEqual(r['employees'][0]['department'], "Architecture")

    def test_post_employee(self):
        params = {
            "name": "Vitor",
            "email": "vitor@email.com",
            "department": "TI"
        }
        response = self.client.post("/api/employee", data=json.dumps(params), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        r = json.loads(response.data.decode('utf-8'))
        employees = Employee.query.all()
        self.assertEqual(len(employees), 2)
        self.assertEqual(r['name'], "Vitor")
        self.assertEqual(r['email'], "vitor@email.com")
        self.assertEqual(r['department'], "TI")

    def test_post_employee_conflict(self):
        params = {
            "name": "Arnaldo Pereira",
            "email": "arnalfo@luizalabs.com",
            "department": "Architecture"
        }
        response = self.client.post("/api/employee", data=json.dumps(params), content_type='application/json')
        self.assertEqual(response.status_code, 409)
        employees = Employee.query.all()
        self.assertEqual(len(employees), 1)
