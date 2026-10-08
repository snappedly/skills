# Triage roles

Snappedly skills use five canonical triage state roles. Map each state role to a label, field value, or status on this repository's work tracker. Record the operation that sets it.

| Canonical role | Tracker value | Operation | Meaning |
| --- | --- | --- | --- |
| `needs-triage` | label `needs-triage` | replace state label | A maintainer needs to evaluate the work. |
| `needs-info` | label `needs-info` | replace state label | The reporter must provide more information. |
| `ready-for-agent` | label `ready-for-agent` | replace state label | The work is specified and ready for an agent. |
| `ready-for-human` | label `ready-for-human` | replace state label | The work needs human implementation or judgment. |
| `wontfix` | label `wontfix` | replace state label | The team will not action the work. |

Replace these defaults when the tracker uses another representation. The two category roles, `bug` and `enhancement`, are mapped in `docs/agents/issue-tracker.md`. Each triaged item carries exactly one state role and one category role.
