"""
Loan Summary Module for Bank Loan Management System
Author: Assistant
Date: 2024

This module handles displaying loan summaries and saving loan records to CSV files.
"""

import csv
import os
from datetime import datetime


def display_loan_summary(loan_data):
    """
    Display a comprehensive loan summary with all key details

    Args:
        loan_data (dict): Dictionary containing loan information:
            - loan_type (str): Type of loan
            - principal (float): Loan amount
            - annual_rate (float): Annual interest rate
            - term_years (int): Loan term in years
            - monthly_payment (float): Monthly payment amount
            - total_interest (float): Total interest amount
            - status (str): Loan status (e.g., "Approved", "Pending", "Rejected")
            - monthly_income (float): Monthly income (optional)
    """
    print("\n" + "=" * 70)
    print("                    LOAN SUMMARY")
    print("=" * 70)

    # Basic loan information
    print(f"\n📋 LOAN DETAILS:")
    print(f"   Loan Type: {loan_data['loan_type']}")
    print(f"   Principal Amount: ${loan_data['principal']:,.2f}")
    print(f"   Annual Interest Rate: {loan_data['annual_rate']:.2f}%")
    print(f"   Loan Term: {loan_data['term_years']} years")

    # Payment information
    print(f"\n💰 PAYMENT BREAKDOWN:")
    print(f"   Monthly Payment: ${loan_data['monthly_payment']:,.2f}")
    print(f"   Total Interest: ${loan_data['total_interest']:,.2f}")
    print(
        f"   Total Amount to Pay: ${loan_data['principal'] + loan_data['total_interest']:,.2f}"
    )

    # Status and affordability (if available)
    status = loan_data.get("status", "Pending Review")
    print(f"\n📊 LOAN STATUS:")
    print(f"   Status: {status}")

    # Show affordability information if available
    if "monthly_income" in loan_data and "affordability" in loan_data:
        affordability = loan_data["affordability"]
        print(
            f"   Payment-to-Income Ratio: {affordability.get('payment_ratio', 0):.1f}%"
        )
        print(
            f"   Affordability: {'✅ Affordable' if affordability.get('is_affordable', False) else '⚠️ Review Required'}"
        )

    # Additional details if available
    if "num_payments" in loan_data:
        print(f"   Total Payments: {loan_data['num_payments']}")

    print("\n" + "=" * 70)


def get_user_confirmation():
    """
    Ask user to confirm before saving the loan record

    Returns:
        bool: True if user confirms, False otherwise
    """
    print("\n💾 SAVE LOAN RECORD")
    print("=" * 30)
    print("Would you like to save this loan application to your records?")
    print("This will help you track your loan applications over time.")

    while True:
        try:
            confirm = input("\nSave loan record? (yes/no): ").lower().strip()

            if confirm in ["yes", "y"]:
                print("✅ Loan record will be saved.")
                return True
            elif confirm in ["no", "n"]:
                print("❌ Loan record will not be saved.")
                return False
            else:
                print("❌ Please enter 'yes' or 'no'.")

        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            return False
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            return False


def save_loan_record(loan_data, filename="loan_records.csv"):
    """
    Save loan record to CSV file with proper headers

    Args:
        loan_data (dict): Dictionary containing loan information
        filename (str): CSV filename (default: "loan_records.csv")

    Returns:
        bool: True if saved successfully, False otherwise
    """
    try:
        # Define CSV headers
        headers = [
            "Date",
            "Loan Type",
            "Loan Amount",
            "Interest Rate",
            "Term (Years)",
            "Monthly Payment",
            "Total Interest",
            "Status",
        ]

        # Prepare record data
        record = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Date
            loan_data["loan_type"],
            f"${loan_data['principal']:,.2f}",
            f"{loan_data['annual_rate']:.2f}%",
            str(loan_data["term_years"]),
            f"${loan_data['monthly_payment']:,.2f}",
            f"${loan_data['total_interest']:,.2f}",
            loan_data.get("status", "Pending Review"),
        ]

        # Check if file exists to determine if we need headers
        file_exists = os.path.exists(filename)

        # Write to CSV file
        with open(filename, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)

            # Write headers if file is empty or doesn't exist
            if not file_exists or os.path.getsize(filename) == 0:
                writer.writerow(headers)

            # Write the record
            writer.writerow(record)

        print(f"✅ Loan record saved successfully to {filename}")
        return True

    except PermissionError:
        print(f"❌ Permission denied. Cannot write to {filename}")
        print("   Please check file permissions or try a different filename.")
        return False
    except Exception as e:
        print(f"❌ Error saving loan record: {e}")
        return False


