"""
Utility Functions for Bank Loan Management System
Author: Assistant
Date: 2024

This module contains helper functions for formatting, file operations, and common utilities.
"""

import os
import csv
from datetime import datetime
from typing import List, Dict, Any, Optional


# =============================================================================
# FORMATTING FUNCTIONS
# =============================================================================


def format_currency(amount: float, symbol: str = "$", decimal_places: int = 2) -> str:
    """
    Format a number as currency string

    Args:
        amount (float): The amount to format
        symbol (str): Currency symbol (default: "$")
        decimal_places (int): Number of decimal places (default: 2)

    Returns:
        str: Formatted currency string

    Examples:
        format_currency(1234.56) -> "$1,234.56"
        format_currency(1000, "€") -> "€1,000.00"
        format_currency(99.5, "$", 0) -> "$100"
    """
    if amount < 0:
        return f"-{symbol}{format_number(abs(amount), decimal_places)}"
    return f"{symbol}{format_number(amount, decimal_places)}"


def format_number(number: float, decimal_places: int = 2) -> str:
    """
    Format a number with commas and specified decimal places

    Args:
        number (float): The number to format
        decimal_places (int): Number of decimal places (default: 2)

    Returns:
        str: Formatted number string

    Examples:
        format_number(1234.56) -> "1,234.56"
        format_number(1000000, 0) -> "1,000,000"
        format_number(99.5, 1) -> "99.5"
    """
    # Round to specified decimal places
    rounded = round(number, decimal_places)

    # Format with commas
    if decimal_places == 0:
        return f"{rounded:,.0f}"
    else:
        return f"{rounded:,.{decimal_places}f}"


def format_percentage(rate: float, decimal_places: int = 2) -> str:
    """
    Format a number as percentage

    Args:
        rate (float): The rate to format (e.g., 4.5 for 4.5%)
        decimal_places (int): Number of decimal places (default: 2)

    Returns:
        str: Formatted percentage string

    Examples:
        format_percentage(4.5) -> "4.50%"
        format_percentage(10, 1) -> "10.0%"
    """
    return f"{rate:.{decimal_places}f}%"


def format_loan_amount(amount: float) -> str:
    """
    Format loan amount with appropriate precision based on size

    Args:
        amount (float): Loan amount

    Returns:
        str: Formatted loan amount

    Examples:
        format_loan_amount(1500.50) -> "$1,500.50"
        format_loan_amount(200000) -> "$200,000.00"
    """
    if amount >= 1000000:
        return format_currency(amount, decimal_places=0)  # No decimals for millions
    elif amount >= 1000:
        return format_currency(amount, decimal_places=2)  # Standard formatting
    else:
        return format_currency(
            amount, decimal_places=2
        )  # Keep decimals for small amounts


def format_payment_amount(amount: float) -> str:
    """
    Format payment amount with appropriate precision

    Args:
        amount (float): Payment amount

    Returns:
        str: Formatted payment amount

    Examples:
        format_payment_amount(1013.37) -> "$1,013.37"
        format_payment_amount(500.00) -> "$500.00"
    """
    return format_currency(amount, decimal_places=2)


def format_large_number(number: float) -> str:
    """
    Format large numbers with K, M, B suffixes for readability

    Args:
        number (float): Number to format

    Returns:
        str: Formatted number with suffix

    Examples:
        format_large_number(1500) -> "1.5K"
        format_large_number(1500000) -> "1.5M"
        format_large_number(1500000000) -> "1.5B"
    """
    if number >= 1_000_000_000:
        return f"{number/1_000_000_000:.1f}B"
    elif number >= 1_000_000:
        return f"{number/1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number/1_000:.1f}K"
    else:
        return format_number(number, 0)


# =============================================================================
# CSV FILE OPERATIONS
# =============================================================================


def ensure_csv_file_exists(filename: str, headers: List[str]) -> bool:
    """
    Check if CSV file exists; if not, create one with headers

    Args:
        filename (str): Path to CSV file
        headers (List[str]): List of column headers

    Returns:
        bool: True if file exists or was created successfully, False otherwise
    """
    try:
        # Check if file exists
        if os.path.exists(filename):
            # Check if file is empty or has no headers
            if os.path.getsize(filename) == 0:
                return _write_csv_headers(filename, headers)
            else:
                # File exists and has content - check if headers match
                return _validate_csv_headers(filename, headers)
        else:
            # File doesn't exist - create it with headers
            return _write_csv_headers(filename, headers)

    except Exception as e:
        print(f"❌ Error ensuring CSV file exists: {e}")
        return False


