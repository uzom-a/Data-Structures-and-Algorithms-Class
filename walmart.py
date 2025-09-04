"""
This is for lab 2

Create a Python program that simulates a shopping experience at Walmart with a
budget of $100. The program should ensure that users do not exceed their budget,
account for
tax, and display a receipt upon checkout.

"""

"""
1. user input product
2. output receipt
3. calculate the tax
4. calculate the limit (100)

5. Cart Display:
o Store item names in an array.
o Store item prices in a corresponding array.

6 Display a receipt at checkout showing:
▪ List of items and their prices.
▪ Number of items purchased.
▪ Total price before tax.
▪ Total price after tax.

Edge cases
1. no negative prices
2. if the items in cart already cost $100, prompt user that price + tax is above budget
3. display left money to spend
4. accept up to 2d.p in amount
5. product names cannot only be numbers

"""


# def add_product():
#     item_name = input("Enter the product's name: ").strip()
#     item_price = int(input("Enter the product's price: "))


def validate_price():
    pass


def calculate_tax(item_price):
    tax_rate = 10.44 / 100
    return item_price * tax_rate + item_price


# Agrawal
def display_receipt():
    pass


# Kelvin
def calculte_budget():
    pass


# Kelvin
def display_cart():
    pass


# Agrawal
def check_out():
    pass


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


# def validate_price():
#     pass
