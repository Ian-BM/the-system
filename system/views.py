import json
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from . import auth, ranks, workouts, mind_schedule
from .models import (
    DailyQuest,
    JournalEntry,
    ScoldSeen,
    StreakRecord,
    TradingEntry,
    WeightEntry,
)
from .quests import QUESTS, QUESTS_BY_ID, quests_by_category
from .scold import dismiss_scold, get_pending_scold
from .streaks import current_streak_days, last_n_days_status, sync_streak_record


# ---------------------------------------------------------------------------
# Auth views
# ---------------------------------------------------------------------------


class SetupView(View):
    """First-run screen: create the 4-digit PIN."""

    template_name = "system/setup.html"

    def get(self, request):
        if auth.pin_is_set():
            return redirect("system:login")
        return render(request, self.template_name, {})

    def post(self, request):
        if auth.pin_is_set():
            return redirect("system:login")

        pin = request.POST.get("pin", "").strip()
        confirm = request.POST.get("confirm", "").strip()

        error = None
        if not (pin.isdigit() and len(pin) == 4):
            error = "PIN must be exactly 4 digits."
        elif pin != confirm:
            error = "PINs do not match."

        if error:
            return render(request, self.template_name, {"error": error})

        auth.set_pin(pin)
        auth.set_config(auth.START_DATE_KEY, timezone.localdate().isoformat())
        auth.log_in(request)
        return redirect("system:dashboard")


class LoginView(View):
    template_name = "system/pin_login.html"

    def get(self, request):
        if not auth.pin_is_set():
            return redirect("system:setup")
        if auth.is_authenticated(request):
            return redirect("system:dashboard")
        return render(request, self.template_name, {})

    def post(self, request):
        if not auth.pin_is_set():
            return redirect("system:setup")

        pin = request.POST.get("pin", "").strip()
        if auth.check_pin(pin):
            auth.log_in(request)
            return redirect("system:dashboard")
        return render(request, self.template_name, {"error": "Incorrect PIN."})


class LogoutView(View):
    def post(self, request):
        auth.log_out(request)
        return redirect("system:login")

    def get(self, request):
        auth.log_out(request)
        return redirect("system:login")


# ---------------------------------------------------------------------------
# Shared mixin
# ---------------------------------------------------------------------------


class RequireAuthMixin:
    def dispatch(self, request, *args, **kwargs):
        if not auth.pin_is_set():
            return redirect("system:setup")
        if not auth.is_authenticated(request):
            return redirect("system:login")
        return super().dispatch(request, *args, **kwargs)


# ---------------------------------------------------------------------------
# Main pages
# ---------------------------------------------------------------------------


class DashboardView(RequireAuthMixin, TemplateView):
    template_name = "system/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = timezone.localdate()

        grouped = quests_by_category()
        completed_ids = set(
            DailyQuest.objects.filter(date=today, completed=True).values_list(
                "quest_id", flat=True
            )
        )
        for cat, qlist in grouped.items():
            for q in qlist:
                q["completed"] = q["id"] in completed_ids

        latest_weight = WeightEntry.objects.order_by("-date", "-created_at").first()
        weight_kg = float(latest_weight.weight_kg) if latest_weight else 130.0
        weight_start = 130
        weight_goal = 85
        span = weight_start - weight_goal
        progress_pct = max(0, min(100, (weight_start - weight_kg) / span * 100)) if span else 0

        streak_days = current_streak_days(today)
        total_earned = sum((t.amount_usd for t in TradingEntry.objects.all()), Decimal("0"))
        best_day = TradingEntry.objects.order_by("-amount_usd").values_list(
            "amount_usd", flat=True
        ).first() or Decimal("0")

        body_r = ranks.body_rank(weight_kg)
        mind_r = ranks.mind_rank(streak_days)
        money_r = ranks.money_rank(total_earned, best_day)

        ctx.update(
            {
                "grouped_quests": grouped,
                "today": today,
                "weight_kg": weight_kg,
                "weight_start": weight_start,
                "weight_goal": weight_goal,
                "progress_pct": round(progress_pct),
                "body_rank": body_r,
                "mind_rank": mind_r,
                "money_rank": money_r,
                "streak_days": streak_days,
            }
        )
        return ctx


