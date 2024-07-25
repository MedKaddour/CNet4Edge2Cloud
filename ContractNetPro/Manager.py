import argparse
import random

import requests
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
contractors = {}
type_of_deployment=""
contractors_idx=1
# Helper function to load schemas
def load_schema(schema_name):
    with open(os.path.join('schemas', f'{schema_name}.json')) as schema_file:
        return json.load(schema_file)
def send_task_to_contractor(task, contractor_endpoint):
    try:
        response = requests.post(f'http://{contractor_endpoint}/execute_task', json=task)
        if response.status_code == 200:
            print(f"Task sent to {contractor_endpoint} successfully.")
        else:
            print(f"Failed to send task to {contractor_endpoint}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while sending task to {contractor_endpoint}: {e}")
@app.route('/create_cfp', methods=['POST'])
def create_call_for_proposal():
    data = request.json

    if type_of_deployment == "RAND":
        # Randomly assign tasks to contractors
        contractor_endpoints = list(contractors.keys())
        if contractor_endpoints:
            chosen_contractor = random.choice(contractor_endpoints)
            send_task_to_contractor(data, chosen_contractor)

    elif type_of_deployment == "FIFO":
        # Assign tasks to contractors in the order they were added
        sorted_contractors = dict(sorted(contractors.items(), key=lambda item: item[1].contractor_id))
        for contractor in sorted_contractors:
            if contractor.available:
                send_task_to_contractor(data, contractor)
                break
            else :
                continue

    elif type_of_deployment == "RR":
        # Distribute tasks in a round-robin fashion
        contractor_endpoints = list(contractors.keys())
        for i, task in enumerate(data):
            chosen_contractor = contractor_endpoints[i % len(contractor_endpoints)]
            send_task_to_contractor(task, chosen_contractor)

    elif type_of_deployment == "CNET":
        # Assign tasks based on Contract Net Protocol
        # For simplicity, assume all contractors can handle all tasks

        best_bid = None
        best_contractor = None
        for contractor in contractors.values():
            bid = contractor.bid_for_task(data)
            if best_bid is None or bid < best_bid:
                best_bid = bid
                best_contractor = contractor
        if best_contractor:
            send_task_to_contractor(data, best_contractor.endpoint)

    schema = load_schema('call_for_proposal')
    # Validate data against schemas (validation code can be added here)
    #call_for_proposal = CallForProposal(**data)
    #call_for_proposals.append(call_for_proposal)
    return jsonify(data), 201

@app.route('/bids', methods=['POST'])
def create_bid():
    data = request.json
    schema = load_schema('bid')
    # Validate data against schemas (validation code can be added here)
    bid = Bid(**data)
    bids.append(bid)
    return jsonify(data), 201


@app.route('/managers', methods=['POST'])
def create_manager():
    data = request.json
    schema = load_schema('manager')
    # Validate data against schemas (validation code can be added here)
    manager = Manager(**data)
    managers.append(manager)
    return jsonify(data), 201

@app.route('/contractors', methods=['POST'])
def create_contractor():
    global contractors_idx
    data = request.json
    schema = load_schema('contractor')
    # Validate data against schemas (validation code can be added here)
    print(data)
    data["contractor_id"]=contractors_idx
    contractors_idx+=1
    contractor = Contractor(**data)
    contractors[str(contractor.endpoint)]=contractor
    return jsonify(data), 201

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Flask server with specified options.')
    parser.add_argument('--host', default='127.0.0.1', help='Hostname to listen on (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5001, help='Port to listen on (default: 5001)')
    parser.add_argument('--tod',  default='RAND', help='type of deployement')
    args = parser.parse_args()
    type_of_deployment=args.tod
    app.run(host=args.host, port=args.port, debug=True)
