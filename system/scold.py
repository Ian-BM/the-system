from datetime import timedelta

from .models import DailyQuest, ScoldSeen
from .quests import QUESTS


def get_pending_scold(today):
    """If yesterday had incomplete quests and hasn't been acknowledged yet,
    return {'date': yesterday, 'missed': [...]}. Otherwise return None."""
    yesterday = today - timedelta(days=1)

    if ScoldSeen.objects.filter(date=yesterday).exists():
        return None

    completed_ids = set(
        DailyQuest.objects.filter(date=yesterday, completed=True).values_list(
            "quest_id", flat=True
        )
    )
    missed = [q for q in QUESTS if q["id"] not in completed_ids]

    if not missed:
        return None

    return {"date": yesterday, "missed": missed}


def dismiss_scold(for_date):
    ScoldSeen.objects.get_or_create(date=for_date)
