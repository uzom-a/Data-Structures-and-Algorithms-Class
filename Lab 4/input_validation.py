"""
Input Validation Module for Bank Loan Management System
Author: Assistant
Date: 2024

This module contains functions to validate user inputs for loan applications.
"""

# Loan type configurations
LOAN_CONFIGS = {
    "Housing": {
        "min_amount": 50000,
        "max_amount": 2000000,
        "min_term": 5,
        "max_term": 25,  # Updated to 25 years
        "min_income_ratio": 0.25,  # Monthly payment should not exceed 25% of income
        "min_monthly_income": 3000,
    },
    "Auto": {
        "min_amount": 5000,
        "max_amount": 100000,
        "min_term": 1,
        "max_term": 6,  # Updated to 6 years
        "min_income_ratio": 0.15,  # Monthly payment should not exceed 15% of income
        "min_monthly_income": 2000,
    },
    "Personal": {
        "min_amount": 1000,
        "max_amount": 50000,
        "min_term": 1,
        "max_term": 10,  # Updated to 10 years
        "min_income_ratio": 0.20,  # Monthly payment should not exceed 20% of income
        "min_monthly_income": 1500,
    },
}


def validate_loan_type(choice):
    """
    Validate loan type selection

    Args:
        choice (str): User's choice for loan type

    Returns:
        bool: True if valid, False otherwise
    """
    if not choice:
        return False

    # Check if choice is a valid option
    valid_choices = ["1", "2", "3"]
    return choice in valid_choices


def validate_loan_amount(amount, loan_type):
    """
    Validate loan amount based on loan type

    Args:
        amount (float): Loan amount requested
        loan_type (str): Type of loan (Housing, Auto, Personal)

    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(amount, (int, float)):
        return False

    if amount <= 0:
        print(f"❌ Loan amount must be positive.")
        return False

    config = LOAN_CONFIGS.get(loan_type)
    if not config:
        print(f"❌ Invalid loan type: {loan_type}")
        return False

    min_amount = config["min_amount"]
    max_amount = config["max_amount"]

    if amount < min_amount:
        print(
            f"❌ Minimum loan amount for {loan_type.lower()} loans is ${min_amount:,}."
        )
        return False

    if amount > max_amount:
        print(
            f"❌ Maximum loan amount for {loan_type.lower()} loans is ${max_amount:,}."
        )
        return False

    return True


def validate_term(term_years, loan_type):
    """
    Validate loan term based on loan type

    Args:
        term_years (int or float): Loan term in years
        loan_type (str): Type of loan (Housing, Auto, Personal)

    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(term_years, (int, float)):
        return False

    if term_years <= 0:
        print("❌ Loan term must be positive.")
        return False

    config = LOAN_CONFIGS.get(loan_type)
    if not config:
        print(f"❌ Invalid loan type: {loan_type}")
        return False

    min_term = config["min_term"]
    max_term = config["max_term"]

    if term_years < min_term:
        print(f"❌ Minimum term for {loan_type.lower()} loans is {min_term} years.")
        return False

    if term_years > max_term:
        print(f"❌ Maximum term for {loan_type.lower()} loans is {max_term} years.")
        return False

    return True


