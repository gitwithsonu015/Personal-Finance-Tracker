import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable

from database import init_db, add_transaction, get_all_transactions, get_balance, get_transactions_by_category, get_monthly_trends
from models import transactions_to_df, compute_balance as compute_balance_df, get_category_totals, get_monthly_trends_df
from charts import create_pie_chart, create_bar_chart

class FinanceGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry("900x700")
        
        self.transactions = []
        self.refresh_data()
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.add_frame = ttk.Frame(self.notebook)
        self.history_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.dashboard_frame, text="Dashboard")
        self.notebook.add(self.add_frame, text="Add Transaction")
        self.notebook.add(self.history_frame, text="History")
        
        self.setup_dashboard()
        self.setup_add_transaction()
        self.setup_history()
    
    def refresh_data(self):
        """Refresh transactions data."""
        self.transactions = get_all_transactions()
    
    def on_refresh(self):
        """Callback for refresh."""
        self.refresh_data()
        self.update_dashboard()
        self.update_history()
    
    def setup_dashboard(self):
        """Setup dashboard tab."""
        # Balance
        balance_frame = ttk.LabelFrame(self.dashboard_frame, text="Current Balance")
        balance_frame.pack(fill=tk.X, padx=10, pady=5)
        self.balance_label = ttk.Label(balance_frame, text="$0.00", font=("Arial", 24, "bold"))
        self.balance_label.pack(pady=10)
        
        # Charts
        charts_frame = ttk.LabelFrame(self.dashboard_frame, text="Visualizations")
        charts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.pie_frame = ttk.Frame(charts_frame)
        self.pie_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.bar_frame = ttk.Frame(charts_frame)
        self.bar_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.pie_canvas = None
        self.bar_canvas = None
        
        ttk.Button(self.dashboard_frame, text="Refresh", command=self.on_refresh).pack(pady=5)
    
    def update_dashboard(self):
        """Update dashboard displays."""
        balance = get_balance()
        self.balance_label.config(text=f"${balance:.2f}")
        
        # Clear old charts
        if self.pie_canvas:
            self.pie_canvas.get_tk_widget().destroy()
        if self.bar_canvas:
            self.bar_canvas.get_tk_widget().destroy()
        
        category_totals = get_transactions_by_category()
        monthly_data = get_monthly_trends()
        
        self.pie_canvas = create_pie_chart(self.pie_frame, category_totals)
        self.bar_canvas = create_bar_chart(self.bar_frame, monthly_data)
    
    def setup_add_transaction(self):
        """Setup add transaction form."""
        ttk.Label(self.add_frame, text="Type:", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.type_var = tk.StringVar(value="expense")
        type_combo = ttk.Combobox(self.add_frame, textvariable=self.type_var, values=["income", "expense"], state="readonly")
        type_combo.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        
        ttk.Label(self.add_frame, text="Category:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(self.add_frame, textvariable=self.category_var, values=["Food", "Transport", "Salary", "Entertainment", "Bills", "Other"])
        category_combo.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
        
        ttk.Label(self.add_frame, text="Amount:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.amount_var = tk.StringVar()
        ttk.Entry(self.add_frame, textvariable=self.amount_var, width=15).grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
        
        ttk.Label(self.add_frame, text="Description:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.desc_var = tk.StringVar()
        ttk.Entry(self.add_frame, textvariable=self.desc_var, width=30).grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)
        
        def submit():
            try:
                amount = float(self.amount_var.get())
                if amount <= 0:
                    raise ValueError("Amount must be positive")
                add_transaction(self.type_var.get(), self.category_var.get(), amount, self.desc_var.get())
                messagebox.showinfo("Success", "Transaction added!")
                self.amount_var.set("")
                self.desc_var.set("")
                self.on_refresh()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(self.add_frame, text="Add Transaction", command=submit).grid(row=4, column=0, columnspan=2, pady=20)
    
    def setup_history(self):
        """Setup history table."""
        cols = ("ID", "Date", "Type", "Category", "Amount", "Description")
        self.tree = ttk.Treeview(self.history_frame, columns=cols, show="headings", height=20)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        scrollbar = ttk.Scrollbar(self.history_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        ttk.Button(self.history_frame, text="Refresh", command=self.on_refresh).pack(pady=5)
    
    def update_history(self):
        """Update history table."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        df = transactions_to_df(self.transactions)
        for _, row in df.iterrows():
            self.tree.insert("", tk.END, values=(row['id'], row['date'].strftime('%Y-%m-%d %H:%M'), 
                                                 row['type'], row['category'], f"${row['amount']:.2f}", row['description']))

def create_gui(root: tk.Tk):
    """Create and return GUI instance."""
    return FinanceGUI(root)

