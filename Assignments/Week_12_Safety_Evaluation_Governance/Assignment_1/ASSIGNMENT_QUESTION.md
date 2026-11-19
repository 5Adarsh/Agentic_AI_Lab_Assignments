# Assignment 1 — A Cost-Category Control

Add a cost estimate to each proposed action and a budget threshold. Reject any proposal whose estimated cost exceeds the threshold unless a separate `finance_approved` flag is set. Write an adversarial test that attempts to bypass this by omitting the cost estimate entirely, and confirm it is rejected rather than defaulting to approved.
