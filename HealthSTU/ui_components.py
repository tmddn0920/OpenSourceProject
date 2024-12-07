import tkinter as tk
from tkinter import filedialog, messagebox
from ocr_processing import process_inbody_image, parse_inbody_data
from calculations import calculate_bmi, calculate_body_fat_percentage, classify_body_type
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib as mpl
import random

mpl.rcParams['font.family'] = 'Malgun Gothic'  
mpl.rcParams['axes.unicode_minus'] = False    

class InbodyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HEALTH STU")
        self.root.geometry("800x800") 
        self.root.resizable(False, False)  
        self.root.configure(bg="#ffffff")
        self.inbody_data = {}

        self.bg_image = tk.PhotoImage(file="C:\\Users\\User\\Desktop\\OpenSourceProject\\HealthSTU\\background.png") 
        self.canvas = tk.Canvas(root, width=800, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)  
        
        self.canvas.create_text(400, 100, text="HEALTH STU (건강 분석기)", fill="#FFFFFF", font=("Arial", 28, "bold"))
        
        self.start_button = tk.Button(root, text="정보 입력 후 시작하기", font=("Arial", 16), bg="#A9D0F5", command=self.show_input_screen)
        self.start_button_window = self.canvas.create_window(400, 400, window=self.start_button)
        
        self.help_button = tk.Button(root, text="사용 방법", font=("Arial", 16), bg="#CDE4F2", command=self.show_help_screen)
        self.help_button_window = self.canvas.create_window(400, 480, window=self.help_button)
        
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_help_screen(self):
        """사용 방법 창을 띄웁니다."""
        help_window = tk.Toplevel(self.root)
        help_window.title("사용 방법")
        help_window.geometry("400x400")
        help_window.resizable(False, False)

        help_label = tk.Label(
            help_window,
            text="HEALTH STU 사용 방법:\n\n"
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
        
    def show_input_screen(self):
        self.clear_screen()

        # Canvas 생성 및 배경 이미지 설정
        self.canvas = tk.Canvas(self.root, width=800, height=800)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        # Canvas 중앙 좌표
        canvas_width = 800
        center_x = canvas_width // 2

        # 이름 입력 설명문 (첫 줄)
        self.canvas.create_text(center_x, 400, text="당신의 이름을 입력해주세요:", fill="black", font=("Arial", 16), anchor="center")
        # 이름 입력 필드 (두 번째 줄)
        self.name_entry = tk.Entry(self.root, font=("Arial", 16), width=20)
        self.name_entry_window = self.canvas.create_window(center_x, 430, window=self.name_entry)

        # 키 입력 설명문 (첫 줄)
        self.canvas.create_text(center_x, 460, text="키(cm)를 입력해주세요:", fill="black", font=("Arial", 16), anchor="center")
        # 키 입력 필드 (두 번째 줄)
        self.height_entry = tk.Entry(self.root, font=("Arial", 16), width=20)
        self.height_entry_window = self.canvas.create_window(center_x, 490, window=self.height_entry)

        # 버튼 추가 (더 아래쪽 배치)
        self.image_button = tk.Button(self.root, text="INBODY 데이터 불러오기", font=("Arial", 18), bg="#cde4f2", command=self.select_image)
        self.image_button_window = self.canvas.create_window(center_x, 550, window=self.image_button)

        self.result_button = tk.Button(self.root, text="내 신체 상태는??", font=("Arial", 18), bg="#e2f7d3", command=self.display_results, state=tk.DISABLED)
        self.result_button_window = self.canvas.create_window(center_x, 650, window=self.result_button)

        
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

    def create_graph(self, bmi, body_fat_percentage):
        # 그래프 생성 (크기 조정)
        fig, ax = plt.subplots(figsize=(5, 5))  # 그래프 크기를 5x5로 줄임
        ax.set_xlim(8, 18)  # 체지방률 범위
        ax.set_ylim(16, 25)  # BMI 범위
        ax.set_xlabel("체지방률 (%)")
        ax.set_ylabel("BMI")
        ax.set_title("체형 분류")

        # 사용자 상태 점 표시
        ax.scatter(body_fat_percentage, bmi, color="black", s=50, label="현재 상태")
        ax.legend()

        # 체형 분류 구역 표시 (사각형)
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
            # 사각형 영역 그리기
            rect = plt.Rectangle(
                (region["x_range"][0], region["y_range"][0]),
                region["x_range"][1] - region["x_range"][0],
                region["y_range"][1] - region["y_range"][0],
                facecolor="skyblue",
                alpha=0.3,
                edgecolor="black"
            )
            ax.add_patch(rect)

            # 중앙에 텍스트 추가
            center_x = (region["x_range"][0] + region["x_range"][1]) / 2
            center_y = (region["y_range"][0] + region["y_range"][1]) / 2
            ax.text(center_x, center_y, region["label"], ha="center", va="center", fontsize=8)

        return fig
    
    def show_exercise_screen(self):
        """운동 선택 화면으로 전환"""
        self.clear_screen()

        tk.Label(self.root, text="운동할 부위를 선택하세요:", font=("Arial", 20), bg="#ffffff").pack(pady=20)

        body_parts = ["어깨", "팔", "가슴", "등", "하체"]
        exercises = {
            "어깨": [["사이드 레터럴 레이즈 머신(측면 스트레칭)"], ["밀리터리 프레스", "오버헤드 프레스"], ["덤벨 숄더 프레스", "아놀드 프레스"], ["프론트 레이즈", "업라이트 로우"], ["페이스 풀", "리버스 펙덱 플라이"]],
            "팔": [["바벨 컬"], ["해머 컬"], ["컨센트레이션 컬", "덤벨 컬"], ["트라이셉스 익스텐션", "케이블 푸쉬 다운"], ["덤벨 오버헤드 익스텐션", "덤벨 킥 백"]],
            "가슴": [["벤치 프레스", "덤벨 체스트 프레스"], ["인클라인 벤치 프레스", "덤벨 인클라인 체스트 프레스"], ["체스트 프레스 머신"], ["딥스"], ["케이블 플라이", "덤벨 플라이"]],
            "등": [["풀 다운", "풀업"], ["컨벤셔널 데드리프트", "루마니안 데드리프트"], ["티바 로우", "바벨 로우"], ["하이 로우", "케이블 로우"], ["렛 풀 다운"]],
            "하체": [["풀 스쿼트"], ["레그 프레스", "핵 스쿼트"], ["레그 컬"], ["레그 익스텐션", "런지"], ["이너 타이", "아웃 타이"]]
        }

        selected_body_part = tk.StringVar(value=body_parts[0])

        for part in body_parts:
            tk.Radiobutton(
                self.root,
                text=part,
                variable=selected_body_part,
                value=part,
                font=("Arial", 14),
                bg="#ffffff"
            ).pack(anchor="w", padx=50)

        def generate_routine():
            part = selected_body_part.get()
            if part in exercises:
                routine = [random.choice(pair) for pair in exercises[part]]
                self.show_routine_screen(part, routine)

        tk.Button(
            self.root,
            text="운동 시작",
            font=("Arial", 16),
            bg="#e2f7d3",
            command=generate_routine
        ).pack(pady=20)

    def clear_screen(self):
        """현재 화면을 초기화"""
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def show_routine_screen(self, body_part, routine):
        """운동 루틴 화면 표시"""
        self.clear_screen()

        routine_frame = tk.Frame(self.root, bg="#ffffff")
        routine_frame.pack(fill="both", expand=True)

        tk.Label(routine_frame, text=f"오늘의 {body_part} 운동 루틴!", font=("Arial", 24), bg="#ffffff").pack(pady=20)

        for idx, exercise in enumerate(routine, start=1):
            tk.Label(routine_frame, text=f"STEP {idx}: {exercise}", font=("Arial", 16), bg="#ffffff").pack(pady=5)

    def display_results(self):
        """몸 상태 화면 표시"""
        try:
            # 입력 데이터 가져오기
            name = self.name_entry.get()
            height = float(self.height_entry.get())
            weight = self.inbody_data["weight_kg"]
            muscle = self.inbody_data["skeletal_muscle_mass"]
            fat = self.inbody_data["body_fat_mass"]

            # 계산
            bmi = calculate_bmi(height, weight)
            body_fat_percentage = calculate_body_fat_percentage(weight, fat)
            body_type = classify_body_type(bmi, body_fat_percentage)

            # 화면 초기화 및 새로운 프레임 생성
            self.clear_screen()
            results_frame = tk.Frame(self.root, bg="#ffffff")
            results_frame.grid(row=0, column=0, sticky="nsew")

            self.root.grid_rowconfigure(0, weight=1)
            self.root.grid_columnconfigure(0, weight=1)

            # 결과 데이터 표시
            header_label = tk.Label(results_frame, text=f"{name} 님은 '{body_type}' 입니다!", font=("Arial", 24), bg="#ffffff")
            header_label.grid(row=0, column=0, columnspan=2, pady=(20, 40))

            result_frame = tk.Frame(results_frame, bg="#ffffff")
            result_frame.grid(row=1, column=0, padx=20, pady=10)

            tk.Label(result_frame, text=f"체중: {weight:.2f} kg", font=("Arial", 16), bg="#ffffff").pack(anchor="center", pady=5)
            tk.Label(result_frame, text=f"골격근량: {muscle:.2f} kg", font=("Arial", 16), bg="#ffffff").pack(anchor="center", pady=5)
            tk.Label(result_frame, text=f"체지방량: {fat:.2f} kg", font=("Arial", 16), bg="#ffffff").pack(anchor="center", pady=5)

            extra_frame = tk.Frame(results_frame, bg="#ffffff")
            extra_frame.grid(row=2, column=0, padx=20, pady=10)

            tk.Label(extra_frame, text=f"BMI: {bmi:.2f}", font=("Arial", 14), bg="#ffffff").pack(anchor="center", pady=5)
            tk.Label(extra_frame, text=f"체지방률: {body_fat_percentage:.2f}%", font=("Arial", 14), bg="#ffffff").pack(anchor="center", pady=5)

            # 그래프 표시
            graph_frame = tk.Frame(results_frame, bg="#ffffff", width=400, height=400)
            graph_frame.grid(row=1, column=1, rowspan=2, padx=20, pady=10)

            fig = self.create_graph(bmi, body_fat_percentage)
            canvas = FigureCanvasTkAgg(fig, master=graph_frame)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            canvas.draw()

            # 운동하기 버튼
            self.exercise_button = tk.Button(
                results_frame,
                text="운동하기",
                font=("Arial", 20),
                bg="#A9D0F5",
                command=self.show_exercise_screen
            )
            self.exercise_button.grid(row=4, column=0, columnspan=2, pady=(20, 10))

        except Exception as e:
            messagebox.showerror("오류", f"결과 계산 중 오류가 발생했습니다: {e}")