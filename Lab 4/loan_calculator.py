"""
Loan Calculator Module for Bank Loan Management System
Author: Assistant
Date: 2024

This module contains functions to calculate loan payments, interest, and affordability checks.
"""

import math


def calculate_monthly_payment(principal, annual_rate, term_years):
    """
    Calculate monthly payment using the standard loan formula:
    M = P × r × (1 + r)^n / ((1 + r)^n - 1)

    Where:
    - M = Monthly payment
    - P = Principal (loan amount)
    - r = Monthly interest rate (annual_rate / 100 / 12)
    - n = Total number of payments (term_years * 12)

    Args:
        principal (float): Loan amount (P)
        annual_rate (float): Annual interest rate as percentage
        term_years (int): Loan term in years

    Returns:
        float: Monthly payment amount

    Raises:
        ValueError: If inputs are invalid
    """
    # Input validation
    if principal <= 0:
        raise ValueError("Principal must be positive")
    if annual_rate < 0:
        raise ValueError("Annual rate cannot be negative")
    if term_years <= 0:
        raise ValueError("Term years must be positive")

    # Handle zero interest rate case
    if annual_rate == 0:
        return principal / (term_years * 12)

    # Calculate monthly rate (r)
    monthly_rate = annual_rate / 100 / 12

    # Calculate number of payments (n)
    num_payments = term_years * 12

    # Apply the loan formula: M = P × r × (1 + r)^n / ((1 + r)^n - 1)
    monthly_payment = (
        principal * monthly_rate * (1 + monthly_rate) ** num_payments
    ) / ((1 + monthly_rate) ** num_payments - 1)

    return round(monthly_payment, 2)


def calculate_total_interest(monthly_payment, principal, term_years):
    """
    Calculate total interest paid over the loan term

    Args:
        monthly_payment (float): Monthly payment amount
        principal (float): Loan amount (principal)
        term_years (int): Loan term in years

    Returns:
        float: Total interest amount

    Raises:
        ValueError: If inputs are invalid
    """
    # Input validation
    if monthly_payment <= 0:
        raise ValueError("Monthly payment must be positive")
    if principal <= 0:
        raise ValueError("Principal must be positive")
    if term_years <= 0:
        raise ValueError("Term years must be positive")

    # Calculate total payments made
    total_payments = monthly_payment * term_years * 12

    # Total interest = Total payments - Principal
    total_interest = total_payments - principal

    return round(total_interest, 2)


def check_affordability(monthly_payment, monthly_income, loan_type):
    """
    Check if the loan is affordable based on payment-to-income ratio

    Args:
        monthly_payment (float): Monthly payment amount
        monthly_income (float): Monthly income
        loan_type (str): Type of loan (Housing, Auto, Personal)

    Returns:
        dict: Dictionary containing affordability analysis:
            - is_affordable (bool): Whether loan is affordable
            - payment_ratio (float): Payment as percentage of income
            - message (str): Affordability message
            - suggestions (list): List of suggestions if not affordable
    """
    if monthly_income <= 0:
        raise ValueError("Monthly income must be positive")
    if monthly_payment <= 0:
        raise ValueError("Monthly payment must be positive")

    # Calculate payment-to-income ratio
    payment_ratio = (monthly_payment / monthly_income) * 100

    # Define affordability thresholds by loan type
    affordability_thresholds = {
        "Housing": 0.30,  # 30% of income
        "Auto": 0.15,  # 15% of income
        "Personal": 0.20,  # 20% of income
    }

    # Get threshold for loan type (default to 25% if not found)
    max_ratio = affordability_thresholds.get(loan_type, 0.25)

    # Check if payment exceeds 50% of income (critical threshold)
    critical_threshold = 0.50

    suggestions = []

    if payment_ratio > critical_threshold * 100:
        # Critical case: payment > 50% of income
        is_affordable = False
        message = f"❌ CRITICAL: Monthly payment (${monthly_payment:,.2f}) exceeds 50% of your income (${monthly_income:,.2f})"

        suggestions.extend(
            [
                "• Significantly reduce the loan amount",
                "• Extend the loan term (if within limits)",
                "• Consider a different loan type with lower rates",
                "• Improve your credit score for better rates",
                "• Consider a co-signer",
            ]
        )

    elif payment_ratio > max_ratio * 100:
        # Above recommended threshold
        is_affordable = False
        message = f"⚠️  WARNING: Monthly payment (${monthly_payment:,.2f}) exceeds recommended {max_ratio*100:.0f}% of income for {loan_type.lower()} loans"

        suggestions.extend(
            [
                "• Consider extending the loan term",
                "• Reduce the loan amount",
                "• Shop for better interest rates",
                "• Consider a smaller down payment to reduce loan amount",
            ]
        )

    else:
        # Affordable
        is_affordable = True
        message = f"✅ APPROVED: Monthly payment (${monthly_payment:,.2f}) is {payment_ratio:.1f}% of income, which is within acceptable limits"

    return {
        "is_affordable": is_affordable,
        "payment_ratio": payment_ratio,
        "message": message,
        "suggestions": suggestions,
    }


