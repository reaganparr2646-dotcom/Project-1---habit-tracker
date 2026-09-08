import json
from pathlib import Path
from datetime import date, timedelta
import sys

# FILE LOCATION

if getattr(sys, 'frozen', False):
    APP_FOLDER = Path(sys.executable).parent
else:
    APP_FOLDER = Path(__file__).parent

DATA_FILE = APP_FOLDER / "habits.json"

#DATA_FILE = Path(r"C:\Users\lion3\Documents\50 projects\Project 1 - habit tracker\habits.json")

# DATE AND RESET FUNCTIONS

def get_reset_marker(frequency):
    today = date.today()
    frequency = frequency.strip().lower()

    if frequency == "weekly":
        days_since_sunday = (today.weekday() + 1) % 7
        current_sunday = today - timedelta(days=days_since_sunday)
        return current_sunday.isoformat()

    return today.isoformat()


def reset_habits(habits):
    changed = False

    for habit in habits:
        frequency = habit.get("frequency", "daily")
        current_reset_marker = get_reset_marker(frequency)

        if habit.get("reset_marker") != current_reset_marker:
            habit["completed"] = False
            habit["reset_marker"] = current_reset_marker
            changed = True

    return changed


# HABIT FUNCTIONS

def create_habit(name, description, frequency):
    frequency = frequency.strip().lower()

    habit = {
        "name": name.strip(),
        "description": description.strip(),
        "frequency": frequency,
        "completed": False,
        "reset_marker": get_reset_marker(frequency)
    }

    return habit


def mark_habit_completed(habit):
    if habit.get("completed", False):
        return False

    habit["completed"] = True
    return True


def mark_habit_incomplete(habit):
    if not habit.get("completed", False):
        return False

    habit["completed"] = False
    return True


def delete_habit(habits, habit):
    if habit not in habits:
        return False

    habits.remove(habit)
    return True


# STORAGE FUNCTIONS

def save_habits(habits):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(habits, file, indent=4)


def load_habits():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            habits = json.load(file)

            if isinstance(habits, list):
                return habits

            return []

    except (FileNotFoundError, json.JSONDecodeError):
        return []