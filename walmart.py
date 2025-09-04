"""
This is for lab 2

Create a Python program that simulates a shopping experience at Walmart with a
budget of $100. The program should ensure that users do not exceed their budget,
account for
tax, and display a receipt upon checkout.

"""

def add_product():
    item_name = input("Enter the product's name: ").strip()

    while True:
            try:
                item_price = int(input("Enter the product's price: "))
                if not validate_price(item_price):
                    print("Invalid input. Item_Price should not be a negative number")
                else:
                     break
            except ValueError:
                print("Invalid input. Item_Price must be an integer")
       

def calculate_tax(item_price):
    tax_rate = 10.44 / 100
    return item_price * tax_rate + item_price

def validate_price():
    pass