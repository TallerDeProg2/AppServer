"""Main.py"""
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
"""[Main] Comentario de funcion hola mundo"""
    return "Hello World!"

if __name__ == "__main__":
	"""Main comentario	"""
	app.run( debug=True)
