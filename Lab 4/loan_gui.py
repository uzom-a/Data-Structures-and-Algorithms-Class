"""
Modern Bank Loan Management System - GUI Application
Author: Assistant
Date: 2024

A professional, responsive GUI for the loan management system featuring:
- Real-time loan calculations
- Input validation
- Professional banking theme
- CSV integration
- Affordability warnings
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from datetime import datetime

# Import our backend modules
from input_validation import (
    validate_loan_amount,
    validate_term,
    validate_income,
    validate_loan_type,
    LOAN_CONFIGS,
)
from loan_calculator import (
    calculate_monthly_payment,
    calculate_total_interest,
    check_affordability,
    calculate_loan_summary,
)
from loan_summary import save_loan_record
from utils import format_currency, format_percentage, print_status_message


class LoanManagementGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.setup_styles()
        self.create_widgets()
        self.setup_bindings()

    def setup_window(self):
        """Configure the main window"""
        self.root.title("🏦 Bank Loan Management System")
        self.root.geometry("800x700")
        self.root.minsize(700, 600)
        self.root.configure(bg="#f0f4f8")

        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"800x700+{x}+{y}")

    def setup_variables(self):
        """Initialize tkinter variables"""
        self.loan_type_var = tk.StringVar(value="Housing")
        self.loan_amount_var = tk.StringVar()
        self.term_years_var = tk.StringVar()
        self.monthly_income_var = tk.StringVar()

        # Calculation results
        self.monthly_payment_var = tk.StringVar(value="$0.00")
        self.total_interest_var = tk.StringVar(value="$0.00")
        self.total_amount_var = tk.StringVar(value="$0.00")
        self.debt_ratio_var = tk.StringVar(value="0.0%")
        self.status_var = tk.StringVar(value="Ready to calculate")

        # Warning status
        self.warning_text = tk.StringVar(value="")
        self.warning_color = "#28a745"  # Green for no warnings

    def setup_styles(self):
        """Configure custom styles"""
        style = ttk.Style()

        # Configure theme colors
        style.configure(
            "Title.TLabel",
            font=("Arial", 16, "bold"),
            foreground="#1e3a8a",
            background="#f0f4f8",
        )

        style.configure(
            "Header.TLabel",
            font=("Arial", 12, "bold"),
            foreground="#374151",
            background="#f0f4f8",
        )

        style.configure(
            "Result.TLabel",
            font=("Arial", 11, "bold"),
            foreground="#1f2937",
            background="#f0f4f8",
        )

        style.configure(
            "Warning.TLabel",
            font=("Arial", 10),
            foreground="#dc2626",
            background="#f0f4f8",
        )

        style.configure(
            "Success.TLabel",
            font=("Arial", 10),
            foreground="#059669",
            background="#f0f4f8",
        )

        # Button styles
        style.configure(
            "Calculate.TButton",
            font=("Arial", 11, "bold"),
            background="#3b82f6",
            foreground="white",
        )

        style.configure(
            "Save.TButton",
            font=("Arial", 11, "bold"),
            background="#059669",
            foreground="white",
        )

        style.configure(
            "Clear.TButton",
            font=("Arial", 11),
            background="#6b7280",
            foreground="white",
        )

        # Frame styles
        style.configure(
            "Card.TFrame", background="white", relief="raised", borderwidth=1
        )

    def create_widgets(self):
        """Create and layout all GUI widgets"""
        # Main container
        main_container = tk.Frame(self.root, bg="#f0f4f8")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_frame = tk.Frame(main_container, bg="#f0f4f8")
        title_frame.pack(fill="x", pady=(0, 20))

        title_label = ttk.Label(
            title_frame, text="🏦 Bank Loan Management System", style="Title.TLabel"
        )
        title_label.pack()

        subtitle_label = ttk.Label(
            title_frame,
            text="Professional Loan Calculator & Application System",
            font=("Arial", 10),
            foreground="#6b7280",
            background="#f0f4f8",
        )
        subtitle_label.pack(pady=(5, 0))

        # Create main content area with notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill="both", expand=True)

        # Loan Calculator Tab
        self.create_loan_calculator_tab()

        # Loan Records Tab
        self.create_loan_records_tab()

        # Help Tab
        self.create_help_tab()

    def create_loan_calculator_tab(self):
        """Create the main loan calculator interface"""
        calculator_frame = ttk.Frame(self.notebook)
        self.notebook.add(calculator_frame, text="📊 Loan Calculator")

        # Left panel - Input form
        left_panel = tk.Frame(calculator_frame, bg="white", relief="raised", bd=1)
        left_panel.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        # Input form title
        input_title = ttk.Label(
            left_panel, text="Loan Application Details", style="Header.TLabel"
        )
        input_title.pack(pady=(15, 10))

        # Create input form
        self.create_input_form(left_panel)

        # Right panel - Results
        right_panel = tk.Frame(calculator_frame, bg="white", relief="raised", bd=1)
        right_panel.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        # Results title
        results_title = ttk.Label(
            right_panel, text="Loan Calculation Results", style="Header.TLabel"
        )
        results_title.pack(pady=(15, 10))

        # Create results display
        self.create_results_display(right_panel)

        # Bottom panel - Actions
        self.create_action_buttons(calculator_frame)

    def create_input_form(self, parent):
        """Create the loan input form"""
        form_frame = tk.Frame(parent, bg="white")
        form_frame.pack(fill="x", padx=20, pady=10)

        # Loan Type Selection
        loan_type_frame = tk.Frame(form_frame, bg="white")
        loan_type_frame.pack(fill="x", pady=5)

        ttk.Label(
            loan_type_frame,
            text="Loan Type:",
            font=("Arial", 10, "bold"),
            background="white",
        ).pack(anchor="w")

        loan_type_combo = ttk.Combobox(
            loan_type_frame,
            textvariable=self.loan_type_var,
            values=["Housing", "Auto", "Personal"],
            state="readonly",
            font=("Arial", 10),
            width=25,
        )
        loan_type_combo.pack(fill="x", pady=(2, 0))

        # Loan Amount
        amount_frame = tk.Frame(form_frame, bg="white")
        amount_frame.pack(fill="x", pady=5)

        ttk.Label(
            amount_frame,
            text="Loan Amount ($):",
            font=("Arial", 10, "bold"),
            background="white",
        ).pack(anchor="w")

        amount_entry = tk.Entry(
            amount_frame,
            textvariable=self.loan_amount_var,
            font=("Arial", 10),
            width=27,
        )
        amount_entry.pack(fill="x", pady=(2, 0))

        # Term Years
        term_frame = tk.Frame(form_frame, bg="white")
        term_frame.pack(fill="x", pady=5)

        ttk.Label(
            term_frame,
            text="Loan Term (Years):",
            font=("Arial", 10, "bold"),
            background="white",
        ).pack(anchor="w")

        term_entry = tk.Entry(
            term_frame, textvariable=self.term_years_var, font=("Arial", 10), width=27
        )
        term_entry.pack(fill="x", pady=(2, 0))

        # Monthly Income
        income_frame = tk.Frame(form_frame, bg="white")
        income_frame.pack(fill="x", pady=5)

        ttk.Label(
            income_frame,
            text="Monthly Income ($):",
            font=("Arial", 10, "bold"),
            background="white",
        ).pack(anchor="w")

        income_entry = tk.Entry(
            income_frame,
            textvariable=self.monthly_income_var,
            font=("Arial", 10),
            width=27,
        )
        income_entry.pack(fill="x", pady=(2, 0))

        # Term limits info
        self.term_info_label = ttk.Label(
            form_frame,
            text="",
            font=("Arial", 9),
            foreground="#6b7280",
            background="white",
        )
        self.term_info_label.pack(anchor="w", pady=(5, 0))

    def create_results_display(self, parent):
        """Create the loan calculation results display"""
        results_frame = tk.Frame(parent, bg="white")
        results_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Monthly Payment
        payment_frame = tk.Frame(results_frame, bg="white")
        payment_frame.pack(fill="x", pady=5)

        ttk.Label(
            payment_frame,
            text="Monthly Payment:",
            font=("Arial", 10, "bold"),
            background="white",
        ).pack(anchor="w")

        payment_result = ttk.Label(
            payment_frame, textvariable=self.monthly_payment_var, style="Result.TLabel"
        )
        payment_result.pack(anchor="w", pady=(2, 0))

        # Total Interest
        interest_frame = tk.Frame(results_frame, bg="white")
        interest_frame.pack(fill="x", pady=5)

        ttk.Label(
            interest_frame,
            text="Total Interest:",
            font=("Arial", 10, "bold"),
            background="white",
        ).pack(anchor="w")

        interest_result = ttk.Label(
            interest_frame, textvariable=self.total_interest_var, style="Result.TLabel"
        )
        interest_result.pack(anchor="w", pady=(2, 0))

        # Total Amount
        total_frame = tk.Frame(results_frame, bg="white")
        total_frame.pack(fill="x", pady=5)

        ttk.Label(
            total_frame,
            text="Total Amount:",
            font=("Arial", 10, "bold"),
            background="white",
        ).pack(anchor="w")

        total_result = ttk.Label(
            total_frame, textvariable=self.total_amount_var, style="Result.TLabel"
        )
        total_result.pack(anchor="w", pady=(2, 0))

        # Debt Ratio
        ratio_frame = tk.Frame(results_frame, bg="white")
        ratio_frame.pack(fill="x", pady=5)

        ttk.Label(
            ratio_frame,
            text="Debt-to-Income Ratio:",
            font=("Arial", 10, "bold"),
            background="white",
        ).pack(anchor="w")

        self.ratio_result = ttk.Label(
            ratio_frame, textvariable=self.debt_ratio_var, style="Result.TLabel"
        )
        self.ratio_result.pack(anchor="w", pady=(2, 0))

        # Status
        status_frame = tk.Frame(results_frame, bg="white")
        status_frame.pack(fill="x", pady=(10, 0))

        ttk.Label(
            status_frame, text="Status:", font=("Arial", 10, "bold"), background="white"
        ).pack(anchor="w")

        self.status_result = ttk.Label(
            status_frame, textvariable=self.status_var, style="Result.TLabel"
        )
        self.status_result.pack(anchor="w", pady=(2, 0))

        # Warning message
        self.warning_label = ttk.Label(
            results_frame,
            textvariable=self.warning_text,
            font=("Arial", 10),
            background="white",
        )
        self.warning_label.pack(anchor="w", pady=(10, 0))

    def create_action_buttons(self, parent):
        """Create action buttons"""
        button_frame = tk.Frame(parent, bg="#f0f4f8")
        button_frame.pack(fill="x", pady=10)

        # Calculate button
        calc_btn = tk.Button(
            button_frame,
            text="🔄 Calculate Loan",
            command=self.calculate_loan,
            font=("Arial", 11, "bold"),
            bg="#3b82f6",
            fg="white",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
        )
        calc_btn.pack(side="left", padx=5)

        # Save button - will be updated based on approval status
        self.save_btn = tk.Button(
            button_frame,
            text="💾 Save Loan Record",
            command=self.save_loan,
            font=("Arial", 11, "bold"),
            bg="#059669",
            fg="white",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
        )
        self.save_btn.pack(side="left", padx=5)

        # Clear button
        clear_btn = tk.Button(
            button_frame,
            text="🗑️ Clear Form",
            command=self.clear_form,
            font=("Arial", 11),
            bg="#6b7280",
            fg="white",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
        )
        clear_btn.pack(side="left", padx=5)

    def create_loan_records_tab(self):
        """Create tab for viewing loan records"""
        records_frame = ttk.Frame(self.notebook)
        self.notebook.add(records_frame, text="📋 Loan Records")

        # Title
        title_label = ttk.Label(
            records_frame, text="Loan Records Management", style="Header.TLabel"
        )
        title_label.pack(pady=20)

        # Records display area
        records_display = tk.Frame(records_frame, bg="white", relief="raised", bd=1)
        records_display.pack(fill="both", expand=True, padx=20, pady=10)

        # Scrollable text widget for records
        self.records_text = tk.Text(
            records_display, font=("Courier", 10), bg="white", fg="#374151", wrap="none"
        )

        scrollbar = ttk.Scrollbar(
            records_display, orient="vertical", command=self.records_text.yview
        )
        self.records_text.configure(yscrollcommand=scrollbar.set)

        self.records_text.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        # Load records button
        load_btn = tk.Button(
            records_frame,
            text="📂 Load Records",
            command=self.load_loan_records,
            font=("Arial", 11),
            bg="#3b82f6",
            fg="white",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
        )
        load_btn.pack(pady=10)

    def create_help_tab(self):
        """Create help and information tab"""
        help_frame = ttk.Frame(self.notebook)
        self.notebook.add(help_frame, text="❓ Help")

        # Help content
        help_text = tk.Text(
            help_frame,
            font=("Arial", 10),
            bg="white",
            fg="#374151",
            wrap="word",
            padx=20,
            pady=20,
        )
        help_text.pack(fill="both", expand=True, padx=20, pady=20)

        help_content = """
