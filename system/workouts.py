"""
7-day workout schedule. The schedule automatically switches from home
workouts (week 1 style) to a gym Push/Pull/Legs rotation once the app
crosses settings.GYM_CUTOVER_DATE.
"""

from datetime import date, timedelta

from django.conf import settings

HOME_SCHEDULE = {
    0: ("Full Body Home Circuit", "Bodyweight squats, push-ups, rows, plank circuit"),
    1: ("Cardio + Core", "20-30 min cardio + core finisher"),
    2: ("Upper Body Home", "Push-ups, pike push-ups, bodyweight rows, dips"),
    3: ("Lower Body Home", "Squats, lunges, glute bridges, calf raises"),
    4: ("Full Body Home Circuit", "Bodyweight squats, push-ups, rows, plank circuit"),
    5: ("Active Recovery / Walk", "Long walk, light stretching, mobility work"),
    6: ("Rest", "Full rest day — recovery"),
}

GYM_PPL_SCHEDULE = {
    0: ("Push", "Chest, shoulders, triceps"),
    1: ("Pull", "Back, biceps"),
    2: ("Legs", "Quads, hamstrings, glutes, calves"),
    3: ("Push", "Chest, shoulders, triceps"),
    4: ("Pull", "Back, biceps"),
    5: ("Legs", "Quads, hamstrings, glutes, calves"),
    6: ("Rest", "Full rest day — recovery"),
}

WEEKDAY_LABELS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def get_cutover_date():
    raw = settings.GYM_CUTOVER_DATE
    if isinstance(raw, date):
        return raw
    year, month, day = (int(p) for p in str(raw).split("-"))
    return date(year, month, day)


def is_gym_phase(for_date):
    return for_date >= get_cutover_date()


def get_workout_for_date(for_date):
    schedule = GYM_PPL_SCHEDULE if is_gym_phase(for_date) else HOME_SCHEDULE
    weekday = for_date.weekday()
    title, detail = schedule[weekday]
    return {
        "weekday": WEEKDAY_LABELS[weekday],
        "title": title,
        "detail": detail,
        "phase": "Gym — Push/Pull/Legs" if is_gym_phase(for_date) else "Home Workouts",
    }


def get_week_schedule(start_date):
    return [get_workout_for_date(start_date + timedelta(days=i)) for i in range(7)]
