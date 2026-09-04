import customtkinter as ctk
from services.calculator import Calculator
from services.predictor import Predictor

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent, project_manager, storage):
        super().__init__(parent)
        self.project_manager = project_manager
        self.storage = storage
        self.build_ui()
        self.refresh_dashboard()

    def build_ui(self):
        # ---------- ساخت المان‌های ثابت UI ----------
        self.dashboard_title = ctk.CTkLabel(
            self,
            text="Dashboard",
            font=("Arial", 28, "bold")
        )
        self.dashboard_title.pack(pady=30)

        self.project_list = ctk.CTkScrollableFrame(self)
        self.project_list.pack(padx=30, pady=20, fill="both", expand=True)

        # کارت پروژه (فقط برای نمایش اولین پروژه طبق منطق فعلی شما)
        self.project_card = ctk.CTkFrame(self.project_list)
        self.project_card.pack(padx=10, pady=10, fill="x")

        self.project_name = ctk.CTkLabel(
            self.project_card,
            text="My First Project",
            font=("Arial", 20, "bold")
        )
        self.project_name.pack(anchor="w", padx=20, pady=15)

        self.progress_label = ctk.CTkLabel(
            self.project_card,
            text="Project Progress: 0%"
        )
        self.progress_label.pack(anchor="w", padx=20, pady=5)

        self.progress_bar = ctk.CTkProgressBar(self.project_card, width=400)
        self.progress_bar.pack(anchor="w", padx=20, pady=5)
        self.progress_bar.set(0)

        self.time_progress_label = ctk.CTkLabel(
            self.project_card,
            text="Time Progress: 0%"
        )
        self.time_progress_label.pack(anchor="w", padx=20, pady=5)

        self.status_label = ctk.CTkLabel(
            self.project_card,
            text="Status: NOT STARTED"
        )
        self.status_label.pack(anchor="w", padx=20, pady=5)

        self.remaining_label = ctk.CTkLabel(
            self.project_card,
            text="Remaining Days: 0"
        )
        self.remaining_label.pack(anchor="w", padx=20, pady=5)

        self.disaster_label = ctk.CTkLabel(
            self.project_card,
            text="Disaster Index: 0"
        )
        self.disaster_label.pack(anchor="w", padx=20, pady=5)

        self.prediction_label = ctk.CTkLabel(
            self.project_card,
            text="Predicted Completion: N/A"
        )
        self.prediction_label.pack(anchor="w", padx=20, pady=5)

    def refresh_dashboard(self):
        projects = self.project_manager.get_all_projects()

        if not projects:
            return

        # طبق کد شما، فقط اولین پروژه را نشان می‌دهیم
        project = projects[0]

        progress = Calculator.calculate_project_progress(project)
        time_progress = Calculator.calculate_time_progress(project)
        remaining_days = Calculator.calculate_time_remaining(project)
        disaster = Calculator.calculate_disaster_index(project)
        status = Calculator.get_project_status(project)
        prediction = Predictor.predict_completion_date(project)

        # آپدیت لیبل‌ها
        self.project_name.configure(text=project.name)
        self.progress_label.configure(text=f"Project Progress: {progress:.0f}%")
        self.progress_bar.set(progress / 100)
        self.time_progress_label.configure(text=f"Time Progress: {time_progress:.0f}%")
        self.remaining_label.configure(text=f"Remaining Days: {remaining_days}")
        self.disaster_label.configure(text=f"Disaster Index: {disaster:.0f}")
        self.status_label.configure(text=f"Status: {status.replace('_', ' ').upper()}")

        if prediction is None:
            self.prediction_label.configure(text="Predicted Completion: N/A")
        else:
            self.prediction_label.configure(text=f"Predicted Completion: {prediction}")

        # رفرش خودکار هر ۶۰ ثانیه
        self.after(60000, self.refresh_dashboard)