🏦 Bank Loan Management System - Help Guide

LOAN TYPES:
• Housing Loans: $50,000 - $2,000,000 (5-25 years)
• Auto Loans: $5,000 - $100,000 (1-6 years)  
• Personal Loans: $1,000 - $50,000 (1-10 years)

HOW TO USE:
1. Select your loan type from the dropdown
2. Enter the loan amount (numbers only)
3. Enter the loan term in years (within limits shown)
4. Enter your monthly income
5. Click "Calculate Loan" to see results
6. Review the debt-to-income ratio (should be under 50%)
7. Click "Save Loan Record" to save to CSV file

VALIDATION RULES:
• All amounts must be positive numbers
• Loan terms must be within the specified limits
• Monthly income must be at least $1,500
• Debt ratio over 50% will show a warning

DEBT-TO-INCOME RATIO:
This shows what percentage of your income the loan payment represents.
• Under 30%: Excellent
• 30-50%: Acceptable
• Over 50%: Warning - may be difficult to afford

SAVE FEATURES:
• Records are saved to 'loan_records.csv'
• Includes all loan details and timestamps
• Can be opened in Excel or other spreadsheet programs

TROUBLESHOOTING:
• If calculations don't appear, check that all fields are filled
• Ensure numbers are entered without currency symbols
• Make sure loan terms are within the specified limits

