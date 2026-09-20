"""
Static definitions for the 20 daily quests. These are not stored in the
database as rows of their own — only completion records (DailyQuest) are
stored, keyed by the integer `id` below. This file is the single source of
truth for quest text, category and scold message.
"""

BODY = "BODY"
FUEL = "FUEL"
MIND = "MIND"
MONEY = "MONEY"

CATEGORY_LABELS = {
    BODY: "Body",
    FUEL: "Fuel",
    MIND: "Mind",
    MONEY: "Money",
}

# Ordered by id, 1-20.
QUESTS = [
    {
        "id": 1,
        "category": BODY,
        "title": "Complete today's workout session",
        "scold": "No workout means no adaptation. Your body only changes when you force it to.",
    },
    {
        "id": 2,
        "category": BODY,
        "title": "Walk 8,000+ steps",
        "scold": "Walking is free fat burning. You left it on the table.",
    },
    {
        "id": 3,
        "category": BODY,
        "title": "Zero alcohol",
        "scold": "Alcohol spikes cortisol, kills testosterone and destroys sleep. Not acceptable.",
    },
    {
        "id": 4,
        "category": BODY,
        "title": "No junk food or sugary drinks",
        "scold": "Every junk meal undoes hours of work. You chose instant pleasure over your goal.",
    },
    {
        "id": 5,
        "category": BODY,
        "title": "In bed by 11pm",
        "scold": "Late nights kill growth hormone, spike hunger hormones and wreck tomorrow's workout.",
    },
    {
        "id": 6,
        "category": BODY,
        "title": "Sleep 7+ hours",
        "scold": "Under 7 hours means your body breaks down muscle for energy. You're working against yourself.",
    },
    {
        "id": 7,
        "category": BODY,
        "title": "Maintain good posture all day",
        "scold": "Posture is how the world reads you before you speak. Slouching is giving up.",
    },
    {
        "id": 8,
        "category": FUEL,
        "title": "Hit 150g+ protein",
        "scold": "Protein is the building material. Without it your body has nothing to rebuild with.",
    },
    {
        "id": 9,
        "category": FUEL,
        "title": "Drink 2-3 litres of water",
        "scold": "Dehydration kills performance and mimics hunger. You drank something else instead.",
    },
    {
        "id": 10,
        "category": FUEL,
        "title": "Eat planned meals only",
        "scold": "Unplanned eating is where the deficit disappears. Stick to the plan.",
    },
    {
        "id": 11,
        "category": FUEL,
        "title": "Zero liquid calories",
        "scold": "Liquid calories don't register as food. You drank your progress away.",
    },
    {
        "id": 12,
        "category": MIND,
        "title": "Maintain celibacy — no masturbation",
        "scold": "You gave your dopamine away for free. Every urge you resist makes the next one weaker.",
    },
    {
        "id": 13,
        "category": MIND,
        "title": "No phone 1 hour before sleep",
        "scold": "Phone before bed means shallow sleep, more hunger tomorrow, less recovery.",
    },
    {
        "id": 14,
        "category": MIND,
        "title": "25 min of silent focused work",
        "scold": "You cannot build concentration you keep avoiding. Silence is where real thinking lives.",
    },
    {
        "id": 15,
        "category": MIND,
        "title": "No background noise while working",
        "scold": "Background noise is a crutch. Your brain learns helplessness every time you reach for it.",
    },
    {
        "id": 16,
        "category": MIND,
        "title": "Write 1 thing you are grateful for",
        "scold": "Gratitude keeps you from spiraling. Skipping it is choosing negativity by default.",
    },
    {
        "id": 17,
        "category": MIND,
        "title": "5 min visualization — see yourself at goal",
        "scold": "Champions see the goal before it exists. You forgot to remind yourself what you're doing this for.",
    },
    {
        "id": 18,
        "category": MONEY,
        "title": "Study trading for 30 min",
        "scold": "Every day you skip study is a day you stay where you are.",
    },
    {
        "id": 19,
        "category": MONEY,
        "title": "Review and journal yesterday's trades",
        "scold": "Traders who don't journal repeat mistakes. You left free lessons on the table.",
    },
    {
        "id": 20,
        "category": MONEY,
        "title": "No revenge trading or emotional decisions",
        "scold": "Revenge trading is how accounts go to zero. Discipline here is the same muscle as everything else.",
    },
]

QUESTS_BY_ID = {q["id"]: q for q in QUESTS}

CELIBACY_QUEST_ID = 12

CATEGORY_ORDER = [BODY, FUEL, MIND, MONEY]


def quests_by_category():
    grouped = {cat: [] for cat in CATEGORY_ORDER}
    for q in QUESTS:
        grouped[q["category"]].append(q)
    return grouped
