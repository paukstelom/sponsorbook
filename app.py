from flask import Flask
from domain.models import Organization


app = Flask(__name__)

@app.get("/")
def hello():
    org = Organization("Edvin", "2023-05-01")
    return str(org)
