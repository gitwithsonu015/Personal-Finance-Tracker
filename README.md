# Personal Finance Tracker

A simple desktop application to track personal finances. Built with Python, Tkinter for GUI, SQLite for data storage, Pandas for data handling, and Matplotlib for charts.

## Features
- Add income and expense transactions with categories and descriptions
- View all transactions in a table
- Dashboard with current balance, expense breakdown by category, and monthly trends
- Interactive pie and bar charts for visualization
- Data persistence via SQLite database

## Project Structure
```
Personal-Finance-Tracker-master/
├── main.py              # App entry point
├── database.py          # SQLite database operations (CRUD)
├── models.py            # Data models and Pandas utilities
├── gui.py               # Tkinter GUI components
├── charts.py            # Matplotlib charts integration
├── requirements.txt     # Python dependencies
├── data/
│   └── finance_tracker.db  # SQLite database file
├── README.md            # This file
├── TODO.md              # Implementation status (core complete)
└── ... (unused web files: index.html, style.css, etc.)
```

## Prerequisites
- Python 3.8+
- pip

## Setup & Run
1. Clone or navigate to the project directory:
   ```
   cd d:/Personal-Finance-Tracker-master
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python main.py
   ```

The app will create the `data/` directory and `finance_tracker.db` automatically on first run.

## Usage
- **Add Transaction**: Select type (income/expense), category, enter amount and description.
- **Dashboard**: View balance, category totals (pie chart), monthly trends (bar chart), transaction table.
- Data is saved automatically.

## Screenshots
*(Add screenshots of GUI dashboard here)*

## Development
- Core features complete per [TODO.md](TODO.md).
- Pending: Authentication (TODO_auth.md), Web version (TODO_web.md).

## Dependencies
- pandas==2.2.2
- matplotlib==3.9.2

## License
MIT License (or specify your preferred license).

