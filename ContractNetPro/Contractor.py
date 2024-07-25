import argparse
import threading
import time
import requests
from flask import Flask, request, jsonify
from models import CallForProposal, Bid, Contract, Manager, Contractor
import json
import os
import subprocess

app = Flask(__name__)

# In-memory storage
call_for_proposals = []
bids = []
contracts = []
managers = []
contractors = []
manager_endpoint = None


# Helper function to load JSON schemas
def load_schema(schema_name):
    with open(os.path.join('schemas', f'{schema_name}.json')) as schema_file:
        return json.load(schema_file)


# Function to execute a list of tasks
def do_task(tasks):
    results = []
    for task in tasks:
        try:
            # Execute the task using subprocess
            result = subprocess.run(task, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            results.append({
                'task': task,
                'status': 'successful',
                'output': result.stdout.decode('utf-8'),
                'error': result.stderr.decode('utf-8')
            })
        except subprocess.CalledProcessError as e:
            results.append({
                'task': task,
                'status': 'failed',
                'output': e.stdout.decode('utf-8') if e.stdout else '',
                'error': e.stderr.decode('utf-8') if e.stderr else str(e)
            })
    print(results)
    return results


@app.route('/execute_task', methods=['POST'])
def execute_tasks():
    data = request.json

    if not data or not isinstance(data.get('tasks'), list):
        return jsonify({'error': 'Invalid input data'}), 400

    tasks = data['tasks']

    # Start a new thread to execute the tasks
    task_thread = threading.Thread(target=do_task, args=(tasks,))
    task_thread.start()

    return jsonify({'message': 'Task execution started'}), 201


@app.route('/call_for_proposals', methods=['POST'])
def create_call_for_proposal():
    data = request.json
    schema = load_schema('call_for_proposal')
    # Validate data against schemas (validation code can be added here)
    call_for_proposal = CallForProposal(**data)
    call_for_proposals.append(call_for_proposal)
    return jsonify(data), 201


@app.route('/bids', methods=['POST'])
def create_bid():
    data = request.json
    schema = load_schema('bid')
    # Validate data against schemas (validation code can be added here)
    bid = Bid(**data)
    bids.append(bid)
    return jsonify(data), 201


@app.route('/contracts', methods=['POST'])
def create_contract():
    data = request.json
    schema = load_schema('contract')
    # Validate data against schemas (validation code can be added here)
    contract = Contract(**data)
    contracts.append(contract)
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
    data = request.json
    schema = load_schema('contractor')
    # Validate data against schemas (validation code can be added here)
    contractor = Contractor(**data)
    contractors.append(contractor)
    return jsonify(data), 201


def notify_manager():
    """Notify the manager about the contractor's existence."""
    if manager_endpoint:
        try:
            response = requests.post(f'http://{manager_endpoint}/contractors', json={
                "contractor_id": "some-id",
                "contractor_description": "some-description",
                "endpoint": f'{args.host}:{args.port}',
                "bid_id": "some-bid-id"
            })
            if response.status_code == 201:
                print("Successfully notified manager.")
            else:
                print(f"Failed to notify manager. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error notifying manager: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Flask server with specified options.')
    parser.add_argument('--host', default='127.0.0.1', help='Hostname to listen on (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000, help='Port to listen on (default: 5000)')
    parser.add_argument('--manager', default='127.0.0.1:5000', help='Manager endpoint (default: 127.0.0.1:5000)')
    args = parser.parse_args()
    manager_endpoint = args.manager

    # Wait for a few seconds before notifying the manager
    time.sleep(5)
    print("Notifying manager after server starts")

    # Notifying the manager after server starts
    notify_manager()

    # Start the Flask application
    app.run(host=args.host, port=args.port, debug=True)
