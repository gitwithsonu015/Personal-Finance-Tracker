import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from typing import Dict

def create_pie_chart(parent: tk.Widget, category_totals: Dict[str, float], width: int = 400, height: int = 400):
    """Create pie chart for expense categories in tkinter frame."""
    fig, ax = plt.subplots(figsize=(width/100, height/100))
    if not category_totals:
        ax.text(0.5, 0.5, 'No expenses yet', ha='center', va='center', transform=ax.transAxes)
    else:
        labels = list(category_totals.keys())
        sizes = list(category_totals.values())
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.set_title('Expense Distribution')
    ax.axis('equal')
    
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    return canvas

def create_bar_chart(parent: tk.Widget, monthly_data: list, width: int = 500, height: int = 300):
    """Create bar chart for monthly trends in tkinter frame."""
    fig, ax = plt.subplots(figsize=(width/100, height/100))
    if not monthly_data:
        ax.text(0.5, 0.5, 'No data yet', ha='center', va='center', transform=ax.transAxes)
    else:
        months = [item['month'] for item in monthly_data]
        income = [item.get('income', 0) for item in monthly_data]
        expense = [item.get('expense', 0) for item in monthly_data]
        x = range(len(months))
        ax.bar([i - 0.2 for i in x], income, 0.4, label='Income', color='green')
        ax.bar([i + 0.2 for i in x], expense, 0.4, label='Expense', color='red')
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount')
        ax.set_title('Monthly Trends')
        ax.set_xticks(x)
        ax.set_xticklabels(months)
        ax.legend()
    
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    return canvas

