"""
Bank Loan Management System - Main Program
Author: Assistant
Date: 2024

This program provides a comprehensive loan management system that allows users to:
- Select different loan types (Housing, Auto, Personal)
- Input loan details (amount, term, income)
- Validate inputs and calculate loan terms
- Display detailed loan summaries
- Save loan records to CSV files
"""

import sys
from input_validation import (
    validate_loan_amount,
    validate_term,
    validate_income,
    validate_loan_type,
    get_all_loan_inputs,
)
from loan_calculator import (
    calculate_monthly_payment,
    calculate_total_interest,
    check_affordability,
    calculate_loan_summary,
    display_loan_calculation,
)
from loan_summary import (
    display_loan_summary,
    process_loan_summary_and_save,
)
from utils import (
    format_currency,
    format_percentage,
    print_section_header,
    print_status_message,
    print_separator,
)


def get_loan_inputs():
    """
    Get loan inputs from user with validation using the comprehensive input collection

    Returns:
        dict: Dictionary containing validated loan inputs
    """
    return get_all_loan_inputs()


def process_loan_application():
    """Process a complete loan application with comprehensive error handling"""
    try:
        print_section_header("LOAN APPLICATION PROCESS")

        # Step 1: Get user inputs with validation
        print_status_message("Step 1: Collecting loan information", "info")
        loan_data = get_loan_inputs()

        # Step 2: Calculate loan details
        print_status_message("Step 2: Calculating loan details", "info")
        print(f"Calculating {loan_data['loan_type'].lower()} loan details...")

        # Use the comprehensive loan calculator
        loan_summary = calculate_loan_summary(
            principal=loan_data["loan_amount"],
            annual_rate=4.5,  # Default rate - in real system this would be calculated based on credit
            term_years=loan_data["term_years"],
            monthly_income=loan_data["monthly_income"],
            loan_type=loan_data["loan_type"],
        )

        # Step 3: Display comprehensive loan analysis
        print_status_message("Step 3: Analyzing loan affordability", "info")
        display_loan_calculation(loan_summary)

        # Step 4: Prepare data for summary and saving
        loan_record_data = {
            "loan_type": loan_data["loan_type"],
            "principal": loan_data["loan_amount"],
            "annual_rate": loan_summary["annual_rate"],
            "term_years": loan_data["term_years"],
            "monthly_payment": loan_summary["monthly_payment"],
            "total_interest": loan_summary["total_interest"],
            "status": (
                "Approved"
                if loan_summary["affordability"]["is_affordable"]
                else "Pending Review"
            ),
            "monthly_income": loan_data["monthly_income"],
            "affordability": loan_summary["affordability"],
        }

        # Step 5: Display summary and save record
        print_status_message("Step 4: Final review and record keeping", "info")
        if process_loan_summary_and_save(loan_record_data):
            print_status_message("Loan application completed and saved!", "success")
        else:
            print_status_message("Loan application completed but not saved", "warning")

        # Step 6: Final confirmation
        print_status_message("Step 5: Final confirmation", "info")
        while True:
            confirm = (
                input("\nDo you want to proceed with this loan? (yes/no): ")
                .lower()
                .strip()
            )
            if confirm in ["yes", "y"]:
                print_status_message(
                    "Congratulations! Your loan application has been submitted.",
                    "success",
                )
                print("A loan officer will contact you within 2-3 business days.")
                return True
            elif confirm in ["no", "n"]:
                print_status_message("Loan application cancelled.", "warning")
                return False
            else:
                print("Please enter 'yes' or 'no'.")

    except KeyboardInterrupt:
        print_status_message("Application process cancelled by user.", "warning")
        return False
    except Exception as e:
        print_status_message(f"An error occurred during loan processing: {e}", "error")
        print("Please contact technical support if this error persists.")
        return False


def run_sample_tests():
    """Run sample loan tests with predefined data"""
    print_section_header("SAMPLE LOAN TESTS")

    # Sample test data
    test_cases = [
        {
            "name": "Housing Loan Test",
            "loan_type": "Housing",
            "principal": 200000,
            "term_years": 20,
            "monthly_income": 6000,
            "annual_rate": 4.5,
        },
        {
            "name": "Auto Loan Test",
            "loan_type": "Auto",
            "principal": 30000,
            "term_years": 5,
            "monthly_income": 4000,
            "annual_rate": 3.2,
        },
        {
            "name": "Personal Loan Test",
            "loan_type": "Personal",
            "principal": 10000,
            "term_years": 8,
            "monthly_income": 2500,
            "annual_rate": 8.5,
        },
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"TEST CASE {i}: {test_case['name']}")
        print(f"{'='*60}")

        try:
            # Calculate loan details
            loan_summary = calculate_loan_summary(
                principal=test_case["principal"],
                annual_rate=test_case["annual_rate"],
                term_years=test_case["term_years"],
                monthly_income=test_case["monthly_income"],
                loan_type=test_case["loan_type"],
            )

            # Display results
            display_loan_calculation(loan_summary)

            # Prepare data for CSV saving
            loan_record_data = {
                "loan_type": test_case["loan_type"],
                "principal": test_case["principal"],
                "annual_rate": loan_summary["annual_rate"],
                "term_years": test_case["term_years"],
                "monthly_payment": loan_summary["monthly_payment"],
                "total_interest": loan_summary["total_interest"],
                "status": (
                    "Test Case - Approved"
                    if loan_summary["affordability"]["is_affordable"]
                    else "Test Case - Pending Review"
                ),
                "monthly_income": test_case["monthly_income"],
                "affordability": loan_summary["affordability"],
            }

            # Save to CSV - only if approved
            from loan_summary import save_loan_record

            if loan_summary["affordability"]["is_affordable"]:
                if save_loan_record(loan_record_data, "sample_loans.csv"):
                    print_status_message(
                        f"Test case {i} (APPROVED) saved to sample_loans.csv", "success"
                    )
                else:
                    print_status_message(f"Failed to save test case {i}", "error")
            else:
                print_status_message(
                    f"Test case {i} (NOT APPROVED) - not saved to CSV", "warning"
                )

        except Exception as e:
            print_status_message(f"Error in test case {i}: {e}", "error")

    print(f"\n{'='*60}")
    print("SAMPLE TESTS COMPLETED")
    print(f"{'='*60}")

    # Display saved records
    try:
        from loan_summary import display_saved_records

        print("\n📋 SAVED TEST RECORDS:")
        display_saved_records("sample_loans.csv", 10)
    except Exception as e:
        print_status_message(f"Error displaying saved records: {e}", "error")


