ROADMAP_WEEKS = [
    {
        "week_number": 1,
        "block": "Python Foundations",
        "title": "Setup and Python Refresh",
        "goal": "Organize environment and review Python basics",
        "status": "completed",
        "planned_hours": 14,
        "actual_hours": 14,
    },
    {
        "week_number": 2,
        "block": "Python Foundations",
        "title": "Functions and Clean Structure",
        "goal": "Practice functions, validations, and file organization",
        "status": "completed",
        "planned_hours": 14,
        "actual_hours": 13,
    },
    {
        "week_number": 3,
        "block": "Python Foundations",
        "title": "OOP and Domain Modeling",
        "goal": "Model telemetry and AI-related entities",
        "status": "in_progress",
        "planned_hours": 14,
        "actual_hours": 8,
    },
]

for week in range(4, 53):
    ROADMAP_WEEKS.append(
        {
            "week_number": week,
            "block": f"Block {(week - 1) // 8 + 1}",
            "title": f"Week {week} Focus",
            "goal": "Planned objective pending refinement",
            "status": "pending",
            "planned_hours": 14,
            "actual_hours": 0,
        }
    )