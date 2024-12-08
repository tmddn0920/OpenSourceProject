import tkinter as tk
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGIC_DIR = os.path.join(BASE_DIR, "logic")
sys.path.append(BASE_DIR)
sys.path.append(LOGIC_DIR)

from ui_components import InbodyApp

if __name__ == "__main__":
    root = tk.Tk()
    app = InbodyApp(root)
    root.mainloop()