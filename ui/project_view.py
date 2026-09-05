import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import date, timedelta

from models.task import Task
from models.enums import TaskStatus

from services.calculator import Calculator
from services.predictor import Predictor


# ============================================================
# COLORS
# ============================================================

BG_COLOR = "#0A0E13"
CARD_COLOR = "#171E27"
CARD_DARK = "#121921"

TEXT_COLOR = "#F4F7FB"
MUTED_COLOR = "#97A3B3"

PRIMARY = "#6C63FF"
PRIMARY_HOVER = "#8078FF"

GREEN = "#22C55E"
GREEN_BG = "#173923"

ORANGE = "#F59E0B"
ORANGE_BG = "#44340F"

RED = "#EF4444"
RED_BG = "#441C20"

BORDER = "#2B3542"


class ProjectView(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        project,
        project_manager,
        storage,
        on_back=None,
        on_project_deleted=None,
        on_project_updated=None
    ):

        super().__init__(
            parent,
            fg_color=BG_COLOR
        )

        self.project = project
        self.manager = project_manager
        self.storage = storage

        self.on_back = on_back
        self.on_project_deleted = on_project_deleted
        self.on_project_updated = on_project_updated

        self.selected_task_id = None

        self.build_ui()

        self.refresh()

    # ========================================================
    # BUILD UI
    # ========================================================

    def build_ui(self):

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(25, 10)
        )

        back_button = ctk.CTkButton(
            header,
            text="←  Back",
            command=self.go_back,
            width=110,
            height=44,
            corner_radius=10,
            fg_color="#283342",
            hover_color="#374555",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        back_button.pack(
            side="left"
        )

        self.project_title = ctk.CTkLabel(
            header,
            text="",
            font=ctk.CTkFont(
                size=31,
                weight="bold"
            ),
            text_color=TEXT_COLOR
        )

        self.project_title.pack(
            side="left",
            padx=20
        )

        buttons = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        buttons.pack(
            side="right"
        )

        report_button = ctk.CTkButton(
            buttons,
            text="▣  Progress Report",
            command=self.create_report,
            width=175,
            height=44,
            corner_radius=10,
            fg_color="#283342",
            hover_color="#374555",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        report_button.pack(
            side="left",
            padx=4
        )

        edit_project_button = ctk.CTkButton(
            buttons,
            text="✎  Edit Project",
            command=self.edit_project,
            width=145,
            height=44,
            corner_radius=10,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        edit_project_button.pack(
            side="left",
            padx=4
        )

        delete_project_button = ctk.CTkButton(
            buttons,
            text="Delete Project",
            command=self.delete_project,
            width=145,
            height=44,
            corner_radius=10,
            fg_color=RED_BG,
            hover_color="#67262E",
            text_color="#FF9CA3",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        delete_project_button.pack(
            side="left",
            padx=(4, 0)
        )

        # ----------------------------------------------------
        # CONTENT
        # ----------------------------------------------------

        self.content = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        self.build_summary()

        self.build_prediction()

        self.build_tasks()

    # ========================================================
    # SUMMARY
    # ========================================================

    def build_summary(self):

        self.summary_card = ctk.CTkFrame(
            self.content,
            fg_color=CARD_COLOR,
            corner_radius=20
        )

        self.summary_card.pack(
            fill="x",
            padx=10,
            pady=10
        )

        # ----------------------------------------------------
        # Status line
        # ----------------------------------------------------

        self.status_line = ctk.CTkFrame(
            self.summary_card,
            height=9,
            corner_radius=8
        )

        self.status_line.pack(
            fill="x",
            padx=18,
            pady=(15, 0)
        )

        top = ctk.CTkFrame(
            self.summary_card,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=25,
            pady=(18, 5)
        )

        self.description_label = ctk.CTkLabel(
            top,
            text="",
            font=ctk.CTkFont(
                size=15
            ),
            text_color=MUTED_COLOR
        )

        self.description_label.pack(
            side="left"
        )

        self.status_badge = ctk.CTkLabel(
            top,
            text="",
            width=175,
            height=42,
            corner_radius=12,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        self.status_badge.pack(
            side="right"
        )

        # ----------------------------------------------------
        # PROJECT PROGRESS
        # ----------------------------------------------------

        project_progress_card = ctk.CTkFrame(
            self.summary_card,
            fg_color=CARD_DARK,
            corner_radius=16
        )

        project_progress_card.pack(
            fill="x",
            padx=25,
            pady=(15, 10)
        )

        project_title = ctk.CTkLabel(
            project_progress_card,
            text="PROJECT PROGRESS",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            text_color=MUTED_COLOR
        )

        project_title.pack(
            anchor="w",
            padx=20,
            pady=(16, 0)
        )

        self.project_progress_value = ctk.CTkLabel(
            project_progress_card,
            text="0%",
            font=ctk.CTkFont(
                size=62,
                weight="bold"
            ),
            text_color=TEXT_COLOR
        )

        self.project_progress_value.pack(
            anchor="w",
            padx=20
        )

        self.project_progress_bar = ctk.CTkProgressBar(
            project_progress_card,
            height=20,
            corner_radius=10,
            fg_color="#2A3440"
        )

        self.project_progress_bar.pack(
            fill="x",
            padx=20,
            pady=(3, 20)
        )

        # ----------------------------------------------------
        # TIME PROGRESS
        # ----------------------------------------------------

        self.time_card = ctk.CTkFrame(
            self.summary_card,
            fg_color=CARD_DARK,
            corner_radius=16
        )

        self.time_card.pack(
            fill="x",
            padx=25,
            pady=10
        )

        time_title_row = ctk.CTkFrame(
            self.time_card,
            fg_color="transparent"
        )

        time_title_row.pack(
            fill="x",
            padx=20,
            pady=(16, 0)
        )

        time_title = ctk.CTkLabel(
            time_title_row,
            text="TIME PROGRESS",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            text_color=MUTED_COLOR
        )

        time_title.pack(
            side="left"
        )

        time_help = ctk.CTkLabel(
            time_title_row,
            text="How much of the available project time has passed",
            font=ctk.CTkFont(
                size=12
            ),
            text_color=MUTED_COLOR
        )

        time_help.pack(
            side="right"
        )

        self.time_progress_value = ctk.CTkLabel(
            self.time_card,
            text="0%",
            font=ctk.CTkFont(
                size=52,
                weight="bold"
            ),
            text_color=GREEN
        )

        self.time_progress_value.pack(
            anchor="w",
            padx=20
        )

        self.time_progress_bar = ctk.CTkProgressBar(
            self.time_card,
            height=18,
            corner_radius=9,
            fg_color="#2A3440"
        )

        self.time_progress_bar.pack(
            fill="x",
            padx=20,
            pady=(3, 7)
        )

        self.time_message = ctk.CTkLabel(
            self.time_card,
            text="",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=MUTED_COLOR
        )

        self.time_message.pack(
            anchor="w",
            padx=20,
            pady=(0, 18)
        )

        # ----------------------------------------------------
        # METRICS
        # ----------------------------------------------------

        metrics = ctk.CTkFrame(
            self.summary_card,
            fg_color="transparent"
        )

        metrics.pack(
            fill="x",
            padx=18,
            pady=(5, 20)
        )

        for i in range(4):
            metrics.grid_columnconfigure(
                i,
                weight=1
            )

        self.elapsed_value = self.create_metric(
            metrics,
            0,
            "ELAPSED TIME",
            "Days passed since project start."
        )

        self.remaining_value = self.create_metric(
            metrics,
            1,
            "TIME REMAINING",
            "Days until the project deadline."
        )

        self.schedule_value = self.create_metric(
            metrics,
            2,
            "SCHEDULE GAP",
            "Time Progress minus Project Progress."
        )

        self.disaster_value = self.create_metric(
            metrics,
            3,
            "DISASTER INDEX",
            "Overall project risk from 0 to 100."
        )

        self.weight_value = self.create_metric(
            metrics,
            0,
            "TOTAL WEIGHT",
            "Total weight of all project tasks."
        )

        # Reorganize last metric into second row.
        # This keeps the cards readable on smaller screens.
        self.weight_value.master.grid(
            row=1,
            column=0,
            padx=6,
            pady=(8, 0),
            sticky="nsew"
        )

        # ----------------------------------------------------
        # Deadline information
        # ----------------------------------------------------

        deadline_info = ctk.CTkFrame(
            self.summary_card,
            fg_color="#131A22",
            corner_radius=12
        )

        deadline_info.pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )

        self.deadline_label = ctk.CTkLabel(
            deadline_info,
            text="",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color=TEXT_COLOR
        )

        self.deadline_label.pack(
            anchor="w",
            padx=18,
            pady=12
        )

    def create_metric(
        self,
        parent,
        column,
        title,
        explanation
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color=CARD_DARK,
            corner_radius=14
        )

        card.grid(
            row=0,
            column=column,
            padx=6,
            sticky="nsew"
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            ),
            text_color=MUTED_COLOR
        )

        title_label.pack(
            anchor="w",
            padx=13,
            pady=(12, 0)
        )

        value_label = ctk.CTkLabel(
            card,
            text="-",
            font=ctk.CTkFont(
                size=23,
                weight="bold"
            ),
            text_color=TEXT_COLOR
        )

        value_label.pack(
            anchor="w",
            padx=13,
            pady=(2, 0)
        )

        explanation_label = ctk.CTkLabel(
            card,
            text=explanation,
            font=ctk.CTkFont(
                size=10
            ),
            text_color=MUTED_COLOR,
            wraplength=220,
            justify="left"
        )

        explanation_label.pack(
            anchor="w",
            padx=13,
            pady=(3, 12)
        )

        return value_label

    # ========================================================
    # PREDICTION
    # ========================================================

    def build_prediction(self):

        card = ctk.CTkFrame(
            self.content,
            fg_color=CARD_COLOR,
            corner_radius=20
        )

        card.pack(
            fill="x",
            padx=10,
            pady=10
        )

        title = ctk.CTkLabel(
            card,
            text="Completion Prediction",
            font=ctk.CTkFont(
                size=23,
                weight="bold"
            ),
            text_color=TEXT_COLOR
        )

        title.pack(
            anchor="w",
            padx=23,
            pady=(18, 2)
        )

        subtitle = ctk.CTkLabel(
            card,
            text=(
                "Uses the project's average daily progress "
                "to estimate completion."
            ),
            font=ctk.CTkFont(
                size=13
            ),
            text_color=MUTED_COLOR
        )

        subtitle.pack(
            anchor="w",
            padx=23
        )

        self.prediction_label = ctk.CTkLabel(
            card,
            text="",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            ),
            text_color=TEXT_COLOR
        )

        self.prediction_label.pack(
            anchor="w",
            padx=23,
            pady=(15, 0)
        )

        self.prediction_details = ctk.CTkLabel(
            card,
            text="",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        self.prediction_details.pack(
            anchor="w",
            padx=23,
            pady=(3, 18)
        )

    # ========================================================
    # TASKS
    # ========================================================

    def build_tasks(self):

        header = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=10,
            pady=(15, 5)
        )

        title = ctk.CTkLabel(
            header,
            text="Tasks",
            font=ctk.CTkFont(
                size=27,
                weight="bold"
            ),
            text_color=TEXT_COLOR
        )

        title.pack(
            side="left"
        )

        self.selection_label = ctk.CTkLabel(
            header,
            text="No task selected",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color=MUTED_COLOR
        )

        self.selection_label.pack(
            side="left",
            padx=20
        )

        buttons = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        buttons.pack(
            side="right"
        )

        add_button = ctk.CTkButton(
            buttons,
            text="+ Add Task",
            command=self.add_task,
            width=125,
            height=43,
            corner_radius=10,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        add_button.pack(
            side="left",
            padx=4
        )

        edit_button = ctk.CTkButton(
            buttons,
            text="Edit Task",
            command=self.edit_task,
            width=115,
            height=43,
            corner_radius=10,
            fg_color="#283342",
            hover_color="#374555",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        edit_button.pack(
            side="left",
            padx=4
        )

        delete_button = ctk.CTkButton(
            buttons,
            text="Delete Task",
            command=self.delete_task,
            width=120,
            height=43,
            corner_radius=10,
            fg_color=RED_BG,
            hover_color="#67262E",
            text_color="#FF9CA3",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        delete_button.pack(
            side="left",
            padx=(4, 0)
        )

        # ----------------------------------------------------
        # QUICK PROGRESS EDITOR
        # ----------------------------------------------------

        self.progress_editor = ctk.CTkFrame(
            self.content,
            fg_color=CARD_COLOR,
            corner_radius=16
        )

        self.progress_editor.pack(
            fill="x",
            padx=10,
            pady=(5, 8)
        )

        editor_title = ctk.CTkLabel(
            self.progress_editor,
            text="Selected Task Progress",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            ),
            text_color=TEXT_COLOR
        )

        editor_title.pack(
            side="left",
            padx=(18, 10),
            pady=16
        )

        self.progress_input = ctk.CTkEntry(
            self.progress_editor,
            width=100,
            height=42,
            corner_radius=10,
            fg_color=CARD_DARK,
            border_color=BORDER,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        self.progress_input.pack(
            side="left",
            padx=5
        )

        percent_label = ctk.CTkLabel(
            self.progress_editor,
            text="%",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            ),
            text_color=MUTED_COLOR
        )

        percent_label.pack(
            side="left",
            padx=(0, 12)
        )

        update_button = ctk.CTkButton(
            self.progress_editor,
            text="Update Progress",
            command=self.update_selected_progress,
            width=160,
            height=42,
            corner_radius=10,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        update_button.pack(
            side="left"
        )

        help_label = ctk.CTkLabel(
            self.progress_editor,
            text=(
                "Select a task below, enter 0–100, "
                "then press Update Progress."
            ),
            font=ctk.CTkFont(
                size=12
            ),
            text_color=MUTED_COLOR
        )

        help_label.pack(
            side="left",
            padx=15
        )

        # ----------------------------------------------------
        # Task cards
        # ----------------------------------------------------

        self.tasks_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        self.tasks_frame.pack(
            fill="x",
            padx=10,
            pady=(5, 20)
        )

    # ========================================================
    # COLORS
    # ========================================================

    def get_project_colors(self):

        status = Calculator.get_project_status(
            self.project
        )

        disaster = Calculator.calculate_disaster_index(
            self.project
        )

        if status == "completed":
            return GREEN, GREEN_BG

        if status == "overdue":
            return RED, RED_BG

        if status == "not_started":
            return ORANGE, ORANGE_BG

        if disaster > 70:
            return RED, RED_BG

        if disaster > 30:
            return ORANGE, ORANGE_BG

        return GREEN, GREEN_BG

    def get_time_color(self, time_progress):

        # Project is completed.
        if Calculator.calculate_project_progress(
            self.project
        ) >= 100:

            return GREEN

        # 0 - 40% of available time used:
        # A lot of time remains.
        if time_progress <= 40:
            return GREEN

        # 40 - 75%:
        # Middle stage.
        if time_progress <= 75:
            return ORANGE

        # More than 75% of the available time is used:
        # Very close to deadline.
        return RED

    # ========================================================
    # REFRESH
    # ========================================================

    def refresh(self):

        self.update_summary()

        self.update_prediction()

        self.refresh_tasks()

    # ========================================================
    # UPDATE SUMMARY
    # ========================================================

    def update_summary(self):

        progress = Calculator.calculate_project_progress(
            self.project
        )

        time_progress = Calculator.calculate_time_progress(
            self.project
        )

        elapsed_days = Calculator.calculate_time_elapsed(
            self.project
        )

        total_days = Calculator.calculate_total_project_days(
            self.project
        )

        remaining_days = Calculator.calculate_time_remaining(
            self.project
        )

        schedule_gap = Calculator.calculate_schedule_gap(
            self.project
        )

        disaster = Calculator.calculate_disaster_index(
            self.project
        )

        total_weight = self.get_total_weight()

        project_color, project_background = (
            self.get_project_colors()
        )

        time_color = self.get_time_color(
            time_progress
        )

        self.project_title.configure(
            text=self.project.name
        )

        description = self.project.description.strip()

        if not description:
            description = "No project description"

        self.description_label.configure(
            text=description
        )

        # ----------------------------------------------------
        # Project status
        # ----------------------------------------------------

        self.status_line.configure(
            fg_color=project_color
        )

        self.status_badge.configure(
            text=self.get_status_text(),
            fg_color=project_background,
            text_color=project_color
        )

        # ----------------------------------------------------
        # Project progress
        # ----------------------------------------------------

        self.project_progress_value.configure(
            text=f"{progress:.0f}%",
            text_color=project_color
        )

        self.project_progress_bar.configure(
            progress_color=project_color
        )

        self.project_progress_bar.set(
            progress / 100
        )

        # ----------------------------------------------------
        # Time progress
        # ----------------------------------------------------

        self.time_progress_value.configure(
            text=f"{time_progress:.0f}%",
            text_color=time_color
        )

        self.time_progress_bar.configure(
            progress_color=time_color
        )

        self.time_progress_bar.set(
            time_progress / 100
        )

        if progress >= 100:

            time_message = (
                "Project completed."
            )

        elif time_progress <= 40:

            time_message = (
                "A lot of project time is still available."
            )

        elif time_progress <= 75:

            time_message = (
                "Project is in the middle of its available time."
            )

        else:

            time_message = (
                "Deadline is getting close. "
                "Finish remaining work soon."
            )

        self.time_message.configure(
            text=time_message,
            text_color=time_color
        )

        # ----------------------------------------------------
        # Metrics
        # ----------------------------------------------------

        self.elapsed_value.configure(
            text=f"{elapsed_days} day(s)"
        )

        if remaining_days < 0:

            self.remaining_value.configure(
                text=f"{abs(remaining_days)} day(s) overdue",
                text_color=RED
            )

        elif progress >= 100:

            self.remaining_value.configure(
                text="Finished",
                text_color=GREEN
            )

        else:

            self.remaining_value.configure(
                text=f"{remaining_days} day(s)",
                text_color=time_color
            )

        if schedule_gap > 0:

            schedule_color = (
                RED
                if schedule_gap > 15
                else ORANGE
            )

            self.schedule_value.configure(
                text=f"+{schedule_gap:.1f}%",
                text_color=schedule_color
            )

        else:

            self.schedule_value.configure(
                text=f"{schedule_gap:.1f}%",
                text_color=GREEN
            )

        self.disaster_value.configure(
            text=f"{disaster:.0f}",
            text_color=project_color
        )

        self.weight_value.configure(
            text=f"{total_weight:g}"
        )

        # ----------------------------------------------------
        # Deadline
        # ----------------------------------------------------

        self.deadline_label.configure(
            text=(
                f"Deadline: {self.project.deadline}   •   "
                f"Total project duration: {total_days} day(s)"
            )
        )

    # ========================================================
    # STATUS TEXT
    # ========================================================

    def get_status_text(self):

        status = Calculator.get_project_status(
            self.project
        )

        mapping = {
            "not_started": "NOT STARTED",
            "in_progress": "IN PROGRESS",
            "completed": "COMPLETED",
            "overdue": "OVERDUE"
        }

        return mapping.get(
            status,
            status.upper()
        )

    # ========================================================
    # PREDICTION
    # ========================================================

    def update_prediction(self):

        summary = Predictor.get_prediction_summary(
            self.project
        )

        predicted_date = summary[
            "predicted_date"
        ]

        expected_delay = summary[
            "expected_delay"
        ]

        progress_rate = summary[
            "progress_rate"
        ]

        if predicted_date is None:

            self.prediction_label.configure(
                text="Prediction is not available"
            )

            self.prediction_details.configure(
                text="More project progress is needed.",
                text_color=MUTED_COLOR
            )

            return

        self.prediction_label.configure(
            text=(
                f"Predicted completion: "
                f"{predicted_date.isoformat()}"
            )
        )

        if expected_delay is None:

            detail = "Expected delay cannot be calculated."

            self.prediction_details.configure(
                text=detail,
                text_color=MUTED_COLOR
            )

        elif expected_delay > 0:

            self.prediction_details.configure(
                text=(
                    f"Expected delay: "
                    f"{expected_delay} day(s) late"
                ),
                text_color=RED
            )

        elif expected_delay < 0:

            self.prediction_details.configure(
                text=(
                    f"Expected: "
                    f"{abs(expected_delay)} day(s) early"
                ),
                text_color=GREEN
            )

        else:

            self.prediction_details.configure(
                text="Expected to finish exactly on deadline.",
                text_color=ORANGE
            )

        if progress_rate is not None:

            current_text = self.prediction_details.cget(
                "text"
            )

            self.prediction_details.configure(
                text=(
                    current_text
                    + f"   •   "
                    f"Average: {progress_rate:.2f}% / day"
                )
            )

    # ========================================================
    # TOTAL WEIGHT
    # ========================================================

    def get_total_weight(self):

        return sum(
            task.weight
            for task in self.project.tasks
        )

    # ========================================================
    # TASK LIST
    # ========================================================

    def refresh_tasks(self):

        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        if not self.project.tasks:

            empty = ctk.CTkFrame(
                self.tasks_frame,
                fg_color=CARD_COLOR,
                corner_radius=16
            )

            empty.pack(
                fill="x",
                pady=10
            )

            label = ctk.CTkLabel(
                empty,
                text="No tasks yet. Add your first task.",
                font=ctk.CTkFont(
                    size=17
                ),
                text_color=MUTED_COLOR
            )

            label.pack(
                pady=40
            )

            self.selection_label.configure(
                text="No task selected",
                text_color=MUTED_COLOR
            )

            self.progress_input.delete(
                0,
                "end"
            )

            return

        # Selected task must still exist.
        if self.selected_task_id is not None:

            if self.project.get_task(
                self.selected_task_id
            ) is None:

                self.selected_task_id = None

        for task in self.project.tasks:

            self.create_task_card(
                task
            )

        selected_task = self.get_selected_task()

        if selected_task is None:

            self.selection_label.configure(
                text="No task selected",
                text_color=MUTED_COLOR
            )

            self.progress_input.delete(
                0,
                "end"
            )

        else:

            self.selection_label.configure(
                text=f"Selected: {selected_task.title}",
                text_color=PRIMARY
            )

            self.progress_input.delete(
                0,
                "end"
            )

            self.progress_input.insert(
                0,
                str(int(selected_task.progress_percent))
            )

    # ========================================================
    # TASK CARD
    # ========================================================

    def create_task_card(
        self,
        task
    ):

        selected = (
            task.id == self.selected_task_id
        )

        if selected:

            border_color = PRIMARY
            border_width = 3

        else:

            border_color = BORDER
            border_width = 1

        if task.status == TaskStatus.COMPLETED:

            task_color = GREEN

        elif task.status in (
            TaskStatus.IN_PROGRESS,
            TaskStatus.REOPENED
        ):

            task_color = ORANGE

        else:

            task_color = MUTED_COLOR

        card = ctk.CTkFrame(
            self.tasks_frame,
            fg_color=CARD_COLOR,
            corner_radius=16,
            border_width=border_width,
            border_color=border_color
        )

        card.pack(
            fill="x",
            pady=7
        )

        # ----------------------------------------------------
        # LEFT
        # ----------------------------------------------------

        left = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        left.pack(
            side="left",
            fill="x",
            expand=True,
            padx=20,
            pady=15
        )

        title_row = ctk.CTkFrame(
            left,
            fg_color="transparent"
        )

        title_row.pack(
            fill="x"
        )

        title = ctk.CTkLabel(
            title_row,
            text=task.title,
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            ),
            text_color=TEXT_COLOR
        )

        title.pack(
            side="left"
        )

        status_map = {
            TaskStatus.TODO: "TODO",
            TaskStatus.IN_PROGRESS: "IN PROGRESS",
            TaskStatus.COMPLETED: "COMPLETED",
            TaskStatus.REOPENED: "REOPENED"
        }

        status = ctk.CTkLabel(
            title_row,
            text=status_map.get(
                task.status,
                task.status.value
            ),
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color=task_color
        )

        status.pack(
            side="left",
            padx=14
        )

        info = ctk.CTkLabel(
            left,
            text=(
                f"Weight: {task.weight:g}"
                f"   •   "
                f"Deadline: "
                f"{task.deadline if task.deadline else 'No deadline'}"
            ),
            font=ctk.CTkFont(
                size=13
            ),
            text_color=MUTED_COLOR
        )

        info.pack(
            anchor="w",
            pady=(5, 0)
        )

        task_progress_bar = ctk.CTkProgressBar(
            left,
            height=11,
            corner_radius=6,
            fg_color="#2A3440",
            progress_color=task_color
        )

        task_progress_bar.pack(
            fill="x",
            pady=(10, 4)
        )

        task_progress_bar.set(
            task.progress_percent / 100
        )

        progress_label = ctk.CTkLabel(
            left,
            text=f"{task.progress_percent:.0f}% complete",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            ),
            text_color=task_color
        )

        progress_label.pack(
            anchor="w"
        )

        # ----------------------------------------------------
        # RIGHT
        # ----------------------------------------------------

        right = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        right.pack(
            side="right",
            padx=18,
            pady=15
        )

        if selected:

            select_text = "✓  SELECTED"
            select_color = PRIMARY
            hover_color = PRIMARY_HOVER

        else:

            select_text = "SELECT"
            select_color = "#283342"
            hover_color = "#374555"

        select_button = ctk.CTkButton(
            right,
            text=select_text,
            command=lambda task_id=task.id:
            self.select_task(task_id),
            width=145,
            height=45,
            corner_radius=10,
            fg_color=select_color,
            hover_color=hover_color,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        select_button.pack(
            pady=(0, 8)
        )

        actions = ctk.CTkFrame(
            right,
            fg_color="transparent"
        )

        actions.pack()

        start_button = ctk.CTkButton(
            actions,
            text="Start",
            command=lambda task_id=task.id:
            self.start_task(task_id),
            width=65,
            height=36,
            corner_radius=9,
            fg_color="#283342",
            hover_color="#374555",
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        )

        start_button.pack(
            side="left",
            padx=2
        )

        done_button = ctk.CTkButton(
            actions,
            text="Done",
            command=lambda task_id=task.id:
            self.complete_task(task_id),
            width=65,
            height=36,
            corner_radius=9,
            fg_color=GREEN_BG,
            hover_color="#245C38",
            text_color=GREEN,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        )

        done_button.pack(
            side="left",
            padx=2
        )

        if task.status == TaskStatus.COMPLETED:

            reopen_button = ctk.CTkButton(
                actions,
                text="Reopen",
                command=lambda task_id=task.id:
                self.reopen_task(task_id),
                width=75,
                height=36,
                corner_radius=9,
                fg_color=ORANGE_BG,
                hover_color="#5A4212",
                text_color=ORANGE,
                font=ctk.CTkFont(
                    size=10,
                    weight="bold"
                )
            )

            reopen_button.pack(
                side="left",
                padx=2
            )

    # ========================================================
    # SELECT TASK
    # ========================================================

    def select_task(
        self,
        task_id
    ):

        task = self.project.get_task(
            task_id
        )

        if task is None:

            messagebox.showerror(
                "Error",
                "Task was not found."
            )

            return

        if self.selected_task_id == task_id:

            self.selected_task_id = None

        else:

            self.selected_task_id = task_id

        self.refresh_tasks()

    def get_selected_task(self):

        if self.selected_task_id is None:
            return None

        return self.project.get_task(
            self.selected_task_id
        )

    def require_selected_task(self):

        task = self.get_selected_task()

        if task is None:

            messagebox.showwarning(
                "No Task Selected",
                "Please select a task first.\n\n"
                "Click SELECT on the task you want to edit."
            )

            return None

        return task

    # ========================================================
    # QUICK PROGRESS UPDATE
    # ========================================================

    def update_selected_progress(self):

        task = self.require_selected_task()

        if task is None:
            return

        value_text = self.progress_input.get().strip()

        try:

            value = float(
                value_text
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Progress",
                "Progress must be a number between 0 and 100."
            )

            return

        if value < 0 or value > 100:

            messagebox.showerror(
                "Invalid Progress",
                "Progress must be between 0 and 100."
            )

            return

        task.update_progress(
            value
        )

        if self.save_changes():

            self.refresh()

    # ========================================================
    # START TASK
    # ========================================================

    def start_task(
        self,
        task_id
    ):

        task = self.project.get_task(
            task_id
        )

        if task is None:
            return

        task.start()

        if self.save_changes():
            self.refresh()

    # ========================================================
    # COMPLETE TASK
    # ========================================================

    def complete_task(
        self,
        task_id
    ):

        task = self.project.get_task(
            task_id
        )

        if task is None:
            return

        task.complete()

        if self.save_changes():
            self.refresh()

    # ========================================================
    # REOPEN TASK
    # ========================================================

    def reopen_task(
        self,
        task_id
    ):

        task = self.project.get_task(
            task_id
        )

        if task is None:
            return

        task.reopen()

        if self.save_changes():
            self.refresh()

    # ========================================================
    # ADD TASK
    # ========================================================

    def add_task(self):

        dialog = ctk.CTkToplevel(
            self
        )

        dialog.title(
            "Add Task"
        )

        dialog.geometry(
            "650x760"
        )

        dialog.resizable(
            False,
            False
        )

        dialog.configure(
            fg_color=BG_COLOR
        )

        dialog.grab_set()

        heading = ctk.CTkLabel(
            dialog,
            text="Add New Task",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            text_color=TEXT_COLOR
        )

        heading.pack(
            padx=35,
            pady=(30, 25),
            anchor="w"
        )

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        self.make_label(
            dialog,
            "Task Title"
        )

        title_entry = ctk.CTkEntry(
            dialog,
            height=48,
            corner_radius=10,
            fg_color=CARD_COLOR,
            border_color=BORDER,
            font=ctk.CTkFont(
                size=15
            )
        )

        title_entry.pack(
            fill="x",
            padx=35,
            pady=(6, 15)
        )

        # ----------------------------------------------------
        # WEIGHT
        # ----------------------------------------------------

        self.make_label(
            dialog,
            "Task Weight"
        )

        weight_entry = ctk.CTkEntry(
            dialog,
            height=48,
            corner_radius=10,
            fg_color=CARD_COLOR,
            border_color=BORDER,
            font=ctk.CTkFont(
                size=15
            )
        )

        weight_entry.pack(
            fill="x",
            padx=35,
            pady=(6, 15)
        )

        # ----------------------------------------------------
        # DEADLINE
        # ----------------------------------------------------

        self.make_label(
            dialog,
            "Deadline"
        )

        deadline_mode = ctk.StringVar(
            value="days"
        )

        mode_frame = ctk.CTkFrame(
            dialog,
            fg_color="transparent"
        )

        mode_frame.pack(
            fill="x",
            padx=35
        )

        days_radio = ctk.CTkRadioButton(
            mode_frame,
            text="Days remaining",
            variable=deadline_mode,
            value="days",
            font=ctk.CTkFont(
                size=13
            )
        )

        days_radio.pack(
            side="left",
            padx=(0, 25)
        )

        date_radio = ctk.CTkRadioButton(
            mode_frame,
            text="Exact date",
            variable=deadline_mode,
            value="date",
            font=ctk.CTkFont(
                size=13
            )
        )

        date_radio.pack(
            side="left"
        )

        deadline_entry = ctk.CTkEntry(
            dialog,
            height=48,
            corner_radius=10,
            fg_color=CARD_COLOR,
            border_color=BORDER,
            font=ctk.CTkFont(
                size=15
            )
        )

        deadline_entry.pack(
            fill="x",
            padx=35,
            pady=(6, 6)
        )

        deadline_entry.insert(
            0,
            "7"
        )

        deadline_hint = ctk.CTkLabel(
            dialog,
            text="Example: 7 = deadline is 7 days from today.",
            font=ctk.CTkFont(
                size=12
            ),
            text_color=MUTED_COLOR
        )

        deadline_hint.pack(
            padx=35,
            anchor="w",
            pady=(0, 15)
        )

        def switch_deadline_mode():

            deadline_entry.delete(
                0,
                "end"
            )

            if deadline_mode.get() == "days":

                deadline_entry.insert(
                    0,
                    "7"
                )

                deadline_hint.configure(
                    text=(
                        "Enter the number of days from today."
                    )
                )

            else:

                deadline_entry.insert(
                    0,
                    date.today().isoformat()
                )

                deadline_hint.configure(
                    text=(
                        "Enter exact date: YYYY-MM-DD"
                    )
                )

        days_radio.configure(
            command=switch_deadline_mode
        )

        date_radio.configure(
            command=switch_deadline_mode
        )

        # ----------------------------------------------------
        # PROGRESS
        # ----------------------------------------------------

        self.make_label(
            dialog,
            "Initial Progress"
        )

        progress_frame = ctk.CTkFrame(
            dialog,
            fg_color="transparent"
        )

        progress_frame.pack(
            fill="x",
            padx=35,
            pady=(5, 20)
        )

        progress_input = ctk.CTkEntry(
            progress_frame,
            width=100,
            height=45,
            corner_radius=10,
            fg_color=CARD_DARK,
            border_color=BORDER,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        progress_input.pack(
            side="left"
        )

        progress_input.insert(
            0,
            "0"
        )

        ctk.CTkLabel(
            progress_frame,
            text="%",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            ),
            text_color=MUTED_COLOR
        ).pack(
            side="left",
            padx=7
        )

        progress_hint = ctk.CTkLabel(
            progress_frame,
            text="Enter any value from 0 to 100.",
            font=ctk.CTkFont(
                size=12
            ),
            text_color=MUTED_COLOR
        )

        progress_hint.pack(
            side="left",
            padx=10
        )

        # ----------------------------------------------------
        # CREATE TASK
        # ----------------------------------------------------

        def create():

            title = title_entry.get().strip()
            weight_text = weight_entry.get().strip()
            deadline_text = deadline_entry.get().strip()
            progress_text = progress_input.get().strip()

            if not title:

                messagebox.showwarning(
                    "Missing Information",
                    "Task title is required."
                )

                return

            try:

                weight = float(
                    weight_text
                )

                progress = float(
                    progress_text
                )

                if weight <= 0:

                    raise ValueError(
                        "Task weight must be greater than zero."
                    )

                if progress < 0 or progress > 100:

                    raise ValueError(
                        "Progress must be between 0 and 100."
                    )

                deadline = None

                if deadline_text:

                    if deadline_mode.get() == "days":

                        days = int(
                            deadline_text
                        )

                        if days < 0:

                            raise ValueError(
                                "Days remaining cannot be negative."
                            )

                        deadline = (
                            date.today()
                            + timedelta(days=days)
                        )

                    else:

                        deadline = date.fromisoformat(
                            deadline_text
                        )

                task = Task(
                    title=title,
                    weight=weight,
                    progress_percent=0,
                    deadline=deadline
                )

                self.project.add_task(
                    task
                )

                # Use Task's own state logic.
                task.update_progress(
                    progress
                )

                if self.save_changes():

                    dialog.destroy()

                    self.selected_task_id = task.id

                    self.refresh()

            except (
                ValueError,
                TypeError
            ) as error:

                messagebox.showerror(
                    "Invalid Data",
                    str(error)
                )

        add_button = ctk.CTkButton(
            dialog,
            text="Add Task",
            command=create,
            width=210,
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
            pady=15
        )

    # ========================================================
    # EDIT TASK
    # ========================================================

    def edit_task(self):

        task = self.require_selected_task()

        if task is None:
            return

        dialog = ctk.CTkToplevel(
            self
        )

        dialog.title(
            "Edit Task"
        )

        dialog.geometry(
            "670x850"
        )

        dialog.resizable(
            False,
            False
        )

        dialog.configure(
            fg_color=BG_COLOR
        )

        dialog.grab_set()

        heading = ctk.CTkLabel(
            dialog,
            text="Edit Task",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            text_color=TEXT_COLOR
        )

        heading.pack(
            padx=35,
            pady=(30, 25),
            anchor="w"
        )

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        self.make_label(
            dialog,
            "Task Title"
        )

        title_entry = ctk.CTkEntry(
            dialog,
            height=48,
            corner_radius=10,
            fg_color=CARD_COLOR,
            border_color=BORDER,
            font=ctk.CTkFont(
                size=15
            )
        )

        title_entry.pack(
            fill="x",
            padx=35,
            pady=(6, 15)
        )

        title_entry.insert(
            0,
            task.title
        )

        # ----------------------------------------------------
        # WEIGHT
        # ----------------------------------------------------

        self.make_label(
            dialog,
            "Task Weight"
        )

        weight_entry = ctk.CTkEntry(
            dialog,
            height=48,
            corner_radius=10,
            fg_color=CARD_COLOR,
            border_color=BORDER,
            font=ctk.CTkFont(
                size=15
            )
        )

        weight_entry.pack(
            fill="x",
            padx=35,
            pady=(6, 15)
        )

        weight_entry.insert(
            0,
            str(task.weight)
        )

        # ----------------------------------------------------
        # DEADLINE
        # ----------------------------------------------------

        self.make_label(
            dialog,
            "Deadline"
        )

        deadline_mode = ctk.StringVar(
            value="days"
        )

        mode_frame = ctk.CTkFrame(
            dialog,
            fg_color="transparent"
        )

        mode_frame.pack(
            fill="x",
            padx=35
        )

        days_radio = ctk.CTkRadioButton(
            mode_frame,
            text="Days remaining",
            variable=deadline_mode,
            value="days",
            font=ctk.CTkFont(
                size=13
            )
        )

        days_radio.pack(
            side="left",
            padx=(0, 25)
        )

        date_radio = ctk.CTkRadioButton(
            mode_frame,
            text="Exact date",
            variable=deadline_mode,
            value="date",
            font=ctk.CTkFont(
                size=13
            )
        )

        date_radio.pack(
            side="left"
        )

        deadline_entry = ctk.CTkEntry(
            dialog,
            height=48,
            corner_radius=10,
            fg_color=CARD_COLOR,
            border_color=BORDER,
            font=ctk.CTkFont(
                size=15
            )
        )

        deadline_entry.pack(
            fill="x",
            padx=35,
            pady=(6, 6)
        )

        if task.deadline:

            current_days = (
                task.deadline - date.today()
            ).days

            deadline_entry.insert(
                0,
                str(max(current_days, 0))
            )

        deadline_hint = ctk.CTkLabel(
            dialog,
            text="",
            font=ctk.CTkFont(
                size=12
            ),
            text_color=MUTED_COLOR
        )

        deadline_hint.pack(
            padx=35,
            anchor="w",
            pady=(0, 20)
        )

        if task.deadline:

            deadline_hint.configure(
                text=(
                    f"Current deadline: {task.deadline}"
                )
            )

        else:

            deadline_hint.configure(
                text="This task currently has no deadline."
            )

        def switch_deadline_mode():

            deadline_entry.delete(
                0,
                "end"
            )

            if deadline_mode.get() == "days":

                current_days = 0

                if task.deadline:

                    current_days = (
                        task.deadline - date.today()
                    ).days

                deadline_entry.insert(
                    0,
                    str(max(current_days, 0))
                )

                deadline_hint.configure(
                    text="Enter number of days from today."
                )

            else:

                if task.deadline:

                    value = task.deadline.isoformat()

                else:

                    value = date.today().isoformat()

                deadline_entry.insert(
                    0,
                    value
                )

                deadline_hint.configure(
                    text="Enter exact date: YYYY-MM-DD"
                )

        days_radio.configure(
            command=switch_deadline_mode
        )

        date_radio.configure(
            command=switch_deadline_mode
        )

        # ----------------------------------------------------
        # PROGRESS
        # ----------------------------------------------------

        self.make_label(
            dialog,
            "Task Progress"
        )

        progress_row = ctk.CTkFrame(
            dialog,
            fg_color="transparent"
        )

        progress_row.pack(
            fill="x",
            padx=35,
            pady=(5, 10)
        )

        progress_input = ctk.CTkEntry(
            progress_row,
            width=105,
            height=45,
            corner_radius=10,
            fg_color=CARD_DARK,
            border_color=BORDER,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        progress_input.pack(
            side="left"
        )

        progress_input.insert(
            0,
            str(int(task.progress_percent))
        )

        ctk.CTkLabel(
            progress_row,
            text="%",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            ),
            text_color=MUTED_COLOR
        ).pack(
            side="left",
            padx=7
        )

        progress_value = ctk.CTkLabel(
            progress_row,
            text=f"{task.progress_percent:.0f}%",
            font=ctk.CTkFont(
                size=23,
                weight="bold"
            ),
            text_color=PRIMARY
        )

        progress_value.pack(
            side="right"
        )

        slider = ctk.CTkSlider(
            dialog,
            from_=0,
            to=100,
            width=540,
            height=23,
            button_length=30
        )

        slider.set(
            task.progress_percent
        )

        slider.pack(
            padx=35,
            pady=(0, 30)
        )

        def slider_changed(value):

            number = float(
                value
            )

            progress_value.configure(
                text=f"{number:.0f}%"
            )

            progress_input.delete(
                0,
                "end"
            )

            progress_input.insert(
                0,
                str(int(number))
            )

        slider.configure(
            command=slider_changed
        )

        def input_changed(event=None):

            text = progress_input.get().strip()

            try:

                value = float(
                    text
                )

                if 0 <= value <= 100:

                    slider.set(
                        value
                    )

                    progress_value.configure(
                        text=f"{value:.0f}%"
                    )

            except ValueError:

                pass

        progress_input.bind(
            "<KeyRelease>",
            input_changed
        )

        # ----------------------------------------------------
        # SAVE
        # ----------------------------------------------------

        def save():

            new_title = title_entry.get().strip()
            weight_text = weight_entry.get().strip()
            deadline_text = deadline_entry.get().strip()
            progress_text = progress_input.get().strip()

            if not new_title:

                messagebox.showwarning(
                    "Missing Information",
                    "Task title cannot be empty."
                )

                return

            try:

                new_weight = float(
                    weight_text
                )

                new_progress = float(
                    progress_text
                )

                if new_weight <= 0:

                    raise ValueError(
                        "Task weight must be greater than zero."
                    )

                if new_progress < 0 or new_progress > 100:

                    raise ValueError(
                        "Progress must be between 0 and 100."
                    )

                new_deadline = None

                if deadline_text:

                    if deadline_mode.get() == "days":

                        days = int(
                            deadline_text
                        )

                        if days < 0:

                            raise ValueError(
                                "Days remaining cannot be negative."
                            )

                        new_deadline = (
                            date.today()
                            + timedelta(days=days)
                        )

                    else:

                        new_deadline = date.fromisoformat(
                            deadline_text
                        )

                self.project.update_task(
                    task.id,
                    new_title=new_title,
                    new_weight=new_weight,
                    new_deadline=new_deadline,
                    new_progress=new_progress
                )

                if self.save_changes():

                    dialog.destroy()

                    self.refresh()

            except (
                ValueError,
                TypeError
            ) as error:

                messagebox.showerror(
                    "Invalid Data",
                    str(error)
                )

        button_frame = ctk.CTkFrame(
            dialog,
            fg_color="transparent"
        )

        button_frame.pack(
            fill="x",
            padx=35
        )

        cancel = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            width=150,
            height=50,
            corner_radius=10,
            fg_color="#283342",
            hover_color="#374555",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        cancel.pack(
            side="left"
        )

        save_button = ctk.CTkButton(
            button_frame,
            text="Save Changes",
            command=save,
            width=190,
            height=50,
            corner_radius=10,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        save_button.pack(
            side="right"
        )

    # ========================================================
    # DELETE TASK
    # ========================================================

    def delete_task(self):

        task = self.require_selected_task()

        if task is None:
            return

        answer = messagebox.askyesno(
            "Delete Task",
            f"Are you sure you want to delete:\n\n"
            f"{task.title}"
        )

        if not answer:
            return

        self.project.remove_task(
            task.id
        )

        self.selected_task_id = None

        if self.save_changes():

            self.refresh()

    # ========================================================
    # DELETE PROJECT
    # ========================================================

    def delete_project(self):

        answer = messagebox.askyesno(
            "Delete Project",
            f"Are you sure you want to delete:\n\n"
            f"{self.project.name}\n\n"
            f"All tasks inside this project will also be deleted."
        )

        if not answer:
            return

        removed = self.manager.remove_project(
            self.project.id
        )

        if not removed:

            messagebox.showerror(
                "Error",
                "Project could not be deleted."
            )

            return

        if self.save_changes():

            if self.on_project_deleted:

                self.on_project_deleted()

            elif self.on_back:

                self.on_back()

    # ========================================================
    # EDIT PROJECT
    # ========================================================

    def edit_project(self):

        app = self.winfo_toplevel()

        if hasattr(
            app,
            "edit_project_view"
        ):

            app.edit_project_view(
                self.project.id
            )

    # ========================================================
    # SAVE
    # ========================================================

    def save_changes(self):

        try:

            self.storage.save_projects(
                self.manager.get_all_projects()
            )

            if self.on_project_updated:

                self.on_project_updated()

            return True

        except Exception as error:

            messagebox.showerror(
                "Save Error",
                f"Changes could not be saved.\n\n{error}"
            )

            return False

    # ========================================================
    # REPORT
    # ========================================================

    def create_report(self):

        progress = Calculator.calculate_project_progress(
            self.project
        )

        time_progress = Calculator.calculate_time_progress(
            self.project
        )

        elapsed_days = Calculator.calculate_time_elapsed(
            self.project
        )

        remaining_days = Calculator.calculate_time_remaining(
            self.project
        )

        schedule_gap = Calculator.calculate_schedule_gap(
            self.project
        )

        disaster = Calculator.calculate_disaster_index(
            self.project
        )

        disaster_level = Calculator.get_disaster_level(
            disaster
        )

        status = Calculator.get_project_status(
            self.project
        )

        prediction = Predictor.get_prediction_summary(
            self.project
        )

        predicted_date = prediction[
            "predicted_date"
        ]

        expected_delay = prediction[
            "expected_delay"
        ]

        progress_rate = prediction[
            "progress_rate"
        ]

        report = []

        report.append(
            "PROJECT LATE AGAIN!!!"
        )

        report.append(
            "PROJECT PROGRESS REPORT"
        )

        report.append(
            "=" * 70
        )

        report.append("")

        report.append(
            "PROJECT INFORMATION"
        )

        report.append(
            "-" * 70
        )

        report.append(
            f"Project Name: {self.project.name}"
        )

        report.append(
            f"Description: {self.project.description}"
        )

        report.append(
            f"Start Date: {self.project.start_date}"
        )

        report.append(
            f"Deadline: {self.project.deadline}"
        )

        report.append(
            f"Report Date: {date.today()}"
        )

        report.append("")

        report.append(
            "PROJECT STATUS & METRICS"
        )

        report.append(
            "-" * 70
        )

        report.append(
            f"Project Progress: {progress:.2f}%"
        )

        report.append(
            f"Time Progress: {time_progress:.2f}%"
        )

        report.append(
            f"Elapsed Days: {elapsed_days}"
        )

        report.append(
            f"Remaining Days: {remaining_days}"
        )

        report.append(
            f"Schedule Gap: {schedule_gap:.2f}%"
        )

        report.append(
            f"Disaster Index: {disaster:.2f}"
        )

        report.append(
            f"Disaster Level: {disaster_level}"
        )

        report.append(
            f"Project Status: {status}"
        )

        report.append(
            f"Total Task Weight: {self.get_total_weight():g}"
        )

        report.append("")

        report.append(
            "COMPLETION PREDICTION"
        )

        report.append(
            "-" * 70
        )

        if predicted_date is None:

            report.append(
                "Predicted Completion: Not available"
            )

        else:

            report.append(
                f"Predicted Completion: {predicted_date}"
            )

        if progress_rate is not None:

            report.append(
                f"Average Progress Rate: "
                f"{progress_rate:.2f}% per day"
            )

        if expected_delay is None:

            report.append(
                "Expected Delay: Not available"
            )

        elif expected_delay > 0:

            report.append(
                f"Expected Delay: "
                f"{expected_delay} day(s) late"
            )

        elif expected_delay < 0:

            report.append(
                f"Expected: "
                f"{abs(expected_delay)} day(s) early"
            )

        else:

            report.append(
                "Expected: On deadline"
            )

        report.append("")

        report.append(
            "TASK DETAILS"
        )

        report.append(
            "-" * 70
        )

        if not self.project.tasks:

            report.append(
                "No tasks."
            )

        else:

            for index, task in enumerate(
                self.project.tasks,
                start=1
            ):

                report.append(
                    f"{index}. {task.title}"
                )

                report.append(
                    f"   Weight: {task.weight:g}"
                )

                report.append(
                    f"   Progress: "
                    f"{task.progress_percent:.2f}%"
                )

                report.append(
                    f"   Status: "
                    f"{task.status.value}"
                )

                report.append(
                    f"   Deadline: "
                    f"{task.deadline if task.deadline else 'None'}"
                )

                if task.completed_at:

                    report.append(
                        f"   Completed At: "
                        f"{task.completed_at}"
                    )

                report.append("")

        report_text = "\n".join(
            report
        )

        # ----------------------------------------------------
        # REPORT WINDOW
        # ----------------------------------------------------

        dialog = ctk.CTkToplevel(
            self
        )

        dialog.title(
            "Project Progress Report"
        )

        dialog.geometry(
            "950x780"
        )

        dialog.configure(
            fg_color=BG_COLOR
        )

        dialog.grab_set()

        title = ctk.CTkLabel(
            dialog,
            text="Project Progress Report",
            font=ctk.CTkFont(
                size=29,
                weight="bold"
            ),
            text_color=TEXT_COLOR
        )

        title.pack(
            anchor="w",
            padx=25,
            pady=(25, 10)
        )

        text_box = ctk.CTkTextbox(
            dialog,
            fg_color=CARD_COLOR,
            text_color=TEXT_COLOR,
            corner_radius=14,
            font=ctk.CTkFont(
                family="Consolas",
                size=14
            )
        )

        text_box.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )

        text_box.insert(
            "1.0",
            report_text
        )

        def save_report():

            path = filedialog.asksaveasfilename(
                title="Save Progress Report",
                defaultextension=".txt",
                filetypes=[
                    ("Text File", "*.txt")
                ]
            )

            if not path:
                return

            try:

                with open(
                    path,
                    "w",
                    encoding="utf-8"
                ) as file:

                    file.write(
                        report_text
                    )

                messagebox.showinfo(
                    "Report Saved",
                    "Progress report saved successfully."
                )

            except Exception as error:

                messagebox.showerror(
                    "Save Error",
                    str(error)
                )

        buttons = ctk.CTkFrame(
            dialog,
            fg_color="transparent"
        )

        buttons.pack(
            fill="x",
            padx=25,
            pady=15
        )

        close_button = ctk.CTkButton(
            buttons,
            text="Close",
            command=dialog.destroy,
            width=130,
            height=45,
            corner_radius=10,
            fg_color="#283342",
            hover_color="#374555",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        close_button.pack(
            side="left"
        )

        save_button = ctk.CTkButton(
            buttons,
            text="Save Report",
            command=save_report,
            width=160,
            height=45,
            corner_radius=10,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        save_button.pack(
            side="right"
        )

    # ========================================================
    # LABEL HELPER
    # ========================================================

    def make_label(
        self,
        parent,
        text
    ):

        label = ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            text_color=TEXT_COLOR
        )

        label.pack(
            padx=35,
            anchor="w"
        )

    # ========================================================
    # BACK
    # ========================================================

    def go_back(self):

        if self.on_back:

            self.on_back()