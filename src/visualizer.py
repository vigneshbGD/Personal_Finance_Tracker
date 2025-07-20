"""
Data Visualization Module for Finance Tracker
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime
import os

class FinanceVisualizer:
    def __init__(self, transactions_df):
        self.transactions = transactions_df
        plt.style.use('seaborn-v0_8')  # Modern styling
        
    def create_expense_pie_chart(self):
        """Create pie chart showing expense breakdown by category"""
        if self.transactions.empty:
            print("No data available for visualization")
            return
            
        expenses = self.transactions[self.transactions['Type'] == 'Expense']
        if expenses.empty:
            print("No expense data available")
            return
            
        expense_by_category = expenses.groupby('Category')['Amount'].sum()
        
        plt.figure(figsize=(10, 8))
        colors = plt.cm.Set3(range(len(expense_by_category)))
        
        wedges, texts, autotexts = plt.pie(expense_by_category.values, 
                                          labels=expense_by_category.index,
                                          autopct='%1.1f%%',
                                          colors=colors,
                                          startangle=90,
                                          explode=[0.05] * len(expense_by_category))
        
        plt.title('Expense Breakdown by Category', fontsize=16, fontweight='bold', pad=20)
        
        # Enhance text appearance
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            
        plt.tight_layout()
        
        # Save the chart
        os.makedirs('reports', exist_ok=True)
        plt.savefig('reports/expense_breakdown.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def create_monthly_trend(self):
        """Create line chart showing monthly income vs expenses"""
        if self.transactions.empty:
            print("No data available for visualization")
            return
            
        # Convert Date column to datetime
        self.transactions['Date'] = pd.to_datetime(self.transactions['Date'])
        self.transactions['Month'] = self.transactions['Date'].dt.to_period('M')
        
        # Group by month and type
        monthly_data = self.transactions.groupby(['Month', 'Type'])['Amount'].sum().unstack(fill_value=0)
        
        if monthly_data.empty:
            print("Insufficient data for monthly trends")
            return
            
        plt.figure(figsize=(12, 6))
        
        if 'Income' in monthly_data.columns:
            plt.plot(monthly_data.index.astype(str), monthly_data['Income'], 
                    marker='o', linewidth=2, label='Income', color='green')
                    
        if 'Expense' in monthly_data.columns:
            plt.plot(monthly_data.index.astype(str), monthly_data['Expense'], 
                    marker='s', linewidth=2, label='Expenses', color='red')
        
        plt.title('Monthly Income vs Expenses Trend', fontsize=16, fontweight='bold')
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Amount (₹)', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig('reports/monthly_trend.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def create_balance_chart(self):
        """Create bar chart showing income, expenses, and balance"""
        if self.transactions.empty:
            print("No data available for visualization")
            return
            
        total_income = self.transactions[self.transactions['Type'] == 'Income']['Amount'].sum()
        total_expenses = self.transactions[self.transactions['Type'] == 'Expense']['Amount'].sum()
        balance = total_income - total_expenses
        
        categories = ['Total Income', 'Total Expenses', 'Net Balance']
        amounts = [total_income, total_expenses, balance]
        colors = ['#2ecc71', '#e74c3c', '#3498db' if balance >= 0 else '#e74c3c']
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(categories, amounts, color=colors, alpha=0.8)
        
        # Add value labels on bars
        for bar, amount in zip(bars, amounts):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + (max(amounts) * 0.01),
                    f'₹{amount:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        plt.title('Financial Overview', fontsize=16, fontweight='bold')
        plt.ylabel('Amount (₹)', fontsize=12)
        plt.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('reports/financial_overview.png', dpi=300, bbox_inches='tight')
        plt.show()
