import json
import uuid

# Retrieve user transactions for a specified number of days and optional category.
def get_transactions(days, category=None):

    # This is a mock transactions. We need to add more
    transactions = [
        {"date": "2023-06-01", "amount": 50.00, "category": "groceries"},
        {"date": "2023-06-02", "amount": 30.00, "category": "entertainment"},
        {"date": "2023-06-03", "amount": 100.00, "category": "utilities"}
    ]
    
    if category:
        transactions = [t for t in transactions if t['category'] == category]
    
    return json.dumps(transactions)

# Create an appointment based on the provided case data.
def createAppointment(casedata):
    
    # Generate a unique ID for the appointment
    appointment_id = str(uuid.uuid4())
    return json.dumps({
        "appointment_id": appointment_id,
        "message": "Appointment created",
        "casedata": casedata
    })

# Execute a function based on its name and provided arguments.
def execute_function(function_name, kwargs):
      
    if function_name == "get_transactions":
        return get_transactions(**kwargs)
    elif function_name == "createAppointment":
        return createAppointment(**kwargs)
    else:
        return json.dumps({"error": "Function not found"})