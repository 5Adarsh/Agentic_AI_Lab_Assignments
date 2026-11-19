# Assignment 2 — Detect a Scheduling Conflict

Extend `read_existing_schedule` to return a second busy day, then modify `_build_plan` (or add a check before it) so that if the student's chosen unavailable days do not actually avoid every busy day returned by the tool, the agent flags the conflict explicitly to the user before finalizing the plan, rather than silently double-booking. Submit the updated code and a transcript showing the conflict being detected and reported.
