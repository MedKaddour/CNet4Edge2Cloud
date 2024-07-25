#!/bin/bash

# Define ports for the services
MANAGER_PORT=5001
CONTRACTOR1_PORT=5002
CONTRACTOR2_PORT=5003
CONTRACTOR3_PORT=5004

# Function to kill process on a specific port
kill_process_on_port() {
    PORT=$1
    PID=$(lsof -t -i:$PORT)
    if [ -n "$PID" ]; then
        echo "Killing process $PID on port $PORT..."
        kill -9 $PID
        echo "Process on port $PORT stopped."
    else
        echo "No process found on port $PORT."
    fi
}

# Stop Manager
echo "Stopping Manager service on port $MANAGER_PORT..."
kill_process_on_port $MANAGER_PORT

# Stop Contractors
echo "Stopping Contractor services on ports $CONTRACTOR1_PORT, $CONTRACTOR2_PORT, and $CONTRACTOR3_PORT..."
kill_process_on_port $CONTRACTOR1_PORT
kill_process_on_port $CONTRACTOR2_PORT
kill_process_on_port $CONTRACTOR3_PORT

echo "All specified services have been stopped."
