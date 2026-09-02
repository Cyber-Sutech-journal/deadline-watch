import customtkinter as ctk

class ProjectView(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)

        self.project_title=ctk.CTkLabel(
            self,
            text="Project View",
            font=("Arial",28,"bold")
        )
        self.project_title.pack(
            pady=30
        )

        self.task_list=ctk.CTkScrolllableFrame(
            self
        )    

        self.task_list.pack(
            padx=30,
            pady=20,
            fill="both",
            expand=True
        )
        self.add_task_button=ctk.CTkButton(
            self,
            text="Add Task"
        )

        self.add_task_button.pack(
            padx=30,
            pady=10
        )

        self.edit_task_button=ctk.CTkButton(
            self,
            text="Edit Task"
        )

        self.edit_task_button.pack(
            padx=30,
            pady=10
        )

        self.delete_task_button=ctk.CTkButton(
            self,
            text="Delete Task"
        )

        self.delete_task_button.pack(
            padx=30,
            pady=10
        )                    

        self.progress_slider=ctk.CTkSlider(
            self,
            from_=0,
            to=100
        )

        self.progress_slider.pack(
            padx=30,
            pady=10
        )

        self.complete_task_button=ctk.CTkButton(
            self,
            text="Complete Task"
        )

        self.complete_task_button.pack(
            padx=30,
            pady=10
        )

        self.reopen_task_button=ctk.CTkButton(
            self,
            text="Reopen Task"
        )

        self.reopen_task_button.pack(
            padx=30,
            pady=10
        )                                   
