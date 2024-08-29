from django.test import TestCase
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient
from rest_framework import status
from .models import Employee
from .views import EmployeeSearchView

class EmployeeSearchViewUnitTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        # Add test data to the database
        Employee.objects.create(
            first_name='John', last_name='Doe', contact_email='john.doe@example.com',
            department='Sales', position='Manager', location='NYC', status='ACTIVE'
        )
        Employee.objects.create(
            first_name='Jane', last_name='Doe', contact_email='jane.doe@example.com',
            department='Engineering', position='Developer', location='SF', status='INACTIVE'
        )

    @patch('employees.filters.DynamicEmployeeFilter')
    @patch('employees.views.EmployeeSearchView.get_queryset')
    def test_search_with_orgA(self, MockGetQueryset, MockFilter):
        # Mock the filterset class
        mock_filter = MagicMock()
        mock_filter.filter.return_value = Employee.objects.all()
        MockFilter.return_value = mock_filter

        # Mock queryset
        mock_queryset = Employee.objects.all()
        MockGetQueryset.return_value = mock_queryset

        # Simulate GET request with organization header
        response = self.client.get('/api/employees/', HTTP_ORGANIZATION='OrgA')

        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()[0]
        self.assertIsInstance(data, dict)

        results = data.get('results', [])
        self.assertIsInstance(results, list)

        for employee in results:
            self.assertIsInstance(employee, dict)
            self.assertIn('first_name', employee)
            self.assertIn('last_name', employee)
            self.assertIn('contact_email', employee)
            self.assertIn('department', employee)
            self.assertIn('location', employee)
            self.assertIn('position', employee)
            self.assertNotIn('contact_phone', employee)  # Not in OrgA's config