def suggest_term_adjustment(
    principal, annual_rate, monthly_income, loan_type, current_term
):
    """
    Suggest optimal loan term based on affordability

    Args:
        principal (float): Loan amount
        annual_rate (float): Annual interest rate as percentage
        monthly_income (float): Monthly income
        loan_type (str): Type of loan
        current_term (int): Current loan term in years

    Returns:
        dict: Dictionary containing term suggestions:
            - optimal_term (int): Suggested optimal term
            - monthly_payment (float): Payment with optimal term
            - total_interest (float): Total interest with optimal term
            - message (str): Explanation of suggestion
    """
    # Define maximum terms by loan type
    max_terms = {"Housing": 25, "Auto": 6, "Personal": 10}

    max_term = max_terms.get(loan_type, 10)

    # Define affordability thresholds
    affordability_thresholds = {"Housing": 0.30, "Auto": 0.15, "Personal": 0.20}

    target_ratio = affordability_thresholds.get(loan_type, 0.25)
    max_affordable_payment = monthly_income * target_ratio

    # Find optimal term
    optimal_term = current_term

    # Try extending term to reduce payment
    for term in range(current_term + 1, max_term + 1):
        try:
            payment = calculate_monthly_payment(principal, annual_rate, term)
            if payment <= max_affordable_payment:
                optimal_term = term
            else:
                break
        except ValueError:
            break

    # Calculate details for optimal term
    optimal_payment = calculate_monthly_payment(principal, annual_rate, optimal_term)
    optimal_interest = calculate_total_interest(
        optimal_payment, principal, optimal_term
    )

    if optimal_term > current_term:
        message = f"💡 SUGGESTION: Extend loan term to {optimal_term} years to reduce monthly payment to ${optimal_payment:,.2f}"
    else:
        message = f"✅ Current term of {current_term} years is optimal"

    return {
        "optimal_term": optimal_term,
        "monthly_payment": optimal_payment,
        "total_interest": optimal_interest,
        "message": message,
    }


def calculate_loan_summary(
    principal, annual_rate, term_years, monthly_income, loan_type
):
    """
    Calculate comprehensive loan summary with affordability analysis

    Args:
        principal (float): Loan amount
        annual_rate (float): Annual interest rate as percentage
        term_years (int): Loan term in years
        monthly_income (float): Monthly income
        loan_type (str): Type of loan

    Returns:
        dict: Complete loan analysis
    """
    # Calculate basic loan details
    monthly_payment = calculate_monthly_payment(principal, annual_rate, term_years)
    total_interest = calculate_total_interest(monthly_payment, principal, term_years)
    total_amount = principal + total_interest

    # Check affordability
    affordability = check_affordability(monthly_payment, monthly_income, loan_type)

    # Get term suggestions if needed
    term_suggestion = suggest_term_adjustment(
        principal, annual_rate, monthly_income, loan_type, term_years
    )

    return {
        "principal": principal,
        "annual_rate": annual_rate,
        "term_years": term_years,
        "monthly_payment": monthly_payment,
        "total_interest": total_interest,
        "total_amount": total_amount,
        "monthly_income": monthly_income,
        "loan_type": loan_type,
        "affordability": affordability,
        "term_suggestion": term_suggestion,
        "num_payments": term_years * 12,
    }


