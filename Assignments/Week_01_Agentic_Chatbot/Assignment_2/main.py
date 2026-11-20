"""
Lab 1 — Assignment 2: Detect a Scheduling Conflict

The schedule tool reports Wednesday and Friday as busy.
The agent checks whether those days are included in the student's
unavailable days. It reports conflicts before generating a final plan.

For this deterministic demonstration, the simulated user resolves the
conflict by marking the busy days unavailable.
"""

import json


SIMULATED_ANSWERS = {
    "subjects": ["Data Structures", "Operating Systems", "AI Agents"],
    "hours_per_day": 2,
    "unavailable_days": ["Sunday"],
}


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
        return self.goal["schedule_generated"] is True

    def read_existing_schedule(self):
        if "error" in self.existing_schedule:
            raise RuntimeError(
                f"Schedule tool failed: {self.existing_schedule['error']}"
            )
        return self.existing_schedule

    def _build_plan(self, busy_slots):
        days = [
            day for day in self.DAYS
            if day not in self.goal["unavailable_days"]
        ]
        subjects = self.goal["subjects"]
        if not subjects:
            raise ValueError("At least one subject is required.")

        busy_days = busy_slots.get("busy_days", [])
        plan = {}

        for index, day in enumerate(days):
            subject = subjects[index % len(subjects)]
            time_slot = "17:00-19:00"
            if day in busy_days:
                time_slot = "20:00-22:00"

            plan[day] = {
                "subject": subject,
                "time": time_slot,
                "duration_hours": self.goal["hours_per_day"],
            }

        return plan



class ConflictAwareStudyPlannerAgent(StudyPlannerAgent):
    def __init__(self, existing_schedule):
        super().__init__(existing_schedule)
        self.conflicts = []

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

    def detect_conflicts(self, busy_slots):
        unavailable = set(self.goal["unavailable_days"] or [])
        busy_days = set(busy_slots.get("busy_days", []))
        self.conflicts = sorted(
            busy_days - unavailable,
            key=self.DAYS.index
        )
        return self.conflicts

    def run(self):
        # Collect the student's requirements.
        for field in ("subjects", "hours_per_day", "unavailable_days"):
            if self.goal[field] is None:
                answer = SIMULATED_ANSWERS[field]
                self.goal[field] = answer.copy() if isinstance(answer, list) else answer
                self.add_log(
                    f"ask for {field}",
                    f"collected user response for {field}",
                    self.goal[field],
                )

        if not self.goal["subjects"]:
            raise ValueError("At least one subject is required.")
        if not isinstance(self.goal["hours_per_day"], (int, float)) or not (
            0 < self.goal["hours_per_day"] <= 24
        ):
            raise ValueError("Study hours per day must be between 0 and 24.")
        if not all(day in self.DAYS for day in self.goal["unavailable_days"]):
            raise ValueError("Unavailable days must be valid weekday names.")

        busy = self.read_existing_schedule()
        self.add_log(
            "read existing schedule",
            "tool call: read_existing_schedule()",
            busy,
        )

        conflicts = self.detect_conflicts(busy)

        if conflicts:
            print("SCHEDULING CONFLICT DETECTED!")
            print("Busy days not marked unavailable:", ", ".join(conflicts))
            print("The plan will not be finalized until these conflicts are resolved.")

            # Simulated user resolution for this reproducible demonstration.
            print("\nSimulated resolution: marking conflicting days unavailable.")
            self.goal["unavailable_days"].extend(conflicts)
            self.goal["unavailable_days"] = sorted(
                set(self.goal["unavailable_days"]),
                key=self.DAYS.index,
            )
            print("Updated unavailable days:", self.goal["unavailable_days"])

            self.add_log(
                "resolve reported scheduling conflicts",
                "marked conflicting busy days unavailable",
                self.goal["unavailable_days"].copy(),
            )
        else:
            print("No scheduling conflicts detected.")

        # Generate the plan only after the conflict check and resolution.
        self.plan = self._build_plan(busy)
        self.goal["schedule_generated"] = True
        self.add_log(
            "generate conflict-free weekly plan",
            "built weekly plan after conflict check",
            self.plan.copy(),
            stopped=True,
            stop_reason="all reported conflicts were resolved",
        )
        return self.plan


if __name__ == "__main__":
    agent = ConflictAwareStudyPlannerAgent(
        existing_schedule={"busy_days": ["Wednesday", "Friday"]}
    )

    final_plan = agent.run()

    print("\n=== Final conflict-checked plan ===")
    print(json.dumps(final_plan, indent=2))

    print("\n=== Full iteration log ===")
    print(json.dumps(agent.log, indent=2))