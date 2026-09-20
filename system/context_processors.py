from django.utils import timezone

from .auth import START_DATE_KEY, get_config, is_authenticated
from .models import DailyQuest
from .quests import QUESTS
from .scold import get_pending_scold


def hud(request):
    if not is_authenticated(request):
        return {}

    today = timezone.localdate()

    start_date_raw = get_config(START_DATE_KEY)
    if start_date_raw:
        y, m, d = (int(p) for p in start_date_raw.split("-"))
        from datetime import date

        start_date = date(y, m, d)
        days_active = (today - start_date).days + 1
    else:
        days_active = 1

    quests_completed_today = DailyQuest.objects.filter(date=today, completed=True).count()

    pending_scold = get_pending_scold(today)

    return {
        "hud_today": today,
        "hud_days_active": days_active,
        "hud_quests_done": quests_completed_today,
        "hud_quests_total": len(QUESTS),
        "hud_pending_scold": pending_scold,
    }