def display_loan_calculation(loan_summary):
    """
    Display formatted loan calculation results

    Args:
        loan_summary (dict): Loan summary from calculate_loan_summary()
    """
    print("\n" + "=" * 60)
    print("           LOAN CALCULATION RESULTS")
    print("=" * 60)

    # Basic loan information
    print(f"\n📋 LOAN DETAILS:")
    print(f"   Loan Type: {loan_summary['loan_type']}")
    print(f"   Principal Amount: ${loan_summary['principal']:,.2f}")
    print(f"   Annual Interest Rate: {loan_summary['annual_rate']:.2f}%")
    print(
        f"   Loan Term: {loan_summary['term_years']} years ({loan_summary['num_payments']} payments)"
    )

    # Payment information
    print(f"\n💰 PAYMENT INFORMATION:")
    print(f"   Monthly Payment: ${loan_summary['monthly_payment']:,.2f}")
    print(f"   Total Interest: ${loan_summary['total_interest']:,.2f}")
    print(f"   Total Amount to Pay: ${loan_summary['total_amount']:,.2f}")

    # Affordability analysis
    affordability = loan_summary["affordability"]
    print(f"\n✅ AFFORDABILITY ANALYSIS:")
    print(f"   {affordability['message']}")
    print(f"   Payment-to-Income Ratio: {affordability['payment_ratio']:.1f}%")

    if not affordability["is_affordable"] and affordability["suggestions"]:
        print(f"\n💡 SUGGESTIONS:")
        for suggestion in affordability["suggestions"]:
            print(f"   {suggestion}")

    # Term suggestion
    term_suggestion = loan_summary["term_suggestion"]
    if term_suggestion["optimal_term"] != loan_summary["term_years"]:
        print(f"\n📅 TERM OPTIMIZATION:")
        print(f"   {term_suggestion['message']}")
        print(f"   Optimized Payment: ${term_suggestion['monthly_payment']:,.2f}")
        print(
            f"   Additional Interest: ${term_suggestion['total_interest'] - loan_summary['total_interest']:,.2f}"
        )

    print("\n" + "=" * 60)


if __name__ == "__main__":
    # Test the calculator functions
    print("Testing Loan Calculator Module")
    print("=" * 40)

    # Test cases
    test_cases = [
        {
            "principal": 200000,
            "annual_rate": 4.5,
            "term_years": 30,
            "monthly_income": 8000,
            "loan_type": "Housing",
        },
        {
            "principal": 25000,
            "annual_rate": 3.2,
            "term_years": 5,
            "monthly_income": 6000,
            "loan_type": "Auto",
        },
        {
            "principal": 15000,
            "annual_rate": 8.5,
            "term_years": 3,
            "monthly_income": 4000,
            "loan_type": "Personal",
        },
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- TEST CASE {i} ---")
        loan_summary = calculate_loan_summary(**test_case)
        display_loan_calculation(loan_summary)

    # Test individual functions
    print(f"\n--- INDIVIDUAL FUNCTION TESTS ---")

    # Test monthly payment calculation
    payment = calculate_monthly_payment(100000, 5.0, 30)
    print(f"Monthly payment for $100,000 at 5% for 30 years: ${payment:,.2f}")

    # Test total interest calculation
    interest = calculate_total_interest(payment, 100000, 30)
    print(f"Total interest: ${interest:,.2f}")

    # Test affordability check
    affordability = check_affordability(payment, 5000, "Housing")
    print(f"Affordable for $5,000/month income: {affordability['is_affordable']}")
    print(f"Payment ratio: {affordability['payment_ratio']:.1f}%")
