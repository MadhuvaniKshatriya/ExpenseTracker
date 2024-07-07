import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
import os
from pyvirtualdisplay import Display

# Start a virtual display
display = Display(visible=0, size=(800, 600))
display.start()

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.expenses = []
        self.categories = ["Food", "Transport", "Utilities", "Entertainment", "Others"]
        self.file_path = "expenses.csv"

        self.load_expenses()
        self.create_ui()

    def create_ui(self):
        tk.Label(self.root, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Description:").grid(row=1, column=0, padx=10, pady=10)
        self.desc_entry = tk.Entry(self.root)
        self.desc_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Amount:").grid(row=2, column=0, padx=10, pady=10)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Category:").grid(row=3, column=0, padx=10, pady=10)
        self.category_var = tk.StringVar(self.root)
        self.category_var.set(self.categories[0])
        self.category_menu = tk.OptionMenu(self.root, self.category_var, *self.categories)
        self.category_menu.grid(row=3, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Add Expense", command=self.add_expense).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Show Summary", command=self.show_summary).grid(row=5, column=0, columnspan=2, pady=10)

    def add_expense(self):
        date = self.date_entry.get()
        description = self.desc_entry.get()
        amount = self.amount_entry.get()
        category = self.category_var.get()

        if not date or not description or not amount:
            messagebox.showerror("Input Error", "All fields are required")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a number")
            return

        expense = {"Date": date, "Description": description, "Amount": amount, "Category": category}
        self.expenses.append(expense)
        self.save_expenses()
        messagebox.showinfo("Success", "Expense added successfully")

        self.date_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

    def save_expenses(self):
        df = pd.DataFrame(self.expenses)
        df.to_csv(self.file_path, index=False)

    def load_expenses(self):
        if os.path.exists(self.file_path):
            df = pd.read_csv(self.file_path)
            self.expenses = df.to_dict('records')

    def show_summary(self):
        df = pd.DataFrame(self.expenses)
        if df.empty:
            messagebox.showinfo("Summary", "No expenses recorded yet")
            return

        summary = df.groupby('Category').sum()['Amount']
        summary_str = summary.to_string()
        messagebox.showinfo("Summary", summary_str)

        plt.figure(figsize=(8, 6))
        summary.plot(kind='pie', autopct='%1.1f%%')
        plt.title('Expenses by Category')
        plt.ylabel('')
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
    display.stop()
