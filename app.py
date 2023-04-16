from dataclasses import dataclass
from datetime import datetime

from bson import ObjectId
from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)
db = MongoClient()['sponsorbook']

tickets = {}


@dataclass
class Ticket:
    id: str
    title: str
    description: str

def gen_mongo_id():
    return ObjectId.from_datetime(datetime.now())

@app.route('/ticket', methods=['POST'])
def create_ticket():
    response = request.get_json()
    try:
        ticket = Ticket(id=str(gen_mongo_id()), title=response['title'],
                        description=response['description'])
    except:
        return 'Missing fields', 400
    # tickets[ticket.id] = ticket
    result = db['tickets'].insert_one({'_id': ObjectId(ticket.id),
                                       'title': ticket.title,
                                       'description:': ticket.description})
    return ticket.__dict__, 201


@app.route('/ticket/<id>', methods=['GET'])
def return_ticket(id):
    try:
        # ticket = tickets[id]
        ticket = db['tickets'].find_one({'_id': ObjectId(id)}, {"_id": False})
    except:
        return 'Ticket not found', 404
    return ticket, 200


@app.route('/tickets', methods=['GET'])
def return_all_tickets():
    return list(db['tickets'].find({}, {"_id": False})), 200


# Running flask
if __name__ == '__main__':
    app.run(debug=True)