For technical support, contact: support@bankloans.com
        """

        help_text.insert("1.0", help_content)
        help_text.config(state="disabled")

    def setup_bindings(self):
        """Set up event bindings for real-time updates"""
        # Bind loan type changes to update term limits
        self.loan_type_var.trace("w", self.update_term_limits)

        # Bind all input changes to real-time calculation
        self.loan_amount_var.trace("w", self.on_input_change)
        self.term_years_var.trace("w", self.on_input_change)
        self.monthly_income_var.trace("w", self.on_input_change)

    def update_term_limits(self, *args):
        """Update term limits when loan type changes"""
        loan_type = self.loan_type_var.get()
        if loan_type in LOAN_CONFIGS:
            config = LOAN_CONFIGS[loan_type]
            self.term_info_label.config(
                text=f"Term limits: {config['min_term']}-{config['max_term']} years"
            )
        else:
            self.term_info_label.config(text="")

    def on_input_change(self, *args):
        """Handle real-time input changes"""
        # Use threading to prevent GUI freezing during calculations
        threading.Thread(target=self.calculate_loan, daemon=True).start()

    def validate_inputs(self):
        """Validate all input fields"""
        errors = []

        # Check if fields are empty first
        if not self.loan_amount_var.get().strip():
            return (
                errors  # Don't show errors for empty fields during real-time validation
            )

        if not self.term_years_var.get().strip():
            return errors

        if not self.monthly_income_var.get().strip():
            return errors

        # Validate loan amount
        try:
            amount = float(self.loan_amount_var.get().replace(",", "").replace("$", ""))
            loan_type = self.loan_type_var.get()
            if not validate_loan_amount(amount, loan_type):
                config = LOAN_CONFIGS.get(loan_type, {})
                min_amount = config.get("min_amount", 0)
                max_amount = config.get("max_amount", float("inf"))
                errors.append(
                    f"Loan amount must be between ${min_amount:,.0f} and ${max_amount:,.0f}"
                )
        except (ValueError, TypeError):
            errors.append("Please enter a valid loan amount")

        # Validate term
        try:
            term = float(self.term_years_var.get())
            loan_type = self.loan_type_var.get()
            if not validate_term(term, loan_type):
                config = LOAN_CONFIGS.get(loan_type, {})
                min_term = config.get("min_term", 0)
                max_term = config.get("max_term", 0)
                errors.append(f"Term must be between {min_term} and {max_term} years")
        except (ValueError, TypeError):
            errors.append("Please enter a valid loan term")

        # Validate income
        try:
            income = float(
                self.monthly_income_var.get().replace(",", "").replace("$", "")
            )
            if not validate_income(income):
                errors.append("Monthly income must be at least $1,500")
        except (ValueError, TypeError):
            errors.append("Please enter a valid monthly income")

        return errors

    def calculate_loan(self):
        """Calculate loan details and update display"""
        try:
            # Check if all fields are filled before attempting calculations
            if (
                not self.loan_amount_var.get().strip()
                or not self.term_years_var.get().strip()
                or not self.monthly_income_var.get().strip()
            ):
                # Reset display for empty fields
                self.monthly_payment_var.set("$0.00")
                self.total_interest_var.set("$0.00")
                self.total_amount_var.set("$0.00")
                self.debt_ratio_var.set("0.0%")
                self.status_var.set("Ready to calculate")
                self.warning_text.set("")
                self.warning_label.config(foreground="#1f2937")
                self.update_save_button(False)  # Disable save button for empty fields
                return

            # Validate inputs first
            errors = self.validate_inputs()
            if errors:
                self.status_var.set("❌ Input validation failed")
                self.warning_text.set("; ".join(errors))
                self.warning_label.config(foreground="#dc2626")
                self.update_save_button(
                    False
                )  # Disable save button for validation errors
                return

            # Get input values - safe to convert now since we checked for empty fields
            loan_type = self.loan_type_var.get()
            principal = float(
                self.loan_amount_var.get().replace(",", "").replace("$", "")
            )
            term_years = float(self.term_years_var.get())
            monthly_income = float(
                self.monthly_income_var.get().replace(",", "").replace("$", "")
            )

            # Calculate loan details using our backend
            annual_rate = 4.5  # Default rate - in real system this would be calculated

            monthly_payment = calculate_monthly_payment(
                principal, annual_rate, term_years
            )
            total_interest = calculate_total_interest(
                monthly_payment, principal, term_years
            )
            total_amount = principal + total_interest

            # Calculate debt ratio
            debt_ratio = (monthly_payment / monthly_income) * 100

            # Update display
            self.monthly_payment_var.set(format_currency(monthly_payment))
            self.total_interest_var.set(format_currency(total_interest))
            self.total_amount_var.set(format_currency(total_amount))
            self.debt_ratio_var.set(f"{debt_ratio:.1f}%")

            # Check affordability and update status
            affordability = check_affordability(
                monthly_payment, monthly_income, loan_type
            )

            if affordability["is_affordable"]:
                self.status_var.set("✅ Loan Approved")
                self.status_result.config(foreground="#059669")
                self.warning_text.set("")
                self.warning_label.config(foreground="#059669")
                self.update_save_button(True)  # Enable save button
            else:
                self.status_var.set("⚠️ Review Required")
                self.status_result.config(foreground="#f59e0b")
                self.warning_text.set(affordability["message"])
                self.warning_label.config(foreground="#f59e0b")
                self.update_save_button(False)  # Disable save button

            # Update debt ratio color based on percentage
            if debt_ratio > 50:
                self.ratio_result.config(foreground="#dc2626")  # Red
                self.warning_text.set(
                    f"⚠️ High debt ratio: {debt_ratio:.1f}% (over 50%)"
                )
                self.warning_label.config(foreground="#dc2626")
            elif debt_ratio > 30:
                self.ratio_result.config(foreground="#f59e0b")  # Orange
            else:
                self.ratio_result.config(foreground="#059669")  # Green

        except Exception as e:
            self.status_var.set("❌ Calculation Error")
            self.warning_text.set(f"Error: {str(e)}")
            self.warning_label.config(foreground="#dc2626")
            self.update_save_button(False)  # Disable save button for calculation errors

    def save_loan(self):
        """Save loan record to CSV - only approved loans"""
        try:
            # Validate that we have valid calculations
            if self.monthly_payment_var.get() == "$0.00":
                messagebox.showwarning(
                    "No Data", "Please calculate a loan first before saving."
                )
                return

            # Check if loan is approved before allowing save
            current_status = self.status_var.get()
            if "Approved" not in current_status:
                messagebox.showwarning(
                    "Loan Not Approved",
                    "Only approved loans can be saved to records.\n\n"
                    "This loan requires review due to:\n"
                    f"• {self.warning_text.get()}\n\n"
                    "Please adjust the loan terms to get approval before saving.",
                )
                return

            # Prepare loan data
            loan_data = {
                "loan_type": self.loan_type_var.get(),
                "principal": float(
                    self.loan_amount_var.get().replace(",", "").replace("$", "")
                ),
                "annual_rate": 4.5,  # Default rate
                "term_years": float(self.term_years_var.get()),
                "monthly_payment": float(
                    self.monthly_payment_var.get().replace(",", "").replace("$", "")
                ),
                "total_interest": float(
                    self.total_interest_var.get().replace(",", "").replace("$", "")
                ),
                "status": "Approved",  # Only approved loans reach this point
                "monthly_income": float(
                    self.monthly_income_var.get().replace(",", "").replace("$", "")
                ),
            }

            # Save using our backend function
            if save_loan_record(loan_data, "loan_records.csv"):
                messagebox.showinfo(
                    "Success",
                    "Approved loan record saved successfully to loan_records.csv",
                )
                self.load_loan_records()  # Refresh the records display
            else:
                messagebox.showerror("Error", "Failed to save loan record")

        except Exception as e:
            messagebox.showerror("Error", f"Error saving loan record: {str(e)}")

    def clear_form(self):
        """Clear all form fields"""
        self.loan_amount_var.set("")
        self.term_years_var.set("")
        self.monthly_income_var.set("")

        # Reset results
        self.monthly_payment_var.set("$0.00")
        self.total_interest_var.set("$0.00")
        self.total_amount_var.set("$0.00")
        self.debt_ratio_var.set("0.0%")
        self.status_var.set("Ready to calculate")
        self.warning_text.set("")

        # Reset colors
        self.ratio_result.config(foreground="#1f2937")
        self.status_result.config(foreground="#1f2937")
        self.warning_label.config(foreground="#1f2937")

        # Disable save button
        self.update_save_button(False)

    def update_save_button(self, enabled):
        """Update save button appearance based on loan approval status"""
        if enabled:
            # Loan is approved - enable save button
            self.save_btn.config(
                text="💾 Save Approved Loan",
                bg="#059669",
                fg="white",
                state="normal",
                cursor="hand2",
            )
        else:
            # Loan not approved or no data - disable save button
            self.save_btn.config(
                text="💾 Save Loan Record (Approved Only)",
                bg="#6b7280",
                fg="white",
                state="disabled",
                cursor="arrow",
            )

    def load_loan_records(self):
        """Load and display loan records from CSV"""
        try:
            self.records_text.delete("1.0", tk.END)

            # Try to read the CSV file
            import csv
            import os

            if not os.path.exists("loan_records.csv"):
                self.records_text.insert(
                    "1.0",
                    "No loan records found. Create and save a loan to see records here.",
                )
                return

            with open("loan_records.csv", "r", newline="", encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                records = list(reader)

            if not records:
                self.records_text.insert("1.0", "No loan records found.")
                return

            # Format and display records
            header = records[0]
            data_rows = records[1:]

            # Create formatted display
            formatted_text = "=" * 100 + "\n"
            formatted_text += f"{'LOAN RECORDS':^100}\n"
            formatted_text += "=" * 100 + "\n\n"

            for i, record in enumerate(data_rows, 1):
                formatted_text += f"RECORD #{i}\n"
                formatted_text += "-" * 50 + "\n"

                for j, field in enumerate(record):
                    if j < len(header):
                        formatted_text += f"{header[j]:<20}: {field}\n"

                formatted_text += "\n"

            self.records_text.insert("1.0", formatted_text)

        except Exception as e:
            self.records_text.insert("1.0", f"Error loading records: {str(e)}")


def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = LoanManagementGUI(root)

    # Load initial records
    app.load_loan_records()

    # Start the GUI
    root.mainloop()


if __name__ == "__main__":
    main()
