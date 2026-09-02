from datetime import date


class Calculator:
    """
    This class contains the main calculations of the application.

    It calculates:
    - Project progress
    - Total project days
    - Elapsed days
    - Remaining days
    - Time progress
    - Schedule gap
    - Project status
    - Disaster Index
    """

    # ------------------------------------------------------------
    # Project Progress
    # ------------------------------------------------------------

    @staticmethod
    def calculate_project_progress(project):
        """
        Calculate the overall project progress using task weights.

        Formula:

        Project Progress =
        Sum(Task Weight * Task Progress) / Sum(Task Weight)

        Returns:
            A number between 0 and 100.
        """

        # If there are no tasks, the project has 0% progress.
        if not project.tasks:
            return 0.0

        # Calculate total weight of all tasks.
        total_weight = sum(
            task.weight for task in project.tasks
        )

        # This should normally never happen because
        # Task weight must be greater than 0.
        if total_weight <= 0:
            return 0.0

        # Calculate weighted progress.
        weighted_progress = sum(
            task.weight * task.progress_percent
            for task in project.tasks
        )

        # Calculate final project progress.
        progress = weighted_progress / total_weight

        # Make sure the result stays between 0 and 100.
        progress = max(0.0, min(100.0, progress))

        return progress

    # ------------------------------------------------------------
    # Total Project Days
    # ------------------------------------------------------------

    @staticmethod
    def calculate_total_project_days(project):
        """
        Calculate the total number of days of the project.

        Formula:

        deadline - start_date
        """

        total_days = (
            project.deadline - project.start_date
        ).days

        return total_days

    # ------------------------------------------------------------
    # Elapsed Days
    # ------------------------------------------------------------

    @staticmethod
    def calculate_time_elapsed(project, today=None):
        """
        Calculate how many days have passed since the project started.

        If the project has not started yet, return 0.

        Args:
            project: Project object.
            today: Optional date used for testing.
                   If not provided, today's date is used.
        """

        if today is None:
            today = date.today()

        # If project starts in the future,
        # no time has passed yet.
        if today < project.start_date:
            return 0

        elapsed_days = (
            today - project.start_date
        ).days

        return elapsed_days

    # ------------------------------------------------------------
    # Remaining Days
    # ------------------------------------------------------------

    @staticmethod
    def calculate_time_remaining(project, today=None):
        """
        Calculate the number of days remaining until the deadline.

        Positive value:
            Days remaining

        Zero:
            Deadline is today

        Negative value:
            Number of days overdue
        """

        if today is None:
            today = date.today()

        remaining_days = (
            project.deadline - today
        ).days

        return remaining_days

    # ------------------------------------------------------------
    # Time Progress
    # ------------------------------------------------------------

    @staticmethod
    def calculate_time_progress(project, today=None):
        """
        Calculate the percentage of project time that has passed.

        Example:

        Project duration = 20 days
        Elapsed days = 5

        Time progress = 25%
        """

        total_days = Calculator.calculate_total_project_days(
            project
        )

        # Prevent division by zero.
        if total_days <= 0:
            return 0.0

        elapsed_days = Calculator.calculate_time_elapsed(
            project,
            today
        )

        time_progress = (
            elapsed_days / total_days
        ) * 100

        # Keep the result between 0 and 100.
        time_progress = max(
            0.0,
            min(100.0, time_progress)
        )

        return time_progress

    # ------------------------------------------------------------
    # Schedule Gap
    # ------------------------------------------------------------

    @staticmethod
    def calculate_schedule_gap(project, today=None):
        """
        Calculate the difference between time progress
        and project progress.

        Formula:

        Schedule Gap =
        Time Progress - Project Progress

        Positive value:
            Project is behind schedule.

        Zero:
            Project is on schedule.

        Negative value:
            Project is ahead of schedule.
        """

        project_progress = (
            Calculator.calculate_project_progress(project)
        )

        time_progress = (
            Calculator.calculate_time_progress(
                project,
                today
            )
        )

        schedule_gap = (
            time_progress - project_progress
        )

        return schedule_gap

    # ------------------------------------------------------------
    # Project Status
    # ------------------------------------------------------------

    @staticmethod
    def get_project_status(project, today=None):
        """
        Determine the current project status.

        Possible values:

        "not_started"
        "in_progress"
        "completed"
        "overdue"
        """

        if today is None:
            today = date.today()

        progress = Calculator.calculate_project_progress(
            project
        )

        # If project is 100% complete,
        # it is completed regardless of deadline.
        if progress >= 100:
            return "completed"

        # If deadline has passed and the project
        # is not complete, it is overdue.
        if today > project.deadline:
            return "overdue"

        # If progress is 0%, project has not started.
        if progress <= 0:
            return "not_started"

        # Otherwise, it is currently in progress.
        return "in_progress"

    # ------------------------------------------------------------
    # Is Project Overdue?
    # ------------------------------------------------------------

    @staticmethod
    def is_project_overdue(project, today=None):
        """
        Check whether the project is overdue.

        A completed project is never overdue.
        """

        if today is None:
            today = date.today()

        progress = Calculator.calculate_project_progress(
            project
        )

        if progress >= 100:
            return False

        return today > project.deadline

    # ------------------------------------------------------------
    # Disaster Index
    # ------------------------------------------------------------

    @staticmethod
    def calculate_disaster_index(project, today=None):
        """
        Calculate the project Disaster Index.

        The score is based on:

        1. Schedule Gap       -> 50 points
        2. Overdue Tasks      -> 30 points
        3. Overdue Task Weight -> 20 points

        Final result:
            0 to 100

        Disaster levels:

            0 - 30   -> Safe
            31 - 70  -> Warning
            71 - 100 -> Danger
        """

        if today is None:
            today = date.today()

        # First check project progress.
        project_progress = (
            Calculator.calculate_project_progress(project)
        )

        # A completed project has no disaster.
        if project_progress >= 100:
            return 0.0

        # --------------------------------------------------------
        # 1. Schedule Gap Score
        # --------------------------------------------------------

        time_progress = (
            Calculator.calculate_time_progress(
                project,
                today
            )
        )

        schedule_gap = (
            time_progress - project_progress
        )

        # Only a positive gap creates risk.
        positive_gap = max(schedule_gap, 0.0)

        gap_score = (
            positive_gap / 100.0
        ) * 50.0

        # --------------------------------------------------------
        # 2. Overdue Tasks
        # --------------------------------------------------------

        # If there are no tasks,
        # there is no task-based risk.
        if not project.tasks:
            return max(
                0.0,
                min(100.0, gap_score)
            )

        overdue_tasks = []

        for task in project.tasks:

            # If task has no deadline,
            # it cannot be considered overdue.
            if task.deadline is None:
                continue

            # A completed task cannot be overdue.
            if task.is_completed():
                continue

            # Check if task deadline has passed.
            if task.deadline < today:
                overdue_tasks.append(task)

        # --------------------------------------------------------
        # 3. Overdue Task Ratio
        # --------------------------------------------------------

        overdue_task_ratio = (
            len(overdue_tasks)
            / len(project.tasks)
        )

        task_score = (
            overdue_task_ratio * 30.0
        )

        # --------------------------------------------------------
        # 4. Overdue Weight Ratio
        # --------------------------------------------------------

        total_weight = sum(
            task.weight for task in project.tasks
        )

        overdue_weight = sum(
            task.weight
            for task in overdue_tasks
        )

        if total_weight > 0:
            overdue_weight_ratio = (
                overdue_weight / total_weight
            )
        else:
            overdue_weight_ratio = 0.0

        weight_score = (
            overdue_weight_ratio * 20.0
        )

        # --------------------------------------------------------
        # Final Disaster Index
        # --------------------------------------------------------

        disaster_index = (
            gap_score
            + task_score
            + weight_score
        )

        # Keep the final value between 0 and 100.
        disaster_index = max(
            0.0,
            min(100.0, disaster_index)
        )

        return disaster_index

    # ------------------------------------------------------------
    # Disaster Level
    # ------------------------------------------------------------

    @staticmethod
    def get_disaster_level(disaster_index):
        """
        Convert the Disaster Index number into a readable level.

        Returns:
            "safe"
            "warning"
            "danger"
        """

        if disaster_index <= 30:
            return "safe"

        if disaster_index <= 70:
            return "warning"

        return "danger"
