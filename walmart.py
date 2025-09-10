items = []
prices = []
BUDGET = 100.0
TAX_RATE = 10.44 / 100


# Uzoma - User input handling and validation
def validate_price(item_price):
    if item_price < 0:
        return False
    return True


def validate_product_name(name):
    # Check if name is empty or only whitespace
    if not name or not name.strip():
        return False

    # Check if name is only digits
    if name.strip().isdigit():
        return False

    # Check if name contains only letters, numbers, and spaces
    for char in name:
        if not (char.isalnum() or char.isspace()):
            return False

    # Ensure name has at least one alphanumeric character
    has_alphanumeric = any(char.isalnum() for char in name)
    if not has_alphanumeric:
        return False

    return True


def calculate_tax(item_price):
    return item_price * TAX_RATE


def get_total_with_tax():
    """Calculate total price with tax for all items in cart"""
    total_before_tax = sum(prices)
    total_tax = total_before_tax * TAX_RATE
    return total_before_tax + total_tax


def get_remaining_budget():
    """Calculate remaining budget after tax"""
    return BUDGET - get_total_with_tax()


# Agrawal - Receipt display and checkout process
def display_receipt():
    """Display detailed receipt with all items and totals"""
    if not items:
        print("Your cart is empty!")
        return

    print("\n" + "=" * 50)
    print("           WALMART RECEIPT")
    print("=" * 50)

    total_before_tax = 0
    for i in range(len(items)):
        print(f"{i+1}. {items[i]:<25} ${prices[i]:.2f}")
        total_before_tax += prices[i]

    total_tax = total_before_tax * TAX_RATE
    total_after_tax = total_before_tax + total_tax

    print("-" * 50)
    print(f"Number of items: {len(items)}")
    print(f"Subtotal (before tax): ${total_before_tax:.2f}")
    print(f"Tax (10.44%): ${total_tax:.2f}")
    print(f"Total (after tax): ${total_after_tax:.2f}")
    print(f"Remaining budget: ${BUDGET - total_after_tax:.2f}")
    print("=" * 50)
    print("Thank you for shopping at Walmart!")
    print("=" * 50)


# Kelvin - Budget constraint logic
def can_afford_item(item_price):
    """Check if user can afford to add an item"""
    current_total = get_total_with_tax()
    item_with_tax = item_price + (item_price * TAX_RATE)
    return (current_total + item_with_tax) <= BUDGET


# Kelvin - Cart display
def display_cart():
    """Display current cart contents"""
    if not items:
        print("Your cart is empty!")
        return

    print("\n--- CURRENT CART ---")
    total_before_tax = 0
    for i in range(len(items)):
        print(f"{i+1}. {items[i]} - ${prices[i]:.2f}")
        total_before_tax += prices[i]

    total_tax = total_before_tax * TAX_RATE
    total_with_tax = total_before_tax + total_tax

    print(f"\nSubtotal: ${total_before_tax:.2f}")
    print(f"Tax: ${total_tax:.2f}")
    print(f"Total with tax: ${total_with_tax:.2f}")
    print(f"Remaining budget: ${BUDGET - total_with_tax:.2f}")
    print("-" * 20)


# Agrawal - Checkout process
def check_out():
    """Process checkout and display final receipt"""
    if not items:
        print("Cannot checkout with an empty cart!")
        return False
    display_cart()

    print("\n" + "=" * 30)
    print("      PROCESSING CHECKOUT")
    print("=" * 30)

    while True:
        confirm = input("\nProceed to checkout? (yes/no): ").lower().strip()
        if confirm in ["yes", "y"]:
            display_receipt()
            print("\n🎉 Checkout completed successfully!")
            print("Thank you for shopping at Walmart!")
            return True
        elif confirm in ["no", "n"]:
            print("Checkout cancelled. You can continue shopping.")
            return False
        else:
            print("Please enter 'yes' or 'no'")


# Uzoma - User input handling and validation
def add_product():
    """Add a product to the cart with validation"""
    # Validate product name
    while True:
        item_name = input("Enter the product's name: ").strip()
        if validate_product_name(item_name):
            break
        else:
            print("Invalid input. Product name cannot be empty or only numbers.")

    # Validate and get price
    while True:
        try:
            price_input = input("Enter the product's price: $").strip()
            item_price = float(price_input)

            # Round to 2 decimal places
            item_price = round(item_price, 2)

            if not validate_price(item_price):
                print("Invalid input. Price cannot be negative.")
                continue

            # Check if item can be afforded
            if not can_afford_item(item_price):
                item_with_tax = item_price + (item_price * TAX_RATE)
                remaining = get_remaining_budget()
                print(
                    f"\nSorry! Adding this item (${item_with_tax:.2f} with tax) would exceed your budget."
                )
                print(f"You have ${remaining:.2f} remaining to spend.")
                print(
                    f"Maximum item price you can afford: ${remaining / (1 + TAX_RATE):.2f}"
                )

                choice = (
                    input("Would you like to try a different price? (yes/no): ")
                    .lower()
                    .strip()
                )
                if choice not in ["yes", "y"]:
                    return
                continue

            break

        except ValueError:
            print("Invalid input. Price must be a number.")

    # Add item to cart
    items.append(item_name)
    prices.append(item_price)
    item_with_tax = item_price + (item_price * TAX_RATE)
    print(f"\n✓ {item_name} (${item_price:.2f}) added successfully!")
    print(f"  Price with tax: ${item_with_tax:.2f}")
    print(f"  Remaining budget: ${get_remaining_budget():.2f}")


def main():
    """Main program loop"""
    print("=" * 50)
    print("      WELCOME TO WALMART!")
    print("      Budget: $100.00")
    print("      Tax Rate: 10.44%")
    print("=" * 50)

    while True:
        # Display current status
        if items:
            print(f"\n📦 Cart: {len(items)} item(s)")
            print(f"💰 Remaining budget: ${get_remaining_budget():.2f}")
        else:
            print(f"\n📦 Cart is empty")
            print(f"💰 Full budget available: ${BUDGET:.2f}")

        # Check if budget is exhausted
        remaining = get_remaining_budget()
        if remaining <= 0:
            print("\n⚠️  You've reached your budget limit!")
            print("Please proceed to checkout or remove items.")

        # Display menu options
        print("\nSelect an option:")
        print("1 - Add Item")
        print("2 - View Cart")
        print("3 - Checkout")
        print("4 - Exit")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            if remaining <= 0:
                print("Cannot add items - budget exhausted!")
                continue
            add_product()

        elif choice == "2":
            display_cart()

        elif choice == "3":
            if check_out():
                break  # Exit after successful checkout

        elif choice == "4":
            if items:
                save_choice = (
                    input(
                        "You have items in your cart. Are you sure you want to exit? (yes/no): "
                    )
                    .lower()
                    .strip()
                )
                if save_choice in ["yes", "y"]:
                    print("Thank you for visiting Walmart!")
                    break
            else:
                print("Thank you for visiting Walmart!")
                break

        else:
            print("Invalid choice. Please select 1-4.")


if __name__ == "__main__":
    main()
