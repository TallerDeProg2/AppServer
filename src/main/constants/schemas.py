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


# TODO: agregar propuesta de camino
trip_request_schema = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'trip': {                           # VER si puede generar conflictos este nombre
            'type': 'object',
            'properties': {
                'start': {
                    'type': 'object',
                    'properties': {

                        'lat': {'type': 'integer'},
                        'lon': {'type': 'integer'}
                    },
                    'required': ['lat', 'lon']
                },
                'end': {
                    'type': 'object',
                    'properties': {
                        'lat': {'type': 'integer'},
                        'lon': {'type': 'integer'}
                    },
                    'required': ['lat', 'lon']
                },
            },
            'required': ['start', 'end']
        },
        'paymethod': {
            'type': 'object',
            'properties': {
                'paymethod': {'type': 'string'},
                # 'parameters': {
                #     'type': 'object',
                #     'properties': {
                #         'MISTICO': {'type': 'string'},  ## ESTA COMO JSON VACIO QUE ONDA?
                #
                #     },
                #     #'required': ['']
                # }
            },
            'required': ['paymethod']
        },
    },
    'required': ['username', 'trip', 'paymethod']
}

trips_reduced_schema = {
    'type': 'object',
    'properties': {
        'trip': {
            'type': 'object',
            'properties': {
                'start': {
                    'type': 'object',
                    'properties': {
                        'address': {
                            'type': 'object',
                            'properties': {
                                # 'street': {'type': 'string'},
                                'location': {
                                    'type': 'object',
                                    'properties': {
                                        'lat': {'type': 'integer'},
                                        'lon': {'type': 'integer'}
                                    },
                                    # 'required': ['lat', 'lon', 'token']
                                },
                            },
                            # 'required': ['lat', 'lon', 'token']
                        },
                        # 'timestamp': {'type': 'integer'}
                    },
                    # 'required': ['lat', 'lon', 'token']
                },
                'end': {
                    'type': 'object',
                    'properties': {
                        'address': {
                            'type': 'object',
                            'properties': {
                                'street': {'type': 'string'},
                                'location': {
                                    'type': 'object',
                                    'properties': {
                                        'lat': {'type': 'integer'},
                                        'lon': {'type': 'integer'}
                                    },
                                    # 'required': ['lat', 'lon', 'token']
                                },
                            },
                            # 'required': ['lat', 'lon', 'token']
                        },
                        # 'timestamp': {'type': 'integer'}
                    },
                    # 'required': ['lat', 'lon', 'token']
                },
            },
            # 'required': ['lat', 'lon', 'token']
        },
        'paymethod': {
            'type': 'object',
            'properties': {
                'paymethod': {'type': 'string'},
                # 'parameters': {
                #     'type': 'object',
                #     'properties': {
                #         'MISTICO': {'type': 'string'},  ## ESTA COMO JSON VACIO QUE ONDA?
                #
                #     },
                #     #'required': ['']
                # }
            },
            # 'required': ['lat', 'lon', 'token']
        },
    },
    # 'required': ['lat', 'lon', 'token']
}

trips_full_schema = {
    'type': 'object',
    'properties': {
        'trip': {
            'type': 'object',
            'properties': {
                'id': {'type': 'string'},
                'applicationOwner': {'type': 'string'},
                'driver': {'type': 'string'},
                'passenger': {'type': 'string'},
                'start': {
                    'type': 'object',
                    'properties': {
                        'address': {
                            'type': 'object',
                            'properties': {
                                'street': {'type': 'string'},
                                'location': {
                                    'type': 'object',
                                    'properties': {
                                        'lat': {'type': 'integer'},
                                        'lon': {'type': 'integer'}
                                    },
                                    # 'required': ['lat', 'lon', 'token']
                                },
                            },
                            # 'required': ['lat', 'lon', 'token']
                        },
                        'timestamp': {'type': 'integer'}
                    },
                    # 'required': ['lat', 'lon', 'token']
                },
                'end': {
                    'type': 'object',
                    'properties': {
                        'address': {
                            'type': 'object',
                            'properties': {
                                'street': {'type': 'string'},
                                'location': {
                                    'type': 'object',
                                    'properties': {
                                        'lat': {'type': 'integer'},
                                        'lon': {'type': 'integer'}
                                    },
                                    # 'required': ['lat', 'lon', 'token']
                                },
                            },
                            # 'required': ['lat', 'lon', 'token']
                        },
                        'timestamp': {'type': 'integer'}
                    },
                    # 'required': ['lat', 'lon', 'token']
                },
            },
            # 'required': ['lat', 'lon', 'token']
        },
        'totalTime': {'type': 'integer'},  # VER QUE TIPO QUIERE ALAN
        'waitTime': {'type': 'integer'},
        'travelTime': {'type': 'integer'},
        'distance': {'type': 'integer'},
        # 'route': {'type': 'integer'},  # ?????? VECTOR DE JSON
        'cost': {
            'type': 'object',
            'properties': {
                'currency': {'type': 'string'},
                'value': {'type': 'integer'}
            },
            # 'required': ['userId', 'authToken']
        },
        'paymethod': {
            'type': 'object',
            'properties': {
                'paymethod': {'type': 'string'},
                # 'parameters': {
                #     'type': 'object',
                #     'properties': {
                #         'MISTICO': {'type': 'string'},  ## ESTA COMO JSON VACIO QUE ONDA?
                #
                #     },
                #     #'required': ['']
                # }
            },
            # 'required': ['lat', 'lon', 'token']
        },
    },
    # 'required': ['lat', 'lon', 'token']
}

#     {
#   "trip": {
#     "id": "string",
#     "applicationOwner": "string",
#     "driver": "string",
#     "passenger": "string",
#     "start": {
#       "address": {
#         "street": "string",
#         "location": {
#           "lat": 0,
#           "lon": 0
#         }
#       },
#       "timestamp": 0
#     },
#     "end": {
#       "address": {
#         "street": "string",
#         "location": {
#           "lat": 0,
#           "lon": 0
#         }
#       },
#       "timestamp": 0
#     },
#     "totalTime": 0,
#     "waitTime": 0,
#     "travelTime": 0,
#     "distance": 0,
#     "route": [
#       {
#         "location": {
#           "lat": 0,
#           "lon": 0
#         },
#         "timestamp": 0
#       }
#     ],
#     "cost": {
#       "currency": "string",
#       "value": 0
#     }
#   },
#   "paymethod": {
#     "paymethod": "string",
#     "parameters": {}
#   }
# }