def _write_csv_headers(filename: str, headers: List[str]) -> bool:
    """
    Write headers to CSV file

    Args:
        filename (str): Path to CSV file
        headers (List[str]): List of column headers

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
        return True
    except Exception as e:
        print(f"❌ Error writing CSV headers: {e}")
        return False


def _validate_csv_headers(filename: str, expected_headers: List[str]) -> bool:
    """
    Validate that CSV file has correct headers

    Args:
        filename (str): Path to CSV file
        expected_headers (List[str]): Expected column headers

    Returns:
        bool: True if headers match, False otherwise
    """
    try:
        with open(filename, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            try:
                actual_headers = next(reader)
                return actual_headers == expected_headers
            except StopIteration:
                # File is empty
                return _write_csv_headers(filename, expected_headers)
    except Exception as e:
        print(f"❌ Error validating CSV headers: {e}")
        return False


def append_to_csv(filename: str, data: List[str]) -> bool:
    """
    Append data row to CSV file

    Args:
        filename (str): Path to CSV file
        data (List[str]): Data row to append

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filename, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)
        return True
    except Exception as e:
        print(f"❌ Error appending to CSV: {e}")
        return False


def read_csv_data(filename: str) -> List[Dict[str, str]]:
    """
    Read all data from CSV file

    Args:
        filename (str): Path to CSV file

    Returns:
        List[Dict[str, str]]: List of dictionaries with CSV data
    """
    try:
        if not os.path.exists(filename):
            return []

        data = []
        with open(filename, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(dict(row))
        return data
    except Exception as e:
        print(f"❌ Error reading CSV data: {e}")
        return []


def get_csv_record_count(filename: str) -> int:
    """
    Get number of data records in CSV file (excluding headers)

    Args:
        filename (str): Path to CSV file

    Returns:
        int: Number of data records
    """
    try:
        if not os.path.exists(filename):
            return 0

        with open(filename, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            # Skip header
            try:
                next(reader)
            except StopIteration:
                return 0

            # Count data rows
            count = sum(1 for row in reader)
            return count
    except Exception as e:
        print(f"❌ Error counting CSV records: {e}")
        return 0


# =============================================================================
# PRINT FORMATTING FUNCTIONS
# =============================================================================


def print_separator(char: str = "=", length: int = 60, title: str = "") -> None:
    """
    Print a separator line with optional title

    Args:
        char (str): Character to use for separator (default: "=")
        length (int): Length of separator (default: 60)
        title (str): Optional title to center in separator

    Examples:
        print_separator() -> "============================================================"
        print_separator("-", 40, "SECTION") -> "---------- SECTION ----------"
    """
    if title:
        # Calculate padding for centered title
        title_len = len(title)
        if title_len >= length - 2:
            print(title)
            return

        padding = (length - title_len - 2) // 2
        print(char * padding + f" {title} " + char * padding)
    else:
        print(char * length)


def print_section_header(title: str, char: str = "=", length: int = 60) -> None:
    """
    Print a formatted section header

    Args:
        title (str): Section title
        char (str): Character to use for separator (default: "=")
        length (int): Length of separator (default: 60)

    Example:
        print_section_header("LOAN SUMMARY") ->
        =========================== LOAN SUMMARY ============================
    """
    print()
    print_separator(char, length, title)


def print_subsection_header(title: str) -> None:
    """
    Print a formatted subsection header

    Args:
        title (str): Subsection title

    Example:
        print_subsection_header("Payment Information") ->

        💰 PAYMENT INFORMATION
        ======================
    """
    print(f"\n{title}")
    print("-" * len(title))


def print_key_value(key: str, value: str, indent: int = 3) -> None:
    """
    Print a key-value pair with consistent formatting

    Args:
        key (str): Key/label
        value (str): Value
        indent (int): Number of spaces for indentation (default: 3)

    Example:
        print_key_value("Loan Amount", "$200,000.00") ->
           Loan Amount: $200,000.00
    """
    print(" " * indent + f"{key}: {value}")


def print_bullet_list(items: List[str], indent: int = 3, bullet: str = "•") -> None:
    """
    Print a bulleted list with consistent formatting

    Args:
        items (List[str]): List of items to print
        indent (int): Number of spaces for indentation (default: 3)
        bullet (str): Bullet character (default: "•")

    Example:
        print_bullet_list(["Item 1", "Item 2"]) ->
           • Item 1
           • Item 2
    """
    for item in items:
        print(" " * indent + f"{bullet} {item}")


def print_table_header(headers: List[str], widths: List[int] = None) -> None:
    """
    Print a table header with specified column widths

    Args:
        headers (List[str]): Column headers
        widths (List[int]): Column widths (if None, auto-calculate)

    Example:
        print_table_header(["Name", "Amount", "Rate"], [15, 12, 8]) ->
        Name            Amount      Rate
        --------------- ----------- --------
    """
    if widths is None:
        widths = [len(header) + 2 for header in headers]

    # Print headers
    header_line = ""
    separator_line = ""

    for i, (header, width) in enumerate(zip(headers, widths)):
        header_line += f"{header:<{width}}"
        separator_line += "-" * width

    print(header_line)
    print(separator_line)


def print_table_row(data: List[str], widths: List[int] = None) -> None:
    """
    Print a table row with specified column widths

    Args:
        data (List[str]): Row data
        widths (List[int]): Column widths (if None, auto-calculate)

    Example:
        print_table_row(["Housing", "$200,000", "4.5%"], [15, 12, 8]) ->
        Housing         $200,000    4.5%
    """
    if widths is None:
        widths = [len(item) + 2 for item in data]

    row_line = ""
    for i, (item, width) in enumerate(zip(data, widths)):
        row_line += f"{item:<{width}}"

    print(row_line)


def print_centered_text(text: str, width: int = 60, char: str = " ") -> None:
    """
    Print centered text within specified width

    Args:
        text (str): Text to center
        width (int): Total width (default: 60)
        char (str): Padding character (default: " ")

    Example:
        print_centered_text("LOAN CALCULATOR", 50) ->
                     LOAN CALCULATOR
    """
    if len(text) >= width:
        print(text)
        return

    padding = (width - len(text)) // 2
    print(char * padding + text + char * padding)


def print_status_message(message: str, status: str = "info") -> None:
    """
    Print a status message with appropriate formatting

    Args:
        message (str): Message to print
        status (str): Status type ("info", "success", "warning", "error")

    Example:
        print_status_message("Loan approved", "success") -> ✅ Loan approved
        print_status_message("Invalid input", "error") -> ❌ Invalid input
    """
    status_icons = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}

    icon = status_icons.get(status, "ℹ️")
    print(f"{icon} {message}")


# =============================================================================
# DATE AND TIME UTILITIES
# =============================================================================


def get_current_timestamp() -> str:
    """
    Get current timestamp as formatted string

    Returns:
        str: Formatted timestamp (YYYY-MM-DD HH:MM:SS)
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_current_date() -> str:
    """
    Get current date as formatted string

    Returns:
        str: Formatted date (YYYY-MM-DD)
    """
    return datetime.now().strftime("%Y-%m-%d")


def format_timestamp(timestamp: str, format_type: str = "full") -> str:
    """
    Format timestamp string for display

    Args:
        timestamp (str): Timestamp string
        format_type (str): Format type ("full", "date", "time", "short")

    Returns:
        str: Formatted timestamp
    """
    try:
        dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

        if format_type == "full":
            return dt.strftime("%B %d, %Y at %I:%M %p")
        elif format_type == "date":
            return dt.strftime("%B %d, %Y")
        elif format_type == "time":
            return dt.strftime("%I:%M %p")
        elif format_type == "short":
            return dt.strftime("%m/%d/%Y")
        else:
            return timestamp
    except ValueError:
        return timestamp


# =============================================================================
# VALIDATION UTILITIES
# =============================================================================


def is_valid_number(value: str) -> bool:
    """
    Check if string represents a valid number

    Args:
        value (str): String to check

    Returns:
        bool: True if valid number, False otherwise
    """
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_positive_number(value: float) -> bool:
    """
    Check if number is positive

    Args:
        value (float): Number to check

    Returns:
        bool: True if positive, False otherwise
    """
    return value > 0


def is_valid_filename(filename: str) -> bool:
    """
    Check if filename is valid for file system

    Args:
        filename (str): Filename to check

    Returns:
        bool: True if valid, False otherwise
    """
    if not filename:
        return False

    # Check for invalid characters
    invalid_chars = ["<", ">", ":", '"', "|", "?", "*", "\\", "/"]
    for char in invalid_chars:
        if char in filename:
            return False

    return True


if __name__ == "__main__":
    # Test the utility functions
    print("Testing Utility Functions")
    print_separator("=", 50, "UTILS TEST")

    # Test formatting functions
    print("\n📊 FORMATTING TESTS:")
    print(f"Currency: {format_currency(123456.78)}")
    print(f"Large number: {format_large_number(1500000)}")
    print(f"Percentage: {format_percentage(4.5)}")
    print(f"Loan amount: {format_loan_amount(200000)}")

    # Test print formatting
    print("\n📝 PRINT FORMATTING TESTS:")
    print_section_header("Test Section")
    print_subsection_header("Test Subsection")
    print_key_value("Test Key", "Test Value")
    print_bullet_list(["Item 1", "Item 2", "Item 3"])

    # Test table formatting
    print("\n📋 TABLE FORMATTING TEST:")
    headers = ["Type", "Amount", "Rate"]
    widths = [10, 12, 8]
    print_table_header(headers, widths)
    print_table_row(["Housing", "$200,000", "4.5%"], widths)
    print_table_row(["Auto", "$25,000", "3.2%"], widths)

    # Test status messages
    print("\n📢 STATUS MESSAGE TESTS:")
    print_status_message("Operation successful", "success")
    print_status_message("Warning message", "warning")
    print_status_message("Error occurred", "error")

    # Test CSV operations
    print("\n📁 CSV OPERATIONS TEST:")
    test_headers = ["Date", "Type", "Amount"]
    if ensure_csv_file_exists("test_utils.csv", test_headers):
        print_status_message("CSV file created/verified", "success")
        if append_to_csv("test_utils.csv", ["2024-01-15", "Housing", "$200,000"]):
            print_status_message("Data appended to CSV", "success")

    # Test date utilities
    print("\n📅 DATE UTILITIES TEST:")
    timestamp = get_current_timestamp()
    print(f"Current timestamp: {timestamp}")
    print(f"Formatted: {format_timestamp(timestamp, 'full')}")

    print("\n✅ All utility tests completed!")
