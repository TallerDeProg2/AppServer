user_reduced_schema = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'},
        'fb': {
            'type': 'object',
            'properties': {
                'userId': {'type': 'string'},
                'authToken': {'type': 'string'}
            },
            'required': ['userId', 'authToken']
        },
    },
    'required': ['username', 'password', 'fb']
}

user_full_schema = {
        'type': 'object',
        'properties': {
            'type': {'type': 'string'},
            'username': {'type': 'string'},
            'password': {'type': 'string'},
            'fb': {
                'type': 'object',
                'properties': {
                    'userId': {'type': 'string'},
                    'authToken': {'type': 'string'}
                },
                'required': ['userId', 'authToken']
            },
            'firstname': {'type': 'string'},
            'lastname': {'type': 'string'},
            'country': {'type': 'string'},
            'email': {'type': 'string'},
            'birthdate': {'type': 'string'}
        },
        'required': ['type', 'username', 'password', 'fb', 'firstname', 'lastname',
                     'country', 'email', 'birthdate']
    }

car_schema = {
        'type': 'object',
        'properties': {
            'brand': {'type': 'string'},
            'model': {'type': 'string'},
            'color': {'type': 'string'},
            'plate': {'type': 'string'},
            'year': {'type': 'string'},
            'status': {'type': 'string'},
            'radio': {'type': 'string'},
            'airconditioner': {'type': 'boolean'}
        },
        'required': ['brand', 'model', 'color', 'plate', 'year',
                     'status', 'radio', 'airconditioner']
    }

payment_schema = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'number': {'type': 'string'},
            'type': {'type': 'string'},
            'expirationmonth': {'type': 'string'},
            'expirationyear': {'type': 'string'}
        },
        'required': ['name', 'number', 'type', 'expirationmonth', 'expirationyear']
    }


location_schema = {
        'type': 'object',
        'properties': {
            'lat': {'type': 'number'},
            'lon': {'type': 'number'},
            'token': {'type': 'integer'}
        },
        'required': ['lat', 'lon', 'token']
    }
