# The System

A personal discipline and levelling tracker inspired by Solo Levelling.
Twenty daily quests across Body, Fuel, Mind and Money, PIN-locked, with an
in-universe accountability system that calls out missed quests the next day.

## Tech stack

- Django 4.2+
- PostgreSQL
- Vanilla HTML/CSS/JS (no frontend framework)

## Setup

### 1. Clone / unzip the project

```bash
cd "The System"
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the PostgreSQL database

```bash
createdb the_system_db
# or, from psql:
# CREATE DATABASE the_system_db;
# CREATE USER the_system_user WITH PASSWORD 'the_system_password';
# GRANT ALL PRIVILEGES ON DATABASE the_system_db TO the_system_user;
```

### 5. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and set `SECRET_KEY`, `DATABASE_URL`, and `TIME_ZONE` (the
timezone the app should treat as "local" — this drives when the day rolls
over and the 12:01 AM accountability check fires). Also set
`GYM_CUTOVER_DATE` if you want the workout schedule to switch from home
workouts to gym Push/Pull/Legs on a different date than 2026-09-28.

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Start the server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`. On first visit you'll be asked to create a
4-digit PIN — this is the only account on the system. From then on, every
visit requires that PIN.

## How it works

- **Dashboard** — today's 20 quests grouped by category, weight progress
  bar (130kg → 85kg), quest completion counter, days-active counter, and
  Body/Mind/Money rank badges.
- **Body** — log weight, see the 7-day workout schedule (home workouts
  until the gym cutover date, then Push/Pull/Legs), and Body rank
  progression (F → A based on weight).
- **Mind** — celibacy streak with a 30-day dot grid, weekly mind-focus
  schedule, and Mind rank progression (F → A based on streak length).
- **Money** — log trading days, see total earned / best day / trading day
  count, and Money rank progression (F → A based on total earned).
- **Log** — free-text daily journal entries.
- **Accountability** — if yesterday had any incomplete quests, a
  full-screen modal appears on your next visit listing each missed quest
  with its scold message. Dismissing it ("I hear you. Moving on.") marks
  that day as seen — it won't show again.

## Installing as an app (PWA)

The System is an installable Progressive Web App — on both mobile and
desktop, the browser (or an "Install App" button in the sidebar/topbar)
lets you add it to your home screen or dock as a standalone app, with its
own icon, no browser chrome. It also registers a service worker that
caches the app shell (CSS/JS/icons) and falls back to a lightweight
offline screen when there's no connection; quest data itself always
requires a live connection to stay accurate.

## Admin access

Django's built-in admin is available at `/admin/` for direct data
inspection. Create a superuser if you want to use it:

```bash
python manage.py createsuperuser
```

(This is separate from the 4-digit PIN, which gates the main app.)

## Project structure

```
config/             Django project settings, URLs, WSGI/ASGI
system/              The single app: models, views, quest data, rank logic
  templates/system/   HTML templates (HUD-style UI)
  static/system/      CSS + vanilla JS
  migrations/          Database migrations
```

No external API calls are made — once dependencies are installed and the
database is migrated, the app runs fully offline.
