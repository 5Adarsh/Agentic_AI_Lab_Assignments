# Assignment 2 — Scope read_file to a Safe Directory

Add a second permission boundary: `read_file` may only read paths inside a declared safe directory (e.g. paths starting with `/safe/`). Write an adversarial test that attempts to read a path outside that directory and confirm the server rejects it with a structured error rather than reading it. Submit the updated code and the adversarial test's result.
