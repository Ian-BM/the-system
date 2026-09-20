from django.db import models


class AppConfig(models.Model):
    """Simple key/value store for app-wide config: PIN hash, start date, etc."""

    key = models.CharField(max_length=100, unique=True)
    value = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = "App Config"
        verbose_name_plural = "App Config"

    def __str__(self):
        return self.key


class DailyQuest(models.Model):
    """Completion record for one quest on one date. Rows only exist once a
    quest has been toggled — an absent row means the quest is incomplete."""

    date = models.DateField()
    quest_id = models.PositiveSmallIntegerField()
    completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("date", "quest_id")
        indexes = [models.Index(fields=["date"])]
        ordering = ["date", "quest_id"]

    def __str__(self):
        return f"{self.date} — quest {self.quest_id} — {'done' if self.completed else 'missed'}"


class WeightEntry(models.Model):
    date = models.DateField()
    weight_kg = models.DecimalField(max_digits=5, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.date}: {self.weight_kg}kg"


class TradingEntry(models.Model):
    date = models.DateField()
    amount_usd = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.date}: ${self.amount_usd}"


class JournalEntry(models.Model):
    date = models.DateField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.date} journal entry"


class StreakRecord(models.Model):
    """Historical record of celibacy streaks (Mind track)."""

    start_date = models.DateField()
    broken_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-start_date"]

    @property
    def is_active(self):
        return self.broken_date is None

    def __str__(self):
        status = "active" if self.is_active else f"broken {self.broken_date}"
        return f"Streak from {self.start_date} ({status})"


class ScoldSeen(models.Model):
    """Marks which dates the accountability modal has already been shown
    and dismissed for, so it never repeats."""

    date = models.DateField(unique=True)
    seen_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Scold seen for {self.date}"
