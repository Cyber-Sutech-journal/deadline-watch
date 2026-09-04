import customtkinter as ctk
from dashboard import Dashboard
from services.project_manager import ProjectManager
from services.storage import JSONStorage

BG_COLOR="#0F1117"
SIDEBAR_COLOR="#151922"
CARD_COLOR="#1C2130"
PRIMARY_COLOR="#6C63FF"
HOVER_COLOR="#8178FF"

TEXT_COLOR="#F5F7FA"
SECONDARY_TEXT_COLOR="#A7AFBF"

SAFE_COLOR="#35D07F"
WARNING_COLOR="#FFB547"
DANGER_COLOR="#FF5C6C"


app=ctk.CTk(fg_color=BG_COLOR)
app.title("Project Late Again")
app.geometry("1000x600")

sidebar=ctk.CTkFrame(
    app,
    width=200,
    fg_color=SIDEBAR_COLOR
 )
sidebar.pack(side="left", fill="y")

title_label=ctk.CTkLabel(
    sidebar,
    text="Project Late Again",
    font=("Arial",20,"bold"),
    text_color=TEXT_COLOR
)

title_label.pack(pady=30)

dashboard_button=ctk.CTkButton(
    sidebar,
    text="Dashboard",
    fg_color=PRIMARY_COLOR,
    hover_color=HOVER_COLOR,
    text_color=TEXT_COLOR
)

dashboard_button.pack(pady=10)

projects_button=ctk.CTkButton(
    sidebar,
    text="Projects",
    fg_color=PRIMARY_COLOR,
    hover_color=HOVER_COLOR,
    text_color=TEXT_COLOR
)    

projects_button.pack(pady=10)

settings_button=ctk.CTkButton(
    sidebar,
    text="Settings",
    fg_color=PRIMARY_COLOR,
    hover_color=HOVER_COLOR,
    text_color=TEXT_COLOR
)

settings_button.pack(pady=10)

main_area=ctk.CTkFrame(
    app,
    fg_color=BG_COLOR,
)
main_area.pack(side="left",fill="both",expand=True)

project_manager=ProjectManager()
storage=JSONStorage()

projects=storage.load_projects()
project_manager.set_projects(projects)

dashboard=Dashboard(
    main_area,
    project_manager,
    storage
)    

dashboard.pack(
    fill="both",
    expand=True
)
project_manager=ProjectManager()
storage=JSONStorage()

projects=storage.load_projects()
project_manager.set_projects(projects)

dashboard=Dashboard(
    main_area,
    project_manager,
    storage
)
dashboard.pack(
    fill="both",
    expand=True
)       
app.mainloop()
