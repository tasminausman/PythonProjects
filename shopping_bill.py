"""
Shopping Bill Calculator (Pandas + NumPy version)
Concepts: Python basics + *args/**kwargs + pandas DataFrame (products and cart)
          + numpy (sum of prices).
"""

import numpy as np
import pandas as pd

# Product list as a table
products = pd.DataFrame({
    "product": ["rice", "oil", "tea", "sugar", "milk", "bread"],
    "price": [180, 550, 450, 140, 220, 120],
})

# Cart table: one row per item
cart = pd.DataFrame(columns=["item", "price", "qty"]).astype(
    {"item": str, "price": int, "qty": int}
)


def calculate_total(*prices, **options):
    # *prices -> any number of prices, **options -> discount=..., tax=...
    total = np.sum(prices)
    discount = options.get("discount", 0)
    tax = options.get("tax", 0)
    total = total - total * discount / 100
    total = total + total * tax / 100
    return round(float(total), 2)


def show_products():
    print("\n----- Products -----")
    print(products.to_string(index=False))


def add_to_cart():
    name = input("Product name: ").strip().lower()
    match = products[products["product"] == name]       # filter the table
    if len(match) == 0:
        print("Product not available.")
        return

    quantity = input("Quantity: ").strip()
    if not quantity.isdigit() or int(quantity) <= 0:
        print("Quantity must be a positive whole number.")
        return
    quantity = int(quantity)
    price = int(match["price"].iloc[0])

    if name in cart["item"].values:
        cart.loc[cart["item"] == name, "qty"] += quantity    # item already in cart
    else:
        cart.loc[len(cart)] = [name, price, quantity]
    print(f"Added {quantity} x {name.title()}")


def view_cart():
    if len(cart) == 0:
        print("Your cart is empty.")
        return
    cart_view = cart.copy()
    cart_view["total"] = cart_view["price"] * cart_view["qty"]
    print()
    print(cart_view.to_string(index=False))


def remove_item():
    name = input("Product to remove: ").strip().lower()
    if name not in cart["item"].values:
        print("Item not in cart.")
        return
    row_index = cart.index[cart["item"] == name]
    cart.drop(row_index, inplace=True)
    cart.reset_index(drop=True, inplace=True)
    print(f"{name.title()} removed.")


def generate_bill():
    if len(cart) == 0:
        print("Your cart is empty.")
        return

    line_totals = (cart["price"] * cart["qty"]).to_numpy()    # numpy array
    subtotal = int(np.sum(line_totals))

    # 10% discount when the subtotal is 2000 or more
    discount = 10 if subtotal >= 2000 else 0
    final_total = calculate_total(*line_totals, discount=discount, tax=5)

    view_cart()
    print("-" * 32)
    print(f"Subtotal : Rs. {subtotal}")
    print(f"Discount : {discount}%")
    print("Tax      : 5%")
    print(f"TOTAL    : Rs. {final_total}")

    premium = cart[cart["price"] > 400]                       # filter expensive items
    if len(premium) > 0:
        print("\nPremium items in your cart:", ", ".join(premium["item"].str.title()))

    biggest = cart.loc[(cart["price"] * cart["qty"]).idxmax(), "item"]
    print(f"Biggest spending: {biggest.title()}")


def main():
    print("=== Shopping Bill Calculator ===")
    while True:
        print("\n1) Show products")
        print("2) Add item to cart")
        print("3) View cart")
        print("4) Remove item")
        print("5) Generate bill")
        print("6) Exit")
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            show_products()
        elif choice == "2":
            add_to_cart()
        elif choice == "3":
            view_cart()
        elif choice == "4":
            remove_item()
        elif choice == "5":
            generate_bill()
        elif choice == "6":
            print("Thank you for shopping!")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
