from dataclasses import dataclass
from uuid import uuid4

from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)
db = MongoClient()['sponsorbook']

tickets = {}


@dataclass
class Ticket:
    title: str
    id: str
    description: str


@app.route('/ticket', methods=['POST'])
def create_ticket():
    response = request.get_json()
    try:
        ticket = Ticket(title=response['title'], id=str(uuid4()), description=response['description'])
    except:
        return 'Missing fields', 400
    # tickets[ticket.id] = ticket
    result = db['tickets'].insert_one({'id': ticket.id,
                                       'title': ticket.title,
                                       'description:': ticket.description})
    return ticket.__dict__, 201


@app.route('/ticket/<id>', methods=['GET'])
def return_ticket(id):
    try:
        # ticket = tickets[id]
        ticket = db['tickets'].find_one({'id': id}, {"_id": False})
    except:
        return 'Ticket not found', 404
    return ticket, 200


@app.route('/tickets', methods=['GET'])
def return_all_tickets():
    return list(db['tickets'].find({}, {"_id": False})), 200


# Running flask
if __name__ == '__main__':
    app.run(debug=True)
