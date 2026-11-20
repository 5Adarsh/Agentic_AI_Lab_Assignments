
from datetime import datetime

FAQ_DB = {
    "wifi": "Connect to 'Campus-Secure' and log in with your student ID.",
    "library": "The central library is open from 8:00 AM to 8:00 PM on weekdays.",
}
TICKET_DB = []


# ----------------------------- Tools ---------------------------------

def tool_search_faq(query):
    """Search the local FAQ without inventing an answer."""
    if not isinstance(query, str):
        return {"found": False}

    normalized_query = query.lower()
    for keyword, answer in FAQ_DB.items():
        if keyword in normalized_query:
            return {
                "found": True,
                "answer": answer,
                "matched_keyword": keyword,
            }
    return {"found": False}


def tool_create_ticket(issue):
    """Create an in-memory support ticket."""
    if not isinstance(issue, str) or not issue.strip():
        raise ValueError("A ticket requires a non-empty issue description.")

    ticket_id = f"T-{len(TICKET_DB) + 1:03d}"
    ticket = {
        "id": ticket_id,
        "issue": issue.strip(),
        "status": "open",
    }
    TICKET_DB.append(ticket)
    return {"ticket_id": ticket_id}


def tool_check_ticket_status(ticket_id):
    """Look up a ticket by its ID."""
    for ticket in TICKET_DB:
        if ticket["id"] == ticket_id:
            return ticket.copy()
    return {"error": "not found"}


# -------------------------- Reusable skill ----------------------------

def triage_skill(issue_text):
    """Search the FAQ first; escalate only when no FAQ match exists."""
    faq_result = tool_search_faq(issue_text)

    if faq_result["found"]:
        return {
            "resolution": "faq",
            "answer": faq_result["answer"],
            "matched_keyword": faq_result["matched_keyword"],
        }

    ticket = tool_create_ticket(issue_text)
    return {
        "resolution": "escalated",
        "ticket_id": ticket["ticket_id"],
    }


# ----------------------------- Memory --------------------------------

class CapstoneMemory:
    """Short-term session state and long-term interaction history."""

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

    results = []

    for issue, expected in cases:
        result = node_graph_run(
            "eval_user", issue, memory, audit_log, prompt_log
        )

        if result["rejected"]:
            actual = "rejected"
        else:
            actual = result["outcome"]["resolution"]

        results.append({
            "issue": issue,
            "expected": expected,
            "actual": actual,
            "passed": actual == expected,
        })

    return results


# ----------------------------- Main demo ------------------------------

def main():
    memory = CapstoneMemory()
    audit_log = []
    prompt_log = []

    print("=== Run 1: FAQ match ===")
    r1 = node_graph_run(
        "alice",
        "How do I connect to wifi on campus?",
        memory,
        audit_log,
        prompt_log,
    )
    print(r1)

    print("\n=== Run 2: Escalation (no FAQ match) ===")
    r2 = node_graph_run(
        "bob",
        "My laptop charger is broken",
        memory,
        audit_log,
        prompt_log,
    )
    print(r2)

    print("\n=== Run 3: Ticket status tool ===")
    ticket_id = r2["outcome"]["ticket_id"]
    print(tool_check_ticket_status(ticket_id))

    print("\n=== Run 4: Safety control rejects empty input ===")
    print(node_graph_run("carol", " ", memory, audit_log, prompt_log))

    print("\n=== Evaluation ===")
    results = run_evaluation()
    for item in results:
        status = "PASS" if item["passed"] else "FAIL"
        print(
            f"[{status}] {item['issue']!r} -> {item['actual']} "
            f"(expected {item['expected']})"
        )

    print("\n=== Prompt log ===")
    for item in prompt_log:
        print(item)

    print("\n=== Audit log ===")
    for item in audit_log:
        print(item)

    print("\n=== Long-term memory / history ===")
    for item in memory.history:
        print(item)

    print("\n=== Short-term session memory ===")
    print(memory.session)

    print("\n=== Architecture / node graph ===")
    print(
        "intake -> safety_check -> triage_skill -> "
        "respond -> memory/audit_log"
    )
    print(
        "Tools: tool_search_faq, tool_create_ticket, "
        "tool_check_ticket_status"
    )
    print("Reusable skill: triage_skill")

    print("\n=== Limitations & next-step roadmap ===")
    print("- FAQ matching is keyword-based, not semantic.")
    print("- Tickets and memory are in-memory and reset when the process exits.")
    print("- No human approval workflow exists for high-priority incidents.")
    print(
        "- Next: add retrieval-based FAQ search, priority classification, "
        "persistent storage, and human approval for critical tickets."
    )



if __name__ == "__main__":
    main()
