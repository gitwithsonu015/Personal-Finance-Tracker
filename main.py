import tkinter as tk
from database import init_db
from gui import create_gui

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = create_gui(root)
    root.mainloop()

