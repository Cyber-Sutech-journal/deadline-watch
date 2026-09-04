import customtkinter as ctk
from dashboard import Dashboard

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

dashboard=Dashboard(main_area)

dashboard.pack(
    fill="both",
    expand=True
)
project_card=ctk.CTkFrame(
    main_area,
    width=500,
    height=250
)

project_card.pack(
    padx=30,
    pady=20,
    fill="x"
)
project_name=ctk.CTkLabel(
    project_card,
    text="My First Project",
    font=("Arial",20,"bold")
)
project_name.pack(
    anchor="w",
    padx=20,
    pady=15
)

progress_label=ctk.CTkLabel(
    project_card,
    text="progress: 65%"
)

progress_label.pack(
    anchor="w",
    padx=20,
    pady=5
)

progress_bar=ctk.CTkProgressBar(
    project_card
)

progress_bar.pack(
    padx=20,
    pady=10,
    fill="x"
)

progress_bar.set(0.65)

status_label=ctk.CTkLabel(
    project_card,
    text="Status:IN PROGRESS"
)    

status_label.pack(
    anchor="w",
    padx=20,
    pady=5
)

remaining_label=ctk.CTkLabel(
    project_card,
    text="Time Remaining:5 days"
)
remaining_label.pack(
    anchor="w",
    padx=20,
    pady=5
)        
app.mainloop()
