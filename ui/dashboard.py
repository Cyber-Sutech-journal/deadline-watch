import customtkinter as ctk
from datetime import date

from services.calculator import Calculator


# ============================================================
# COLORS
# ============================================================

BG_COLOR = "#0A0E13"
CARD_COLOR = "#171E27"

TEXT_COLOR = "#F4F7FB"
MUTED_COLOR = "#97A3B3"

PRIMARY = "#6C63FF"
PRIMARY_HOVER = "#8078FF"

GREEN = "#22C55E"
GREEN_BG = "#173923"

YELLOW = "#F59E0B"
YELLOW_BG = "#44340F"

RED = "#EF4444"
RED_BG = "#441C20"


class Dashboard(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        project_manager,
        on_open_project,
        on_edit_project,
        on_delete_project,
        on_add_project
    ):

        super().__init__(
            parent,
            fg_color=BG_COLOR
        )

        self.manager = project_manager

        self.on_open_project = on_open_project
        self.on_edit_project = on_edit_project
        self.on_delete_project = on_delete_project
        self.on_add_project = on_add_project

        self.build_ui()
        self.refresh()

    # ========================================================
    # UI
    # ========================================================

    def build_ui(self):

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=35,
            pady=(30, 5)
        )

        title = ctk.CTkLabel(
            header,
            text="Project Dashboard",
            font=ctk.CTkFont(
                size=35,
                weight="bold"
            ),
            text_color=TEXT_COLOR
        )

        title.pack(
            side="left"
        )

        add_button = ctk.CTkButton(
            header,
            text="+  New Project",
            command=self.on_add_project,
            width=180,
            height=50,
            corner_radius=12,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        add_button.pack(
            side="right"
        )

        self.subtitle = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(
                size=15
            ),
            text_color=MUTED_COLOR
        )

        self.subtitle.pack(
            anchor="w",
            padx=35
        )

        # ----------------------------------------------------
        # Statistics
        # ----------------------------------------------------

        self.stats_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.stats_frame.pack(
            fill="x",
            padx=30,
            pady=25
        )

        for i in range(4):
            self.stats_frame.grid_columnconfigure(
                i,
                weight=1
            )

        self.projects_value = self.create_stat_card(
            self.stats_frame,
            0,
            "PROJECTS"
        )

        self.tasks_value = self.create_stat_card(
            self.stats_frame,
            1,
            "TASKS"
        )

        self.completed_value = self.create_stat_card(
            self.stats_frame,
            2,
            "COMPLETED TASKS"
        )

        self.overdue_value = self.create_stat_card(
            self.stats_frame,
            3,
            "OVERDUE TASKS"
        )

        # ----------------------------------------------------
        # Projects section
        # ----------------------------------------------------

        section_title = ctk.CTkLabel(
            self,
            text="Your Projects",
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            ),
            text_color=TEXT_COLOR
        )

        section_title.pack(
            anchor="w",
            padx=35,
            pady=(0, 10)
        )

        self.projects_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.projects_scroll.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

    # ========================================================
    # STAT CARD
    # ========================================================

    def create_stat_card(
        self,
        parent,
        column,
        title
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color=CARD_COLOR,
            corner_radius=16,
            height=115
        )

        card.grid(
            row=0,
            column=column,
            padx=7,
            sticky="nsew"
        )

        card.grid_propagate(
            False
        )

        label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=MUTED_COLOR
        )

        label.pack(
            anchor="w",
            padx=20,
            pady=(17, 0)
        )

        value = ctk.CTkLabel(
            card,
            text="0",
            font=ctk.CTkFont(
                size=34,
                weight="bold"
            ),
            text_color=TEXT_COLOR
        )

        value.pack(
            anchor="w",
            padx=20,
            pady=(0, 10)
        )

        return value

    # ========================================================
    # PROJECT COLOR
    # ========================================================

    def get_project_colors(self, project):

        status = Calculator.get_project_status(
            project
        )

        disaster = Calculator.calculate_disaster_index(
            project
        )

        # Completed = Green
        if status == "completed":
            return GREEN, GREEN_BG

        # Overdue = Red
        if status == "overdue":
            return RED, RED_BG

        # Not started = Yellow
        if status == "not_started":
            return YELLOW, YELLOW_BG

        # In progress depends on disaster index.
        if disaster > 70:
            return RED, RED_BG

        if disaster > 30:
            return YELLOW, YELLOW_BG

        return GREEN, GREEN_BG

    # ========================================================
    # REFRESH
    # ========================================================

    def refresh(self):

        for widget in self.projects_scroll.winfo_children():
            widget.destroy()

        projects = self.manager.get_all_projects()

        total_tasks = 0
        completed_tasks = 0
        overdue_tasks = 0

        today = date.today()

        for project in projects:

            total_tasks += len(
                project.tasks
            )

            completed_tasks += len(
                project.get_completed_tasks()
            )

            for task in project.tasks:

                if task.is_overdue(today):
                    overdue_tasks += 1

        self.projects_value.configure(
            text=str(len(projects))
        )

        self.tasks_value.configure(
            text=str(total_tasks)
        )

        self.completed_value.configure(
            text=str(completed_tasks)
        )

        self.overdue_value.configure(
            text=str(overdue_tasks)
        )

        self.subtitle.configure(
            text=(
                f"{len(projects)} project(s)   •   "
                f"{total_tasks} task(s)   •   "
                f"{completed_tasks} completed"
            )
        )

        if not projects:
            self.show_empty_state()
            return

        for project in projects:
            self.create_project_card(
                project
            )

    # ========================================================
    # EMPTY STATE
    # ========================================================

    def show_empty_state(self):

        card = ctk.CTkFrame(
            self.projects_scroll,
            fg_color=CARD_COLOR,
            corner_radius=18
        )

        card.pack(
            fill="x",
            padx=15,
            pady=20
        )

        title = ctk.CTkLabel(
            card,
            text="No Projects Yet",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            ),
            text_color=TEXT_COLOR
        )

        title.pack(
            pady=(45, 5)
        )

        subtitle = ctk.CTkLabel(
            card,
            text="Create your first project to start tracking progress.",
            font=ctk.CTkFont(
                size=16
            ),
            text_color=MUTED_COLOR
        )

        subtitle.pack(
            pady=(0, 25)
        )

        button = ctk.CTkButton(
            card,
            text="+ Create Project",
            command=self.on_add_project,
            width=190,
            height=50,
            corner_radius=12,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        button.pack(
            pady=(0, 40)
        )

    # ========================================================
    # PROJECT CARD
    # ========================================================

    def create_project_card(self, project):

        progress = Calculator.calculate_project_progress(
            project
        )

        time_progress = Calculator.calculate_time_progress(
            project
        )

        remaining_days = Calculator.calculate_time_remaining(
            project
        )

        schedule_gap = Calculator.calculate_schedule_gap(
            project
        )

        disaster = Calculator.calculate_disaster_index(
            project
        )

        status = Calculator.get_project_status(
            project
        )

        accent, status_background = self.get_project_colors(
            project
        )

        card = ctk.CTkFrame(
            self.projects_scroll,
            fg_color=status_background,
            corner_radius=18,
            border_width=2,
            border_color=accent
        )

        card.pack(
            fill="x",
            padx=15,
            pady=9
        )

        # ----------------------------------------------------
        # TOP
        # ----------------------------------------------------

        top = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=22,
            pady=(20, 5)
        )

        title_frame = ctk.CTkFrame(
            top,
            fg_color="transparent"
        )

        title_frame.pack(
            side="left",
            fill="x",
            expand=True
        )

        title = ctk.CTkLabel(
            title_frame,
            text=project.name,
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            ),
            text_color=TEXT_COLOR
        )

        title.pack(
            anchor="w"
        )

        description = project.description.strip()

        if not description:
            description = "No description"

        desc = ctk.CTkLabel(
            title_frame,
            text=description,
            font=ctk.CTkFont(
                size=14
            ),
            text_color=MUTED_COLOR
        )

        desc.pack(
            anchor="w",
            pady=(4, 0)
        )

        status_map = {
            "not_started": "NOT STARTED",
            "in_progress": "IN PROGRESS",
            "completed": "COMPLETED",
            "overdue": "OVERDUE"
        }

        status_badge = ctk.CTkLabel(
            top,
            text=status_map.get(
                status,
                status.upper()
            ),
            width=170,
            height=42,
            corner_radius=12,
            fg_color=status_background,
            text_color=accent,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        status_badge.pack(
            side="right"
        )

        # ----------------------------------------------------
        # PROGRESS
        # ----------------------------------------------------

        progress_area = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        progress_area.pack(
            fill="x",
            padx=22,
            pady=(15, 5)
        )

        project_progress_title = ctk.CTkLabel(
            progress_area,
            text="PROJECT PROGRESS",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=MUTED_COLOR
        )

        project_progress_title.pack(
            anchor="w"
        )

        project_progress_value = ctk.CTkLabel(
            progress_area,
            text=f"{progress:.0f}%",
            font=ctk.CTkFont(
                size=42,
                weight="bold"
            ),
            text_color=accent
        )

        project_progress_value.pack(
            anchor="w"
        )

        progress_bar = ctk.CTkProgressBar(
            progress_area,
            height=16,
            corner_radius=8,
            fg_color="#2C3541",
            progress_color=accent
        )

        progress_bar.pack(
            fill="x",
            pady=(4, 0)
        )

        progress_bar.set(
            progress / 100
        )

        # ----------------------------------------------------
        # METRICS
        # ----------------------------------------------------

        metrics = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        metrics.pack(
            fill="x",
            padx=18,
            pady=15
        )

        for i in range(4):
            metrics.grid_columnconfigure(
                i,
                weight=1
            )

        self.create_metric(
            metrics,
            0,
            "TIME PROGRESS",
            f"{time_progress:.0f}%"
        )

        if remaining_days < 0:
            remaining_text = (
                f"{abs(remaining_days)}d overdue"
            )
        else:
            remaining_text = (
                f"{remaining_days} day(s)"
            )

        self.create_metric(
            metrics,
            1,
            "TIME REMAINING",
            remaining_text
        )

        gap_text = (
            f"+{schedule_gap:.1f}%"
            if schedule_gap > 0
            else f"{schedule_gap:.1f}%"
        )

        self.create_metric(
            metrics,
            2,
            "SCHEDULE GAP",
            gap_text
        )

        self.create_metric(
            metrics,
            3,
            "DISASTER INDEX",
            f"{disaster:.0f}"
        )

        # ----------------------------------------------------
        # FOOTER
        # ----------------------------------------------------

        footer = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        footer.pack(
            fill="x",
            padx=22,
            pady=(0, 20)
        )

        if schedule_gap <= 0:
            schedule_text = "On schedule"
        else:
            schedule_text = (
                f"{schedule_gap:.1f}% behind schedule"
            )

        schedule_label = ctk.CTkLabel(
            footer,
            text=schedule_text,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=accent
        )

        schedule_label.pack(
            side="left"
        )

        buttons = ctk.CTkFrame(
            footer,
            fg_color="transparent"
        )

        buttons.pack(
            side="right"
        )

        open_button = ctk.CTkButton(
            buttons,
            text="Open",
            command=lambda pid=project.id:
            self.on_open_project(pid),
            width=105,
            height=43,
            corner_radius=10,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        open_button.pack(
            side="left",
            padx=4
        )

        edit_button = ctk.CTkButton(
            buttons,
            text="Edit",
            command=lambda pid=project.id:
            self.on_edit_project(pid),
            width=100,
            height=43,
            corner_radius=10,
            fg_color="#283342",
            hover_color="#374555",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        edit_button.pack(
            side="left",
            padx=4
        )

        delete_button = ctk.CTkButton(
            buttons,
            text="Delete",
            command=lambda pid=project.id:
            self.on_delete_project(pid),
            width=100,
            height=43,
            corner_radius=10,
            fg_color=RED_BG,
            hover_color="#63242B",
            text_color="#FF9AA2",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        delete_button.pack(
            side="left",
            padx=(4, 0)
        )

    # ========================================================
    # METRIC
    # ========================================================

    def create_metric(
        self,
        parent,
        column,
        title,
        value
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color="#121921",
            corner_radius=13
        )

        card.grid(
            row=0,
            column=column,
            padx=5,
            sticky="nsew"
        )

        label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            ),
            text_color=MUTED_COLOR
        )

        label.pack(
            anchor="w",
            padx=13,
            pady=(11, 0)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                size=21,
                weight="bold"
            ),
            text_color=TEXT_COLOR
        )

        value_label.pack(
            anchor="w",
            padx=13,
            pady=(1, 11)
        )

        return card