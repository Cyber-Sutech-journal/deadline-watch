# ui/dashboard.py

import tkinter as tk
import customtkinter as ctk
from datetime import date


BG_COLOR = "#0F1117"
CARD_COLOR = "#181E28"
LATEST_CARD_COLOR = "#202837"
PRIMARY_COLOR = "#6C63FF"
HOVER_COLOR = "#8178FF"
TEXT_COLOR = "#F5F7FA"
MUTED_COLOR = "#8E97A8"
DANGER_COLOR = "#FF5F6D"
SUCCESS_COLOR = "#4ADE80"
WARNING_COLOR = "#FBBF24"


class Dashboard(ctk.CTkFrame):
    def __init__(self, parent, app, manager):
        super().__init__(
            parent,
            fg_color=BG_COLOR,
            corner_radius=0
        )

        self.app = app
        self.manager = manager

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_body()

        self.refresh()

    # =========================================================
    # HEADER
    # This stays fixed while the project list scrolls.
    # =========================================================

    def _build_header(self):
        self.header = ctk.CTkFrame(
            self,
            fg_color=BG_COLOR,
            corner_radius=0
        )
        self.header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=12,
            pady=(5, 0)
        )

        self.header.grid_columnconfigure(0, weight=1)

        top = ctk.CTkFrame(
            self.header,
            fg_color="transparent"
        )
        top.grid(
            row=0,
            column=0,
            sticky="ew"
        )
        top.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            top,
            text="Dashboard",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=TEXT_COLOR
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.date_label = ctk.CTkLabel(
            top,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=MUTED_COLOR
        )
        self.date_label.grid(
            row=1,
            column=0,
            sticky="w",
            pady=(2, 0)
        )

        self._build_stats()

    def _build_stats(self):
        self.stats_frame = ctk.CTkFrame(
            self.header,
            fg_color="transparent"
        )
        self.stats_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(18, 14)
        )

        for i in range(4):
            self.stats_frame.grid_columnconfigure(
                i,
                weight=1
            )

        self.stat_labels = {}

        stats = [
            ("projects", "PROJECTS"),
            ("tasks", "TASKS"),
            ("completed", "COMPLETED"),
            ("overdue", "OVERDUE"),
        ]

        for index, (key, title) in enumerate(stats):
            card = ctk.CTkFrame(
                self.stats_frame,
                fg_color=CARD_COLOR,
                corner_radius=12,
                height=82
            )
            card.grid(
                row=0,
                column=index,
                sticky="ew",
                padx=4
            )
            card.grid_propagate(False)

            value = ctk.CTkLabel(
                card,
                text="0",
                font=ctk.CTkFont(size=25, weight="bold"),
                text_color=TEXT_COLOR
            )
            value.pack(
                anchor="w",
                padx=15,
                pady=(11, 0)
            )

            ctk.CTkLabel(
                card,
                text=title,
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=MUTED_COLOR
            ).pack(
                anchor="w",
                padx=15
            )

            self.stat_labels[key] = value

    # =========================================================
    # BODY
    # =========================================================

    def _build_body(self):
        self.body = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0
        )
        self.body.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=12,
            pady=(0, 5)
        )

        self.body.grid_columnconfigure(0, weight=1)

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(self):
        self.date_label.configure(
            text=date.today().strftime("%A, %d %B %Y")
        )

        projects = self.manager.get_all_projects()

        for widget in self.body.winfo_children():
            widget.destroy()

        total_tasks = sum(
            len(project.tasks)
            for project in projects
        )

        completed_tasks = sum(
            len(project.get_completed_tasks())
            for project in projects
        )

        overdue_tasks = sum(
            1
            for project in projects
            for task in project.tasks
            if task.is_overdue(date.today())
        )

        self.stat_labels["projects"].configure(
            text=str(len(projects))
        )
        self.stat_labels["tasks"].configure(
            text=str(total_tasks)
        )
        self.stat_labels["completed"].configure(
            text=str(completed_tasks)
        )
        self.stat_labels["overdue"].configure(
            text=str(overdue_tasks)
        )

        if not projects:
            self._show_empty()
            return

        projects = sorted(
            projects,
            key=lambda p: p.deadline
        )

        latest_project = max(
            projects,
            key=lambda p: (
                p.start_date,
                p.deadline
            )
        )

        latest_container = ctk.CTkFrame(
            self.body,
            fg_color="transparent"
        )
        latest_container.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=5,
            pady=(4, 14)
        )
        latest_container.grid_columnconfigure(0, weight=1)

        self._create_project_card(
            latest_container,
            latest_project,
            latest=True
        )

        others_label = ctk.CTkLabel(
            self.body,
            text="ALL PROJECTS",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color=MUTED_COLOR
        )
        others_label.grid(
            row=1,
            column=0,
            sticky="w",
            padx=10,
            pady=(4, 7)
        )

        others = [
            project
            for project in projects
            if project.id != latest_project.id
        ]

        for index, project in enumerate(
            others,
            start=2
        ):
            self._create_project_card(
                self.body,
                project,
                latest=False,
                row=index
            )

    # =========================================================
    # EMPTY
    # =========================================================

    def _show_empty(self):
        container = ctk.CTkFrame(
            self.body,
            fg_color=CARD_COLOR,
            corner_radius=18
        )
        container.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=8,
            pady=30
        )

        ctk.CTkLabel(
            container,
            text="No projects yet",
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(
            pady=(45, 7)
        )

        ctk.CTkLabel(
            container,
            text="Create your first project and start watching the deadline.",
            font=ctk.CTkFont(size=13),
            text_color=MUTED_COLOR
        ).pack(
            pady=(0, 20)
        )

        ctk.CTkButton(
            container,
            text="＋  Create Project",
            command=self.app.add_project_view,
            width=190,
            height=44,
            fg_color=PRIMARY_COLOR,
            hover_color=HOVER_COLOR
        ).pack(
            pady=(0, 45)
        )

    # =========================================================
    # PROJECT CARD
    # =========================================================

    def _create_project_card(
        self,
        parent,
        project,
        latest=False,
        row=None
    ):
        today = date.today()

        if latest:
            card = ctk.CTkFrame(
                parent,
                fg_color=LATEST_CARD_COLOR,
                corner_radius=18,
                border_width=1,
                border_color="#30394A"
            )
        else:
            card = ctk.CTkFrame(
                parent,
                fg_color=CARD_COLOR,
                corner_radius=15
            )

        if row is not None:
            card.grid(
                row=row,
                column=0,
                sticky="ew",
                padx=5,
                pady=7
            )
        else:
            card.pack(
                fill="x",
                padx=5
            )

        card.grid_columnconfigure(0, weight=1)

        # -----------------------------------------------------
        # TOP
        # -----------------------------------------------------

        top = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )
        top.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20 if latest else 17,
            pady=(18 if latest else 15, 5)
        )
        top.grid_columnconfigure(0, weight=1)

        title_area = ctk.CTkFrame(
            top,
            fg_color="transparent"
        )
        title_area.grid(
            row=0,
            column=0,
            sticky="w"
        )

        if latest:
            ctk.CTkLabel(
                title_area,
                text="LATEST PROJECT",
                font=ctk.CTkFont(
                    size=10,
                    weight="bold"
                ),
                text_color=PRIMARY_COLOR
            ).pack(
                anchor="w",
                pady=(0, 2)
            )

        title = ctk.CTkLabel(
            title_area,
            text=project.name,
            font=ctk.CTkFont(
                size=24 if latest else 19,
                weight="bold"
            ),
            text_color=TEXT_COLOR,
            anchor="w"
        )
        title.pack(anchor="w")

        if project.description:
            ctk.CTkLabel(
                title_area,
                text=project.description,
                font=ctk.CTkFont(size=12),
                text_color=MUTED_COLOR,
                anchor="w",
                justify="left"
            ).pack(
                anchor="w",
                pady=(3, 0)
            )

        menu_button = ctk.CTkButton(
            top,
            text="⋮",
            width=38,
            height=38,
            corner_radius=10,
            fg_color="transparent",
            hover_color="#303846",
            text_color=TEXT_COLOR,
            font=ctk.CTkFont(size=22, weight="bold")
        )
        menu_button.grid(
            row=0,
            column=1,
            sticky="ne",
            padx=(10, 0)
        )

        menu_button.configure(
            command=lambda b=menu_button, p=project:
            self.show_project_menu(p, b)
        )

        # -----------------------------------------------------
        # MAIN METRICS
        # -----------------------------------------------------

        metrics = self._calculate_metrics(project)

        metric_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )
        metric_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=20 if latest else 17,
            pady=(8, 5)
        )

        metric_frame.grid_columnconfigure(
            0,
            weight=1
        )
        metric_frame.grid_columnconfigure(
            1,
            weight=1
        )

        # PROJECT PROGRESS
        progress_box = ctk.CTkFrame(
            metric_frame,
            fg_color="#151A23",
            corner_radius=13
        )
        progress_box.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 5)
        )

        ctk.CTkLabel(
            progress_box,
            text="PROJECT PROGRESS",
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            ),
            text_color=MUTED_COLOR
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 0)
        )

        progress_percent = ctk.CTkLabel(
            progress_box,
            text=f"{metrics['progress']:.0f}%",
            font=ctk.CTkFont(
                size=36 if latest else 30,
                weight="bold"
            ),
            text_color=TEXT_COLOR
        )
        progress_percent.pack(
            anchor="w",
            padx=15,
            pady=(0, 2)
        )

        progress_bar = ctk.CTkProgressBar(
            progress_box,
            height=9,
            corner_radius=5
        )
        progress_bar.pack(
            fill="x",
            padx=15,
            pady=(2, 5)
        )
        progress_bar.set(
            metrics["progress"] / 100
        )

        ctk.CTkLabel(
            progress_box,
            text=(
                f"{metrics['completed_tasks']} / "
                f"{metrics['total_tasks']} tasks completed"
            ),
            font=ctk.CTkFont(size=11),
            text_color=MUTED_COLOR
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 12)
        )

        # TIME PASSED
        time_box = ctk.CTkFrame(
            metric_frame,
            fg_color="#151A23",
            corner_radius=13
        )
        time_box.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(5, 0)
        )

        ctk.CTkLabel(
            time_box,
            text="TIME PASSED",
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            ),
            text_color=MUTED_COLOR
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 0)
        )

        time_percent = ctk.CTkLabel(
            time_box,
            text=f"{metrics['time_percent']:.0f}%",
            font=ctk.CTkFont(
                size=36 if latest else 30,
                weight="bold"
            ),
            text_color=(
                DANGER_COLOR
                if metrics["time_percent"] > metrics["progress"]
                else TEXT_COLOR
            )
        )
        time_percent.pack(
            anchor="w",
            padx=15,
            pady=(0, 2)
        )

        time_bar = ctk.CTkProgressBar(
            time_box,
            height=9,
            corner_radius=5
        )
        time_bar.pack(
            fill="x",
            padx=15,
            pady=(2, 5)
        )
        time_bar.set(
            metrics["time_percent"] / 100
        )

        ctk.CTkLabel(
            time_box,
            text=metrics["time_text"],
            font=ctk.CTkFont(size=11),
            text_color=MUTED_COLOR
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 12)
        )

        # -----------------------------------------------------
        # DEADLINE / HEALTH
        # -----------------------------------------------------

        deadline_row = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )
        deadline_row.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=20 if latest else 17,
            pady=(7, 5)
        )
        deadline_row.grid_columnconfigure(1, weight=1)

        deadline_label = self._deadline_text(
            project,
            today
        )

        ctk.CTkLabel(
            deadline_row,
            text="DEADLINE",
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            ),
            text_color=MUTED_COLOR
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            deadline_row,
            text=deadline_label,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=(
                DANGER_COLOR
                if project.deadline < today
                else TEXT_COLOR
            )
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=12
        )

        status_text = self._health_text(metrics)

        ctk.CTkLabel(
            deadline_row,
            text=status_text,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color=self._health_color(metrics)
        ).grid(
            row=0,
            column=2,
            sticky="e"
        )

        # -----------------------------------------------------
        # ACTIONS
        # -----------------------------------------------------

        actions = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )
        actions.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=20 if latest else 17,
            pady=(8, 18 if latest else 15)
        )

        actions.grid_columnconfigure(
            0,
            weight=2
        )
        actions.grid_columnconfigure(
            1,
            weight=1
        )

        ctk.CTkButton(
            actions,
            text="↻  Update Progress",
            command=lambda p=project:
            self.app.update_project_progress(p.id),
            height=44 if latest else 40,
            fg_color=PRIMARY_COLOR,
            hover_color=HOVER_COLOR,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 5)
        )

        ctk.CTkButton(
            actions,
            text="Edit",
            command=lambda p=project:
            self.app.edit_project_view(p.id),
            height=44 if latest else 40,
            fg_color="#252C38",
            hover_color="#323B4B",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(5, 0)
        )

        # Entire project card opens the detailed project view.
        self._bind_card_click(
            card,
            lambda p=project:
            self.app.open_project_view(p.id),
            ignored_widgets={
                menu_button
            }
        )

    # =========================================================
    # PROJECT MENU
    # =========================================================

    def show_project_menu(self, project, button):
        menu = tk.Menu(
            self,
            tearoff=False,
            bg="#1B202B",
            fg=TEXT_COLOR,
            activebackground="#303846",
            activeforeground=TEXT_COLOR,
            relief="flat",
            borderwidth=0,
            font=("Arial", 10)
        )

        menu.add_command(
            label="Update Progress",
            command=lambda:
            self.app.update_project_progress(project.id)
        )

        menu.add_command(
            label="Edit Project",
            command=lambda:
            self.app.edit_project_view(project.id)
        )

        menu.add_separator()

        menu.add_command(
            label="Delete Project",
            command=lambda:
            self.app.delete_project_view(project.id)
        )

        # IMPORTANT:
        # Popup directly next to the three-dot button.
        self.update_idletasks()

        x = button.winfo_rootx() + button.winfo_width() - 5
        y = button.winfo_rooty() + button.winfo_height() + 2

        menu.tk_popup(x, y)
        menu.bind(
            "<FocusOut>",
            lambda event: menu.destroy()
        )

    # =========================================================
    # METRICS
    # =========================================================

    def _calculate_metrics(self, project):
        today = date.today()

        total_weight = sum(
            float(task.weight)
            for task in project.tasks
        )

        if total_weight > 0:
            progress = sum(
                float(task.progress_percent) *
                float(task.weight)
                for task in project.tasks
            ) / total_weight
        else:
            progress = 0

        total_tasks = len(project.tasks)

        completed_tasks = sum(
            1
            for task in project.tasks
            if task.is_completed()
        )

        start = project.start_date
        deadline = project.deadline

        total_days = max(
            1,
            (deadline - start).days
        )

        elapsed_days = (
            today - start
        ).days

        time_percent = (
            elapsed_days / total_days
        ) * 100

        time_percent = max(
            0,
            min(100, time_percent)
        )

        if today < start:
            time_text = "Project has not started"
        elif today >= deadline:
            time_text = "Deadline reached"
        else:
            remaining_days = (
                deadline - today
            ).days

            time_text = (
                f"{remaining_days} day"
                f"{'' if remaining_days == 1 else 's'} remaining"
            )

        return {
            "progress": max(0, min(100, progress)),
            "time_percent": time_percent,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "time_text": time_text
        }

    def _deadline_text(self, project, today):
        if project.deadline < today:
            days = (today - project.deadline).days

            return (
                f"{project.deadline.isoformat()}  •  "
                f"{days} day{'s' if days != 1 else ''} overdue"
            )

        if project.deadline == today:
            return "TODAY"

        days = (project.deadline - today).days

        return (
            f"{project.deadline.isoformat()}  •  "
            f"{days} day{'s' if days != 1 else ''} left"
        )

    def _health_text(self, metrics):
        progress = metrics["progress"]
        time = metrics["time_percent"]

        if progress >= 100:
            return "✓ COMPLETED"

        if time >= 100 and progress < 100:
            return "⚠ OVERDUE"

        if time - progress >= 20:
            return "⚠ BEHIND"

        if progress >= time:
            return "✓ ON TRACK"

        return "• WATCH"

    def _health_color(self, metrics):
        progress = metrics["progress"]
        time = metrics["time_percent"]

        if progress >= 100:
            return SUCCESS_COLOR

        if time >= 100 and progress < 100:
            return DANGER_COLOR

        if time - progress >= 20:
            return DANGER_COLOR

        if progress >= time:
            return SUCCESS_COLOR

        return WARNING_COLOR

    # =========================================================
    # CLICK HANDLING
    # =========================================================

    def _bind_card_click(
        self,
        widget,
        callback,
        ignored_widgets=None
    ):
        ignored_widgets = ignored_widgets or set()

        def bind_recursive(current):
            if current in ignored_widgets:
                return

            if isinstance(
                current,
                (
                    ctk.CTkButton,
                    ctk.CTkEntry,
                    ctk.CTkSlider
                )
            ):
                return

            current.bind(
                "<Button-1>",
                lambda event: callback(),
                add="+"
            )

            for child in current.winfo_children():
                bind_recursive(child)

        bind_recursive(widget)