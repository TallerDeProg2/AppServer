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
        'lon': {'type': 'number'}
    },
    'required': ['lat', 'lon']
}

trips_full_schema = {
    'type': 'object',
    'properties': {
        'trip': {
            'type': 'object',
            'properties': {
                'legs': {'minItems': 1,
                        'type': 'array'}
            #     'bounds': {'type': 'object'},
            #     "copyrights": {'type': 'object'},
            #     "overview_polyline": {'type': 'object'},
            #     "summary": {'type': 'string'},
            #     "warnings": {'type': 'object'},
            #     "waypoint_order":{'type': 'object'},
                },
            'required': ['legs']
        },
        'paymethod': {
            'type': 'object',
            'properties': {
                'paymethod': {'type': 'string'},
            },
        },
    },
    'required': ['trip', 'paymethod']
}

# trips_full_schema = {
#     'type': 'object',
#     'properties': {
#         'trip': {
#             'type': 'object',
#             'properties': {
#                 'id': {'type': 'string'},
#                 'applicationOwner': {'type': 'string'},
#                 'driver': {'type': 'string'},
#                 'passenger': {'type': 'string'},
#                 'start': {
#                     'type': 'object',
#                     'properties': {
#                         'address': {
#                             'type': 'object',
#                             'properties': {
#                                 'street': {'type': 'string'},
#                                 'location': {
#                                     'type': 'object',
#                                     'properties': {
#                                         'lat': {'type': 'integer'},
#                                         'lon': {'type': 'integer'}
#                                     },
#                                     # 'required': ['lat', 'lon', 'token']
#                                 },
#                             },
#                             # 'required': ['lat', 'lon', 'token']
#                         },
#                         'timestamp': {'type': 'integer'}
#                     },
#                     # 'required': ['lat', 'lon', 'token']
#                 },
#                 'end': {
#                     'type': 'object',
#                     'properties': {
#                         'address': {
#                             'type': 'object',
#                             'properties': {
#                                 'street': {'type': 'string'},
#                                 'location': {
#                                     'type': 'object',
#                                     'properties': {
#                                         'lat': {'type': 'integer'},
#                                         'lon': {'type': 'integer'}
#                                     },
#                                     # 'required': ['lat', 'lon', 'token']
#                                 },
#                             },
#                             # 'required': ['lat', 'lon', 'token']
#                         },
#                         'timestamp': {'type': 'integer'}
#                     },
#                     # 'required': ['lat', 'lon', 'token']
#                 },
#             },
#             # 'required': ['lat', 'lon', 'token']
#         },
#         'totalTime': {'type': 'integer'},  # VER QUE TIPO QUIERE ALAN
#         'waitTime': {'type': 'integer'},
#         'travelTime': {'type': 'integer'},
#         'distance': {'type': 'integer'},
#         # 'route': {'type': 'integer'},  # ?????? VECTOR DE JSON
#         'cost': {
#             'type': 'object',
#             'properties': {
#                 'currency': {'type': 'string'},
#                 'value': {'type': 'integer'}
#             },
#             # 'required': ['userId', 'authToken']
#         },
#         'paymethod': {
#             'type': 'object',
#             'properties': {
#                 'paymethod': {'type': 'string'},
#                 # 'parameters': {
#                 #     'type': 'object',
#                 #     'properties': {
#                 #         'MISTICO': {'type': 'string'},  ## ESTA COMO JSON VACIO QUE ONDA?
#                 #
#                 #     },
#                 #     #'required': ['']
#                 # }
#             },
#             # 'required': ['lat', 'lon', 'token']
#         },
#     },
#     # 'required': ['lat', 'lon', 'token']
# }
