# Distributed Task Management System

This application is a distributed task management system implemented using Flask. The system consists of a manager and multiple contractors that handle task execution. Tasks can be scheduled based on different deployment types such as Random, FIFO, Round-Robin, and Contract Net Protocol (CNET).

## Features

- **Task Execution:** Contractors can execute a list of system tasks (e.g., `ps`, `echo`, `ifconfig`) and return the results.
- **Dynamic Contractor Registration:** Contractors register themselves with the manager and can be assigned tasks.
- **Flexible Scheduling:** Supports different scheduling algorithms for task distribution (Random, FIFO, Round-Robin, CNET).

## Components

1. **Manager:** Handles the creation of call for proposals, bids, and contracts.
2. **Contractors:** Execute tasks and register themselves with the manager.

## Endpoints

### Manager

- `/call_for_proposals` (POST): Create a call for proposal.
- `/bids` (POST): Create a bid.
- `/contracts` (POST): Create a contract.
- `/managers` (POST): Register a manager.
- `/contractors` (POST): Register a contractor.

### Contractor

- `/execute_task` (POST): Execute a list of tasks.

## Getting Started

### Prerequisites

- Python 3.9+
- Flask
- Requests

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/MedKaddour/CNet4Edge2Cloud.git
   cd CNet4Edge2Cloud/ContractNetPro
