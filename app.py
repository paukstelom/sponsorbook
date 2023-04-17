from flask import Flask, request
from pymongo import MongoClient

from use_cases.create_ticket import create_ticket
from use_cases.delete_ticket import delete_ticket
from use_cases.get_ticket import get_ticket
from use_cases.get_tickets import get_tickets

app = Flask(__name__)
db = MongoClient()['sponsorbook']

tickets = db['tickets']
archived_tickets = db['archived_tickets']


@app.route('/tickets', methods=['POST'])
def create_ticket_endpoint():
    return create_ticket(tickets, request.get_json())


@app.route('/tickets/<id>', methods=['GET'])
def get_ticket_endpoint(id: str):
    return get_ticket(id, tickets)


@app.route('/tickets', methods=['GET'])
def get_tickets_endpoint():
    return get_tickets(tickets)


@app.route('/tickets/<id>', methods=['DELETE'])
def delete_ticket_endpoint(id):
    return delete_ticket(tickets, archived_tickets, id)


# Running flask
if __name__ == '__main__':
    app.run(debug=True)
