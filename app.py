from bson import ObjectId
from bson.errors import InvalidId
from flask import Flask, request
from pymongo import MongoClient

from use_cases.create_ticket import create_ticket

app = Flask(__name__)
db = MongoClient()['sponsorbook']

tickets = db['tickets']
archived_tickets = db['archived_tickets']


@app.route('/tickets', methods=['POST'])
def create_ticket_endpoint():
    return create_ticket(tickets, request.get_json())


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
