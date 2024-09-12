import pandas as pd
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def populate_customer_data(data):
    """
    Analyzes customer data
    """
    # Personal Details Analysis
    dob = datetime.strptime(data["dateOfBirth"], "%Y-%m-%d")
    age = (datetime.now() - dob).days // 365

    personal_info = {
        "First Name": data["firstName"],
        "Last Name": data["lastName"],
        "Age": age,
        "Gender": data["gender"],
        "Marital Status": data["maritalStatus"],
        "Dependents": data["dependents"]
    }

    # Financial Summary
    financial_summary = {
        "Credit Score": data["creditScore"],
        "Checking Account Balance": data["account_checking_balance"],
        "Savings Account Balance": data["account_savings_balance"],
        "Immovable Assets": data["immovable_assets"]
    }

    # Loan Details
    loan_details = {
        "Principal": data["loan_mortgage_principal"],
        "Remaining Balance": data["loan_mortgage_remainingBalance"],
        "Interest Rate": data["loan_mortgage_interestRate"],
        "Start Date": data["loan_mortgage_startDate"],
        "End Date": data["loan_mortgage_endDate"]
    }

    # Transaction Analysis
    transactions = pd.DataFrame(data["transactions"])

    # Total Spending
    total_spending = transactions['amount'].sum()

    # Categorized Spending
    categorized_spending = transactions.groupby('categoryType')['amount'].sum()

    # Daily Spending Trends
    transactions['date'] = pd.to_datetime(transactions['date'])
    daily_spending = transactions.groupby(transactions['date'].dt.date)['amount'].sum()

    # Summary
    logger.error(f"Personal Information: {personal_info}")
    logger.error(f"Financial Summary: {financial_summary}")
    logger.error(f"Loan Details: {loan_details}")
    logger.error(f"Total Spending: {total_spending}")
    logger.error(f"Categorized Spending: {categorized_spending}" )
    logger.error(f"Daily Spending Trends: {daily_spending}")