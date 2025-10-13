"""
Bank Loan Management System - GUI Application
Clean and user-friendly interface for loan calculations
"""

import tkinter as tk
from tkinter import ttk, messagebox
import csv
from loan_logic import (
    LOAN_TYPES,
    validate_loan_amount, 
    validate_term,
    validate_income,
    calculate_monthly_payment,
    calculate_total_interest,
    check_affordability,
    calculate_loan_eligibility,
    format_currency
)


class LoanManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Loan Management System")
        self.root.geometry("700x750")
        self.root.configure(bg="#f0f4f8")
        
        # Center window on screen
        self.center_window()
        
        # Create UI components
        self.create_widgets()
        
        # Store last calculation data
        self.last_calculation = None
    
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = 650
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#f5f5f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🏦 Bank Loan Calculator",
            font=("Arial", 24, "bold"),
            bg="#f5f5f5",
            fg="#2c3e50"
        )
        title_label.pack(pady=(0, 20))
        
        # Input Frame
        input_frame = tk.LabelFrame(
            main_frame,
            text="  Loan Information  ",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#34495e",
            padx=20,
            pady=15
        )
        input_frame.pack(fill=tk.BOTH, pady=(0, 15))
        
        # Loan Type
        tk.Label(
            input_frame,
            text="Loan Type:",
            font=("Arial", 11),
            bg="white"
        ).grid(row=0, column=0, sticky="w", pady=8)
        
        self.loan_type_var = tk.StringVar(value="Housing")
        loan_type_combo = ttk.Combobox(
            input_frame,
            textvariable=self.loan_type_var,
            values=list(LOAN_TYPES.keys()),
            state="readonly",
            font=("Arial", 11),
            width=28
        )
        loan_type_combo.grid(row=0, column=1, pady=8, sticky="ew")
        loan_type_combo.bind("<<ComboboxSelected>>", self.update_loan_info)
        
        # Loan info label (shows rate and max term)
        self.loan_info_label = tk.Label(
            input_frame,
            text=self.get_loan_info_text("Housing"),
            font=("Arial", 9),
            bg="white",
            fg="#7f8c8d"
        )
        self.loan_info_label.grid(row=1, column=1, sticky="w", pady=(0, 8))
        
        # Loan Amount
        tk.Label(
            input_frame,
            text="Loan Amount ($):",
            font=("Arial", 11),
            bg="white"
        ).grid(row=2, column=0, sticky="w", pady=8)
        
        self.loan_amount_var = tk.StringVar()
        tk.Entry(
            input_frame,
            textvariable=self.loan_amount_var,
            font=("Arial", 11),
            width=30
        ).grid(row=2, column=1, pady=8, sticky="ew")
        
        # Loan Term
        tk.Label(
            input_frame,
            text="Loan Term (Years):",
            font=("Arial", 11),
            bg="white"
        ).grid(row=3, column=0, sticky="w", pady=8)
        
        self.term_var = tk.StringVar()
        tk.Entry(
            input_frame,
            textvariable=self.term_var,
            font=("Arial", 11),
            width=30
        ).grid(row=3, column=1, pady=8, sticky="ew")
        
        # Monthly Income
        tk.Label(
            input_frame,
            text="Monthly Income ($):",
            font=("Arial", 11),
            bg="white"
        ).grid(row=4, column=0, sticky="w", pady=8)
        
        self.income_var = tk.StringVar()
        tk.Entry(
            input_frame,
            textvariable=self.income_var,
            font=("Arial", 11),
            width=30
        ).grid(row=4, column=1, pady=8, sticky="ew")
        
        input_frame.columnconfigure(1, weight=1)
        
        # Calculate Button
        calc_button = tk.Button(
            main_frame,
            text="Calculate Loan",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            padx=30,
            pady=12,
            cursor="hand2",
            relief=tk.FLAT,
            command=self.calculate_loan
        )
        calc_button.pack(pady=10)
        
        # Results Frame
        results_frame = tk.LabelFrame(
            main_frame,
            text="  Calculation Results  ",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#34495e",
            padx=20,
            pady=15
        )
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Monthly Payment
        tk.Label(
            results_frame,
            text="Monthly Payment:",
            font=("Arial", 11, "bold"),
            bg="white"
        ).grid(row=0, column=0, sticky="w", pady=8)
        
        self.monthly_payment_label = tk.Label(
            results_frame,
            text="$0.00",
            font=("Arial", 11),
            bg="white",
            fg="#27ae60"
        )
        self.monthly_payment_label.grid(row=0, column=1, sticky="e", pady=8)
        
        # Total Interest
        tk.Label(
            results_frame,
            text="Total Interest:",
            font=("Arial", 11, "bold"),
            bg="white"
        ).grid(row=1, column=0, sticky="w", pady=8)
        
        self.total_interest_label = tk.Label(
            results_frame,
            text="$0.00",
            font=("Arial", 11),
            bg="white",
            fg="#e74c3c"
        )
        self.total_interest_label.grid(row=1, column=1, sticky="e", pady=8)
        
        # Total Amount
        tk.Label(
            results_frame,
            text="Total Amount to Pay:",
            font=("Arial", 11, "bold"),
            bg="white"
        ).grid(row=2, column=0, sticky="w", pady=8)
        
        self.total_amount_label = tk.Label(
            results_frame,
            text="$0.00",
            font=("Arial", 11),
            bg="white",
            fg="#34495e"
        )
        self.total_amount_label.grid(row=2, column=1, sticky="e", pady=8)
        
        # Payment to Income Ratio
        tk.Label(
            results_frame,
            text="Payment-to-Income:",
            font=("Arial", 11, "bold"),
            bg="white"
        ).grid(row=3, column=0, sticky="w", pady=8)
        
        self.debt_ratio_label = tk.Label(
            results_frame,
            text="0.00%",
            font=("Arial", 11),
            bg="white",
            fg="#34495e"
        )
        self.debt_ratio_label.grid(row=3, column=1, sticky="e", pady=8)
        
        # Separator
        ttk.Separator(results_frame, orient='horizontal').grid(
            row=4, column=0, columnspan=2, sticky="ew", pady=10
        )
        
        # Status Message
        self.status_label = tk.Label(
            results_frame,
            text="Enter loan details and click Calculate",
            font=("Arial", 10),
            bg="white",
            fg="#7f8c8d",
            wraplength=550,
            justify="left"
        )
        self.status_label.grid(row=5, column=0, columnspan=2, sticky="w", pady=(5, 0))
        
        results_frame.columnconfigure(1, weight=1)
        
        # Clear Button
        clear_button = tk.Button(
            main_frame,
            text="Clear Form",
            font=("Arial", 10),
            bg="#95a5a6",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2",
            relief=tk.FLAT,
            command=self.clear_form
        )
        clear_button.pack(pady=(10, 0))
    
    def get_loan_info_text(self, loan_type):
        """Get formatted loan type information"""
        info = LOAN_TYPES[loan_type]
        return f"Interest Rate: {info['rate']}% | Max Term: {info['max_term']} years"
    
    def update_loan_info(self, event=None):
        """Update loan information when type changes"""
        loan_type = self.loan_type_var.get()
        self.loan_info_label.config(text=self.get_loan_info_text(loan_type))
    
    def calculate_loan(self):
        """Main calculation logic"""
        try:
            # Get inputs
            loan_type = self.loan_type_var.get()
            loan_amount_str = self.loan_amount_var.get().strip()
            term_str = self.term_var.get().strip()
            income_str = self.income_var.get().strip()
            
            # Validate loan amount
            is_valid, error = validate_loan_amount(loan_amount_str)
            if not is_valid:
                messagebox.showerror("Invalid Input", f"Loan Amount: {error}")
                return
            
            # Validate term
            is_valid, error = validate_term(term_str, loan_type)
            if not is_valid:
                messagebox.showerror("Invalid Input", f"Loan Term: {error}")
                return
            
            # Validate income
            is_valid, error = validate_income(income_str)
            if not is_valid:
                messagebox.showerror("Invalid Input", f"Monthly Income: {error}")
                return
            
            # Convert to numbers
            loan_amount = float(loan_amount_str)
            term_years = int(term_str)
            monthly_income = float(income_str)
            interest_rate = LOAN_TYPES[loan_type]["rate"]
            
            # Calculate monthly payment and total interest
            monthly_payment = calculate_monthly_payment(loan_amount, interest_rate, term_years)
            total_interest = calculate_total_interest(monthly_payment, loan_amount, term_years)
            total_amount = loan_amount + total_interest
            affordability = check_affordability(monthly_payment, monthly_income)
            eligibility = calculate_loan_eligibility(loan_amount, monthly_income)
            
            # Update display
            self.monthly_payment_label.config(text=f"${monthly_payment:,.2f}")
            self.total_interest_label.config(text=f"${total_interest:,.2f}")
            self.total_amount_label.config(text=f"${total_amount:,.2f}")
            self.debt_ratio_label.config(text=f"{affordability['payment_ratio']:.2f}%")
            
            # Update status message and suggest term adjustment if needed
            if affordability['is_affordable']:
                status_text = (
                    f"✓ APPROVED: This loan is affordable. "
                    f"Monthly payment is {affordability['payment_ratio']:.1f}% "
                    f"of your income (maximum 50%)."
                )
                status_color = "#059669"  # Green
                loan_status = "Approved"
            else:
                # Calculate a suggested term to make the loan affordable
                max_term = LOAN_TYPES[loan_type]["max_term"]
                suggested_term = self.suggest_term(loan_amount, interest_rate, monthly_income, term_years, max_term)
                
                if suggested_term is not None and suggested_term > term_years and suggested_term <= max_term:
                    status_text = (
                        f"⚠ WARNING: Monthly payment (${monthly_payment:,.2f}) "
                        f"is {affordability['payment_ratio']:.1f}% of your income, exceeding the 50% limit. "
                        f"Suggestion: Consider extending your term to {suggested_term} years "
                        f"to reduce the monthly payment."
                    )
                else:
                    status_text = (
                        f"⚠ WARNING: Monthly payment (${monthly_payment:,.2f}) "
                        f"is {affordability['payment_ratio']:.1f}% of your income, exceeding the 50% limit. "
                        f"Consider reducing your loan amount or increasing your income."
                    )
                status_color = "#dc2626"  # Red
                loan_status = "Needs Adjustment"
            
            self.status_label.config(text=status_text, fg=status_color)
            
            # Store calculation for finalization
            self.last_calculation = {
                "loan_type": loan_type,
                "loan_amount": loan_amount,
                "interest_rate": interest_rate,
                "term": term_years,
                "monthly_payment": monthly_payment,
                "total_interest": total_interest,
                "status": loan_status
            }
            # If eligibility fails (e.g., loan amount too large compared to income), treat as Rejected
            if not eligibility['eligible']:
                self.status_label.config(text=f"REJECTED: {eligibility['reason']}", fg="#b91c1c")
                # Do not show finalize dialog when rejected
                return

            # If payment exceeds 50% of income, don't offer finalization. Suggest adjustments.
            if not affordability['is_affordable']:
                max_term = LOAN_TYPES[loan_type]["max_term"]
                suggested_term = self.suggest_term(loan_amount, interest_rate, monthly_income, term_years, max_term)
                if suggested_term is not None and suggested_term > term_years:
                    warn_msg = (
                        f"Monthly payment {format_currency(monthly_payment)} is {affordability['payment_ratio']:.1f}% of your income,\n"
                        f"which exceeds the 50% allowed debt ratio.\n\n"
                        f"Suggestion: extend the term to {suggested_term} years to reduce the monthly payment.\n"
                        f"Or reduce the loan amount and try again."
                    )
                else:
                    warn_msg = (
                        f"Monthly payment {format_currency(monthly_payment)} is {affordability['payment_ratio']:.1f}% of your income,\n"
                        f"which exceeds the 50% allowed debt ratio.\n\n"
                        "Consider reducing the loan amount or increasing your income."
                    )
                messagebox.showwarning("Debt Ratio Exceeded", warn_msg)
                return

            # Show a concise summary dialog with option to proceed or adjust
            summary_msg = (
                f"Loan Type: {loan_type}\n"
                f"Loan Amount: {format_currency(loan_amount)}\n"
                f"Term: {term_years} years\n"
                f"Monthly Payment: {format_currency(monthly_payment)}\n"
                f"Total Interest: {format_currency(total_interest)}\n"
                f"Payment-to-Income: {affordability['payment_ratio']:.1f}%\n\n"
                "Would you like to finalize this loan (save to CSV) or adjust inputs?"
            )

            proceed = messagebox.askyesno("Loan Summary", summary_msg)
            if proceed:
                # If user chooses to proceed, call finalize which will save the record
                self.finalize_loan()
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def suggest_term(self, loan_amount, interest_rate, monthly_income, current_term, max_term):
        """Suggest a term (greater than current_term) that would make the loan affordable.

        Returns the suggested term (int) or None if no longer term up to max_term would help.
        """
        # Max affordable payment is 50% of monthly income
        max_payment = monthly_income * 0.5

        # Start from the next year after current term to avoid suggesting same term
        for term in range(current_term + 1, max_term + 1):
            payment = calculate_monthly_payment(loan_amount, interest_rate, term)
            if payment <= max_payment:
                return term

        # If no term works, return None
        return None
    
    def finalize_loan(self):
        """Finalize and save the loan to CSV"""
        if self.last_calculation is None:
            messagebox.showwarning("No Calculation", "Please calculate a loan first before finalizing.")
            return
        
        # For loans that need adjustment, ask for confirmation
        if self.last_calculation["status"] == "Needs Adjustment":
            proceed = messagebox.askyesno(
                "Loan Needs Adjustment",
                "This loan exceeds the recommended debt-to-income ratio. Do you still want to proceed?"
            )
            if not proceed:
                return
        
        # Save to CSV
        try:
            self.save_loan_to_csv()
            messagebox.showinfo(
                "Loan Finalized",
                "Loan has been finalized and saved to loan_records.csv!"
            )
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save loan record: {str(e)}")
    
    def save_loan_to_csv(self):
        """Save loan details to CSV file"""
        file_path = "loan_records.csv"
        
        # Check if file exists to determine if we need headers
        try:
            with open(file_path, 'x', newline='') as file:
                writer = csv.writer(file)
                # Write header row
                writer.writerow([
                    "Loan Type", "Loan Amount", "Interest Rate", 
                    "Term", "Monthly Payment", "Total Interest", "Status"
                ])
                file_exists = False
        except FileExistsError:
            file_exists = True
        
        # Append the new record
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                self.last_calculation["loan_type"],
                f"{self.last_calculation['loan_amount']:.2f}",
                f"{self.last_calculation['interest_rate']:.2f}",
                self.last_calculation["term"],
                f"{self.last_calculation['monthly_payment']:.2f}",
                f"{self.last_calculation['total_interest']:.2f}",
                self.last_calculation["status"]
            ])
        
        return True
    
    def clear_form(self):
        """Clear all input fields and results"""
        self.loan_amount_var.set("")
        self.term_var.set("")
        self.income_var.set("")
        self.loan_type_var.set("Housing")
        self.update_loan_info()
        
        self.monthly_payment_label.config(text="$0.00")
        self.total_interest_label.config(text="$0.00")
        self.total_amount_label.config(text="$0.00")
        self.debt_ratio_label.config(text="0.00%")
        self.status_label.config(
            text="Enter loan details and click Calculate",
            fg="#7f8c8d"
        )
        
        self.last_calculation = None


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = LoanManagementGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
