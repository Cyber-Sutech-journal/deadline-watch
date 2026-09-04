import customtkinter as ctk
from tkinter import messagebox

# ایمپورت‌های صحیح (با ui. در ابتدا)
from ui.dashboard import Dashboard
from services.project_manager import ProjectManager
from services.storage import JSONStorage
from ui.project_view import ProjectView

BG_COLOR = "#0F1117"
SIDEBAR_COLOR = "#151922"
CARD_COLOR = "#1C2130"
PRIMARY_COLOR = "#6C63FF"
HOVER_COLOR = "#8178FF"
TEXT_COLOR = "#F5F7FA"
SECONDARY_TEXT_COLOR = "#A7AFBF"

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BG_COLOR)
        self.title("Project Late Again")
        self.geometry("1000x600")

        # ساخت سرویس‌ها
        self.storage = JSONStorage()
        self.project_manager = ProjectManager()

        # لود کردن پروژه‌ها
        loaded_projects = self.storage.load_projects()
        if loaded_projects:
            self.project_manager.set_projects(loaded_projects)

        # برای ذخیره پروژه‌ی باز شده
        self.project_view = None

        # سایدبار
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color=SIDEBAR_COLOR, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.title_label = ctk.CTkLabel(self.sidebar, text="Project Late Again", font=("Arial", 20, "bold"), text_color=TEXT_COLOR)
        self.title_label.pack(pady=30)

        self.dashboard_button = ctk.CTkButton(self.sidebar, text="Dashboard", fg_color=PRIMARY_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR, command=self.show_dashboard)
        self.dashboard_button.pack(pady=10)

        self.projects_button = ctk.CTkButton(self.sidebar, text="Projects", fg_color=PRIMARY_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR)
        self.projects_button.pack(pady=10)

        self.settings_button = ctk.CTkButton(self.sidebar, text="Settings", fg_color=PRIMARY_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR)
        self.settings_button.pack(pady=10)

        # ناحیه اصلی
        self.main_area = ctk.CTkFrame(self, fg_color=BG_COLOR)
        self.main_area.pack(side="left", fill="both", expand=True)

        # ساخت داشبورد (با 3 آرگومان - storage اضافه شد)
        self.dashboard = Dashboard(self.main_area, self.project_manager, self.storage)
        self.dashboard.pack(fill="both", expand=True)

    def show_dashboard(self):
        if self.project_view is not None:
            self.project_view.destroy()
            self.project_view = None
        
        self.dashboard.refresh()
        self.dashboard.pack(fill="both", expand=True)

    def open_project_view(self, project_id):
        project = self.project_manager.get_project(project_id)
        if project is None:
            messagebox.showerror("Error", "Project not found.")
            return

        if self.project_view is not None:
            self.project_view.destroy()
            self.project_view = None

        self.dashboard.pack_forget()

        # ساخت ProjectView (با همه آرگومان‌ها)
        self.project_view = ProjectView(
            self.main_area, project, self.project_manager, self.storage, on_back=self.show_dashboard
        )
        self.project_view.pack(fill="both", expand=True)

    def add_project_view(self):
        messagebox.showinfo("Add Project", "The Add Project form is not implemented yet.")

if __name__ == "__main__":
    app = App()
    app.mainloop()