class BodyView(RequireAuthMixin, TemplateView):
    template_name = "system/body.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = timezone.localdate()

        entries = WeightEntry.objects.order_by("-date")[:14]
        latest_weight = entries[0] if entries else None
        weight_kg = float(latest_weight.weight_kg) if latest_weight else 130.0

        rank, next_rank, pct = ranks.body_rank_progress(weight_kg)

        week_schedule = workouts.get_week_schedule(today)
        today_workout = workouts.get_workout_for_date(today)

        ctx.update(
            {
                "entries": entries,
                "weight_kg": weight_kg,
                "body_rank": rank,
                "body_next_rank": next_rank,
                "body_progress_pct": pct,
                "week_schedule": week_schedule,
                "today_workout": today_workout,
                "rank_bands": [
                    ("F", "130kg+"),
                    ("E", "110-130kg"),
                    ("D", "95-110kg"),
                    ("C", "85-95kg"),
                    ("B", "75-85kg"),
                    ("A", "65-75kg"),
                ],
            }
        )
        return ctx


class MindView(RequireAuthMixin, TemplateView):
    template_name = "system/mind.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = timezone.localdate()

        streak_days = current_streak_days(today)
        dot_grid = last_n_days_status(today, 30)
        rank, next_rank, pct = ranks.mind_rank_progress(streak_days)

        week_schedule = mind_schedule.get_week_schedule(today - timedelta(days=today.weekday()))
        today_focus = mind_schedule.get_mind_focus_for_date(today)

        best_streak = 0
        for record in StreakRecord.objects.all():
            end = record.broken_date or today
            length = (end - record.start_date).days
            if record.is_active:
                length = streak_days
            best_streak = max(best_streak, length)

        ctx.update(
            {
                "streak_days": streak_days,
                "best_streak": best_streak,
                "dot_grid": dot_grid,
                "mind_rank": rank,
                "mind_next_rank": next_rank,
                "mind_progress_pct": pct,
                "week_schedule": week_schedule,
                "today_focus": today_focus,
                "rank_bands": [
                    ("F", "0-9 days"),
                    ("E", "10-29 days"),
                    ("D", "30-59 days"),
                    ("C", "60-101 days"),
                    ("B", "102+ days"),
                    ("A", "Full mastery"),
                ],
            }
        )
        return ctx


class MoneyView(RequireAuthMixin, TemplateView):
    template_name = "system/money.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        entries = TradingEntry.objects.order_by("-date")[:30]
        all_entries = TradingEntry.objects.all()
        total_earned = sum((t.amount_usd for t in all_entries), Decimal("0"))
        trading_days = all_entries.count()
        best_day = max((t.amount_usd for t in all_entries), default=Decimal("0"))

        rank, next_rank, pct = ranks.money_rank_progress(total_earned, best_day)

        ctx.update(
            {
                "entries": entries,
                "total_earned": total_earned,
                "trading_days": trading_days,
                "best_day": best_day,
                "money_rank": rank,
                "money_next_rank": next_rank,
                "money_progress_pct": pct,
                "rank_bands": [
                    ("F", "$0"),
                    ("E", "First $200 day"),
                    ("D", "$10,000 total"),
                    ("C", "$50,000 total"),
                    ("B", "$200,000 total"),
                    ("A", "Scale beyond"),
                ],
            }
        )
        return ctx


class LogView(RequireAuthMixin, TemplateView):
    template_name = "system/log.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["entries"] = JournalEntry.objects.order_by("-created_at")[:100]
        ctx["today"] = timezone.localdate()
        return ctx


# ---------------------------------------------------------------------------
# API / AJAX endpoints
# ---------------------------------------------------------------------------


