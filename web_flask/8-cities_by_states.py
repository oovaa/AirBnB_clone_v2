#!/usr/bin/python3
"""Starts a Flask web application.

The application listens on 0.0.0.0, port 5000.
Routes:
    /states_list: HTML page with a list of all State objects in DBStorage.
"""
from models import state, storage
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """Displays an HTML page with a list of all State objects in DBStorage.

    States are sorted by name.
    """
    states = storage.all("State")
    cities = sorted(list(storage.all("City").values()), key=lambda x: x.name)
    states = sorted(list(storage.all("State").values()), key=lambda x: x.name)
    return render_template("8-cities_by_states.html", states=states, cities=cities)


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
