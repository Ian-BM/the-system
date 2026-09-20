"""Celibacy streak (Mind track) computation and StreakRecord bookkeeping."""

from datetime import timedelta

from .models import DailyQuest, StreakRecord
from .quests import CELIBACY_QUEST_ID


def current_streak_days(today):
    """Count consecutive completed days for the celibacy quest, walking
    backward from `today`. A day with no record counts as a miss."""
    streak = 0
    d = today
    completed_dates = set(
        DailyQuest.objects.filter(
            quest_id=CELIBACY_QUEST_ID, completed=True, date__lte=today
        ).values_list("date", flat=True)
    )
    while d in completed_dates:
        streak += 1
        d -= timedelta(days=1)
    return streak


def last_n_days_status(today, n=30):
    """Return a list of {date, status} for the last n days, oldest first.
    status is 'kept', 'missed', or 'pending' (today/future, not yet marked)."""
    records = {
        r.date: r.completed
        for r in DailyQuest.objects.filter(
            quest_id=CELIBACY_QUEST_ID,
            date__gte=today - timedelta(days=n - 1),
            date__lte=today,
        )
    }
    days = []
    for i in range(n - 1, -1, -1):
        d = today - timedelta(days=i)
        if d == today and d not in records:
            status = "pending"
        elif records.get(d, False):
            status = "kept"
        else:
            status = "missed"
        days.append({"date": d, "status": status})
    return days


def sync_streak_record(for_date, completed):
    """Keep StreakRecord history in sync when the celibacy quest is toggled
    for `for_date`. Called right after the DailyQuest row is saved."""
    active = StreakRecord.objects.filter(broken_date__isnull=True).order_by("-start_date").first()

    if completed:
        if active is None:
            StreakRecord.objects.create(start_date=for_date)
        elif for_date < active.start_date:
            active.start_date = for_date
            active.save(update_fields=["start_date"])
    else:
        if active is not None and for_date >= active.start_date:
            if for_date == active.start_date:
                active.delete()
            else:
                active.broken_date = for_date
                active.save(update_fields=["broken_date"])
