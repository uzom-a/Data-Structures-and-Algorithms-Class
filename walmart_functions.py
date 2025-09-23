
items = []
prices = []
TAX_RATE = 10.44 / 100
TRANSACTIONS_FILE = "transactions.csv"

import csv
import os
import json
from datetime import datetime


#Uzoma - User input handling and validation
def validate_price(item_price):
    if item_price < 0:
        return False
    return True

def validate_product_name(name):
    
    if not name or name.strip() == "":
        return False
    if name.strip().isdigit():
        return False
    return True


def calculate_tax(item_price):
    return item_price * TAX_RATE

def get_total_with_tax(prices_list):
    """Calculate total price with tax for all items in cart"""
    subtotal = sum(prices_list)
    tax = subtotal * TAX_RATE
    return subtotal + tax

# Transaction management functions
def save_transaction(items, prices, transaction_file=TRANSACTIONS_FILE):
    """Save transaction to CSV file"""
    # Create file if it doesn't exist
    file_exists = os.path.isfile(transaction_file)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Calculate totals
    subtotal = sum(prices)
    tax = subtotal * TAX_RATE
    total = subtotal + tax
    
    # Format items as JSON string
    items_data = []
    for i in range(len(items)):
        items_data.append({
            "name": items[i],
            "price": prices[i]
        })
    items_json = json.dumps(items_data)
    
    # Write to CSV
    with open(transaction_file, 'a', newline='') as file:
        writer = csv.writer(file)
        
        # Write header if new file is needed
        if not file_exists:
            writer.writerow(["timestamp", "items", "subtotal", "tax", "total"])
        
        # Write transaction data here
        writer.writerow([timestamp, items_json, subtotal, tax, total])
    
    return {
        "timestamp": timestamp,
        "subtotal": subtotal,
        "tax": tax,
        "total": total
    }

def load_transactions(transaction_file=TRANSACTIONS_FILE):
    """Load transactions from CSV file and calculate statistics"""
    if not os.path.isfile(transaction_file):
        return {
            "transactions": [],
            "total_sales": 0,
            "total_items": 0,
            "transaction_count": 0,
            "avg_transaction": 0
        }
    
    # Read transaction data
    transactions = []
    total_sales = 0
    total_items = 0
    
    with open(transaction_file, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        
        for row in reader:
            timestamp, items_json, subtotal, tax, total = row
            items_data = json.loads(items_json)
            item_count = len(items_data)
            
            transactions.append({
                "timestamp": timestamp,
                "items": items_data,
                "subtotal": float(subtotal),
                "tax": float(tax),
                "total": float(total),
                "item_count": item_count
            })
            
            total_sales += float(total)
            total_items += item_count
    
    transaction_count = len(transactions)
    avg_transaction = total_sales / transaction_count if transaction_count > 0 else 0
    
    return {
        "transactions": transactions,
        "total_sales": total_sales,
        "total_items": total_items,
        "transaction_count": transaction_count,
        "avg_transaction": avg_transaction
    }

def get_transaction_details(timestamp, transaction_file=TRANSACTIONS_FILE):
    """Get detailed information for a specific transaction"""
    if not os.path.isfile(transaction_file):
        return None
    
    with open(transaction_file, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        
        for row in reader:
            row_timestamp, items_json, subtotal, tax, total = row
            
            # Match based on timestamp
            if row_timestamp == timestamp:
                return {
                    "timestamp": row_timestamp,
                    "items": json.loads(items_json),
                    "subtotal": float(subtotal),
                    "tax": float(tax),
                    "total": float(total)
                }
    
    return None


