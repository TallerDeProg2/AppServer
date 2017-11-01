"""Main.py"""
from flask import Flask


app = Flask(__name__)


@app.route("/token", methods=['GET'])
def hello():
    """Comentario"""
    return "Hello World!"


@app.route("/users", methods=['GET'])
def hello():
    """Comentario"""
    return "Hello World!"


@app.route("/users/{userId}/location", methods=['GET'])
def hello():
    """Comentario"""
    return "Hello World!"


@app.route("/users/{userId}/trips", methods=['GET'] )
def hello():
    """Comentario"""
    return "Hello World!"


@app.route("/passengers", methods=['GET'])
def hello():
    """Comentario"""
    return "Hello World!"


@app.route("/passengers/{passengerId}", methods=['GET'])
def hello():
    """Comentario"""
    return "Hello World!"


@app.route("/passengers/{passengerId}/drivers", methods=['GET'])
def hello():
    """Comentario"""
    return "Hello World!"


@app.route("/drivers", methods=['GET'])
def hello():
    """Comentario"""
    return "Hello World!"


@app.route("/drivers/{driverId}", methods=['GET'])
def hello():
    """Comentario"""
    return "Hello World!"


@app.route("/drivers/{driverId}/cars", methods=['GET'])
def hello():
    """Comentario"""
    return "Hello World!"


@app.route("/drivers/{driverId}/cars/{carId}", methods=['GET'])
def hello():
    """Comentario"""
    return "Hello World!"


@app.route("/drivers/{driverId}/passengers", methods=['GET'])
def hello():
    """Comentario"""
    return "Hello World!"


@app.route("/trips", methods=['GET'])
def hello():
    """Comentario"""
    return "Hello World!"


@app.route("/trips/{tripId}", methods=['GET'])
def hello():
    """Comentario"""
    return "Hello World!"


@app.route("/")
def hello():
    """Comentario"""
    return "Hello World!"@app.route("/")


if __name__ == "__main__":
    """Main comentario	"""
    app.run( debug=True)
