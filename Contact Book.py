import tkinter as tk
from tkinter import messagebox
import re

class ContactBookApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Contact Book")
        self.geometry("500x600")
        self.configure(bg="white")
        
        # Dictionary to store contacts
        self.contacts = {}
        
        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        """Create and arrange the widgets in the GUI."""
        
        # Title Label
        title_label = tk.Label(self, text="Contact Book", font=("Arial", 18), bg="white")
        title_label.pack(pady=10)
        
        # Name Entry
        self.name_label = tk.Label(self, text="Name:", font=("Arial", 12), bg="white")
        self.name_label.pack(pady=5)
        self.name_entry = tk.Entry(self, font=("Arial", 12), width=40)
        self.name_entry.pack(pady=5)
        
        # Phone Entry
        self.phone_label = tk.Label(self, text="Phone:", font=("Arial", 12), bg="white")
        self.phone_label.pack(pady=5)
        self.phone_entry = tk.Entry(self, font=("Arial", 12), width=40)
        self.phone_entry.pack(pady=5)
        
        # Email Entry
        self.email_label = tk.Label(self, text="Email:", font=("Arial", 12), bg="white")
        self.email_label.pack(pady=5)
        self.email_entry = tk.Entry(self, font=("Arial", 12), width=40)
        self.email_entry.pack(pady=5)
        
        # Address Entry
        self.address_label = tk.Label(self, text="Address:", font=("Arial", 12), bg="white")
        self.address_label.pack(pady=5)
        self.address_entry = tk.Entry(self, font=("Arial", 12), width=40)
        self.address_entry.pack(pady=5)
        
        # Buttons for adding, updating, deleting, and viewing contacts
        add_button = tk.Button(self, text="Add Contact", font=("Arial", 12), command=self.add_contact)
        add_button.pack(pady=10)
        
        view_button = tk.Button(self, text="View Contacts", font=("Arial", 12), command=self.view_contacts)
        view_button.pack(pady=10)
        
        update_button = tk.Button(self, text="Update Contact", font=("Arial", 12), command=self.update_contact)
        update_button.pack(pady=10)
        
        delete_button = tk.Button(self, text="Delete Contact", font=("Arial", 12), command=self.delete_contact)
        delete_button.pack(pady=10)
        
        # Listbox to display contacts
        self.contact_listbox = tk.Listbox(self, font=("Arial", 12), width=60, height=15)
        self.contact_listbox.pack(pady=10)
        
        # Search Entry and Button
        self.search_label = tk.Label(self, text="Search:", font=("Arial", 12), bg="white")
        self.search_label.pack(pady=5)
        self.search_entry = tk.Entry(self, font=("Arial", 12), width=40)
        self.search_entry.pack(pady=5)
        
        search_button = tk.Button(self, text="Search Contact", font=("Arial", 12), command=self.search_contact)
        search_button.pack(pady=10)

    def add_contact(self):
        """Add a new contact to the contact book."""
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if not self.validate_phone(phone):
            messagebox.showwarning("Warning", "Enter a valid phone number.")
            return

        if not self.validate_email(email):
            messagebox.showwarning("Warning", "Enter a valid email address.")
            return

        if name and phone:
            # Store contact details in the dictionary
            self.contacts[name] = {
                'phone': phone,
                'email': email,
                'address': address
            }
            messagebox.showinfo("Success", f"Contact '{name}' added successfully!")
            self.clear_entries()
            self.update_listbox()
        else:
            messagebox.showwarning("Warning", "Name and Phone are required fields.")

    def view_contacts(self):
        """Display all contacts in the contact book."""
        self.update_listbox()

    def update_contact(self):
        """Update an existing contact's details."""
        selected_contact = self.contact_listbox.get(tk.ACTIVE)
        name = selected_contact.split(", ")[0][6:]

        if name in self.contacts:
            phone = self.phone_entry.get()
            email = self.email_entry.get()
            address = self.address_entry.get()

            if phone and self.validate_phone(phone):
                self.contacts[name]['phone'] = phone
            else:
                messagebox.showwarning("Warning", "Enter a valid phone number.")
                return

            if email and self.validate_email(email):
                self.contacts[name]['email'] = email
            else:
                messagebox.showwarning("Warning", "Enter a valid email address.")
                return

            if address:
                self.contacts[name]['address'] = address

            messagebox.showinfo("Success", f"Contact '{name}' updated successfully!")
            self.clear_entries()
            self.update_listbox()
        else:
            messagebox.showwarning("Warning", "Contact not found.")

    def delete_contact(self):
        """Delete a contact from the contact book."""
        selected_contact = self.contact_listbox.get(tk.ACTIVE)
        name = selected_contact.split(", ")[0][6:]

        if name in self.contacts:
            del self.contacts[name]
            messagebox.showinfo("Success", f"Contact '{name}' deleted successfully!")
            self.update_listbox()
        else:
            messagebox.showwarning("Warning", "Contact not found.")

    def search_contact(self):
        """Search for a contact by name or phone number."""
        search_term = self.search_entry.get()
        found_contacts = []

        for name, details in self.contacts.items():
            if search_term.lower() in name.lower() or search_term in details['phone']:
                found_contacts.append(f"Name: {name}, Phone: {details['phone']}, Email: {details['email']}, Address: {details['address']}")

        self.contact_listbox.delete(0, tk.END)
        if found_contacts:
            for contact in found_contacts:
                self.contact_listbox.insert(tk.END, contact)
        else:
            self.contact_listbox.insert(tk.END, "No contact found.")

    def update_listbox(self):
        """Refresh the listbox to display the current list of contacts."""
        self.contact_listbox.delete(0, tk.END)
        for name, details in self.contacts.items():
            self.contact_listbox.insert(tk.END, f"Name: {name}, Phone: {details['phone']}")

    def clear_entries(self):
        """Clear the entry fields after adding or updating a contact."""
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)

    def validate_phone(self, phone):
        """Validate the phone number to ensure it contains only '+' and digits."""
        return bool(re.fullmatch(r'[\+\d]+', phone))

    def validate_email(self, email):
        """Validate the email address format."""
        return bool(re.fullmatch(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))

if __name__ == "__main__":
    app = ContactBookApp()
    app.mainloop()