class ToggleQuestView(RequireAuthMixin, View):
    def post(self, request):
        try:
            payload = json.loads(request.body or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        quest_id = payload.get("quest_id")
        if quest_id not in QUESTS_BY_ID:
            return JsonResponse({"error": "Unknown quest_id"}, status=400)

        target_date = timezone.localdate()

        record, _ = DailyQuest.objects.get_or_create(
            date=target_date, quest_id=quest_id, defaults={"completed": False}
        )
        record.completed = not record.completed
        record.save(update_fields=["completed", "updated_at"])

        from .quests import CELIBACY_QUEST_ID

        if quest_id == CELIBACY_QUEST_ID:
            sync_streak_record(target_date, record.completed)

        completed_today = DailyQuest.objects.filter(date=target_date, completed=True).count()

        return JsonResponse(
            {
                "quest_id": quest_id,
                "completed": record.completed,
                "quests_done": completed_today,
                "quests_total": len(QUESTS),
            }
        )


class SaveWeightView(RequireAuthMixin, View):
    def post(self, request):
        try:
            payload = json.loads(request.body or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        try:
            weight = Decimal(str(payload.get("weight_kg")))
        except (InvalidOperation, TypeError):
            return JsonResponse({"error": "Invalid weight"}, status=400)

        if weight <= 0 or weight > 400:
            return JsonResponse({"error": "Weight out of range"}, status=400)

        target_date = timezone.localdate()
        entry, created = WeightEntry.objects.update_or_create(
            date=target_date, defaults={"weight_kg": weight}
        )

        rank, next_rank, pct = ranks.body_rank_progress(float(weight))

        return JsonResponse(
            {
                "weight_kg": float(entry.weight_kg),
                "date": entry.date.isoformat(),
                "body_rank": rank,
                "body_next_rank": next_rank,
                "body_progress_pct": pct,
            }
        )


class SaveTradingView(RequireAuthMixin, View):
    def post(self, request):
        try:
            payload = json.loads(request.body or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        try:
            amount = Decimal(str(payload.get("amount_usd")))
        except (InvalidOperation, TypeError):
            return JsonResponse({"error": "Invalid amount"}, status=400)

        entry_date_raw = payload.get("date")
        if entry_date_raw:
            y, m, d = (int(p) for p in entry_date_raw.split("-"))
            entry_date = date(y, m, d)
        else:
            entry_date = timezone.localdate()

        notes = (payload.get("notes") or "").strip()

        entry = TradingEntry.objects.create(date=entry_date, amount_usd=amount, notes=notes)

        all_entries = TradingEntry.objects.all()
        total_earned = sum((t.amount_usd for t in all_entries), Decimal("0"))
        best_day = max((t.amount_usd for t in all_entries), default=Decimal("0"))
        rank, next_rank, pct = ranks.money_rank_progress(total_earned, best_day)

        return JsonResponse(
            {
                "id": entry.id,
                "date": entry.date.isoformat(),
                "amount_usd": float(entry.amount_usd),
                "total_earned": float(total_earned),
                "best_day": float(best_day),
                "trading_days": all_entries.count(),
                "money_rank": rank,
                "money_next_rank": next_rank,
                "money_progress_pct": pct,
            }
        )


class SaveJournalView(RequireAuthMixin, View):
    def post(self, request):
        try:
            payload = json.loads(request.body or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        text = (payload.get("text") or "").strip()
        if not text:
            return JsonResponse({"error": "Journal entry cannot be empty"}, status=400)

        entry = JournalEntry.objects.create(date=timezone.localdate(), text=text)

        return JsonResponse(
            {
                "id": entry.id,
                "date": entry.date.isoformat(),
                "text": entry.text,
                "created_at": timezone.localtime(entry.created_at).strftime("%b %d, %Y — %H:%M"),
            }
        )


class ScoldDismissView(RequireAuthMixin, View):
    def post(self, request):
        try:
            payload = json.loads(request.body or "{}")
        except json.JSONDecodeError:
            payload = {}

        raw_date = payload.get("date")
        if raw_date:
            y, m, d = (int(p) for p in raw_date.split("-"))
            target_date = date(y, m, d)
        else:
            target_date = timezone.localdate() - timedelta(days=1)

        dismiss_scold(target_date)
        return JsonResponse({"dismissed": target_date.isoformat()})
