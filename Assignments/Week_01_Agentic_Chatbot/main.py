import json

SIMULATED_ANSWERS = {
    "subjects": ["Data Structures", "Operating Systems", "AI Agents"],
    "hours_per_day": 2,
    "unavailable_days": ["Sunday"],
}

SIMULATED_FEEDBACK = "Move Tuesday's session to the evening."


class StudyPlannerAgent:
    DAYS = [
        "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday"
    ]

    def __init__(self, existing_schedule):
        self.goal = {
            "subjects": None,
            "hours_per_day": None,
            "unavailable_days": None,
            "schedule_generated": False,
        }
        self.existing_schedule = existing_schedule
        self.plan = None
        self.log = []

    def satisfied(self):
        return self.goal["schedule_generated"]

    def next_step(self):
        for field in ("subjects", "hours_per_day", "unavailable_days"):
            if self.goal[field] is None:
                return "ask", field
        return "generate_plan", None

    def read_existing_schedule(self):
        if "error" in self.existing_schedule:
            raise RuntimeError(
                f"Schedule tool failed: {self.existing_schedule['error']}"
            )
        return self.existing_schedule

    def validate_requirements(self):
        subjects = self.goal["subjects"]
        hours = self.goal["hours_per_day"]
        unavailable = self.goal["unavailable_days"]

        if not isinstance(subjects, list) or not subjects:
            raise ValueError("At least one subject must be provided.")
        if not all(isinstance(subject, str) and subject.strip() for subject in subjects):
            raise ValueError("Every subject must be a non-empty string.")
        if not isinstance(hours, (int, float)) or hours <= 0 or hours > 24:
            raise ValueError("Study hours per day must be between 0 and 24.")
        if not isinstance(unavailable, list):
            raise ValueError("Unavailable days must be provided as a list.")
        if not all(day in self.DAYS for day in unavailable):
            raise ValueError("Unavailable days must contain valid weekday names.")

    def add_log(self, planned, action, observed, stopped=False, stop_reason=None):
        entry = {
            "iteration": len(self.log) + 1,
            "planned": planned,
            "action": action,
            "observed": observed,
            "stopped": stopped,
        }
        if stop_reason:
            entry["stop_reason"] = stop_reason
        self.log.append(entry)

    def run(self):
        while not self.satisfied():
            step, argument = self.next_step()

            if step == "ask":
                answer = SIMULATED_ANSWERS[argument]
                self.goal[argument] = answer
                self.add_log(
                    f"ask for {argument}",
                    f"collected user response for {argument}",
                    answer,
                )

            elif step == "generate_plan":
                self.validate_requirements()
                busy = self.read_existing_schedule()
                self.add_log(
                    "read existing schedule before generating plan",
                    "tool call: read_existing_schedule()",
                    busy,
                )

                self.plan = self._build_plan(busy)
                self.goal["schedule_generated"] = True