# Assignment 1 — Add Per-User Rate Limiting

Add a new control: each user may run at most 3 tasks per session. Implement this as a check inside `receive_task` (or a thin wrapper around it) without changing `run_task`'s core loop signature or its skill-dispatch logic. Submit the updated code and a transcript showing a 4th task being rejected.
