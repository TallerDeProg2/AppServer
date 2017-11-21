import os

# deberia crearla como variable de entorno
SECRET_KEY_default = "a"

VAR = os.environ

if "SECRET_KEY" in os.environ:
    SECRET_KEY = os.environ["SECRET_KEY"]
else:
    SECRET_KEY = SECRET_KEY_default

token = os["app_token"]
