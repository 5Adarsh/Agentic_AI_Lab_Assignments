# Assignment 2 — Escalate After Two Failures

Add a rule: if the same skill fails twice in one session for the same user, the third attempt must escalate to a human instead of retrying the skill again. Implement this using the existing audit log (count prior error entries for that user/skill pair) rather than adding new hidden state. Submit the updated code and a transcript showing two failures followed by an escalation instead of a third attempt.
