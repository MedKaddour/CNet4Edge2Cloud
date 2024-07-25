#!/bin/bash

# Define ports for the services
MANAGER_PORT=5001
CONTRACTOR1_PORT=5002
CONTRACTOR2_PORT=5003
CONTRACTOR3_PORT=5004

# Define the path to the Python files
MANAGER_SCRIPT="manager.py"
CONTRACTOR_SCRIPT="contractor.py"
LOCUST_SCRIPT="locustfile.py"

# Define the manager endpoint
MANAGER_ENDPOINT="127.0.0.1:$MANAGER_PORT"

# Launch Manager
echo "Starting Manager service on port $MANAGER_PORT..."
nohup python $MANAGER_SCRIPT --port $MANAGER_PORT > manager.log 2>&1 &

# Launch Contractors
echo "Starting Contractor services on ports $CONTRACTOR1_PORT, $CONTRACTOR2_PORT, and $CONTRACTOR3_PORT..."

nohup python $CONTRACTOR_SCRIPT --port $CONTRACTOR1_PORT --manager $MANAGER_ENDPOINT > contractor1.log 2>&1 &
nohup python $CONTRACTOR_SCRIPT --port $CONTRACTOR2_PORT --manager $MANAGER_ENDPOINT > contractor2.log 2>&1 &
nohup python $CONTRACTOR_SCRIPT --port $CONTRACTOR3_PORT --manager $MANAGER_ENDPOINT > contractor3.log 2>&1 &

# Wait a few seconds to ensure services are up
sleep 5

# Launch Locust
echo "Starting Locust load test..."
nohup locust -f $LOCUST_SCRIPT --host http://127.0.0.1:$MANAGER_PORT > locust.log 2>&1 &

# Print the status
echo "Manager and Contractor services have been launched."
echo "Locust load test has been started."
echo "Logs are available in manager.log, contractor1.log, contractor2.log, contractor3.log, and locust.log."