def display_main_menu():
    """Display the main menu with enhanced formatting"""
    print_section_header("MAIN MENU")
    print("1. Apply for a Loan")
    print("2. View Loan Information")
    print("3. Contact Information")
    print("4. Run Sample Tests")
    print("5. Exit")


def main():
    """Main program loop with comprehensive error handling"""
    try:
        print_section_header("BANK LOAN MANAGEMENT SYSTEM")
        print("Welcome to your trusted partner for all lending needs!")
        print("\nWe offer competitive rates and flexible terms for:")
        print("🏠 Housing Loans    🚗 Auto Loans    💼 Personal Loans")

        while True:
            try:
                # Display main menu
                display_main_menu()

                choice = input("\nEnter your choice (1-5): ").strip()

                if choice == "1":
                    # Apply for new loan
                    print_status_message("Starting loan application process", "info")
                    if process_loan_application():
                        # Ask if user wants to apply for another loan
                        while True:
                            another = (
                                input(
                                    "\nWould you like to apply for another loan? (yes/no): "
                                )
                                .lower()
                                .strip()
                            )
                            if another in ["yes", "y"]:
                                break
                            elif another in ["no", "n"]:
                                print_status_message(
                                    "Thank you for using our Loan Management System!",
                                    "success",
                                )
                                sys.exit(0)
                            else:
                                print("Please enter 'yes' or 'no'.")

                elif choice == "2":
                    # View loan information
                    print_section_header("LOAN INFORMATION")
                    print("🏠 Housing Loans:")
                    print("   • Amount: $50,000 - $2,000,000")
                    print("   • Term: 5-25 years")
                    print("   • Interest Rate: 3.5% - 6.5%")
                    print("   • Minimum Income: $3,000/month")

                    print("\n🚗 Auto Loans:")
                    print("   • Amount: $5,000 - $100,000")
                    print("   • Term: 1-6 years")
                    print("   • Interest Rate: 2.9% - 8.9%")
                    print("   • Minimum Income: $2,000/month")

                    print("\n💼 Personal Loans:")
                    print("   • Amount: $1,000 - $50,000")
                    print("   • Term: 1-10 years")
                    print("   • Interest Rate: 5.9% - 15.9%")
                    print("   • Minimum Income: $1,500/month")

                    input("\nPress Enter to continue...")

                elif choice == "3":
                    # Contact information
                    print_section_header("CONTACT INFORMATION")
                    print("🏦 Main Office: 123 Bank Street, City, State 12345")
                    print("📞 Phone: (555) 123-4567")
                    print("📧 Email: loans@bank.com")
                    print("🕒 Hours: Monday-Friday 9:00 AM - 5:00 PM")
                    print("🌐 Website: www.bankloans.com")

                    input("\nPress Enter to continue...")

                elif choice == "4":
                    # Run sample tests
                    run_sample_tests()
                    input("\nPress Enter to continue...")

                elif choice == "5":
                    # Exit program
                    print_status_message(
                        "Thank you for using our Loan Management System!", "success"
                    )
                    print("Have a great day! 👋")
                    sys.exit(0)

                else:
                    print_status_message("Invalid choice. Please select 1-5.", "error")

            except KeyboardInterrupt:
                print_status_message("Operation cancelled by user.", "warning")
                continue
            except Exception as e:
                print_status_message(f"An error occurred: {e}", "error")
                print("Please try again or contact support if the problem persists.")
                continue

    except Exception as e:
        print_status_message(f"Critical error in main program: {e}", "error")
        print("The program encountered an unexpected error and must exit.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
        print("Thank you for using our Loan Management System!")
        sys.exit(0)
    except Exception as e:
        print(f"\nCritical system error: {e}")
        print("The program encountered an unexpected error and must exit.")
        print("Please contact technical support.")
        sys.exit(1)
