
"""
Walmart Shopping System with GUI
- User Interface for shopping
- Admin Interface for transaction analysis
- Persistent transaction storage
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv
import os
from datetime import datetime
import json
from tkinter import scrolledtext

# Add this check for running in a headless environment
def is_headless():
    """Check if running in a headless environment"""
    return "DISPLAY" not in os.environ or not os.environ["DISPLAY"]


# Constants
BUDGET = 100.0
TAX_RATE = 10.44 / 100
TRANSACTIONS_FILE = "transactions.csv"

class WalmartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Walmart Shopping System")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Initialize data structures
        self.reset_cart()
        
        # Setup main frame
        self.setup_main_view()
    
    def reset_cart(self):
        """Reset the cart to empty state"""
        self.items = []
        self.prices = []
    
    def setup_main_view(self):
        """Setup the main view with user/admin selection"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Title
        title_label = tk.Label(main_frame, text="WALMART SHOPPING SYSTEM", 
                              font=("Arial", 20, "bold"))
        title_label.pack(pady=20)
        
        # Buttons Frame
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=30)
        
        # User Button
        user_btn = tk.Button(btn_frame, text="Customer Mode", 
                            command=self.setup_user_view,
                            font=("Arial", 14), width=15, height=2,
                            bg="#4CAF50", fg="white")
        user_btn.pack(side=tk.LEFT, padx=20)
        
        # Admin Button
        admin_btn = tk.Button(btn_frame, text="Admin Mode", 
                             command=self.setup_admin_view,
                             font=("Arial", 14), width=15, height=2,
                             bg="#2196F3", fg="white")
        admin_btn.pack(side=tk.LEFT, padx=20)
    
    def setup_user_view(self):
        """Setup the user shopping interface"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.reset_cart()
        
        # Main container
        container = tk.Frame(self.root)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Top frame for title and back button
        top_frame = tk.Frame(container, bg="#f0f0f0")
        top_frame.pack(fill=tk.X)
        
        # Back button
        back_btn = tk.Button(top_frame, text="← Back", 
                            command=self.setup_main_view,
                            font=("Arial", 10), bg="#ddd")
        back_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(top_frame, text="WALMART SHOPPING CART", 
                              font=("Arial", 16, "bold"), bg="#f0f0f0")
        title_label.pack(side=tk.LEFT, padx=50, pady=10)
        
        # Left frame for adding items
        left_frame = tk.Frame(container, padx=20, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add item frame
        add_frame = tk.LabelFrame(left_frame, text="Add Item", font=("Arial", 12))
        add_frame.pack(fill=tk.X, pady=10)
        
        # Item name
        name_frame = tk.Frame(add_frame)
        name_frame.pack(fill=tk.X, pady=5)
        name_label = tk.Label(name_frame, text="Item Name:", width=10, anchor='w')
        name_label.pack(side=tk.LEFT, padx=5)
        self.name_entry = tk.Entry(name_frame)
        self.name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Item price
        price_frame = tk.Frame(add_frame)
        price_frame.pack(fill=tk.X, pady=5)
        price_label = tk.Label(price_frame, text="Price ($):", width=10, anchor='w')
        price_label.pack(side=tk.LEFT, padx=5)
        self.price_entry = tk.Entry(price_frame)
        self.price_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Add button
        add_btn = tk.Button(add_frame, text="Add to Cart", 
                           command=self.add_to_cart,
                           bg="#4CAF50", fg="white")
        add_btn.pack(pady=10)
        
        # Budget info
        budget_frame = tk.Frame(left_frame)
        budget_frame.pack(fill=tk.X, pady=10)
        
        self.budget_label = tk.Label(budget_frame, 
                                    text=f"Budget: ${BUDGET:.2f}",
                                    font=("Arial", 12))
        self.budget_label.pack(side=tk.LEFT)
        
        self.remaining_label = tk.Label(budget_frame, 
                                      text=f"Remaining: ${BUDGET:.2f}",
                                      font=("Arial", 12))
        self.remaining_label.pack(side=tk.RIGHT)
        
        # Right frame for cart display
        right_frame = tk.LabelFrame(container, text="Shopping Cart", 
                                   font=("Arial", 12), padx=20, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Cart display
        self.cart_display = tk.Frame(right_frame)
        self.cart_display.pack(fill=tk.BOTH, expand=True)
        
        # Cart scrollable area
        cart_scroll = tk.Scrollbar(self.cart_display)
        cart_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.cart_list = tk.Listbox(self.cart_display, 
                                   yscrollcommand=cart_scroll.set,
                                   font=("Arial", 10), height=10)
        self.cart_list.pack(fill=tk.BOTH, expand=True)
        cart_scroll.config(command=self.cart_list.yview)
        
        # Total section
        total_frame = tk.Frame(right_frame)
        total_frame.pack(fill=tk.X, pady=10)
        
        self.subtotal_label = tk.Label(total_frame, 
                                      text="Subtotal: $0.00", 
                                      font=("Arial", 10))
        self.subtotal_label.pack(anchor='w')
        
        self.tax_label = tk.Label(total_frame, 
                                 text=f"Tax ({TAX_RATE*100:.2f}%): $0.00", 
                                 font=("Arial", 10))
        self.tax_label.pack(anchor='w')
        
        self.total_label = tk.Label(total_frame, 
                                   text="Total: $0.00", 
                                   font=("Arial", 12, "bold"))
        self.total_label.pack(anchor='w')
        
        # Buttons
        btn_frame = tk.Frame(right_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        remove_btn = tk.Button(btn_frame, text="Remove Selected", 
                              command=self.remove_item,
                              bg="#f44336", fg="white")
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        checkout_btn = tk.Button(btn_frame, text="Checkout", 
                                command=self.checkout,
                                bg="#2196F3", fg="white")
        checkout_btn.pack(side=tk.RIGHT, padx=5)
        
        # Update display
        self.update_cart_display()
    
    def setup_admin_view(self):
        """Setup the admin transaction analysis interface"""
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        container = tk.Frame(self.root)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Top frame for title and back button
        top_frame = tk.Frame(container, bg="#f0f0f0")
        top_frame.pack(fill=tk.X)
        
        # Back button
        back_btn = tk.Button(top_frame, text="← Back", 
                            command=self.setup_main_view,
                            font=("Arial", 10), bg="#ddd")
        back_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(top_frame, text="ADMIN DASHBOARD", 
                              font=("Arial", 16, "bold"), bg="#f0f0f0")
        title_label.pack(side=tk.LEFT, padx=50, pady=10)
        
        # Main frame for transaction display
        main_frame = tk.Frame(container, padx=20, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Transactions display
        transaction_frame = tk.LabelFrame(main_frame, text="Transaction History", 
                                        font=("Arial", 12))
        transaction_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create Treeview for transactions
        columns = ("date", "items", "subtotal", "tax", "total")
        self.tree = ttk.Treeview(transaction_frame, columns=columns, show="headings")
        
        # Define headings
        self.tree.heading("date", text="Date & Time")
        self.tree.heading("items", text="Items")
        self.tree.heading("subtotal", text="Subtotal ($)")
        self.tree.heading("tax", text="Tax ($)")
        self.tree.heading("total", text="Total ($)")
        
        # Define columns
        self.tree.column("date", width=150)
        self.tree.column("items", width=250)
        self.tree.column("subtotal", width=100, anchor="e")
        self.tree.column("tax", width=100, anchor="e")
        self.tree.column("total", width=100, anchor="e")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(transaction_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Add double-click event to view details
        self.tree.bind("<Double-1>", self.view_transaction_details)
        
        # Analytics Frame
        analytics_frame = tk.LabelFrame(main_frame, text="Analytics", 
                                      font=("Arial", 12))
        analytics_frame.pack(fill=tk.X, pady=10)
        
        # Stats display
        stats_frame = tk.Frame(analytics_frame)
        stats_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # Create stats labels
        self.total_sales_label = tk.Label(stats_frame, 
                                        text="Total Sales: $0.00", 
                                        font=("Arial", 12))
        self.total_sales_label.grid(row=0, column=0, padx=10, sticky='w')
        
        self.avg_transaction_label = tk.Label(stats_frame, 
                                            text="Avg. Transaction: $0.00", 
                                            font=("Arial", 12))
        self.avg_transaction_label.grid(row=0, column=1, padx=10, sticky='w')
        
        self.total_items_label = tk.Label(stats_frame, 
                                        text="Total Items Sold: 0", 
                                        font=("Arial", 12))
        self.total_items_label.grid(row=1, column=0, padx=10, sticky='w')
        
        self.transaction_count_label = tk.Label(stats_frame, 
                                             text="Transaction Count: 0", 
                                             font=("Arial", 12))
        self.transaction_count_label.grid(row=1, column=1, padx=10, sticky='w')
        
        # Load transactions
        self.load_transactions()
    
    def add_to_cart(self):
        """Add an item to the cart with validation"""
        # Get item details
        item_name = self.name_entry.get().strip()
        price_str = self.price_entry.get().strip()
        
        # Validate name
        if not item_name or item_name.isdigit():
            messagebox.showerror("Input Error", "Item name cannot be empty or only numbers")
            return
        
        # Validate price
        try:
            item_price = float(price_str)
            item_price = round(item_price, 2)
            
            if item_price < 0:
                messagebox.showerror("Input Error", "Price cannot be negative")
                return
        except ValueError:
            messagebox.showerror("Input Error", "Price must be a number")
            return
        
        # Check budget
        current_total = self.get_total_with_tax()
        item_with_tax = item_price + (item_price * TAX_RATE)
        
        if (current_total + item_with_tax) > BUDGET:
            remaining = BUDGET - current_total
            messagebox.showwarning("Budget Exceeded", 
                                 f"Adding this item (${item_with_tax:.2f} with tax) would exceed your budget.\n"
                                 f"You have ${remaining:.2f} remaining to spend.")
            return
        
        # Add to cart
        self.items.append(item_name)
        self.prices.append(item_price)
        
        # Clear entries
        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.name_entry.focus()
        
        # Update display
        self.update_cart_display()
        
        # Show confirmation
        messagebox.showinfo("Item Added", 
                          f"{item_name} (${item_price:.2f}) added to cart successfully!")
    
    def remove_item(self):
        """Remove selected item from cart"""
        try:
            # Get selected index
            selected_idx = self.cart_list.curselection()[0]
            
            # Remove from lists
            del self.items[selected_idx]
            del self.prices[selected_idx]
            
            # Update display
            self.update_cart_display()
            
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select an item to remove")
    
    def update_cart_display(self):
        """Update the cart display with current items"""
        # Clear current display
        self.cart_list.delete(0, tk.END)
        
        # Add items to list
        for i in range(len(self.items)):
            self.cart_list.insert(tk.END, f"{i+1}. {self.items[i]} - ${self.prices[i]:.2f}")
        
        # Calculate totals
        subtotal = sum(self.prices)
        tax = subtotal * TAX_RATE
        total = subtotal + tax
        remaining = BUDGET - total
        
        # Update labels
        self.subtotal_label.config(text=f"Subtotal: ${subtotal:.2f}")
        self.tax_label.config(text=f"Tax ({TAX_RATE*100:.2f}%): ${tax:.2f}")
        self.total_label.config(text=f"Total: ${total:.2f}")
        self.remaining_label.config(text=f"Remaining: ${remaining:.2f}")
    
    def get_total_with_tax(self):
        """Calculate total price with tax for all items in cart"""
        subtotal = sum(self.prices)
        tax = subtotal * TAX_RATE
        return subtotal + tax
    
    def checkout(self):
        """Process checkout and save transaction"""
        if not self.items:
            messagebox.showwarning("Empty Cart", "Cannot checkout with an empty cart!")
            return
        
        # Calculate totals
        subtotal = sum(self.prices)
        tax = subtotal * TAX_RATE
        total = subtotal + tax
        
        # Confirm checkout
        confirm = messagebox.askyesno("Confirm Checkout", 
                                     f"Proceed to checkout?\n\n"
                                     f"Subtotal: ${subtotal:.2f}\n"
                                     f"Tax: ${tax:.2f}\n"
                                     f"Total: ${total:.2f}")
        
        if not confirm:
            return
        
        # Save transaction
        self.save_transaction(subtotal, tax, total)
        
        # Show receipt
        self.show_receipt(subtotal, tax, total)
        
        # Reset cart and return to main menu
        self.reset_cart()
        self.setup_main_view()
    
    def save_transaction(self, subtotal, tax, total):
        """Save transaction to CSV file"""
        # Create file if it doesn't exist
        file_exists = os.path.isfile(TRANSACTIONS_FILE)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Format items as JSON string
        items_data = []
        for i in range(len(self.items)):
            items_data.append({
                "name": self.items[i],
                "price": self.prices[i]
            })
        items_json = json.dumps(items_data)
        
        # Write to CSV
        with open(TRANSACTIONS_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            
            # Write header if new file
            if not file_exists:
                writer.writerow(["timestamp", "items", "subtotal", "tax", "total"])
            
            # Write transaction data
            writer.writerow([timestamp, items_json, subtotal, tax, total])
    
    def load_transactions(self):
        """Load transactions from CSV file and display in admin view"""
        # Clear current display
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        # Check if file exists
        if not os.path.isfile(TRANSACTIONS_FILE):
            return
        
        # Read transaction data
        transactions = []
        total_sales = 0
        total_items = 0
        
        with open(TRANSACTIONS_FILE, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                transactions.append(row)
                
                # Update statistics
                total_sales += float(row['total'])
                
                # Get items count
                items = json.loads(row['items'])
                total_items += len(items)
        
        # Display transactions in tree
        for t in transactions:
            # Get item count
            items = json.loads(t['items'])
            item_display = f"{len(items)} items"
            
            # Insert into tree
            self.tree.insert("", tk.END, values=(
                t['timestamp'],
                item_display,
                f"{float(t['subtotal']):.2f}",
                f"{float(t['tax']):.2f}",
                f"{float(t['total']):.2f}"
            ))
        
        # Update statistics
        transaction_count = len(transactions)
        avg_transaction = total_sales / transaction_count if transaction_count > 0 else 0
        
        self.total_sales_label.config(text=f"Total Sales: ${total_sales:.2f}")
        self.avg_transaction_label.config(text=f"Avg. Transaction: ${avg_transaction:.2f}")
        self.total_items_label.config(text=f"Total Items Sold: {total_items}")
        self.transaction_count_label.config(text=f"Transaction Count: {transaction_count}")
    
    def view_transaction_details(self, event):
        """Display detailed transaction information when double-clicked"""
        # Get selected item
        item = self.tree.selection()[0]
        transaction = self.tree.item(item, "values")
        
        # Get full transaction data
        with open(TRANSACTIONS_FILE, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['timestamp'] == transaction[0]:  # Match by timestamp
                    # Create detail window
                    detail_window = tk.Toplevel(self.root)
                    detail_window.title("Transaction Details")
                    detail_window.geometry("500x400")
                    
                    # Transaction info
                    tk.Label(detail_window, text=f"Transaction: {row['timestamp']}", 
                            font=("Arial", 14, "bold")).pack(pady=10)
                    
                    # Items frame with scrollbar
                    items_frame = tk.Frame(detail_window)
                    items_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
                    
                    # Create text widget for items
                    items_text = scrolledtext.ScrolledText(items_frame, wrap=tk.WORD, 
                                                         width=40, height=10)
                    items_text.pack(fill=tk.BOTH, expand=True)
                    
                    # Add items to text widget
                    items = json.loads(row['items'])
                    items_text.insert(tk.END, "Items:\n")
                    for i, item in enumerate(items):
                        items_text.insert(tk.END, f"{i+1}. {item['name']} - ${float(item['price']):.2f}\n")
                    
                    # Add totals
                    totals_frame = tk.Frame(detail_window)
                    totals_frame.pack(fill=tk.X, padx=20, pady=10)
                    
                    tk.Label(totals_frame, text=f"Subtotal: ${float(row['subtotal']):.2f}", 
                            font=("Arial", 12)).pack(anchor='w')
                    tk.Label(totals_frame, text=f"Tax: ${float(row['tax']):.2f}", 
                            font=("Arial", 12)).pack(anchor='w')
                    tk.Label(totals_frame, text=f"Total: ${float(row['total']):.2f}", 
                            font=("Arial", 12, "bold")).pack(anchor='w')
                    
                    # Close button
                    tk.Button(detail_window, text="Close", 
                             command=detail_window.destroy,
                             font=("Arial", 12)).pack(pady=10)
                    
                    # Make items_text read-only
                    items_text.config(state=tk.DISABLED)
                    
                    # Center the window
                    detail_window.update_idletasks()
                    width = detail_window.winfo_width()
                    height = detail_window.winfo_height()
                    x = (detail_window.winfo_screenwidth() // 2) - (width // 2)
                    y = (detail_window.winfo_screenheight() // 2) - (height // 2)
                    detail_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
                    
                    break
    
    def show_receipt(self, subtotal, tax, total):
        """Display receipt in a new window"""
        receipt_window = tk.Toplevel(self.root)
        receipt_window.title("Walmart Receipt")
        receipt_window.geometry("400x500")
        
        # Receipt content
        receipt_frame = tk.Frame(receipt_window, padx=20, pady=20)
        receipt_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        tk.Label(receipt_frame, text="WALMART RECEIPT", 
               font=("Arial", 16, "bold")).pack(pady=10)
        
        tk.Label(receipt_frame, text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
               font=("Arial", 10)).pack()
        
        # Separator
        ttk.Separator(receipt_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Items list with scrollbar
        items_frame = tk.Frame(receipt_frame)
        items_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        scrollbar = tk.Scrollbar(items_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        items_text = tk.Text(items_frame, height=10, yscrollcommand=scrollbar.set)
        items_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=items_text.yview)
        
        # Add items to text
        for i in range(len(self.items)):
            items_text.insert(tk.END, f"{i+1}. {self.items[i]:<25} ${self.prices[i]:.2f}\n")
        
        # Make text read-only
        items_text.config(state=tk.DISABLED)
        
        # Totals
        totals_frame = tk.Frame(receipt_frame)
        totals_frame.pack(fill=tk.X, pady=10)
        
        # Separator
        ttk.Separator(totals_frame, orient='horizontal').pack(fill=tk.X, pady=5)
        
        tk.Label(totals_frame, text=f"Number of items: {len(self.items)}", 
               font=("Arial", 10)).pack(anchor='w')
        tk.Label(totals_frame, text=f"Subtotal (before tax): ${subtotal:.2f}", 
               font=("Arial", 10)).pack(anchor='w')
        tk.Label(totals_frame, text=f"Tax ({TAX_RATE*100:.2f}%): ${tax:.2f}", 
               font=("Arial", 10)).pack(anchor='w')
        
        # Final total
        tk.Label(totals_frame, text=f"Total (after tax): ${total:.2f}", 
               font=("Arial", 12, "bold")).pack(anchor='w')
        
        # Footer
        tk.Label(receipt_frame, text="Thank you for shopping at Walmart!", 
               font=("Arial", 12)).pack(pady=10)
        
        # Print button
        tk.Button(receipt_frame, text="Close", 
                command=receipt_window.destroy).pack(pady=10)
        
        # Center the window
        receipt_window.update_idletasks()
        width = receipt_window.winfo_width()
        height = receipt_window.winfo_height()
        x = (receipt_window.winfo_screenwidth() // 2) - (width // 2)
        y = (receipt_window.winfo_screenheight() // 2) - (height // 2)
        receipt_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

# Main application
if __name__ == "__main__":
    
        # GUI mode
        root = tk.Tk()
        app = WalmartApp(root)
        root.mainloop()