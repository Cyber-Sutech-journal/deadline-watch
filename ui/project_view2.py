from services import calculator
import customtkinter as ctk


class ProjectView(ctk.CTkFrame):
    def __init__(self,parent,project,project_manager,storage):
        super().__init__(parent)

        self.project=project
        self.project_manager=project_manager
        self.storage=storage

        value=slider.get()
        self.project.update_task(
            task.id,
            new_progress=value
        )
        self.project.update_task(
            task.id,
            new_progress=value
        )
        self.storage.save_projects(
            self.project_manager.get_all_projects()
        ) 
        task.complete()

        self.storage.save_projects(
            self.project_manager.get_all_projects()
        )

        self.refresh_tasks()
        
        task.reopen()
        self.storage.save_projects(
            self.project_manager.get_all_projects()
        )

        self.refresh_tasks()

        self.project.remove_task(task.id)

        self.storage.save_projects(
            self.project_manager.get_all_projects()
        )

        self.refresh_tasks()

        self.project.add_task(task)

        self.storage.save_projects(
            self.project_manager.get_all_projects()
        )

        self.refresh_tasks()

        self.project.update_task(
            task.id,
            new_title=new_title,
            new_weight=new_weight,
            new_deadline=new_deadline,
            new_progress=new_progress
        )

        self.storage.save_projects(
            self.project_manager.get_all_projects()
        )

        self.refresh_tasks()

        self.project_title=ctk.CTkLabel(
            self,
            text="Project View",
            font=("Arial",28,"bold")
        )
        self.project_title.pack(
            pady=30
        )

        self.task_list=ctk.CTkScrollableFrame(
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
