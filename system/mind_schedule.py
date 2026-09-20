"""Weekly mind-focus theme schedule, shown on the Mind tab."""

WEEKDAY_LABELS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

MIND_FOCUS_SCHEDULE = {
    0: ("Deep Work", "25 min focused block, no distractions, hardest task first"),
    1: ("Discipline Check", "Celibacy + no-phone-before-bed are non-negotiable today"),
    2: ("Reflection", "Journal + gratitude — review what's working"),
    3: ("Deep Work", "25 min focused block, no distractions, hardest task first"),
    4: ("Visualization", "5 min goal visualization, reset intent for the week"),
    5: ("Recovery", "Lighter mental load — protect sleep and screen time"),
    6: ("Full Reset", "Plan the week ahead, no reactive scrolling"),
}


def get_mind_focus_for_date(for_date):
    weekday = for_date.weekday()
    title, detail = MIND_FOCUS_SCHEDULE[weekday]
    return {"weekday": WEEKDAY_LABELS[weekday], "title": title, "detail": detail}


def get_week_schedule(start_date):
    from datetime import timedelta

    return [get_mind_focus_for_date(start_date + timedelta(days=i)) for i in range(7)]
