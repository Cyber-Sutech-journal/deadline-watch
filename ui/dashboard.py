import customtkinter as ctk

class Dashboard(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)

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
