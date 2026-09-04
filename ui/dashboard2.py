import customtkinter as ctk
from services.calculator import Calculator
from services.predictor import Predictor

class Dashboard(ctk.CTkFrame):
    def __init__(self,parent,project_manager,storage):
        super().__init__(parent)
        self.project_manager=project_manager
        self.storage=storage
        self.build_ui()
        self.refresh_dashboard()

        self.dashboard_title=ctk.CTkLabel(
             self,
            text="Dashboard",
            font=("Arial",28,"bold")
    )

        self.dashboard_title.pack(
            pady=30
    )    
        self.project_list=ctk.CTkScrollableFrame(
            self
        )

        self.project_list.pack(
            padx=30,
            pady=20,
            fill="both",
            expand=True
        )   
        self.project_card=ctk.CTkFrame(
            self.project_list

        )

        self.project_card.pack(
            padx=10,
            pady=10,
            fill="x"
        ) 

        self.project_name=ctk.CTkLabel(
            self.project_card,
            text="My First Project",
            font=("Arial",20,"bold")
        )

        self.project_name.pack(
            anchor="w",
            padx=20,
            pady=15
        )

        self.project_progress=ctk.CTkLabel(
            self.project_card,
            text="Project Progress:65%"
        )

        self.project_progress.pack(
            anchor="w",
            padx=20,
            pady=5
        )
        self.time_progress=ctk.CTkLabel(
            self.project_card,
            text="Time Progress:40%"
        )

        self.time_progress.pack(
            anchor="w",
            padx=20,
            pady=5
        )

        self.status=ctk.CTkLabel(
            self.project_card,
            text="Status: IN PROGRESS"
        )
        self.status.pack(
            anchor="w",
            padx=20,
            pady=5
        )
        self.remaining_days=ctk.CTkLabel(
            self.project_card,
            text="Remaining Days: 5"
        )

        self.remaining_days.pack(
            anchor="w",
            padx=20,
            pady=5
        )
        self.disaster_index=ctk.CTkLabel(
            self.project_card,
            text="Disaster Index: 25"
        )

        self.disaster_index.pack(
            anchor="w",
            padx=20,
            pady=5
        )     
    def refresh_dashboard(self):
        projects = self.project_manager.get_all_projects()

        if not projects:
            return

        project = projects[0]

        progress = Calculator.calculate_project_progress(project)
        time_progress = Calculator.calculate_time_progress(project)
        remaining_days = Calculator.calculate_time_remaining(project)
        disaster = Calculator.calculate_disaster_index(project)
        status = Calculator.get_project_status(project)

        prediction = Predictor.predict_completion_date(project)

        self.project_name.configure(
            text=project.name
        )

        self.progress_label.configure(
        text=f"Project Progress: {progress:.0f}%"
        )

        self.progress_bar.set(
            progress / 100
        )

        self.time_progress_label.configure(
            text=f"Time Progress: {time_progress:.0f}%"
        )

        self.remaining_label.configure(
            text=f"Remaining Days: {remaining_days}"
        )

        self.disaster_label.configure(
            text=f"Disaster Index: {disaster:.0f}"
        )

        self.status_label.configure(
            text=f"Status: {status.replace('_', ' ').upper()}"
        )

        if prediction is None:
            self.prediction_label.configure(
                text="Predicted Completion: N/A"
            )
        else:
            self.prediction_label.configure(
                text=f"Predicted Completion: {prediction}"
            )

        self.after(60000, self.refresh_dashboard)
