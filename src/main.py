"""
Personal Finance Tracker - Main Application
A simple tool to track income, expenses, and generate reports
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
from visualizer import FinanceVisualizer  # Import our new visualizer

class FinanceTracker:
    def __init__(self):
        self.data_file = "data/transactions.csv"
        self.transactions = self.load_data()

    def load_data(self):
        """Load existing transaction data or create empty DataFrame"""
        if os.path.exists(self.data_file):
            return pd.read_csv(self.data_file)
        else:
            return pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Type', 'Description'])

    def add_transaction(self, category, amount, transaction_type, description=""):
        """Add a new transaction"""
        new_transaction = {
            'Date': datetime.now().strftime('%Y-%m-%d'),
            'Category': category,
            'Amount': amount,
            'Type': transaction_type,
            'Description': description
        }

        self.transactions = pd.concat(
            [self.transactions, pd.DataFrame([new_transaction])], ignore_index=True)
        self.save_data()
        print(f"✅ {transaction_type} of ₹{amount} added successfully!")

    def save_data(self):
        """Save transactions to CSV file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        self.transactions.to_csv(self.data_file, index=False)

    def show_summary(self):
        """Display financial summary"""
        if self.transactions.empty:
            print("No transactions found!")
            return

        total_income = self.transactions[self.transactions['Type'] == 'Income']['Amount'].sum()
        total_expenses = self.transactions[self.transactions['Type'] == 'Expense']['Amount'].sum()
        balance = total_income - total_expenses

        print("\n" + "="*40)
        print("         FINANCIAL SUMMARY")
        print("="*40)
        print(f"Total Income:  ₹{total_income:,.2f}")
        print(f"Total Expenses: ₹{total_expenses:,.2f}")
        print(f"Net Balance:   ₹{balance:,.2f}")
        print("="*40)
        
    def view_transactions(self):
        """Display all transactions in a formatted table"""
        if self.transactions.empty:
            print("No transactions found!")
            return
            
        print("\n" + "="*80)
        print("                           TRANSACTION HISTORY")
        print("="*80)
        
        # Sort by date (newest first)
        sorted_transactions = self.transactions.sort_values('Date', ascending=False)
        
        for index, row in sorted_transactions.iterrows():
            print(f"Date: {row['Date']} | Type: {row['Type']:<7} | Category: {row['Category']:<12} | Amount: ₹{row['Amount']:<8.2f} | {row['Description']}")
        
        print("="*80)
        
    def export_to_excel(self):
        """Export transactions to Excel file"""
        if self.transactions.empty:
            print("No transactions to export!")
            return
            
        try:
            os.makedirs('reports', exist_ok=True)
            filename = f'reports/finance_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
            
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # All transactions
                self.transactions.to_excel(writer, sheet_name='All Transactions', index=False)
                
                # Summary by category
                income_summary = self.transactions[self.transactions['Type'] == 'Income'].groupby('Category')['Amount'].sum()
                expense_summary = self.transactions[self.transactions['Type'] == 'Expense'].groupby('Category')['Amount'].sum()
                
                if not income_summary.empty:
                    income_summary.to_excel(writer, sheet_name='Income Summary')
                if not expense_summary.empty:
                    expense_summary.to_excel(writer, sheet_name='Expense Summary')
            
            print(f"✅ Data exported successfully to: {filename}")
            
        except Exception as e:
            print(f"❌ Error exporting data: {e}")

def main():
    """Main application loop"""
    tracker = FinanceTracker()

    print("🏦 Welcome to Personal Finance Tracker!")
    print("=" * 50)

    while True:
        print("\nOptions:")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Summary")
        print("4. View All Transactions")
        print("5. Generate Charts")
        print("6. Export to Excel")
        print("7. Exit")

        choice = input("\nEnter your choice (1-7): ").strip()

        if choice == '1':
            category = input("Income category (e.g., Salary, Freelance): ")
            amount = float(input("Amount: ₹"))
            description = input("Description (optional): ")
            tracker.add_transaction(category, amount, 'Income', description)

        elif choice == '2':
            category = input("Expense category (e.g., Food, Transport): ")
            amount = float(input("Amount: ₹"))
            description = input("Description (optional): ")
            tracker.add_transaction(category, amount, 'Expense', description)
            
        elif choice == '3':
            tracker.show_summary()
            
        elif choice == '4':
            tracker.view_transactions()

        elif choice == '5':
            if tracker.transactions.empty:
                print("No data available for charts! Add some transactions first.")
            else:
                visualizer = FinanceVisualizer(tracker.transactions)
                print("\nChart Options:")
                print("a. Expense Breakdown (Pie Chart)")
                print("b. Monthly Trends (Line Chart)")
                print("c. Financial Overview (Bar Chart)")
                print("d. Generate All Charts")
                
                chart_choice = input("Choose chart (a/b/c/d): ").lower()
                
                if chart_choice == 'a':
                    visualizer.create_expense_pie_chart()
                elif chart_choice == 'b':
                    visualizer.create_monthly_trend()
                elif chart_choice == 'c':
                    visualizer.create_balance_chart()
                elif chart_choice == 'd':
                    visualizer.create_expense_pie_chart()
                    visualizer.create_monthly_trend()
                    visualizer.create_balance_chart()
                else:
                    print("Invalid choice!")
                    
        elif choice == '6':
            tracker.export_to_excel()

        elif choice == '7':
            print("👋 Thanks for using Finance Tracker!")
            break
            
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
