
    return {"found": False}


def tool_create_ticket(issue):
    """Create an in-memory support ticket."""
    if not isinstance(issue, str) or not issue.strip():
        raise ValueError("A ticket requires a non-empty issue description.")

    ticket_id = f"T-{len(TICKET_DB) + 1:03d}"
    TICKET_DB.append({
        "id": ticket_id,
        "issue": issue.strip(),
        "status": "open",
    })
    return {"ticket_id": ticket_id}


def tool_check_ticket_status(ticket_id):
    """Return a copy of the matching ticket, or an error if it does not exist."""
    for ticket in TICKET_DB:
        if ticket["id"] == ticket_id:
            return ticket.copy()
    return {"error": "not found"}


# ------------------------ Reusable skills ----------------------------

def password_reset_skill(issue_text):
    """Provide password-reset steps.

    Constraint: never request or collect the user's current password or OTP.
    """
    return {
        "resolution": "password_guidance",
        "answer": (
            "Open the university account portal and select 'Forgot Password'. "
            "Verify your identity using your registered email or phone, then "
            "create a new, unique password. Never share your password or OTP "
            "with anyone, including support staff."
        ),
    }


def triage_skill(issue_text):
    """Search the FAQ first; create a ticket only when no FAQ matches."""
    faq = tool_search_faq(issue_text)

    if faq["found"]:
        return {
            "resolution": "faq",
            "answer": faq["answer"],
            "matched_keyword": faq["matched_keyword"],
        }

    ticket = tool_create_ticket(issue_text)
    return {
        "resolution": "escalated",
        "ticket_id": ticket["ticket_id"],
    }


# ----------------------------- Memory --------------------------------

class CapstoneMemory:
    """Maintain current session state and interaction history."""

    def __init__(self):
        self.session = {}
        self.history = []

    def record(self, user, issue, outcome):
        entry = {
            "user": user,
            "issue": issue,
            "outcome": outcome.copy(),
            "date": datetime.now().isoformat(timespec="seconds"),
        }
        self.history.append(entry)
        self.session["last_issue"] = issue
        self.session["last_outcome"] = outcome.copy()

            "rejected": True,
            "reason": "issue text must be a non-empty string",
        }

    normalized_issue = issue.lower()

    # Password-related requests are routed to the dedicated safe skill.
    password_keywords = ("password", "reset")
    if any(keyword in normalized_issue for keyword in password_keywords):
        outcome = password_reset_skill(issue)
        selected_skill = "password_reset_skill"
    else:
        outcome = triage_skill(issue)
        selected_skill = "triage_skill"

    prompt_log.append({
        "stage": "triage",
        "selected_skill": selected_skill,
        "output": outcome.copy(),
    })

    if "answer" in outcome:
        response = outcome["answer"]
    else:
        response = (
            f"Ticket {outcome['ticket_id']} created; support will follow up."
        )

    memory.record(user, issue, outcome)

    audit_log.append({
        "stage": "complete",
        "user": user,
        "skill": selected_skill,
        "issue": issue,
        "outcome": outcome.copy(),
    })

    return {
        "rejected": False,
        "selected_skill": selected_skill,
        "response": response,
        "outcome": outcome,
    }


# ----------------------------- Evaluation ----------------------------

def run_evaluation():
    """Verify password guidance, FAQ routing, escalation, and input safety."""
    memory = CapstoneMemory()
    audit_log = []
    prompt_log = []

    cases = [
        ("alice", "I forgot my password and need a reset",
         "password_reset_skill"),
        ("bob", "How do I connect to campus wifi?",
         "triage_skill"),
        ("carol", "My laptop battery is damaged",
         "triage_skill"),
    ]

    results = []
    for user, issue, expected_skill in cases:
        result = node_graph_run(user, issue, memory, audit_log, prompt_log)
        actual_skill = result.get("selected_skill")
        results.append({
            "issue": issue,
            "expected_skill": expected_skill,
            "actual_skill": actual_skill,
            "passed": actual_skill == expected_skill,
        })

    invalid_result = node_graph_run(
        "dave", " ", memory, audit_log, prompt_log
    )
    results.append({
        "issue": " ",
        "expected_skill": "rejected",
        "actual_skill": (
            "rejected" if invalid_result["rejected"] else "accepted"
        ),
        "passed": invalid_result["rejected"],
    })

    return results


# ----------------------------- Main demo ------------------------------

def main():
    memory = CapstoneMemory()
    audit_log = []
    prompt_log = []

    print("=== Assignment 1: Two-skill routing ===")

    demo_cases = [
        ("alice", "I forgot my password and need a reset"),
        ("bob", "How do I connect to campus wifi?"),
        ("carol", "My laptop battery is damaged"),
    ]

    for user, issue in demo_cases:
        result = node_graph_run(
            user, issue, memory, audit_log, prompt_log
        )
        print(f"\nIssue: {issue}")
        print(f"Selected skill: {result.get('selected_skill')}")
        print(f"Response: {result.get('response', result.get('reason'))}")

    print("\n=== Evaluation ===")
    results = run_evaluation()
    for item in results:
        status = "PASS" if item["passed"] else "FAIL"
        print(
            f"[{status}] {item['issue']!r}: "
            f"{item['actual_skill']} "
            f"(expected {item['expected_skill']})"
        )

    assert all(item["passed"] for item in results), (
        "One or more evaluation cases failed."
    )

    print("\n=== Prompt / routing trace ===")
    for entry in prompt_log:
        print(entry)

    print("\n=== Audit trace ===")
    for entry in audit_log:
        print(entry)

    print("\n=== Session memory ===")
    print(memory.session)

    print("\n=== Interaction history ===")
    for entry in memory.history:
        print(entry)

    print("\n=== Architecture ===")
    print(
        "intake -> safety_check -> skill_router -> "
        "password_reset_skill / triage_skill -> respond -> memory/audit_log"
    )
    print(
        "Tools: tool_search_faq, tool_create_ticket, "
        "tool_check_ticket_status"
    )
    print("Reusable skills: password_reset_skill, triage_skill")
    print("\nAll evaluation cases passed.")


if __name__ == "__main__":
    main()
