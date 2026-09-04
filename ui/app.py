# app.py

import customtkinter as ctk
from tkinter import messagebox
from datetime import date, datetime

from ui.dashboard import Dashboard
from ui.project_view import ProjectView
from services.project_manager import ProjectManager
from services.storage import JSONStorage
from models.project import Project
from models.task import Task


BG_COLOR = "#0F1117"
SIDEBAR_COLOR = "#151922"
PRIMARY_COLOR = "#6C63FF"
HOVER_COLOR = "#8178FF"
TEXT_COLOR = "#F5F7FA"
MUTED_COLOR = "#8E97A8"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Deadline Watch")
        self.geometry("1450x900")
        self.minsize(1150, 720)
        self.configure(fg_color=BG_COLOR)

        self.storage = JSONStorage()
        self.manager = ProjectManager()

        self._load_projects()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self._build_layout()

    # ---------------------------------------------------------
    # DATA
    # ---------------------------------------------------------

    def _load_projects(self):
        try:
            projects = self.storage.load_projects()
            self.manager.set_projects(projects)
        except Exception as exc:
            messagebox.showerror(
                "Loading Error",
                f"Could not load projects:\n\n{exc}"
            )

    def _save_projects(self):
        try:
            self.storage.save_projects(self.manager.get_all_projects())
            return True
        except Exception as exc:
            messagebox.showerror(
                "Save Error",
                f"Could not save projects:\n\n{exc}"
            )
            return False

    # ---------------------------------------------------------
    # LAYOUT
    # ---------------------------------------------------------

    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(
            self,
            width=245,
            corner_radius=0,
            fg_color=SIDEBAR_COLOR
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        self.main_container = ctk.CTkFrame(
            self,
            fg_color=BG_COLOR,
            corner_radius=0
        )
        self.main_container.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(0, 12),
            pady=12
        )
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self._build_sidebar()

        self.dashboard = Dashboard(
            self.main_container,
            app=self,
            manager=self.manager
        )
        self.dashboard.grid(row=0, column=0, sticky="nsew")

    def _build_sidebar(self):
        logo = ctk.CTkLabel(
            self.sidebar,
            text="DEADLINE WATCH",
            font=ctk.CTkFont(size=21, weight="bold"),
            text_color=TEXT_COLOR
        )
        logo.pack(
            anchor="w",
            padx=24,
            pady=(30, 6)
        )

        subtitle = ctk.CTkLabel(
            self.sidebar,
            text="Project control center",
            font=ctk.CTkFont(size=12),
            text_color=MUTED_COLOR
        )
        subtitle.pack(
            anchor="w",
            padx=25,
            pady=(0, 30)
        )

        self._sidebar_button(
            "▦   Dashboard",
            self.show_dashboard
        )

        self._sidebar_button(
            "＋   Add New Project",
            self.add_project_view
        )

        self._sidebar_button(
            "↻   Quick Update",
            self.quick_update
        )

        divider = ctk.CTkFrame(
            self.sidebar,
            height=1,
            fg_color="#272D3A"
        )
        divider.pack(
            fill="x",
            padx=22,
            pady=25
        )

        info = ctk.CTkLabel(
            self.sidebar,
            text="Everything important\nin one place.",
            justify="left",
            font=ctk.CTkFont(size=12),
            text_color=MUTED_COLOR
        )
        info.pack(
            anchor="w",
            padx=25
        )

    def _sidebar_button(self, text, command):
        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            command=command,
            height=44,
            corner_radius=10,
            anchor="w",
            fg_color="transparent",
            hover_color="#202633",
            text_color=TEXT_COLOR,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        button.pack(
            fill="x",
            padx=14,
            pady=4
        )

    # ---------------------------------------------------------
    # DASHBOARD
    # ---------------------------------------------------------

    def show_dashboard(self):
        self.dashboard.refresh()

    # ---------------------------------------------------------
    # PROJECT VIEW
    # ---------------------------------------------------------

    def open_project_view(self, project_id):
        project = self.manager.get_project(project_id)

        if project is None:
            messagebox.showerror(
                "Project Not Found",
                "This project no longer exists."
            )
            return

        ProjectView(
            self,
            project=project,
            app=self
        )

    # ---------------------------------------------------------
    # ADD PROJECT
    # ---------------------------------------------------------

    def add_project_view(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add New Project")
        dialog.geometry("620x720")
        dialog.minsize(560, 650)
        dialog.configure(fg_color=BG_COLOR)
        dialog.transient(self)
        dialog.grab_set()

        dialog.grid_columnconfigure(0, weight=1)
        dialog.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(
            dialog,
            text="Create New Project",
            font=ctk.CTkFont(size=27, weight="bold"),
            text_color=TEXT_COLOR
        )
        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=35,
            pady=(28, 18)
        )

        content = ctk.CTkScrollableFrame(
            dialog,
            fg_color="transparent"
        )
        content.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=25
        )

        content.grid_columnconfigure(0, weight=1)

        name_entry = self._form_entry(
            content,
            "Project Name",
            "e.g. Website Redesign",
            0
        )

        description_entry = self._form_entry(
            content,
            "Description",
            "What is this project about?",
            1
        )

        start_entry = self._form_entry(
            content,
            "Start Date",
            "YYYY-MM-DD",
            2
        )

        deadline_entry = self._form_entry(
            content,
            "Deadline",
            "YYYY-MM-DD",
            3
        )

        task_count_entry = self._form_entry(
            content,
            "Number of Tasks",
            "e.g. 5",
            4
        )

        def create():
            name = name_entry.get().strip()
            description = description_entry.get().strip()
            start_text = start_entry.get().strip()
            deadline_text = deadline_entry.get().strip()
            count_text = task_count_entry.get().strip()

            if not name:
                messagebox.showerror(
                    "Invalid Project",
                    "Project name is required.",
                    parent=dialog
                )
                return

            try:
                start_date = date.fromisoformat(start_text)
                deadline = date.fromisoformat(deadline_text)
            except ValueError:
                messagebox.showerror(
                    "Invalid Date",
                    "Use YYYY-MM-DD for dates.",
                    parent=dialog
                )
                return

            if start_date >= deadline:
                messagebox.showerror(
                    "Invalid Dates",
                    "Start date must be before the deadline.",
                    parent=dialog
                )
                return

            try:
                task_count = int(count_text)
            except ValueError:
                messagebox.showerror(
                    "Invalid Tasks",
                    "Number of tasks must be a whole number.",
                    parent=dialog
                )
                return

            if task_count < 0:
                messagebox.showerror(
                    "Invalid Tasks",
                    "Number of tasks cannot be negative.",
                    parent=dialog
                )
                return

            tasks = []

            for index in range(task_count):
                task_title = self._ask_input(
                    "Task",
                    f"Task {index + 1} name:"
                )

                if task_title is None:
                    return

                task_title = task_title.strip()

                if not task_title:
                    messagebox.showerror(
                        "Invalid Task",
                        f"Task {index + 1} needs a name.",
                        parent=dialog
                    )
                    return

                weight_text = self._ask_input(
                    "Task Weight",
                    f"Weight for '{task_title}':"
                )

                if weight_text is None:
                    return

                try:
                    weight = float(weight_text)
                except ValueError:
                    messagebox.showerror(
                        "Invalid Weight",
                        "Task weight must be a number.",
                        parent=dialog
                    )
                    return

                if weight <= 0:
                    messagebox.showerror(
                        "Invalid Weight",
                        "Task weight must be greater than zero.",
                        parent=dialog
                    )
                    return

                tasks.append(
                    Task(
                        title=task_title,
                        weight=weight
                    )
                )

            try:
                project = Project(
                    name=name,
                    description=description,
                    start_date=start_date,
                    deadline=deadline,
                    tasks=tasks
                )

                self.manager.add_project(project)

            except Exception as exc:
                messagebox.showerror(
                    "Could Not Create Project",
                    str(exc),
                    parent=dialog
                )
                return

            if self._save_projects():
                dialog.destroy()
                self.dashboard.refresh()

        buttons = ctk.CTkFrame(
            dialog,
            fg_color="transparent"
        )
        buttons.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=30,
            pady=20
        )

        buttons.grid_columnconfigure(0, weight=1)
        buttons.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            buttons,
            text="Cancel",
            command=dialog.destroy,
            height=46,
            fg_color="#252B36",
            hover_color="#303846"
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 7)
        )

        ctk.CTkButton(
            buttons,
            text="Create Project",
            command=create,
            height=46,
            fg_color=PRIMARY_COLOR,
            hover_color=HOVER_COLOR
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(7, 0)
        )

    def _form_entry(self, parent, label, placeholder, row):
        frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        frame.grid(
            row=row,
            column=0,
            sticky="ew",
            pady=9
        )

        ctk.CTkLabel(
            frame,
            text=label,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        entry = ctk.CTkEntry(
            frame,
            height=42,
            placeholder_text=placeholder
        )
        entry.pack(fill="x")

        return entry

    # ---------------------------------------------------------
    # EDIT PROJECT
    # ---------------------------------------------------------

    def edit_project_view(self, project_id):
        project = self.manager.get_project(project_id)

        if project is None:
            messagebox.showerror(
                "Project Not Found",
                "Project could not be found."
            )
            return

        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Project")
        dialog.geometry("570x600")
        dialog.configure(fg_color=BG_COLOR)
        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text=f"Edit: {project.name}",
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color=TEXT_COLOR
        ).pack(
            anchor="w",
            padx=30,
            pady=(28, 5)
        )

        ctk.CTkLabel(
            dialog,
            text="Choose exactly what you want to change.",
            font=ctk.CTkFont(size=13),
            text_color=MUTED_COLOR
        ).pack(
            anchor="w",
            padx=30,
            pady=(0, 22)
        )

        options = [
            ("Project Name", "name"),
            ("Description", "description"),
            ("Start Date", "start_date"),
            ("Deadline", "deadline"),
            ("Tasks", "tasks"),
        ]

        variables = {}

        container = ctk.CTkFrame(
            dialog,
            fg_color="#151922",
            corner_radius=14
        )
        container.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 20)
        )

        for text, key in options:
            var = ctk.BooleanVar(value=False)
            variables[key] = var

            ctk.CTkCheckBox(
                container,
                text=text,
                variable=var,
                height=48,
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color=TEXT_COLOR,
                fg_color=PRIMARY_COLOR,
                hover_color=HOVER_COLOR
            ).pack(
                fill="x",
                padx=20,
                pady=7
            )

        def continue_editing():
            selected = [
                key
                for key, variable in variables.items()
                if variable.get()
            ]

            if not selected:
                messagebox.showwarning(
                    "Nothing Selected",
                    "Select at least one section to edit.",
                    parent=dialog
                )
                return

            dialog.destroy()
            self._edit_selected_fields(project, selected)

        ctk.CTkButton(
            dialog,
            text="Continue",
            command=continue_editing,
            height=48,
            fg_color=PRIMARY_COLOR,
            hover_color=HOVER_COLOR
        ).pack(
            fill="x",
            padx=30,
            pady=(0, 30)
        )

    def _edit_selected_fields(self, project, selected):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Selected Fields")
        dialog.geometry("700x760")
        dialog.configure(fg_color=BG_COLOR)
        dialog.transient(self)
        dialog.grab_set()

        dialog.grid_columnconfigure(0, weight=1)
        dialog.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            dialog,
            text="Update Project",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=TEXT_COLOR
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=30,
            pady=(25, 15)
        )

        content = ctk.CTkScrollableFrame(
            dialog,
            fg_color="transparent"
        )
        content.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=20
        )
        content.grid_columnconfigure(0, weight=1)

        entries = {}

        row = 0

        if "name" in selected:
            ctk.CTkLabel(
                content,
                text="Project Name",
                font=ctk.CTkFont(size=13, weight="bold")
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=10,
                pady=(10, 5)
            )

            entry = ctk.CTkEntry(content, height=42)
            entry.insert(0, project.name)
            entry.grid(
                row=row + 1,
                column=0,
                sticky="ew",
                padx=10,
                pady=(0, 15)
            )

            entries["name"] = entry
            row += 2

        if "description" in selected:
            ctk.CTkLabel(
                content,
                text="Description",
                font=ctk.CTkFont(size=13, weight="bold")
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=10,
                pady=(10, 5)
            )

            entry = ctk.CTkEntry(content, height=42)
            entry.insert(0, project.description)
            entry.grid(
                row=row + 1,
                column=0,
                sticky="ew",
                padx=10,
                pady=(0, 15)
            )

            entries["description"] = entry
            row += 2

        if "start_date" in selected:
            ctk.CTkLabel(
                content,
                text="Start Date",
                font=ctk.CTkFont(size=13, weight="bold")
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=10,
                pady=(10, 5)
            )

            entry = ctk.CTkEntry(content, height=42)
            entry.insert(0, project.start_date.isoformat())
            entry.grid(
                row=row + 1,
                column=0,
                sticky="ew",
                padx=10,
                pady=(0, 15)
            )

            entries["start_date"] = entry
            row += 2

        if "deadline" in selected:
            ctk.CTkLabel(
                content,
                text="Deadline",
                font=ctk.CTkFont(size=13, weight="bold")
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=10,
                pady=(10, 5)
            )

            entry = ctk.CTkEntry(content, height=42)
            entry.insert(0, project.deadline.isoformat())
            entry.grid(
                row=row + 1,
                column=0,
                sticky="ew",
                padx=10,
                pady=(0, 15)
            )

            entries["deadline"] = entry
            row += 2

        task_entries = []

        if "tasks" in selected:
            ctk.CTkLabel(
                content,
                text="Tasks",
                font=ctk.CTkFont(size=17, weight="bold"),
                text_color=TEXT_COLOR
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=10,
                pady=(15, 8)
            )
            row += 1

            for task in project.tasks:
                task_frame = ctk.CTkFrame(
                    content,
                    fg_color="#1A1F2A",
                    corner_radius=10
                )
                task_frame.grid(
                    row=row,
                    column=0,
                    sticky="ew",
                    padx=10,
                    pady=5
                )
                task_frame.grid_columnconfigure(0, weight=1)

                title_entry = ctk.CTkEntry(task_frame, height=38)
                title_entry.insert(0, task.title)
                title_entry.grid(
                    row=0,
                    column=0,
                    sticky="ew",
                    padx=10,
                    pady=(10, 5)
                )

                weight_entry = ctk.CTkEntry(
                    task_frame,
                    width=100,
                    height=38
                )
                weight_entry.insert(0, str(task.weight))
                weight_entry.grid(
                    row=1,
                    column=0,
                    sticky="w",
                    padx=10,
                    pady=(5, 10)
                )

                task_entries.append(
                    (task, title_entry, weight_entry)
                )

                row += 1

        def save():
            # Stage everything first so invalid input never partially
            # changes the actual project.

            new_name = project.name
            new_description = project.description
            new_start = project.start_date
            new_deadline = project.deadline
            staged_tasks = []

            if "name" in selected:
                new_name = entries["name"].get().strip()

                if not new_name:
                    messagebox.showerror(
                        "Invalid Name",
                        "Project name cannot be empty.",
                        parent=dialog
                    )
                    return

            if "description" in selected:
                new_description = entries["description"].get().strip()

            try:
                if "start_date" in selected:
                    new_start = date.fromisoformat(
                        entries["start_date"].get().strip()
                    )

                if "deadline" in selected:
                    new_deadline = date.fromisoformat(
                        entries["deadline"].get().strip()
                    )
            except ValueError:
                messagebox.showerror(
                    "Invalid Date",
                    "Use YYYY-MM-DD for dates.",
                    parent=dialog
                )
                return

            if new_start >= new_deadline:
                messagebox.showerror(
                    "Invalid Dates",
                    "Start date must be before the deadline.",
                    parent=dialog
                )
                return

            if "tasks" in selected:
                for task, title_entry, weight_entry in task_entries:
                    title = title_entry.get().strip()

                    if not title:
                        messagebox.showerror(
                            "Invalid Task",
                            "Task names cannot be empty.",
                            parent=dialog
                        )
                        return

                    try:
                        weight = float(weight_entry.get().strip())
                    except ValueError:
                        messagebox.showerror(
                            "Invalid Weight",
                            f"Invalid weight for '{title}'.",
                            parent=dialog
                        )
                        return

                    if weight <= 0:
                        messagebox.showerror(
                            "Invalid Weight",
                            f"Weight for '{title}' must be greater than zero.",
                            parent=dialog
                        )
                        return

                    staged_tasks.append(
                        (task, title, weight)
                    )

            project.name = new_name
            project.description = new_description
            project.start_date = new_start
            project.deadline = new_deadline

            for task, title, weight in staged_tasks:
                task.title = title
                task.weight = weight

            if self._save_projects():
                dialog.destroy()
                self.dashboard.refresh()

        ctk.CTkButton(
            dialog,
            text="Save Changes",
            command=save,
            height=48,
            fg_color=PRIMARY_COLOR,
            hover_color=HOVER_COLOR
        ).grid(
            row=2,
            column=0,
            sticky="ew",
            padx=30,
            pady=20
        )

    # ---------------------------------------------------------
    # UPDATE PROGRESS
    # ---------------------------------------------------------

    def update_project_progress(self, project_id):
        project = self.manager.get_project(project_id)

        if project is None:
            messagebox.showerror(
                "Project Not Found",
                "Project could not be found."
            )
            return

        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Update Progress — {project.name}")
        dialog.geometry("760x760")
        dialog.minsize(650, 650)
        dialog.configure(fg_color=BG_COLOR)
        dialog.transient(self)
        dialog.grab_set()

        dialog.grid_columnconfigure(0, weight=1)
        dialog.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(
            dialog,
            fg_color="transparent"
        )
        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=30,
            pady=(25, 15)
        )
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Update Task Progress",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=TEXT_COLOR
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            header,
            text=project.name,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=PRIMARY_COLOR
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(4, 0)
        )

        content = ctk.CTkScrollableFrame(
            dialog,
            fg_color="transparent"
        )
        content.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=20
        )
        content.grid_columnconfigure(0, weight=1)

        if not project.tasks:
            ctk.CTkLabel(
                content,
                text="This project has no tasks yet.",
                font=ctk.CTkFont(size=15),
                text_color=MUTED_COLOR
            ).pack(
                pady=50
            )

        progress_entries = []

        for index, task in enumerate(project.tasks, start=1):
            card = ctk.CTkFrame(
                content,
                fg_color="#181E28",
                corner_radius=14
            )
            card.pack(
                fill="x",
                padx=8,
                pady=7
            )

            card.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                card,
                text=f"Task {index}",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=MUTED_COLOR
            ).grid(
                row=0,
                column=0,
                sticky="w",
                padx=16,
                pady=(13, 0)
            )

            ctk.CTkLabel(
                card,
                text=task.title,
                font=ctk.CTkFont(size=17, weight="bold"),
                text_color=TEXT_COLOR,
                anchor="w"
            ).grid(
                row=1,
                column=0,
                sticky="ew",
                padx=16,
                pady=(2, 2)
            )

            details = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )
            details.grid(
                row=2,
                column=0,
                sticky="ew",
                padx=16,
                pady=(2, 5)
            )

            ctk.CTkLabel(
                details,
                text=f"Weight: {task.weight:g}",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=MUTED_COLOR
            ).pack(
                side="left",
                padx=(0, 18)
            )

            status_text = getattr(task.status, "value", str(task.status))

            ctk.CTkLabel(
                details,
                text=f"Status: {status_text}",
                font=ctk.CTkFont(size=12),
                text_color=MUTED_COLOR
            ).pack(
                side="left"
            )

            if task.deadline:
                ctk.CTkLabel(
                    details,
                    text=f"Deadline: {task.deadline.isoformat()}",
                    font=ctk.CTkFont(size=12),
                    text_color=MUTED_COLOR
                ).pack(
                    side="right"
                )

            progress_row = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )
            progress_row.grid(
                row=3,
                column=0,
                sticky="ew",
                padx=16,
                pady=(5, 14)
            )
            progress_row.grid_columnconfigure(0, weight=1)

            progress_var = ctk.DoubleVar(
                value=float(task.progress_percent)
            )

            slider = ctk.CTkSlider(
                progress_row,
                from_=0,
                to=100,
                variable=progress_var
            )
            slider.grid(
                row=0,
                column=0,
                sticky="ew",
                padx=(0, 15)
            )

            percent_label = ctk.CTkLabel(
                progress_row,
                text=f"{task.progress_percent:.0f}%",
                width=65,
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color=TEXT_COLOR
            )
            percent_label.grid(
                row=0,
                column=1
            )

            def update_label(value, label=percent_label):
                label.configure(
                    text=f"{float(value):.0f}%"
                )

            slider.configure(
                command=update_label
            )

            progress_entries.append(
                (task, progress_var)
            )

        def save_progress():
            try:
                for task, variable in progress_entries:
                    value = float(variable.get())
                    project.update_task(
                        task.id,
                        new_progress=value
                    )

                if not self._save_projects():
                    return

                dialog.destroy()
                self.dashboard.refresh()

            except Exception as exc:
                messagebox.showerror(
                    "Update Failed",
                    str(exc),
                    parent=dialog
                )

        ctk.CTkButton(
            dialog,
            text="Save Progress",
            command=save_progress,
            height=50,
            fg_color=PRIMARY_COLOR,
            hover_color=HOVER_COLOR,
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(
            row=2,
            column=0,
            sticky="ew",
            padx=30,
            pady=20
        )

    # ---------------------------------------------------------
    # QUICK UPDATE
    # ---------------------------------------------------------

    def quick_update(self):
        projects = self.manager.get_all_projects()

        if not projects:
            messagebox.showinfo(
                "No Projects",
                "Create a project first."
            )
            return

        dialog = ctk.CTkToplevel(self)
        dialog.title("Quick Update")
        dialog.geometry("520x560")
        dialog.configure(fg_color=BG_COLOR)
        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="Quick Update",
            font=ctk.CTkFont(size=26, weight="bold")
        ).pack(
            anchor="w",
            padx=30,
            pady=(28, 5)
        )

        ctk.CTkLabel(
            dialog,
            text="Select a project to update its tasks.",
            text_color=MUTED_COLOR
        ).pack(
            anchor="w",
            padx=30,
            pady=(0, 20)
        )

        scroll = ctk.CTkScrollableFrame(
            dialog,
            fg_color="transparent"
        )
        scroll.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        for project in reversed(projects):
            ctk.CTkButton(
                scroll,
                text=project.name,
                command=lambda p=project: (
                    dialog.destroy(),
                    self.update_project_progress(p.id)
                ),
                height=48,
                anchor="w",
                fg_color="#191F2A",
                hover_color="#252D3A"
            ).pack(
                fill="x",
                pady=5
            )

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------

    def delete_project_view(self, project_id):
        project = self.manager.get_project(project_id)

        if project is None:
            return

        confirmed = messagebox.askyesno(
            "Delete Project",
            f"Delete '{project.name}'?\n\nThis cannot be undone."
        )

        if not confirmed:
            return

        if self.manager.remove_project(project_id):
            if self._save_projects():
                self.dashboard.refresh()

    # ---------------------------------------------------------
    # HELPERS
    # ---------------------------------------------------------

    def _ask_input(self, title, prompt):
        dialog = ctk.CTkInputDialog(
            text=prompt,
            title=title
        )
        return dialog.get_input()

    def on_close(self):
        self._save_projects()
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()