def display_saved_records(filename="loan_records.csv", num_records=5):
    """
    Display recent loan records from CSV file

    Args:
        filename (str): CSV filename (default: "loan_records.csv")
        num_records (int): Number of recent records to display (default: 5)
    """
    try:
        if not os.path.exists(filename):
            print(f"📄 No loan records found. File '{filename}' does not exist.")
            return

        if os.path.getsize(filename) == 0:
            print(f"📄 No loan records found. File '{filename}' is empty.")
            return

        print(f"\n📋 RECENT LOAN RECORDS (Last {num_records})")
        print("=" * 80)

        with open(filename, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)

            # Read all records
            records = list(reader)

            if len(records) <= 1:  # Only headers or no data
                print("📄 No loan records found.")
                return

            # Get headers and data
            headers = records[0]
            data_records = records[1:]

            # Display recent records (last N)
            recent_records = data_records[-num_records:]

            # Display headers
            print(
                f"{'Date':<20} {'Type':<10} {'Amount':<12} {'Rate':<8} {'Term':<6} {'Payment':<12} {'Interest':<12} {'Status':<15}"
            )
            print("-" * 80)

            # Display records
            for record in recent_records:
                if len(record) >= len(headers):
                    print(
                        f"{record[0]:<20} {record[1]:<10} {record[2]:<12} {record[3]:<8} {record[4]:<6} {record[5]:<12} {record[6]:<12} {record[7]:<15}"
                    )

            print(f"\nTotal records: {len(data_records)}")

    except Exception as e:
        print(f"❌ Error reading loan records: {e}")


def process_loan_summary_and_save(loan_data):
    """
    Complete process: display summary, get confirmation, and save record

    Args:
        loan_data (dict): Dictionary containing loan information

    Returns:
        bool: True if record was saved, False otherwise
    """
    # Display the loan summary
    display_loan_summary(loan_data)

    # Ask for confirmation
    if get_user_confirmation():
        # Save the record
        return save_loan_record(loan_data)
    else:
        return False


def export_loan_records(filename="loan_records.csv", export_filename=None):
    """
    Export loan records to a new file (backup or different format)

    Args:
        filename (str): Source CSV filename
        export_filename (str): Export filename (default: adds timestamp)

    Returns:
        bool: True if exported successfully, False otherwise
    """
    try:
        if not os.path.exists(filename):
            print(f"❌ Source file '{filename}' does not exist.")
            return False

        # Generate export filename if not provided
        if not export_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_filename = f"loan_records_backup_{timestamp}.csv"

        # Copy file
        with open(filename, "r", encoding="utf-8") as source:
            with open(export_filename, "w", encoding="utf-8") as target:
                target.write(source.read())

        print(f"✅ Loan records exported to {export_filename}")
        return True

    except Exception as e:
        print(f"❌ Error exporting loan records: {e}")
        return False


def get_loan_statistics(filename="loan_records.csv"):
    """
    Calculate and display statistics from loan records

    Args:
        filename (str): CSV filename
    """
    try:
        if not os.path.exists(filename):
            print(f"📄 No loan records found for statistics.")
            return

        with open(filename, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            records = list(reader)

            if len(records) <= 1:
                print("📄 No loan records found for statistics.")
                return

            data_records = records[1:]  # Skip headers

            # Calculate statistics
            total_records = len(data_records)
            loan_types = {}
            total_loan_amount = 0
            total_monthly_payments = 0

            for record in data_records:
                if len(record) >= 8:
                    loan_type = record[1]
                    loan_amount = float(record[2].replace("$", "").replace(",", ""))
                    monthly_payment = float(record[5].replace("$", "").replace(",", ""))

                    # Count loan types
                    loan_types[loan_type] = loan_types.get(loan_type, 0) + 1

                    # Sum amounts
                    total_loan_amount += loan_amount
                    total_monthly_payments += monthly_payment

            # Display statistics
            print(f"\n📊 LOAN RECORDS STATISTICS")
            print("=" * 40)
            print(f"Total Applications: {total_records}")
            print(f"Total Loan Amount: ${total_loan_amount:,.2f}")
            print(
                f"Average Monthly Payment: ${total_monthly_payments/total_records:,.2f}"
            )

            print(f"\nLoan Types:")
            for loan_type, count in loan_types.items():
                percentage = (count / total_records) * 100
                print(f"   {loan_type}: {count} ({percentage:.1f}%)")

    except Exception as e:
        print(f"❌ Error calculating statistics: {e}")


if __name__ == "__main__":
    # Test the loan summary module
    print("Testing Loan Summary Module")
    print("=" * 40)

    # Sample loan data for testing
    sample_loan_data = {
        "loan_type": "Housing",
        "principal": 200000,
        "annual_rate": 4.5,
        "term_years": 30,
        "monthly_payment": 1013.37,
        "total_interest": 164813.20,
        "status": "Approved",
        "monthly_income": 8000,
        "affordability": {"payment_ratio": 12.7, "is_affordable": True},
        "num_payments": 360,
    }

    # Test display function
    print("\n1. Testing loan summary display:")
    display_loan_summary(sample_loan_data)

    # Test saving (commented out for automated testing)
    # print("\n2. Testing save functionality:")
    # if process_loan_summary_and_save(sample_loan_data):
    #     print("✅ Loan record saved successfully!")

    # Test statistics if records exist
    print("\n3. Testing statistics:")
    get_loan_statistics()

    # Test displaying records
    print("\n4. Testing record display:")
    display_saved_records()

    print("\n✅ All tests completed!")