def validate_income(monthly_income):
    """
    Validate monthly income

    Args:
        monthly_income (float): Monthly income amount

    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(monthly_income, (int, float)):
        return False

    if monthly_income <= 0:
        print("❌ Monthly income must be positive.")
        return False

    if monthly_income < 1000:
        print("❌ Minimum monthly income required is $1,000.")
        return False

    return True


def validate_affordability(
    loan_amount, term_years, monthly_income, loan_type, monthly_payment
):
    """
    Validate if the loan is affordable based on income and payment ratio

    Args:
        loan_amount (float): Loan amount
        term_years (int): Loan term in years
        monthly_income (float): Monthly income
        loan_type (str): Type of loan
        monthly_payment (float): Calculated monthly payment

    Returns:
        tuple: (is_affordable, message)
    """
    config = LOAN_CONFIGS.get(loan_type)
    if not config:
        return False, f"Invalid loan type: {loan_type}"

    # Check minimum income requirement
    min_income = config["min_monthly_income"]
    if monthly_income < min_income:
        return (
            False,
            f"Minimum monthly income for {loan_type.lower()} loans is ${min_income:,}.",
        )

    # Check payment-to-income ratio
    max_ratio = config["min_income_ratio"]
    payment_ratio = monthly_payment / monthly_income

    if payment_ratio > max_ratio:
        max_affordable_payment = monthly_income * max_ratio
        return False, (
            f"Monthly payment (${monthly_payment:.2f}) exceeds {max_ratio*100:.0f}% of your income.\n"
            f"Maximum affordable payment: ${max_affordable_payment:.2f}"
        )

    return True, "Loan is affordable based on your income."


def get_loan_config(loan_type):
    """
    Get loan configuration for a specific loan type

    Args:
        loan_type (str): Type of loan

    Returns:
        dict: Loan configuration or None if invalid
    """
    return LOAN_CONFIGS.get(loan_type)


def clean_numeric_input(user_input):
    """
    Clean and parse numeric input by removing common formatting

    Args:
        user_input (str): Raw user input

    Returns:
        float: Cleaned numeric value

    Raises:
        ValueError: If input cannot be converted to a valid number
    """
    if not user_input:
        raise ValueError("Input cannot be empty")

    # Remove common formatting characters
    cleaned = user_input.strip().replace(",", "").replace("$", "").replace("%", "")

    # Handle negative numbers
    if cleaned.startswith("-"):
        cleaned = cleaned[1:]  # Remove negative sign for now
        is_negative = True
    else:
        is_negative = False

    # Convert to float
    try:
        value = float(cleaned)
        return -value if is_negative else value
    except ValueError:
        raise ValueError(f"'{user_input}' is not a valid number")


def get_loan_type_input():
    """
    Get and validate loan type choice from user with clear prompts

    Returns:
        str: Validated loan type (Housing, Auto, Personal)
    """
    print("\n🏦 LOAN TYPE SELECTION")
    print("=" * 30)
    print("Please select the type of loan you need:")
    print("1. Housing Loan - For purchasing or refinancing a home")
    print("2. Auto Loan - For purchasing a vehicle")
    print("3. Personal Loan - For personal expenses, debt consolidation, etc.")

    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()

            if not choice:
                print("❌ Please enter a choice (1, 2, or 3).")
                continue

            if validate_loan_type(choice):
                loan_type_map = {"1": "Housing", "2": "Auto", "3": "Personal"}
                selected_type = loan_type_map[choice]
                print(f"✅ Selected: {selected_type} Loan")
                return selected_type
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")

        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            raise
        except Exception as e:
            print(f"❌ An error occurred: {e}")


def get_loan_amount_input(loan_type):
    """
    Get and validate loan amount from user with clear prompts

    Args:
        loan_type (str): Type of loan selected

    Returns:
        float: Validated loan amount
    """
    config = LOAN_CONFIGS[loan_type]
    min_amount = config["min_amount"]
    max_amount = config["max_amount"]

    print(f"\n💰 {loan_type.upper()} LOAN AMOUNT")
    print("=" * 30)
    print(f"Enter the loan amount you need:")
    print(f"• Minimum: ${min_amount:,}")
    print(f"• Maximum: ${max_amount:,}")

    while True:
        try:
            amount_input = input(f"\nEnter {loan_type.lower()} loan amount: $").strip()

            if not amount_input:
                print("❌ Please enter a loan amount.")
                continue

            loan_amount = clean_numeric_input(amount_input)

            if validate_loan_amount(loan_amount, loan_type):
                print(f"✅ Loan amount: ${loan_amount:,.2f}")
                return loan_amount
            else:
                print(
                    f"❌ Please enter a valid amount between ${min_amount:,} and ${max_amount:,}."
                )

        except ValueError as e:
            print(f"❌ Invalid input: {e}")
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            raise
        except Exception as e:
            print(f"❌ An error occurred: {e}")


def get_loan_term_input(loan_type):
    """
    Get and validate loan term from user with clear prompts

    Args:
        loan_type (str): Type of loan selected

    Returns:
        int: Validated loan term in years
    """
    config = LOAN_CONFIGS[loan_type]
    min_term = config["min_term"]
    max_term = config["max_term"]

    print(f"\n📅 {loan_type.upper()} LOAN TERM")
    print("=" * 30)
    print(f"Enter the loan term (duration) in years:")
    print(f"• Minimum: {min_term} years")
    print(f"• Maximum: {max_term} years")

    while True:
        try:
            term_input = input(
                f"\nEnter loan term in years ({min_term}-{max_term}): "
            ).strip()

            if not term_input:
                print("❌ Please enter a loan term.")
                continue

            term_years = int(clean_numeric_input(term_input))

            if validate_term(term_years, loan_type):
                print(f"✅ Loan term: {term_years} years")
                return term_years
            else:
                print(
                    f"❌ Please enter a valid term between {min_term} and {max_term} years."
                )

        except ValueError as e:
            print(f"❌ Invalid input: {e}")
            print("Please enter a whole number (e.g., 5, 10, 15).")
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            raise
        except Exception as e:
            print(f"❌ An error occurred: {e}")


def get_income_input():
    """
    Get and validate monthly income from user with clear prompts

    Returns:
        float: Validated monthly income
    """
    print(f"\n💵 MONTHLY INCOME")
    print("=" * 20)
    print("Enter your monthly income (before taxes):")
    print("• This helps us determine loan affordability")
    print("• Minimum required: $1,000/month")

    while True:
        try:
            income_input = input("\nEnter your monthly income: $").strip()

            if not income_input:
                print("❌ Please enter your monthly income.")
                continue

            monthly_income = clean_numeric_input(income_input)

            if validate_income(monthly_income):
                print(f"✅ Monthly income: ${monthly_income:,.2f}")
                return monthly_income
            else:
                print("❌ Please enter a valid monthly income (minimum $1,000).")

        except ValueError as e:
            print(f"❌ Invalid input: {e}")
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            raise
        except Exception as e:
            print(f"❌ An error occurred: {e}")


def get_all_loan_inputs():
    """
    Get all loan inputs from user with comprehensive validation and cleaning

    Returns:
        dict: Dictionary containing cleaned and validated inputs:
            - loan_type (str): Type of loan
            - loan_amount (float): Loan amount
            - term_years (int): Loan term in years
            - monthly_income (float): Monthly income
    """
    print("\n" + "=" * 60)
    print("        LOAN APPLICATION INPUT COLLECTION")
    print("=" * 60)
    print("We'll collect your loan information step by step.")
    print("All inputs will be validated to ensure accuracy.")

    try:
        # Get loan type
        loan_type = get_loan_type_input()

        # Get loan amount
        loan_amount = get_loan_amount_input(loan_type)

        # Get loan term
        term_years = get_loan_term_input(loan_type)

        # Get monthly income
        monthly_income = get_income_input()

        # Summary of inputs
        print(f"\n📋 INPUT SUMMARY")
        print("=" * 20)
        print(f"Loan Type: {loan_type}")
        print(f"Loan Amount: ${loan_amount:,.2f}")
        print(f"Loan Term: {term_years} years")
        print(f"Monthly Income: ${monthly_income:,.2f}")

        return {
            "loan_type": loan_type,
            "loan_amount": loan_amount,
            "term_years": term_years,
            "monthly_income": monthly_income,
        }

    except KeyboardInterrupt:
        print("\n\n❌ Loan application cancelled by user.")
        raise
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        raise


def display_loan_limits():
    """
    Display loan limits for all loan types

    Returns:
        str: Formatted string with loan limits
    """
    output = "\n📋 LOAN LIMITS AND REQUIREMENTS:\n"
    output += "=" * 50 + "\n"

    for loan_type, config in LOAN_CONFIGS.items():
        output += f"\n🏦 {loan_type.upper()} LOANS:\n"
        output += f"   • Amount Range: ${config['min_amount']:,} - ${config['max_amount']:,}\n"
        output += (
            f"   • Term Range: {config['min_term']} - {config['max_term']} years\n"
        )
        output += f"   • Minimum Income: ${config['min_monthly_income']:,}/month\n"
        output += (
            f"   • Max Payment Ratio: {config['min_income_ratio']*100:.0f}% of income\n"
        )

    return output


if __name__ == "__main__":
    # Test the validation functions
    print("Testing Input Validation Module")
    print("=" * 40)

    # Test loan type validation
    print(f"Valid loan type '1': {validate_loan_type('1')}")
    print(f"Invalid loan type '5': {validate_loan_type('5')}")

    # Test loan amount validation with new term limits
    print(f"Valid Housing loan amount: {validate_loan_amount(100000, 'Housing')}")
    print(f"Invalid Housing loan amount: {validate_loan_amount(10000, 'Housing')}")

    # Test term validation with updated limits
    print(f"Valid Auto loan term (6 years): {validate_term(6, 'Auto')}")
    print(f"Invalid Auto loan term (7 years): {validate_term(7, 'Auto')}")
    print(f"Valid Personal loan term (10 years): {validate_term(10, 'Personal')}")
    print(f"Invalid Personal loan term (11 years): {validate_term(11, 'Personal')}")
    print(f"Valid Housing loan term (25 years): {validate_term(25, 'Housing')}")
    print(f"Invalid Housing loan term (26 years): {validate_term(26, 'Housing')}")

    # Test income validation
    print(f"Valid income: {validate_income(5000)}")
    print(f"Invalid income: {validate_income(500)}")

    # Test input cleaning
    print("\nTesting input cleaning:")
    test_inputs = ["$1,000", "5000.50", "10,000", "25%", "-100", "abc"]
    for test_input in test_inputs:
        try:
            cleaned = clean_numeric_input(test_input)
            print(f"'{test_input}' -> {cleaned}")
        except ValueError as e:
            print(f"'{test_input}' -> Error: {e}")

    # Display loan limits
    print(display_loan_limits())

    # Test comprehensive input collection (commented out for automated testing)
    # print("\n" + "="*50)
    # print("Testing comprehensive input collection:")
    # print("="*50)
    # try:
    #     inputs = get_all_loan_inputs()
    #     print("Successfully collected all inputs!")
    #     print(f"Collected data: {inputs}")
    # except KeyboardInterrupt:
    #     print("Input collection cancelled by user.")
    # except Exception as e:
    #     print(f"Error during input collection: {e}")
