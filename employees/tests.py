from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Employee


class EmployeeAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.employee_data = {
            "id": 1,
            "first_name": "Annmarie",
            "last_name": "Crooke",
            "email": "acrooke0@gizmodo.com",
            "gender": "F",
            "date_of_birth": "09/07/1978",
            "industry": "Technology",
            "salary": 180466.37,
            "years_of_experience": 10
        }
        self.url = '/api/employees/'
        self.update_url = '/api/employee/{pk}/'.format(pk=1)

    def test_create_employee(self):
        response = self.client.post(self.url, data=self.employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
