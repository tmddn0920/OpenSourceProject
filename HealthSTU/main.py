import tkinter as tk
from ui_components import InbodyApp

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = InbodyApp(root)
        root.mainloop()
    except Exception as e:
        print(f"프로그램 실행 중 오류가 발생했습니다: {e}")