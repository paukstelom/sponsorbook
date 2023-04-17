from dataclasses import dataclass

from bson import ObjectId
from bson.errors import InvalidId
from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)
db = MongoClient()['sponsorbook']

tickets = db['tickets']
archived_tickets = db['archived_tickets']


@dataclass
class Ticket:
    id: str
    title: str
    description: str


def gen_mongo_id():
    return ObjectId()


@app.route('/tickets', methods=['POST'])
def create_ticket():
    response = request.get_json()
    try:
        ticket = Ticket(id=str(gen_mongo_id()), title=response['title'],
                        description=response['description'])
    except KeyError:
        return 'Missing fields', 400

    tickets.insert_one({'_id': ObjectId(ticket.id),
                        'title': ticket.title,
                        'description:': ticket.description})
    return ticket.__dict__, 201


@app.route('/tickets/<id>', methods=['GET'])
def get_ticket(id: str):
    try:
        mongo_id = ObjectId(id)
    except InvalidId:
        return "Id is not well-formed", 400

    ticket = tickets.find_one({'_id': mongo_id}, {"_id": False})

    if ticket is None:
        return "Ticket not found", 404

    return ticket, 200


@app.route('/tickets', methods=['GET'])
def list_tickets():
    return list(tickets.find({}, {"_id": False})), 200


@app.route('/tickets/<id>', methods=['DELETE'])
def delete_ticket(id):
    try:
        mongo_id = ObjectId(id)
    except InvalidId:
        return "Id is not well-formed", 400

    ticket = tickets.find_one({'_id': mongo_id})
    if ticket is None:
        return 'Ticket not found', 400

    tickets.delete_one({'_id': mongo_id})
    archived_tickets.insert_one(ticket)
    return 'Ticket deleted', 200


# Running flask
if __name__ == '__main__':
    app.run(debug=True)
