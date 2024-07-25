from datetime import datetime

class CallForProposal:
    def __init__(self, call_for_proposal_id, manager_id, manager_description,tasks, task_description,
                 contractor_selection_criterion, bid_selection_criterion, task_deadline, cfp_deadline, cfp_state):
        self.call_for_proposal_id = call_for_proposal_id
        self.manager_id = manager_id
        self.manager_description = manager_description
        self.tasks = tasks
        self.task_description = task_description
        self.contractor_selection_criterion = contractor_selection_criterion
        self.bid_selection_criterion = bid_selection_criterion
        self.task_deadline = datetime.strptime(task_deadline, "%Y-%m-%dT%H:%M:%S")
        self.cfp_deadline = datetime.strptime(cfp_deadline, "%Y-%m-%dT%H:%M:%S")
        self.cfp_state = cfp_state

class Bid:
    def __init__(self, bid_id, contractor_id, contractor_description, call_for_proposal_id, manager_id,
                 answer_criterion_cfp, answer_task_deadline, eligibility_bid, row_bid, bid_state):
        self.bid_id = bid_id
        self.contractor_id = contractor_id
        self.contractor_description = contractor_description
        self.call_for_proposal_id = call_for_proposal_id
        self.manager_id = manager_id
        self.answer_criterion_cfp = answer_criterion_cfp
        self.answer_task_deadline = datetime.strptime(answer_task_deadline, "%Y-%m-%dT%H:%M:%S")
        self.eligibility_bid = eligibility_bid
        self.row_bid = row_bid
        self.bid_state = bid_state

class Contract:
    def __init__(self, contract_id, manager_id, manager_description, contractor_id, contractor_description, bid_id,
                 contract_description, contract_state):
        self.contract_id = contract_id
        self.manager_id = manager_id
        self.manager_description = manager_description
        self.contractor_id = contractor_id
        self.contractor_description = contractor_description
        self.bid_id = bid_id
        self.contract_description = contract_description
        self.contract_state = contract_state

class Manager:
    def __init__(self, manager_id, manager_description, contractors_id, call_for_proposal_id, bids_id, contracts_id):
        self.manager_id = manager_id
        self.manager_description = manager_description
        self.contractors_id = contractors_id
        self.call_for_proposal_id = call_for_proposal_id
        self.bids_id = bids_id
        self.contracts_id = contracts_id

class Contractor:
    def __init__(self, contractor_id,endpoint, contractor_description, bid_id):
        self.contractor_id = contractor_id
        self.endpoint = endpoint
        self.contractor_description = contractor_description
        self.bid_id = bid_id
