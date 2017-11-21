log_in_schema = {
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
            'required': ['userID', 'authToken']
        },
    },
    'required': ['username', 'password', 'fb']
}

sign_up_schema = {
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

dataCar_schema = {
    'type': 'object',
    'properties': {
        # 'username': {'type': 'string'},
        # 'password': {'type': 'string'},
        # 'fb': {
        #     'type': 'object',
        #     'properties': {
        #         'userID': {'type': 'string'},
        #         'authToken': {'type': 'string'}
        #     },
        #     'required': ['userID', 'authToken']
        # },
    },
    'required': ['username', 'password', 'fb']
}

dataPayment_schema = {
    'type': 'object',
    'properties': {
        # 'username': {'type': 'string'},
        # 'password': {'type': 'string'},
        # 'fb': {
        #     'type': 'object',
        #     'properties': {
        #         'userID': {'type': 'string'},
        #         'authToken': {'type': 'string'}
        #     },
        #     'required': ['userID', 'authToken']
        # },
    },
    'required': ['username', 'password', 'fb']
}
