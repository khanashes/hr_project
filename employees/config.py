# config.py

ORGANIZATION_CONFIG = {
    'OrgA': {
        'columns': ['first_name', 'last_name', 'contact_email', 'department', 'location', 'position'],
        'filters': ['status', 'location', 'department', 'position'],
        'organization_filter': {'status': 'ACTIVE'}  # OrgA only wants active employees
    },
    'OrgB': {
        'columns': ['department', 'location', 'position'],
        'filters': ['department', 'location'],
        'organization_filter': {'location': 'NYC'}  # OrgB only wants employees in NYC
    },
}
