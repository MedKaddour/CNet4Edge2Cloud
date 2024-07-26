from flask import Flask, request, jsonify
from models import CallForProposal, Bid, Contract, Manager, Contractor
import json
import os

app = Flask(__name__)

# In-memory storage
call_for_proposals = []
bids = []
contracts = []
managers = []
contractors = []

# Helper function to load schemas
def load_schema(schema_name):
    with open(os.path.join('schemas', f'{schema_name}.json')) as schema_file:
        return json.load(schema_file)

@app.route('/call_for_proposals', methods=['POST'])
def create_call_for_proposal():
    data = request.json
    schema = load_schema('call_for_proposal')
    
    call_for_proposal = CallForProposal(**data)
    call_for_proposals.append(call_for_proposal)
    return jsonify(data), 201

@app.route('/bids', methods=['POST'])
def create_bid():
    data = request.json
    schema = load_schema('bid')
    
    bid = Bid(**data)
    bids.append(bid)
    return jsonify(data), 201

@app.route('/contracts', methods=['POST'])
def create_contract():
    data = request.json
    schema = load_schema('contract')
    
    contract = Contract(**data)
    contracts.append(contract)
    return jsonify(data), 201

@app.route('/managers', methods=['POST'])
def create_manager():
    data = request.json
    schema = load_schema('manager')
    
    manager = Manager(**data)
    managers.append(manager)
    return jsonify(data), 201

@app.route('/contractors', methods=['POST'])
def create_contractor():
    data = request.json
    schema = load_schema('contractor')
    
    contractor = Contractor(**data)
    contractors.append(contractor)
    return jsonify(data), 201

if __name__ == '__main__':
    app.run(debug=True)
