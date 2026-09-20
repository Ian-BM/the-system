from django.contrib import admin

from .models import (
    AppConfig,
    DailyQuest,
    JournalEntry,
    ScoldSeen,
    StreakRecord,
    TradingEntry,
    WeightEntry,
)


@admin.register(AppConfig)
class AppConfigAdmin(admin.ModelAdmin):
    list_display = ("key", "value")


@admin.register(DailyQuest)
class DailyQuestAdmin(admin.ModelAdmin):
    list_display = ("date", "quest_id", "completed", "updated_at")
    list_filter = ("completed", "date")
    ordering = ("-date", "quest_id")


@admin.register(WeightEntry)
class WeightEntryAdmin(admin.ModelAdmin):
    list_display = ("date", "weight_kg", "created_at")
    ordering = ("-date",)


@admin.register(TradingEntry)
class TradingEntryAdmin(admin.ModelAdmin):
    list_display = ("date", "amount_usd", "created_at")
    ordering = ("-date",)


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ("date", "created_at")
    ordering = ("-created_at",)


@admin.register(StreakRecord)
class StreakRecordAdmin(admin.ModelAdmin):
    list_display = ("start_date", "broken_date")
    ordering = ("-start_date",)


@admin.register(ScoldSeen)
class ScoldSeenAdmin(admin.ModelAdmin):
    list_display = ("date", "seen_at")
    ordering = ("-date",)
