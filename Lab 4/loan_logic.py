"""
Bank Loan Management System - Logic Layer
Contains all calculation and validation functions
"""

# Loan types with their interest rates and maximum terms (as per requirements)
LOAN_TYPES = {
    "Housing": {"rate": 5.2, "max_term": 25},
    "Auto": {"rate": 7.5, "max_term": 6},
    "Personal": {"rate": 9.6, "max_term": 10}
}


def validate_loan_amount(amount_str):
    """
    Validate loan amount input
    Returns: (is_valid, error_message)
    """
    try:
        amount = float(amount_str)
        if amount <= 0:
            return False, "Loan amount must be greater than zero"
        if amount > 10000000:
            return False, "Loan amount cannot exceed $10,000,000"
        return True, None
    except ValueError:
        return False, "Please enter a valid number"


def validate_term(term_str, loan_type):
    """
    Validate loan term based on loan type
    Returns: (is_valid, error_message)
    """
    try:
        term = int(term_str)
        if term <= 0:
            return False, "Term must be greater than zero"
        
        max_term = LOAN_TYPES[loan_type]["max_term"]
        if term > max_term:
            return False, f"Term cannot exceed {max_term} years for {loan_type} loans"
        
        return True, None
    except ValueError:
        return False, "Please enter a valid whole number for years"


def validate_income(income_str):
    """
    Validate monthly income input
    Returns: (is_valid, error_message)
    """
    try:
        income = float(income_str)
        if income <= 0:
            return False, "Monthly income must be greater than zero"
        if income < 500:
            return False, "Monthly income must be at least $500"
        return True, None
    except ValueError:
        return False, "Please enter a valid number"


def calculate_monthly_payment(principal, annual_rate, years):
    """
    Calculate monthly loan payment using the amortization formula
    Formula: M = P[r(1+r)^n]/[(1+r)^n-1]
    Where:
        M = Monthly payment
        P = Principal (loan amount)
        r = Monthly interest rate (annual rate / 12 / 100)
        n = Number of payments (years * 12)
    """
    # Convert annual rate to monthly decimal rate
    r = annual_rate / 100 / 12
    n = years * 12
    
    # Handle zero interest case
    if r == 0:
        return principal / n
    
    # Amortization formula as specified in the requirements
    monthly_payment = principal * r * (1 + r) ** n / ((1 + r) ** n - 1)
    
    return round(monthly_payment, 2)


def calculate_total_interest(monthly_payment, principal, years):
    """
    Calculate total interest paid over the life of the loan
    """
    total_paid = monthly_payment * years * 12
    total_interest = total_paid - principal
    return round(total_interest, 2)


def check_affordability(monthly_payment, monthly_income):
    """
    Check if the loan is affordable based on payment-to-income ratio
    General rule: Monthly payment should not exceed 50% of monthly income
    """
    payment_ratio = (monthly_payment / monthly_income) * 100
    is_affordable = payment_ratio <= 50
    max_affordable_payment = monthly_income * 0.5
    
    return {
        "is_affordable": is_affordable,
        "payment_ratio": round(payment_ratio, 2),
        "max_payment": round(max_affordable_payment, 2)
    }


def calculate_loan_eligibility(loan_amount, monthly_income, credit_score=None):
    """
    Calculate basic loan eligibility
    This is a simplified version - real banks use complex algorithms
    """
    # Rule: Total loan should not exceed 5 years of income
    max_loan = monthly_income * 12 * 5
    
    eligibility = {
        "eligible": loan_amount <= max_loan,
        "max_eligible_loan": round(max_loan, 2),
        "reason": ""
    }
    
    if not eligibility["eligible"]:
        eligibility["reason"] = f"Loan amount exceeds maximum eligible amount of ${max_loan:,.2f}"
    else:
        eligibility["reason"] = "Loan amount within eligible range"
    
    return eligibility


def format_currency(amount):
    """
    Format number as currency
    """
    return f"${amount:,.2f}"


def get_loan_summary(loan_type, loan_amount, term_years, monthly_income):
    """
    Generate complete loan summary with all calculations
    """
    interest_rate = LOAN_TYPES[loan_type]["rate"]
    
    # Calculate all values
    monthly_payment = calculate_monthly_payment(loan_amount, interest_rate, term_years)
    total_interest = calculate_total_interest(monthly_payment, loan_amount, term_years)
    total_amount = loan_amount + total_interest
    affordability = check_affordability(monthly_payment, monthly_income)
    eligibility = calculate_loan_eligibility(loan_amount, monthly_income)
    
    summary = {
        "loan_type": loan_type,
        "loan_amount": loan_amount,
        "interest_rate": interest_rate,
        "term_years": term_years,
        "monthly_payment": monthly_payment,
        "total_interest": total_interest,
        "total_amount": total_amount,
        "affordability": affordability,
        "eligibility": eligibility,
        "monthly_income": monthly_income
    }
    
    return summary
