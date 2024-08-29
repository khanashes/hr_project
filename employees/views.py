from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination


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
