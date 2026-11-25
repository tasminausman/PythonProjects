"""
Contact Book (Pandas + NumPy version)
Concepts: Python basics + pandas DataFrame (store, filter, sort contacts)
          + numpy (np.unique to count contacts per city).
"""

import numpy as np
import pandas as pd

# DataFrame = a table. Each row is one contact.
contacts = pd.DataFrame(columns=["name", "phone", "email", "city"])


def add_contact():
    name = input("Name: ").strip().title()
    if name == "":
        print("Name cannot be empty.")
        return
    if name in contacts["name"].values:
        print("This contact already exists.")
        return

    phone = input("Phone (digits only, at least 10): ").strip()
    if not phone.isdigit() or len(phone) < 10:
        print("Invalid phone number.")
        return

    email = input("Email (press Enter to skip): ").strip()
    if email == "":
        email = "N/A"
    city = input("City: ").strip().title()

    contacts.loc[len(contacts)] = [name, phone, email, city]
    print(f"{name} saved!")


def view_all():
    if len(contacts) == 0:
        print("Contact book is empty.")
        return
    sorted_contacts = contacts.sort_values("name")
    print()
    print(sorted_contacts[["name", "phone", "city"]].to_string(index=False))


def search_contact():
    if len(contacts) == 0:
        print("Contact book is empty.")
        return
    keyword = input("Search name: ").strip().lower()
    matches = contacts[contacts["name"].str.lower().str.contains(keyword, regex=False)]
    if len(matches) == 0:
        print("No contact found.")
    else:
        print()
        print(matches.to_string(index=False))


def update_contact():
    name = input("Name of contact to update: ").strip().title()
    if name not in contacts["name"].values:
        print("Contact not found.")
        return

    mask = contacts["name"] == name           # True only for this contact's row
    print("Press Enter to keep the old value.")
    phone = input("New phone: ").strip()
    email = input("New email: ").strip()
    city = input("New city: ").strip().title()

    if phone != "":
        if phone.isdigit() and len(phone) >= 10:
            contacts.loc[mask, "phone"] = phone
        else:
            print("Invalid phone, old phone kept.")
    if email != "":
        contacts.loc[mask, "email"] = email
    if city != "":
        contacts.loc[mask, "city"] = city
    print("Contact updated!")


def delete_contact():
    name = input("Name of contact to delete: ").strip().title()
    if name not in contacts["name"].values:
        print("Contact not found.")
        return
    row_index = contacts.index[contacts["name"] == name]
    contacts.drop(row_index, inplace=True)
    contacts.reset_index(drop=True, inplace=True)
    print(f"{name} deleted.")


def city_summary():
    if len(contacts) == 0:
        print("Contact book is empty.")
        return
    cities = contacts["city"].to_numpy(dtype=str)
    unique_cities, counts = np.unique(cities, return_counts=True)   # numpy counting

    print("\nContacts per city:")
    for city, number in zip(unique_cities, counts):
        print(f"  {city}: {number}")

    with_email = (contacts["email"] != "N/A").sum()
    print(f"\nTotal contacts      : {len(contacts)}")
    print(f"Contacts with email : {with_email}")


def main():
    print("=== Contact Book ===")
    while True:
        print("\n1) Add contact")
        print("2) View all contacts")
        print("3) Search contact")
        print("4) Update contact")
        print("5) Delete contact")
        print("6) Summary")
        print("7) Exit")

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            add_contact()
        elif choice == "2":
            view_all()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            city_summary()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
