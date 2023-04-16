from bson import ObjectId
from bson.errors import InvalidId
from flask import Blueprint, request
from pymongo import MongoClient

from models import Organization

organizations_api = Blueprint('organizations', __name__)
db = MongoClient()['sponsorbook']
# TODO: This shit is dumb af. If we are doing data hierarchy then it has to be organization_name, not organizations
organizations = db['organizations']


def gen_mongo_id():
    return ObjectId()


@organizations_api.route('/organizations', methods=["POST"])
def create_organisation():
    response = request.get_json()
    try:
        organization = Organization(id=str(gen_mongo_id()), name=response.name, sub_organizations=list())
    except KeyError:
        return 'Missing fields', 400

    organizations.insert_one({'_id': ObjectId(organization.id),
                              'name': organization.name,
                              'sub_organizations': organization.sub_organizations})
    return organization.__dict__, 201


@organizations_api.route('/organizations/<id>', methods=['GET'])
def delete_organization(id):
    try:
        mongo_id = ObjectId(id)
    except InvalidId:
        return "Id is not well-formed", 400

    organization = organizations.find_one({'_id': mongo_id})
    if organization is None:
        return 'Organization not found', 400

    organizations.delete_one({'_id': mongo_id})
    # TODO: Find out which date we are planning to archive and in what way
    # archived_tickets.insert_one(ticket)
    return 'Ticket deleted', 200
