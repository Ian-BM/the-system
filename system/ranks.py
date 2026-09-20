"""
Rank progression logic for Body, Mind and Money tracks. Each function
returns a single letter rank F-A (F lowest, A highest).
"""

RANK_ORDER = ["F", "E", "D", "C", "B", "A"]

RANK_LABELS = {
    "F": "F-Rank",
    "E": "E-Rank",
    "D": "D-Rank",
    "C": "C-Rank",
    "B": "B-Rank",
    "A": "A-Rank",
}


def body_rank(weight_kg):
    if weight_kg is None:
        return "F"
    if weight_kg >= 130:
        return "F"
    if weight_kg >= 110:
        return "E"
    if weight_kg >= 95:
        return "D"
    if weight_kg >= 85:
        return "C"
    if weight_kg >= 75:
        return "B"
    return "A"


def body_rank_progress(weight_kg):
    """Return (current_rank, next_rank, pct_to_next) within the current band."""
    bands = [
        ("F", 130, 999),
        ("E", 110, 130),
        ("D", 95, 110),
        ("C", 85, 95),
        ("B", 75, 85),
        ("A", 65, 75),
    ]
    if weight_kg is None:
        weight_kg = 130
    rank = body_rank(weight_kg)
    idx = RANK_ORDER.index(rank)
    next_rank = RANK_ORDER[idx + 1] if idx + 1 < len(RANK_ORDER) else None
    for label, low, high in bands:
        if label == rank:
            span = high - low
            pct = 0 if span <= 0 else max(0, min(100, (high - weight_kg) / span * 100))
            return rank, next_rank, round(pct)
    return rank, next_rank, 0


def mind_rank(streak_days):
    # A "Full mastery" is treated as a sustained one-year streak.
    if streak_days >= 365:
        return "A"
    if streak_days >= 102:
        return "B"
    if streak_days >= 60:
        return "C"
    if streak_days >= 30:
        return "D"
    if streak_days >= 10:
        return "E"
    return "F"


def mind_rank_progress(streak_days):
    bands = [
        ("F", 0, 10),
        ("E", 10, 30),
        ("D", 30, 60),
        ("C", 60, 102),
        ("B", 102, 365),
        ("A", 365, 365),
    ]
    rank = mind_rank(streak_days)
    idx = RANK_ORDER.index(rank)
    next_rank = RANK_ORDER[idx + 1] if idx + 1 < len(RANK_ORDER) else None
    for label, low, high in bands:
        if label == rank:
            span = high - low
            pct = 100 if span <= 0 else max(0, min(100, (streak_days - low) / span * 100))
            return rank, next_rank, round(pct)
    return rank, next_rank, 0


def money_rank(total_earned, best_day):
    total_earned = total_earned or 0
    best_day = best_day or 0
    # "Scale beyond" B-rank is treated as a further 5x milestone.
    if total_earned >= 500000:
        return "A"
    if total_earned >= 200000:
        return "B"
    if total_earned >= 50000:
        return "C"
    if total_earned >= 10000:
        return "D"
    if best_day >= 200 or total_earned >= 200:
        return "E"
    return "F"


def money_rank_progress(total_earned, best_day):
    bands = [
        ("F", 0, 200),
        ("E", 200, 10000),
        ("D", 10000, 50000),
        ("C", 50000, 200000),
        ("B", 200000, 500000),
        ("A", 500000, 500000),
    ]
    total_earned = total_earned or 0
    rank = money_rank(total_earned, best_day)
    idx = RANK_ORDER.index(rank)
    next_rank = RANK_ORDER[idx + 1] if idx + 1 < len(RANK_ORDER) else None
    for label, low, high in bands:
        if label == rank:
            span = high - low
            pct = 100 if span <= 0 else max(0, min(100, (total_earned - low) / span * 100))
            return rank, next_rank, round(pct)
    return rank, next_rank, 0
