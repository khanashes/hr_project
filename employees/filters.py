import django_filters
from .models import Employee
from .config import ORGANIZATION_CONFIG

import django_filters
from .models import Employee

class DynamicEmployeeFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')], label='Status')
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains', label='Location')
    department = django_filters.CharFilter(field_name='department', lookup_expr='icontains', label='Department')
    position = django_filters.CharFilter(field_name='position', lookup_expr='icontains', label='Position')

    class Meta:
        model = Employee
        fields = ['status', 'location', 'department', 'position']

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.get('request').META.get('HTTP_ORGANIZATION', 'OrgA')  # Default to 'OrgA'
        super().__init__(*args, **kwargs)
        
        allowed_filters = ORGANIZATION_CONFIG.get(self.organization, {}).get('filters', [])
        for field in list(self.filters.keys()):
            if field not in allowed_filters:
                self.filters.pop(field)

