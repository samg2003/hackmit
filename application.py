import os

from flask import Flask, render_template, session, request, redirect, url_for, jsonify , make_response
from flask_session import Session
import time
import requests
from utilities import *
app = Flask(__name__, static_folder = "images")



app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        coordinate = request.form.get("coordinates")
        if coordinate == None:
            return render_template("index.html", message = "Something went wrong")
        coordinate = coordinate.split(",")
        coordinate = [float(coordinate[0].strip()), float(coordinate[1].strip())]
        year, name = coordinates(coordinate[0], coordinate[1])
        return render_template("index.html", message = year, path = name)
    return render_template("index.html")
