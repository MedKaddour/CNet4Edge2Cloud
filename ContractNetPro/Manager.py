import argparse
import random
import threading
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
deployment_type = ""
contractor_id_counter = 1
round_robin_index = 1

# Create a lock for thread-safe operations
lock = threading.Lock()

# Helper function to load JSON schemas
def load_schema(schema_name):
    with open(os.path.join('schemas', f'{schema_name}.json')) as schema_file:
        return json.load(schema_file)

# Function to send a task to a contractor's endpoint
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
    global round_robin_index
    data = request.json

    if deployment_type == "RAND":
        # Randomly assign tasks to contractors
        contractor_endpoints = list(contractors.keys())
        if contractor_endpoints:
            chosen_contractor = random.choice(contractor_endpoints)
            send_task_to_contractor(data, chosen_contractor)

    elif deployment_type == "FIFO":
        # Assign tasks to contractors in the order they were added
        if contractors:
            sorted_contractors = dict(sorted(contractors.items(), key=lambda item: item[1].contractor_id))
            for endpoint in sorted_contractors.keys():
                if sorted_contractors[endpoint].available:
                    send_task_to_contractor(data, endpoint)
                    break

    elif deployment_type == "RR":
        # Distribute tasks in a round-robin fashion
        if contractors:
            with lock:
                contractor_endpoints = list(contractors.keys())
                chosen_contractor = contractor_endpoints[round_robin_index - 1]
                round_robin_index = (round_robin_index % len(contractor_endpoints)) + 1
                send_task_to_contractor(data, chosen_contractor)

    elif deployment_type == "CNET":
        # Assign tasks based on Contract Net Protocol
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
def register_contractor():
    global contractor_id_counter
    data = request.json
    schema = load_schema('contractor')
    # Validate data against schemas (validation code can be added here)
    data["contractor_id"] = contractor_id_counter
    contractor_id_counter += 1
    contractor = Contractor(**data)
    contractors[str(contractor.endpoint)] = contractor
    return jsonify(data), 201

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Flask server with specified options.')
    parser.add_argument('--host', default='127.0.0.1', help='Hostname to listen on (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5001, help='Port to listen on (default: 5001)')
    parser.add_argument('--deployment-type', default='RR', help='Type of deployment (e.g., RAND, FIFO, RR, CNET)')
    args = parser.parse_args()
    deployment_type = args.deployment_type
    app.run(host=args.host, port=args.port, debug=True)
