# Assignment 2 — A Safe Auto-Remediation Path

Add a WARNING-level (not ALARM/degraded-critical) scenario where the proposed action is a low-risk `restart_single_pod`. Demonstrate that this low-risk action is allowed to execute automatically (per `risk_level`), while any rollback-class action anywhere in your extended code still always routes through the approval-request path and never auto-executes.
