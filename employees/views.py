from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from employees.config import ORGANIZATION_CONFIG
from employees.filters import DynamicEmployeeFilter
from employees.mixins import RateLimitMixin
from employees.models import Employee
from employees.serializers import DynamicEmployeeSerializer


class EmployeeSearchView(RateLimitMixin, ListAPIView):
    queryset = Employee.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = DynamicEmployeeFilter
    pagination_class = PageNumberPagination
    serializer_class = DynamicEmployeeSerializer
    search_fields = ['first_name', 'last_name', 'department', 'position', 'location']


    def get_serializer_context(self):
        context = super().get_serializer_context()
        organization = self.request.headers.get('Organization', 'OrgA')  # Default to 'OrgA'
        context['organization'] = organization
        return context

    def get_filterset(self, *args, **kwargs):
        filterset_class = self.get_filterset_class()
        return filterset_class(self.request.GET, queryset=self.get_queryset(), request=self.request)

    def get_queryset(self):
        queryset = super().get_queryset()
        # Apply organization-specific filtering
        organization = self.request.headers.get('Organization', 'OrgA')
        organization_filter = ORGANIZATION_CONFIG.get(organization, {}).get('organization_filter', {})
        if organization_filter:
            queryset = queryset.filter(**organization_filter)

        return queryset

    def get(self, request, *args, **kwargs):
        self.check_rate_limit(request)
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="Search employees by first name, last name, department, position, or location", type=openapi.TYPE_STRING),
            openapi.Parameter('Organization', openapi.IN_HEADER, description="Specify the organization for filtering and column customization", type=openapi.TYPE_STRING)
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
