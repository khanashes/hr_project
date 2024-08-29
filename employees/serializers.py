from rest_framework import serializers
from .models import Employee
from .config import ORGANIZATION_CONFIG

class DynamicEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'  # Default to all fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get the organization from context (passed via the view)
        organization = self.context.get('organization')
        
        if organization:
            allowed_columns = ORGANIZATION_CONFIG.get(organization, {}).get('columns', [])
            existing_fields = set(self.fields.keys())
            
            # Remove fields not in the organization's column configuration
            for field in existing_fields - set(allowed_columns):
                self.fields.pop(field)
