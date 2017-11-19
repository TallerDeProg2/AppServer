dataUser_schema = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'},
        'fb': {
            'type': 'object',
            'properties': {
                'userID': {'type': 'string'},
                'authToken': {'type': 'string'}
            },
            'required': ['userID', 'authToken']
        },
    },
    'required': ['username', 'password', 'fb']
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
