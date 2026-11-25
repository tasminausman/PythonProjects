"""
Expense Tracker (Pandas + NumPy version)
Concepts: Python basics + pandas (DataFrame, groupby, sort)
          + numpy (sum, mean, median, std, min, max).
"""

import numpy as np
import pandas as pd

# Expense table: one row per expense
expenses = pd.DataFrame(columns=["category", "amount", "note"]).astype(
    {"category": str, "amount": float, "note": str}
)


def read_amount():
    while True:
        value = input("Amount: ").strip()
        if value.replace(".", "", 1).isdigit() and float(value) > 0:
            return float(value)
        print("Enter a valid positive amount.")


def add_expense():
    category = input("Category (food, transport, bills...): ").strip().title()
    if category == "":
        print("Category cannot be empty.")
        return
    amount = read_amount()
    note = input("Note (optional): ").strip()
    expenses.loc[len(expenses)] = [category, amount, note]
    print("Expense added!")


def view_expenses():
    if len(expenses) == 0:
        print("No expenses yet.")
        return
    table = expenses.copy()
    table.index = table.index + 1          # numbering starts from 1
    table.index.name = "No."
    print()
    print(table.to_string())


def delete_expense():
    if len(expenses) == 0:
        print("No expenses yet.")
        return
    view_expenses()
    number = input("Enter the number to delete: ").strip()
    if number.isdigit() and 1 <= int(number) <= len(expenses):
        expenses.drop(expenses.index[int(number) - 1], inplace=True)
        expenses.reset_index(drop=True, inplace=True)
        print("Expense deleted.")
    else:
        print("Invalid number.")


def category_summary():
    if len(expenses) == 0:
        print("No expenses yet.")
        return
    # group rows by category and add up the amounts
    totals = expenses.groupby("category")["amount"].sum().sort_values(ascending=False)
    grand_total = totals.sum()

    print("\n----- Spending by Category -----")
    for category, amount in totals.items():
        percent = amount / grand_total * 100
        print(f"{category:<12}{amount:<10.2f}{percent:.1f}%")


def show_statistics():
    if len(expenses) == 0:
        print("No expenses yet.")
        return
    amounts = expenses["amount"].to_numpy()            # numpy array
    biggest = expenses.loc[expenses["amount"].idxmax()]

    print("\n----- Statistics -----")
    print(f"Number of expenses : {len(amounts)}")
    print(f"Total spent        : {np.sum(amounts):.2f}")
    print(f"Average expense    : {np.mean(amounts):.2f}")
    print(f"Median expense     : {np.median(amounts):.2f}")
    print(f"Std deviation      : {np.std(amounts):.2f}")
    print(f"Smallest expense   : {np.min(amounts):.2f}")
    print(f"Biggest expense    : {np.max(amounts):.2f} ({biggest['category']})")
    print(f"Categories used    : {', '.join(sorted(expenses['category'].unique()))}")


def export_csv():
    if len(expenses) == 0:
        print("No expenses yet.")
        return
    expenses.to_csv("expenses.csv", index=False)
    print("Saved as expenses.csv")


def main():
    print("=== Expense Tracker ===")
    while True:
        print("\n1) Add expense")
        print("2) View all expenses")
        print("3) Delete expense")
        print("4) Spending by category")
        print("5) Statistics")
        print("6) Export to CSV")
        print("7) Exit")
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            delete_expense()
        elif choice == "4":
            category_summary()
        elif choice == "5":
            show_statistics()
        elif choice == "6":
            export_csv()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
