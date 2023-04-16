from bson import ObjectId
from bson.errors import InvalidId
from flask import Blueprint, request
from pymongo import MongoClient
from models import SubOrganization

organizations_api = Blueprint('organizations', __name__)
db = MongoClient()['sponsorbook']
organizations = db['organizations']

