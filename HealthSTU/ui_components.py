import tkinter as tk
from tkinter import filedialog, messagebox
from ocr_processing import process_inbody_image, parse_inbody_data
from calculations import calculate_bmi, calculate_body_fat_percentage, classify_body_type

class InbodyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HEALTH STU")
        self.root.geometry("800x800") 
        self.root.resizable(False, False)  
        self.root.configure(bg="#ffffff")
        self.inbody_data = {}

        tk.Label(root, text="HEALTH STU에 오신 것을 환영합니다!", bg="#ffffff", font=("Arial", 28)).pack(pady=100)
        self.start_button = tk.Button(root, text="시작하기", font=("Arial", 16), bg="#A9D0F5", command=self.show_input_screen)
        self.start_button.pack(pady=0)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_input_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text="이름을 입력하세요:", font=("Arial", 16), bg="#ffffff").grid(row=0, column=0, padx=10, pady=(50, 10), sticky="w")
        self.name_entry = tk.Entry(self.root, font=("Arial", 16))
        self.name_entry.grid(row=0, column=1, padx=10, pady=(50, 10), sticky="ew")

        tk.Label(self.root, text="키(cm)를 입력하세요:", font=("Arial", 16), bg="#ffffff").grid(row=1, column=0, padx=10, pady=(10, 100), sticky="w")
        self.height_entry = tk.Entry(self.root, font=("Arial", 16))
        self.height_entry.grid(row=1, column=1, padx=10, pady=(10, 100), sticky="ew")

        self.image_button = tk.Button(self.root, text="INBODY 데이터 불러오기", font=("Arial", 20), bg="#cde4f2", command=self.select_image)
        self.image_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.result_button = tk.Button(self.root, text="  결과 보기  ", font=("Arial", 20), bg="#e2f7d3", command=self.display_results, state=tk.DISABLED)
        self.result_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.root.configure(bg="#ffffff")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
    def select_image(self):
        image_path = filedialog.askopenfilename(title="이미지 파일 선택", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if image_path:
            ocr_text = process_inbody_image(image_path)  # 수정된 부분
            self.inbody_data = parse_inbody_data(ocr_text)  # 수정된 부분
            if self.inbody_data:
                self.result_button.config(state=tk.NORMAL)
                messagebox.showinfo("성공", "인바디 데이터가 성공적으로 추출되었습니다.")
            else:
                self.manual_input()

    def manual_input(self):
        messagebox.showwarning("데이터 부족", "OCR 데이터가 부족합니다. 수동 입력이 필요합니다.")
        manual_window = tk.Toplevel(self.root)
        manual_window.title("수동 데이터 입력")

        tk.Label(manual_window, text="체중(kg):").grid(row=0, column=0, padx=10, pady=10)
        weight_entry = tk.Entry(manual_window)
        weight_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(manual_window, text="골격근량(kg):").grid(row=1, column=0, padx=10, pady=10)
        muscle_entry = tk.Entry(manual_window)
        muscle_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(manual_window, text="체지방량(kg):").grid(row=2, column=0, padx=10, pady=10)
        fat_entry = tk.Entry(manual_window)
        fat_entry.grid(row=2, column=1, padx=10, pady=10)

        def save_manual_data():
            try:
                self.inbody_data = {
                    "weight_kg": float(weight_entry.get()),
                    "skeletal_muscle_mass": float(muscle_entry.get()),
                    "body_fat_mass": float(fat_entry.get()),
                }
                self.result_button.config(state=tk.NORMAL)
                messagebox.showinfo("성공", "수동 데이터 입력 완료!")
                manual_window.destroy()
            except ValueError:
                messagebox.showerror("오류", "올바른 숫자를 입력하세요.")

        tk.Button(manual_window, text="저장", command=save_manual_data).grid(row=3, column=0, columnspan=2, pady=10)
        
    def display_results(self):
        try:
            # 입력값과 계산된 결과
            name = self.name_entry.get()
            height = float(self.height_entry.get())
            weight = self.inbody_data["weight_kg"]
            muscle = self.inbody_data["skeletal_muscle_mass"]
            fat = self.inbody_data["body_fat_mass"]

            bmi = calculate_bmi(height, weight)
            body_fat_percentage = calculate_body_fat_percentage(weight, fat)
            body_type = classify_body_type(bmi, body_fat_percentage)

            self.clear_screen()

            # 헤더: "<이름> 님은 <체형> 입니다!"
            header_label = tk.Label(self.root, text=f"{name} 님은 '{body_type}' 입니다!", font=("Arial", 24), bg="#ffffff")
            header_label.grid(row=0, column=0, columnspan=2, pady=(20, 40))

            # 결과 데이터: 체중, 골격근량, 체지방량
            result_frame = tk.Frame(self.root, bg="#ffffff")
            result_frame.grid(row=1, column=0, padx=20, pady=10)

            tk.Label(result_frame, text=f"체중: {weight:.2f} kg", font=("Arial", 16), bg="#ffffff").pack(anchor="center", pady=5)
            tk.Label(result_frame, text=f"골격근량: {muscle:.2f} kg", font=("Arial", 16), bg="#ffffff").pack(anchor="center", pady=5)
            tk.Label(result_frame, text=f"체지방량: {fat:.2f} kg", font=("Arial", 16), bg="#ffffff").pack(anchor="center", pady=5)

            # 추가 데이터: BMI와 체지방률
            extra_frame = tk.Frame(self.root, bg="#ffffff")
            extra_frame.grid(row=2, column=0, padx=20, pady=10)

            tk.Label(extra_frame, text=f"BMI: {bmi:.2f}", font=("Arial", 14), bg="#ffffff").pack(anchor="center", pady=5)
            tk.Label(extra_frame, text=f"체지방률: {body_fat_percentage:.2f}%", font=("Arial", 14), bg="#ffffff").pack(anchor="center", pady=5)

            # 그래프 표시 공간
            graph_frame = tk.Frame(self.root, bg="#ffffff", width=400, height=400)
            graph_frame.grid(row=1, column=1, rowspan=2, padx=20, pady=10)

            # 그래프 영역: 나중에 그래프 추가
            tk.Label(graph_frame, text="그래프 영역 (추후 구현)", font=("Arial", 14), bg="#cde4f2", width=30, height=10).pack()

            # 창 배경 설정
            self.root.configure(bg="#ffffff")
            self.root.grid_columnconfigure(0, weight=3)
            self.root.grid_columnconfigure(1, weight=1)

        except Exception as e:
            messagebox.showerror("오류", f"결과 계산 중 오류가 발생했습니다: {e}")
