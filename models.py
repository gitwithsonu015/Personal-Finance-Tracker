import pandas as pd
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transaction:
    id: int
    date: str
    type: str  # 'income' or 'expense'
    category: str
    amount: float
    description: str = ''

def transactions_to_df(transactions: List[Dict]) -> pd.DataFrame:
    """Convert list of transactions dicts to pandas DataFrame."""
    df = pd.DataFrame(transactions)
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
    return df

def compute_balance(df: pd.DataFrame) -> float:
    """Compute balance from DataFrame."""
    if df.empty:
        return 0.0
    income = df[df['type'] == 'income']['amount'].sum()
    expense = df[df['type'] == 'expense']['amount'].sum()
    return income - expense

def get_category_totals(df: pd.DataFrame) -> Dict[str, float]:
    """Get expense totals per category."""
    expense_df = df[df['type'] == 'expense']
    if expense_df.empty:
        return {}
    return expense_df.groupby('category')['amount'].sum().to_dict()

def get_monthly_trends_df(df: pd.DataFrame) -> pd.DataFrame:
    """Get monthly income/expense totals."""
    if df.empty:
        return pd.DataFrame()
    df['month'] = df['date'].dt.to_period('M').astype(str)
    monthly = df.groupby(['month', 'type'])['amount'].sum().reset_index()
    pivot = monthly.pivot(index='month', columns='type', values='amount').fillna(0)
    pivot['net'] = pivot.get('income', 0) - pivot.get('expense', 0)
    return pivot.sort_index(ascending=False).reset_index()

