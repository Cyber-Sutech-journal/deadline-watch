import customtkinter as ctk
from tkinter import messagebox
from datetime import date, timedelta

from models.project import Project
from services.project_manager import ProjectManager
from services.storage import JSONStorage

from ui.dashboard import Dashboard
from ui.project_view import ProjectView


# ============================================================
# COLORS
# ============================================================

BG_COLOR = "#0A0E13"
SIDEBAR_COLOR = "#111720"
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


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title(
            "Project Late Again!!!"
        )

        self.geometry(
            "1500x920"
        )

        self.minsize(
            1200,
            760
        )

        ctk.set_appearance_mode(
            "dark"
        )

        ctk.set_default_color_theme(
            "blue"
        )

        self.configure(
            fg_color=BG_COLOR
        )

        # ----------------------------------------------------
        # DATA
        # ----------------------------------------------------

        self.storage = JSONStorage()
        self.manager = ProjectManager()

        self.load_projects()

        # ----------------------------------------------------
        # UI REFERENCES
        # ----------------------------------------------------

        self.sidebar = None
        self.main_container = None

        self.dashboard = None
        self.project_view = None

        self.build_layout()

        self.show_dashboard()

        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )

    # ========================================================
    # DATA
    # ========================================================

    def load_projects(self):

        try:
            projects = self.storage.load_projects()

            self.manager.set_projects(
                projects
            )

        except Exception as error:

            messagebox.showerror(
                "Load Error",
                f"Could not load projects.\n\n{error}"
            )

    def save_projects(self):

        try:

            self.storage.save_projects(
                self.manager.get_all_projects()
            )

            return True

        except Exception as error:

            messagebox.showerror(
                "Save Error",
                f"Could not save projects.\n\n{error}"
            )

            return False

    # ========================================================
    # MAIN LAYOUT
    # ========================================================

    def build_layout(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=280,
            corner_radius=0,
            fg_color=SIDEBAR_COLOR
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(
            False
        )

        self.main_container = ctk.CTkFrame(
            self,
            fg_color=BG_COLOR,
            corner_radius=0
        )

        self.main_container.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.build_sidebar()

    # ========================================================
    # SIDEBAR
    # ========================================================

    def build_sidebar(self):

        for widget in self.sidebar.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(
            self.sidebar,
            text="PROJECT\nLATE AGAIN!!!",
            font=ctk.CTkFont(
                size=29,
                weight="bold"
            ),
            text_color=TEXT_COLOR,
            justify="left"
        )

        title.pack(
            padx=25,
            pady=(35, 5),
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            self.sidebar,
            text="Entertainment Project Manager",
            font=ctk.CTkFont(
                size=14
            ),
            text_color=MUTED_COLOR
        )

        subtitle.pack(
            padx=25,
            anchor="w"
        )

        self.create_sidebar_button(
            "⌂   Dashboard",
            self.show_dashboard
        )

        self.create_sidebar_button(
            "+   New Project",
            self.add_project_view
        )

        separator = ctk.CTkFrame(
            self.sidebar,
            height=2,
            fg_color="#2A3440"
        )

        separator.pack(
            fill="x",
            padx=25,
            pady=25
        )

        count = len(
            self.manager.get_all_projects()
        )

        count_label = ctk.CTkLabel(
            self.sidebar,
            text=f"Projects: {count}",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            ),
            text_color=TEXT_COLOR
        )

        count_label.pack(
            padx=25,
            anchor="w"
        )

        footer = ctk.CTkLabel(
            self.sidebar,
            text="Track progress.\nBeat the deadline.",
            font=ctk.CTkFont(
                size=14
            ),
            text_color=MUTED_COLOR,
            justify="left"
        )

        footer.pack(
            side="bottom",
            padx=25,
            pady=30,
            anchor="w"
        )

    def create_sidebar_button(
        self,
        text,
        command
    ):

        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            command=command,
            width=225,
            height=52,
            corner_radius=12,
            fg_color="transparent",
            hover_color="#202A36",
            text_color=TEXT_COLOR,
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            ),
            anchor="w"
        )

        button.pack(
            padx=25,
            pady=6
        )

    # ========================================================
    # NAVIGATION
    # ========================================================

    def clear_main(self):

        for widget in self.main_container.winfo_children():
            widget.destroy()

    def show_dashboard(self):

        self.clear_main()

        self.build_sidebar()

        self.dashboard = Dashboard(
            self.main_container,
            project_manager=self.manager,
            on_open_project=self.open_project_view,
            on_edit_project=self.edit_project_view,
            on_delete_project=self.delete_project_view,
            on_add_project=self.add_project_view
        )

        self.dashboard.pack(
            fill="both",
            expand=True
        )

        self.project_view = None

    def open_project_view(
        self,
        project_id
    ):

        project = self.manager.get_project(
            project_id
        )

        if project is None:

            messagebox.showerror(
                "Error",
                "Project was not found."
            )

            return

        self.clear_main()

        self.project_view = ProjectView(
            self.main_container,
            project=project,
            project_manager=self.manager,
            storage=self.storage,
            on_back=self.show_dashboard,
            on_project_deleted=self.show_dashboard,
            on_project_updated=self.build_sidebar
        )

        self.project_view.pack(
            fill="both",
            expand=True
        )

    # ========================================================
    # CREATE PROJECT
    # ========================================================

    def add_project_view(self):

        dialog = ctk.CTkToplevel(
            self
        )

        dialog.title(
            "Create New Project"
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

        title = ctk.CTkLabel(
            dialog,
            text="Create New Project",
            font=ctk.CTkFont(
                size=31,
                weight="bold"
            ),
            text_color=TEXT_COLOR
        )

        title.pack(
            padx=35,
            pady=(30, 5),
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            dialog,
            text="Create your project and set its deadline.",
            font=ctk.CTkFont(
                size=14
            ),
            text_color=MUTED_COLOR
        )

        subtitle.pack(
            padx=35,
            pady=(0, 20),
            anchor="w"
        )

        # ----------------------------------------------------
        # Project Name
        # ----------------------------------------------------

        name_entry = self.create_form_entry(
            dialog,
            "Project Name"
        )

        # ----------------------------------------------------
        # Description
        # ----------------------------------------------------

        description_entry = self.create_form_entry(
            dialog,
            "Description"
        )

        # ----------------------------------------------------
        # Start Date
        # ----------------------------------------------------

        start_entry = self.create_form_entry(
            dialog,
            "Start Date (YYYY-MM-DD)",
            date.today().isoformat()
        )

        # ----------------------------------------------------
        # Deadline choice
        # ----------------------------------------------------

        deadline_title = ctk.CTkLabel(
            dialog,
            text="Deadline",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            text_color=TEXT_COLOR
        )

        deadline_title.pack(
            padx=35,
            anchor="w",
            pady=(8, 6)
        )

        choice_frame = ctk.CTkFrame(
            dialog,
            fg_color="transparent"
        )

        choice_frame.pack(
            fill="x",
            padx=35
        )

        deadline_mode = ctk.StringVar(
            value="days"
        )

        days_radio = ctk.CTkRadioButton(
            choice_frame,
            text="Enter days remaining",
            variable=deadline_mode,
            value="days",
            font=ctk.CTkFont(
                size=14
            )
        )

        days_radio.pack(
            side="left",
            padx=(0, 30)
        )

        date_radio = ctk.CTkRadioButton(
            choice_frame,
            text="Enter exact date",
            variable=deadline_mode,
            value="date",
            font=ctk.CTkFont(
                size=14
            )
        )

        date_radio.pack(
            side="left"
        )

        deadline_entry = self.create_form_entry(
            dialog,
            "Days Remaining",
            "30"
        )

        # ----------------------------------------------------
        # Hint
        # ----------------------------------------------------

        hint = ctk.CTkLabel(
            dialog,
            text=(
                "Example: enter 20 to make the deadline "
                "20 days from today."
            ),
            font=ctk.CTkFont(
                size=12
            ),
            text_color=MUTED_COLOR
        )

        hint.pack(
            padx=35,
            anchor="w",
            pady=(0, 15)
        )

        def update_deadline_label():

            if deadline_mode.get() == "days":

                deadline_title.configure(
                    text="Deadline"
                )

                deadline_entry.delete(
                    0,
                    "end"
                )

                deadline_entry.insert(
                    0,
                    "30"
                )

                hint.configure(
                    text=(
                        "Enter the number of days from today."
                    )
                )

                date_radio.configure(
                    fg_color=PRIMARY
                )

            else:

                deadline_entry.delete(
                    0,
                    "end"
                )

                deadline_entry.insert(
                    0,
                    date.today().isoformat()
                )

                hint.configure(
                    text=(
                        "Enter the exact deadline: YYYY-MM-DD"
                    )
                )

        # Radio buttons don't automatically refresh
        # the entry, so connect them here.
        days_radio.configure(
            command=update_deadline_label
        )

        date_radio.configure(
            command=update_deadline_label
        )

        # ----------------------------------------------------
        # Create
        # ----------------------------------------------------

        def create_project():

            name = name_entry.get().strip()
            description = description_entry.get().strip()
            start_text = start_entry.get().strip()
            deadline_text = deadline_entry.get().strip()

            if not name:

                messagebox.showwarning(
                    "Missing Information",
                    "Project name is required."
                )

                return

            try:

                start_date = date.fromisoformat(
                    start_text
                )

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

                if start_date >= deadline:

                    raise ValueError(
                        "Start date must be before deadline."
                    )

                project = Project(
                    name=name,
                    description=description,
                    start_date=start_date,
                    deadline=deadline
                )

                self.manager.add_project(
                    project
                )

                if self.save_projects():

                    dialog.destroy()

                    self.build_sidebar()

                    self.open_project_view(
                        project.id
                    )

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
            padx=35,
            pady=25
        )

        cancel = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            width=150,
            height=50,
            corner_radius=12,
            fg_color="#28313D",
            hover_color="#354150",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        cancel.pack(
            side="left"
        )

        create = ctk.CTkButton(
            button_frame,
            text="Create Project",
            command=create_project,
            width=195,
            height=50,
            corner_radius=12,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        create.pack(
            side="right"
        )

    # ========================================================
    # EDIT PROJECT
    # ========================================================

    def edit_project_view(
        self,
        project_id
    ):

        project = self.manager.get_project(
            project_id
        )

        if project is None:

            messagebox.showerror(
                "Error",
                "Project was not found."
            )

            return

        dialog = ctk.CTkToplevel(
            self
        )

        dialog.title(
            "Edit Project"
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

        title = ctk.CTkLabel(
            dialog,
            text="Edit Project",
            font=ctk.CTkFont(
                size=31,
                weight="bold"
            ),
            text_color=TEXT_COLOR
        )

        title.pack(
            padx=35,
            pady=(30, 25),
            anchor="w"
        )

        name_entry = self.create_form_entry(
            dialog,
            "Project Name",
            project.name
        )

        description_entry = self.create_form_entry(
            dialog,
            "Description",
            project.description
        )

        start_entry = self.create_form_entry(
            dialog,
            "Start Date (YYYY-MM-DD)",
            project.start_date.isoformat()
        )

        # ----------------------------------------------------
        # Deadline choice
        # ----------------------------------------------------

        deadline_title = ctk.CTkLabel(
            dialog,
            text="Deadline",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            text_color=TEXT_COLOR
        )

        deadline_title.pack(
            padx=35,
            anchor="w",
            pady=(8, 6)
        )

        choice_frame = ctk.CTkFrame(
            dialog,
            fg_color="transparent"
        )

        choice_frame.pack(
            fill="x",
            padx=35
        )

        deadline_mode = ctk.StringVar(
            value="days"
        )

        days_radio = ctk.CTkRadioButton(
            choice_frame,
            text="Days remaining",
            variable=deadline_mode,
            value="days",
            font=ctk.CTkFont(
                size=14
            )
        )

        days_radio.pack(
            side="left",
            padx=(0, 30)
        )

        date_radio = ctk.CTkRadioButton(
            choice_frame,
            text="Exact date",
            variable=deadline_mode,
            value="date",
            font=ctk.CTkFont(
                size=14
            )
        )

        date_radio.pack(
            side="left"
        )

        current_days = (
            project.deadline - date.today()
        ).days

        deadline_entry = self.create_form_entry(
            dialog,
            "Days Remaining",
            str(max(current_days, 0))
        )

        hint = ctk.CTkLabel(
            dialog,
            text="Enter the number of days from today.",
            font=ctk.CTkFont(
                size=12
            ),
            text_color=MUTED_COLOR
        )

        hint.pack(
            padx=35,
            anchor="w",
            pady=(0, 25)
        )

        def switch_mode():

            if deadline_mode.get() == "days":

                current_days = (
                    project.deadline - date.today()
                ).days

                deadline_entry.delete(
                    0,
                    "end"
                )

                deadline_entry.insert(
                    0,
                    str(max(current_days, 0))
                )

                hint.configure(
                    text=(
                        "Enter the number of days from today."
                    )
                )

            else:

                deadline_entry.delete(
                    0,
                    "end"
                )

                deadline_entry.insert(
                    0,
                    project.deadline.isoformat()
                )

                hint.configure(
                    text=(
                        "Enter exact date: YYYY-MM-DD"
                    )
                )

        days_radio.configure(
            command=switch_mode
        )

        date_radio.configure(
            command=switch_mode
        )

        def save_project():

            name = name_entry.get().strip()
            description = description_entry.get().strip()
            start_text = start_entry.get().strip()
            deadline_text = deadline_entry.get().strip()

            if not name:

                messagebox.showwarning(
                    "Missing Information",
                    "Project name cannot be empty."
                )

                return

            try:

                new_start = date.fromisoformat(
                    start_text
                )

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

                if new_start >= new_deadline:

                    raise ValueError(
                        "Start date must be before deadline."
                    )

                project.name = name
                project.description = description
                project.start_date = new_start
                project.deadline = new_deadline

                if self.save_projects():

                    dialog.destroy()

                    if self.project_view is not None:

                        self.open_project_view(
                            project.id
                        )

                    else:

                        self.show_dashboard()

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
            padx=35,
            pady=25
        )

        cancel = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            width=150,
            height=50,
            corner_radius=12,
            fg_color="#28313D",
            hover_color="#354150",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        cancel.pack(
            side="left"
        )

        save = ctk.CTkButton(
            button_frame,
            text="Save Changes",
            command=save_project,
            width=195,
            height=50,
            corner_radius=12,
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        save.pack(
            side="right"
        )

    # ========================================================
    # DELETE PROJECT
    # ========================================================

    def delete_project_view(
        self,
        project_id
    ):

        project = self.manager.get_project(
            project_id
        )

        if project is None:

            messagebox.showerror(
                "Error",
                "Project was not found."
            )

            return

        answer = messagebox.askyesno(
            "Delete Project",
            f"Are you sure you want to delete:\n\n"
            f"{project.name}\n\n"
            f"All tasks inside this project will also be deleted."
        )

        if not answer:
            return

        removed = self.manager.remove_project(
            project_id
        )

        if removed:

            if self.save_projects():

                self.build_sidebar()

                self.show_dashboard()

    # ========================================================
    # FORM HELPER
    # ========================================================

    def create_form_entry(
        self,
        parent,
        label_text,
        value=""
    ):

        frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        frame.pack(
            fill="x",
            padx=35,
            pady=8
        )

        label = ctk.CTkLabel(
            frame,
            text=label_text,
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            text_color=TEXT_COLOR
        )

        label.pack(
            anchor="w",
            pady=(0, 6)
        )

        entry = ctk.CTkEntry(
            frame,
            height=49,
            corner_radius=10,
            fg_color=CARD_COLOR,
            border_color="#303A48",
            text_color=TEXT_COLOR,
            font=ctk.CTkFont(
                size=15
            )
        )

        entry.pack(
            fill="x"
        )

        if value:

            entry.insert(
                0,
                value
            )

        return entry

    # ========================================================
    # CLOSE
    # ========================================================

    def on_close(self):

        self.save_projects()

        self.destroy()


if __name__ == "__main__":

    app = App()

    app.mainloop()