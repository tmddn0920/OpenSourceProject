import tkinter as tk
from tkinter import filedialog, messagebox, IntVar
from logic.ocr_processing import process_inbody_image, parse_inbody_data
from logic.calculations import calculate_bmi, calculate_body_fat_percentage, classify_body_type
from logic.body_type_messages import get_body_type_message
from logic.routine_generator import generate_routine, cardio_exercise
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

# 폰트 및 배경화면 사용 준비
mpl.rcParams['font.family'] = 'Malgun Gothic'  
mpl.rcParams['axes.unicode_minus'] = False    
current_dir = os.path.dirname(os.path.abspath(__file__))
background_path = os.path.join(current_dir, "assets", "background.png")

class InbodyApp:
    # 시작 화면 
    def __init__(self, root):
        self.root = root
        self.root.title("HEALTH STU")
        self.root.geometry("800x800") 
        self.root.resizable(False, False)  
        self.root.configure(bg="#ffffff")
        self.inbody_data = {}

        self.bg_image = tk.PhotoImage(file=background_path) 
        self.canvas = tk.Canvas(root, width=800, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)  
        
        self.canvas.create_text(400, 100, text="HEALTH STU", fill="#000000", font=("Arial", 32, "bold"))
        
        self.start_button = tk.Button(
            root,
            text="정보 입력 후 시작하기",
            font=("Arial", 16, "bold"), 
            bg="#A9D0F5",
            command=self.show_input_screen
        )
        self.start_button_window = self.canvas.create_window(330, 450, window=self.start_button)

        self.help_button = tk.Button(
            root,
            text="사용 방법",
            font=("Arial", 16, "bold"),  
            bg="#CDE4F2",
            command=self.show_help_screen
        )
        self.help_button_window = self.canvas.create_window(520, 450, window=self.help_button)
        
    # 위젯 클리어 함수    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # 사용 방법을 클릭 시, 사용 방법 출력
    def show_help_screen(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("사용 방법")
        help_window.geometry("400x400")
        help_window.resizable(False, False)

        help_label = tk.Label(
            help_window,
            text="HEALTH STU 사용 방법:\n"
                 "개발 : 차승우(서울과학기술대 컴퓨터공학과)\n\n"
                 "1. '시작하기' 버튼을 눌러 이름과 키를 입력합니다.\n\n"
                 "2. INBODY 데이터를 불러옵니다. 실패 시 직접 입력합니다.\n\n"
                 "3. 결과 보기 버튼을 눌러 신체 정보를 확인합니다.\n\n"
                 "4. 오늘의 운동 부위를 선택 후, 운동 루틴을 받아보세요!\n\n",
            font=("Arial", 12),
            justify="left",
            wraplength=380,
            padx=10,
            pady=20
        )
        help_label.pack()

        close_button = tk.Button(help_window, text="닫기", font=("Arial", 12), command=help_window.destroy)
        close_button.pack(pady=10)
        
    # 인바디 데이터 입력 화면 출력
    def show_input_screen(self):
        self.clear_screen()

        self.canvas = tk.Canvas(self.root, width=800, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        canvas_width = 800
        center_x = canvas_width // 2

        self.canvas.create_text(200, 50, text="당신의 이름을 입력해주세요:", fill="black", font=("Arial", 16, "bold"), anchor="center")
        self.name_entry = tk.Entry(self.root, font=("Arial", 16, "bold"), width=24)
        self.name_entry_window = self.canvas.create_window(600, 50, window=self.name_entry)

        self.canvas.create_text(200, 100, text="키(cm)를 입력해주세요:", fill="black", font=("Arial", 16, "bold"), anchor="center")
        self.height_entry = tk.Entry(self.root, font=("Arial", 16, "bold"), width=24)
        self.height_entry_window = self.canvas.create_window(600, 100, window=self.height_entry)

        self.image_button = tk.Button(self.root, text="INBODY 데이터 불러오기", font=("Arial", 18, "bold"), bg="#CDE4F2", command=self.select_image)
        self.image_button_window = self.canvas.create_window(center_x, 400, window=self.image_button)

        self.result_button = tk.Button(self.root, text="결과 확인하기", font=("Arial", 18, "bold"), bg="#A9D0F5", disabledforeground="#FFFFFF", command=self.display_results, state=tk.DISABLED)
        self.result_button_window = self.canvas.create_window(center_x, 460, window=self.result_button)
        
    # ocr_processing을 통한 이미지 가공 및 데이터 추출    
    def select_image(self):
        image_path = filedialog.askopenfilename(title="이미지 파일 선택", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if image_path:
            try:
                ocr_text = process_inbody_image(image_path)
                self.inbody_data = parse_inbody_data(ocr_text)
                if self.inbody_data:
                    self.result_button.config(state=tk.NORMAL)
                    messagebox.showinfo("성공", "인바디 데이터가 성공적으로 추출되었습니다.")
                else:
                    self.manual_input()
            except Exception as e:
                messagebox.showerror("오류", f"이미지 처리 중 오류가 발생했습니다: {e}")

    # 데이터 추출 실패 시 수동 입력 창 출력
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

        # 데이터 저장
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

    # 체형 별 그래프 생성
    def create_graph(self, bmi, body_fat_percentage):

        fig, ax = plt.subplots(figsize=(5, 5)) 
        ax.set_xlim(8, 18)  
        ax.set_ylim(16, 25) 
        ax.set_xlabel("체지방률 (%)", fontweight="bold")
        ax.set_ylabel("BMI", fontweight="bold")
        ax.set_title("체형 분류", fontweight="bold")

        ax.scatter(body_fat_percentage, bmi, color="black", s=45, label="내 위치")
        legend = ax.legend(
            fontsize=8,  
            loc="lower right",   
            frameon=True,  
            prop={"weight": "bold"}  
        )
        for text in legend.get_texts():
            text.set_va("center")

        regions = [
            {"x_range": (8, 13), "y_range": (23, 25), "label": "운동선수"},
            {"x_range": (13, 16), "y_range": (23, 25), "label": "과체중"},
            {"x_range": (16, 18), "y_range": (23, 25), "label": "비만"},
            {"x_range": (8, 13), "y_range": (20.75, 23), "label": "근육형"},
            {"x_range": (13, 16), "y_range": (18.5, 23), "label": "적정"},
            {"x_range": (16, 18), "y_range": (20.75, 23), "label": "경도 비만"},
            {"x_range": (8, 10), "y_range": (18.5, 20.75), "label": "근육형 날씬"},
            {"x_range": (10, 13), "y_range": (18.5, 20.75), "label": "날씬"},
            {"x_range": (16, 18), "y_range": (16, 20.75), "label": "마른 비만"},
            {"x_range": (8, 10), "y_range": (16, 18.5), "label": "마름"},
            {"x_range": (10, 16), "y_range": (16, 18.5), "label": "약간 마름"}
        ]

        for region in regions:

            rect = plt.Rectangle(
                (region["x_range"][0], region["y_range"][0]),
                region["x_range"][1] - region["x_range"][0],
                region["y_range"][1] - region["y_range"][0],
                facecolor="#FFFF99",
                alpha=0.3,
                edgecolor="black"
            )
            ax.add_patch(rect)

            center_x = (region["x_range"][0] + region["x_range"][1]) / 2
            center_y = (region["y_range"][0] + region["y_range"][1]) / 2
            ax.text(center_x, center_y, region["label"], ha="center", va="center", fontsize=8, fontweight="bold")

        return fig
    
    # 운동 부위 선택 화면 출력
    def show_exercise_screen(self):

        self.clear_screen()

        self.root.configure(bg="#CDE4F2")

        tk.Label(
            self.root,
            text="운동할 부위를 선택하세요:",
            font=("Arial", 20, "bold"),
            bg="#CDE4F2"
        ).pack(pady=20)

        main_frame = tk.Frame(self.root, bg="#CDE4F2")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)  
        main_frame.grid_columnconfigure(1, weight=1) 

        options_frame = tk.Frame(main_frame, bg="#CDE4F2")
        options_frame.grid(row=0, column=0, sticky="w")

        right_frame = tk.Frame(main_frame, bg="#CDE4F2")
        right_frame.grid(row=0, column=1, sticky="e", padx=20)

        body_parts = ["어깨", "팔", "가슴", "등", "하체"]
        selected_body_part = tk.StringVar(value=body_parts[0]) 

        selected_label = tk.Label(
            right_frame,
            text=f"선택한 운동은 {selected_body_part.get()} 입니다.",
            font=("Arial", 18, "bold"),
            bg="#CDE4F2",
            anchor="w",
            justify="left"
        )
        selected_label.pack(pady=10)

        for part in body_parts:
            part_frame = tk.Frame(
                options_frame,
                bg="#ffffff",
                relief="solid",
                bd=1
            )
            part_frame.pack(fill="x", pady=5, padx=5) 

            tk.Radiobutton(
                part_frame,
                text=part,
                variable=selected_body_part,
                value=part,
                font=("Arial", 16, "bold"),
                bg="#ffffff",
                selectcolor="#CDE4F2",
                indicatoron=True,
                command=lambda: selected_label.config(
                    text=f"선택한 운동은 {selected_body_part.get()} 입니다." 
                )
            ).pack(anchor="w", padx=(10, 150), pady=10)

        tk.Button(
            right_frame,
            text="운동 시작",
            font=("Arial", 16, "bold"),
            bg="#A9D0F5",
            command=lambda: self.show_routine_screen(selected_body_part.get(), generate_routine(selected_body_part.get()))
        ).pack(pady=20)
        
        description_frame = tk.Frame(
            self.root,
            bg="#ffffff",
            relief="solid",  
            bd=2  
        )
        description_frame.pack(fill="x", pady=10, padx=10)

        tk.Label(
            description_frame,
            text="어떻게 운동해야 하나요?\n"
                "----------------------------------------------------------------\n"
                "운동 부위를 선택한 후, '운동 시작' 버튼을 눌러주세요.\n"
                "각 운동에 대한 루틴이 생성됩니다. 순서대로 진행하시면 됩니다!\n"
                "유산소 운동이 필요한 경우에는 맞춤 유산소 운동도 함께 생성됩니다.\n\n"
                "근력 운동을 할 때는 한 운동 당 3 ~ 4세트, 8개 ~ 12개로 반복해주세요.\n"
                "세트마다 쉬는 시간은 필수입니다.",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            justify="center",
            wraplength=1000 
        ).pack(pady=20, padx=10)

    # 운동 루틴 출력
    def show_routine_screen(self, body_part, routine):
        self.clear_screen()

        background_color = "#CDE4F2"

        routine_frame = tk.Frame(self.root, bg=background_color)
        routine_frame.pack(fill="both", expand=True)

        title_frame = tk.Frame(routine_frame, bg=background_color)
        title_frame.pack(pady=20)

        tk.Label(
            title_frame,
            text="오늘의 '",
            font=("Arial", 20, "bold"),
            bg=background_color
        ).pack(side="left")

        tk.Label(
            title_frame,
            text=body_part,
            font=("Arial", 20, "bold"),
            bg=background_color,
            fg="#FF9999" 
        ).pack(side="left")

        tk.Label(
            title_frame,
            text="' 운동 루틴!",
            font=("Arial", 20, "bold"),
            bg=background_color
        ).pack(side="left")

        check_vars = []

        # 모든 운동 완료 시, 메세지 출력
        def check_all_done():
            if all(var.get() for var in check_vars):  
                tk.messagebox.showinfo("운동 완료", "오늘의 운동을 완료하였습니다!") 

        for idx, exercise in enumerate(routine, start=1):

            check_var = tk.IntVar()
            check_vars.append(check_var)

            exercise_frame = tk.Frame(
                routine_frame,
                bg="#ffffff",
                relief="solid",
                bd=1  
            )
            exercise_frame.pack(pady=10, fill="x", padx=20)

            tk.Label(
                exercise_frame,
                text=f"STEP {idx}: {exercise}",
                font=("Arial", 16, "bold"),
                bg="#ffffff"
            ).pack(side="left", padx=10)

            tk.Checkbutton(
                exercise_frame,
                variable=check_var,
                command=check_all_done,  
                bg="#ffffff",
                activebackground="#ffffff",
                font=("Arial", 16),
                width=4,  
                height=2  
            ).pack(side="right")

        body_type = self.inbody_data.get("body_type", "")
        cardio_needed = ["과체중", "비만", "경도 비만", "마른 비만"]

        if body_type in cardio_needed:
            cardio = cardio_exercise() 
            cardio_frame = tk.Frame(
                routine_frame,
                bg="#ffffff",
                relief="solid",
                bd=1  
            )
            cardio_frame.pack(pady=20, fill="x", padx=20)

            tk.Label(
                cardio_frame,
                text="오늘의 유산소 운동:",
                font=("Arial", 18, "bold"),
                bg="#ffffff"
            ).pack(pady=10, padx=10)

            tk.Label(
                cardio_frame,
                text=f"{cardio}",
                font=("Arial", 16, "bold"),
                bg="#ffffff"
            ).pack(pady=5, padx=10)

        tk.Button(
            routine_frame,
            text="뒤로가기",
            font=("Arial", 16, "bold"),
            bg="#A9D0F5",  
            command=self.show_exercise_screen
        ).pack(pady=20)

    # 데이터 분석 결과 출력
    def display_results(self):
        """몸 상태 화면 표시"""
        try:
            name = self.name_entry.get()
            height = float(self.height_entry.get())
            weight = self.inbody_data["weight_kg"]
            muscle = self.inbody_data["skeletal_muscle_mass"]
            fat = self.inbody_data["body_fat_mass"]

            bmi = calculate_bmi(height, weight)
            body_fat_percentage = calculate_body_fat_percentage(weight, fat)
            body_type = classify_body_type(bmi, body_fat_percentage)
            self.inbody_data["body_type"] = body_type
            message = get_body_type_message(body_type)

            self.clear_screen()
            results_frame = tk.Frame(self.root, bg="#CDE4F2", padx=20, pady=20) 
            results_frame.grid(row=0, column=0, sticky="nsew")

            self.root.grid_rowconfigure(0, weight=1)
            self.root.grid_columnconfigure(0, weight=1)

            header_frame = tk.Frame(results_frame, bg="#CDE4F2")
            header_frame.grid(row=0, column=0, columnspan=2, pady=(10, 0))

            header_label1 = tk.Label(
                header_frame,
                text=f"{name} 님은 ",
                font=("Arial", 24, "bold"),
                bg="#CDE4F2",
            )
            header_label1.pack(side="left")

            header_label2 = tk.Label(
                header_frame,
                text=f"'{body_type}'",
                font=("Arial", 24, "bold"),
                bg="#CDE4F2",
                fg="#FF9999"  
            )
            header_label2.pack(side="left")

            header_label3 = tk.Label(
                header_frame,
                text=" 입니다!",
                font=("Arial", 24, "bold"),
                bg="#CDE4F2",
            )
            header_label3.pack(side="left")

            message_label = tk.Label(
                results_frame,
                text=message,
                font=("Arial", 14, "bold"),
                bg="#CDE4F2",
                fg="#606060",
                padx=20
            )
            message_label.grid(row=1, column=0, columnspan=2, sticky="n")

            result_frame = tk.Frame(
                results_frame,
                bg="#ffffff",
                padx=20,
                pady=10,
                relief="solid",  
                bd=2  
            )
            result_frame.grid(row=2, column=0, pady=10, sticky="s")
            
            tk.Label(result_frame, text="<기본 정보>", font=("Arial", 16, "bold"), bg="#ffffff").pack(anchor="w", pady=2)
            tk.Label(result_frame, text=f"체중: {weight:.2f} kg", font=("Arial", 12, "bold"), bg="#ffffff").pack(anchor="w", pady=2)
            tk.Label(result_frame, text=f"골격근량: {muscle:.2f} kg", font=("Arial", 12, "bold"), bg="#ffffff").pack(anchor="w", pady=2)
            tk.Label(result_frame, text=f"체지방량: {fat:.2f} kg", font=("Arial", 12, "bold"), bg="#ffffff").pack(anchor="w", pady=2)

            extra_frame = tk.Frame(
                results_frame,
                bg="#ffffff",
                padx=20,
                pady=10,
                relief="solid", 
                bd=2  
            )
            extra_frame.grid(row=3, column=0, pady=10, sticky="n")

            tk.Label(extra_frame, text="<결과>", font=("Arial", 16, "bold"), bg="#ffffff").pack(anchor="w", pady=2)
            tk.Label(extra_frame, text=f"BMI: {bmi:.2f}", font=("Arial", 12, "bold"), bg="#ffffff").pack(anchor="w", pady=2)
            tk.Label(extra_frame, text=f"체지방률: {body_fat_percentage:.2f}%", font=("Arial", 12, "bold"), bg="#ffffff").pack(anchor="w", pady=2)

            graph_frame = tk.Frame(
                results_frame,
                bg="#ffffff",
                width=400,
                height=400,
                padx=5,
                pady=5,
                relief="solid", 
                bd=2 
            )
            graph_frame.grid(row=2, column=1, rowspan=2, pady=10, sticky="n")

            fig = self.create_graph(bmi, body_fat_percentage)
            canvas = FigureCanvasTkAgg(fig, master=graph_frame)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            canvas.draw()

            results_frame.grid_rowconfigure(1, weight=1)
            results_frame.grid_columnconfigure(0, weight=1)
            results_frame.grid_columnconfigure(1, weight=1)

            self.exercise_button = tk.Button(
                results_frame,
                text="오늘의 운동 루틴 정하기",
                font=("Arial", 18, "bold"),
                bg="#A9D0F5",
                command=self.show_exercise_screen
            )
            self.exercise_button.grid(row=4, column=0, columnspan=2, pady=(20, 10), sticky="ew")
        except Exception as e:
            print(f"Error: {e}")