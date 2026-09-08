import tkinter as tk
from tkinter import ttk, messagebox

from habit_tracker import (
    create_habit,
    delete_habit,
    get_reset_marker,
    load_habits,
    mark_habit_completed,
    mark_habit_incomplete,
    save_habits,
    reset_habits,
)

def toggle_habbit(habit, completed_var, habits):
    if completed_var.get():
        mark_habit_completed(habit)
    else:
        mark_habit_incomplete(habit)

    save_habits(habits)

def confirm_delete_habit(habit, habits, habit_frame):
    confirm = messagebox.askyesno(
        "Delete Habit",
        f"Are you sure you want to delete the habit '{habit['name']}'?"
    )

    if not confirm:
        return

    if delete_habit(habits, habit):
        save_habits(habits)
        refresh_habits(habit_frame, habits)

def open_edit_habit_window(habit, habit_frame, habits):
    edit_window = tk.Toplevel()
    edit_window.title("Edit Habit")
    edit_window.geometry("350x300")
    edit_window.resizable(False, False)

    ttk.Label(
        edit_window,
        text="Habit Name"
    ).pack(
        anchor=tk.W,
        padx=20,
        pady=(20, 5)
    )

    name_entry = ttk.Entry(edit_window)
    name_entry.insert(0, habit["name"])
    name_entry.pack(
        fill=tk.X,
        padx=20
    )

    ttk.Label(
        edit_window,
        text="Description"
    ).pack(
        anchor=tk.W,
        padx=20,
        pady=(15, 5)
    )

    description_entry = ttk.Entry(edit_window)
    description_entry.insert(0, habit.get("description", ""))
    description_entry.pack(
        fill=tk.X,
        padx=20
    )

    ttk.Label(
        edit_window,
        text="Frequency"
    ).pack(
        anchor=tk.W,
        padx=20,
        pady=(15, 5)
    )

    frequency_box = ttk.Combobox(
        edit_window,
        values=["daily", "weekly"],
        state="readonly"
    )
    frequency_box.pack(
        fill=tk.X,
        padx=20
    )
    frequency_box.set(habit.get("frequency", "daily"))

    def save_changes():
            name = name_entry.get().strip()
            description = description_entry.get().strip()
            frequency = frequency_box.get()

            if not name:
                messagebox.showerror(
                    "Missing Name",
                    "Please enter a habit name."
                )
                return


            old_frequency = habit.get("frequency", "daily")

            habit["name"] = name
            habit["description"] = description
            habit["frequency"] = frequency
            habit["reset_marker"] = get_reset_marker(frequency)

            if old_frequency != frequency:
                habit["completed"] = False
                habit["reset_marker"] = get_reset_marker(frequency)

            save_habits(habits)
            refresh_habits(habit_frame, habits)

            edit_window.destroy()
    save_button = ttk.Button(
        edit_window,
        text="Save Changes",
        command=save_changes
    )
    save_button.pack(pady=25)

    name_entry.focus()

def display_section(habit_frame, section_title, section_habits, habits):
    heading = ttk.Label(
        habit_frame,
        text=section_title,
        font=("Arial", 16, "bold")
    )
    heading.pack(
        anchor=tk.W,
        pady=(15, 8)
    )

    if not section_habits:
        empty_label = ttk.Label(
            habit_frame,
            text="No habits in this section.",
            font=("Arial", 12, "italic")
        )
        empty_label.pack(
            anchor=tk.W,
            padx=10,
            pady=5
        )
        return

    for habit in section_habits:
        habit_row = ttk.Frame(
            habit_frame,
            padding=10
        )
        habit_row.pack(
            fill=tk.X,
            pady=4
        )

        completed_var = tk.BooleanVar(value=habit.get("completed", False))

        status_checkbox = ttk.Checkbutton(
            habit_row,
            variable=completed_var,
            command=lambda h=habit, v=completed_var: toggle_habbit(h, v, habits)
        )
        status_checkbox.pack(
            side=tk.LEFT,
            padx=(0, 10)
        )

        information_frame = ttk.Frame(habit_row)
        information_frame.pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True
        )

        edit_button = ttk.Button(
            habit_row,
            text="Edit",
            command=lambda h=habit: open_edit_habit_window(h, habit_frame, habits)
        )
        edit_button.pack(
            side=tk.RIGHT,
            padx=(5, 0)
        )

        delete_button = ttk.Button(
            habit_row,
            text="Delete",
            command=lambda h=habit: confirm_delete_habit(h, habits, habit_frame)
        )

        delete_button.pack(
            side=tk.RIGHT,
            padx=(10, 0)
        )

        name_label = ttk.Label(
            information_frame,
            text=habit["name"],
            font=("Arial", 12, "bold")
        )
        name_label.pack(anchor=tk.W)

        description = habit.get("description", "")

        if description:
            description_label = ttk.Label(
                information_frame,
                text=description
            )
            description_label.pack(anchor=tk.W)

def refresh_habits(habit_frame, habits):
    for widget in habit_frame.winfo_children():
        widget.destroy()

    daily_habits = [
        habit
        for habit in habits
        if habit.get("frequency") == "daily"
    ]

    weekly_habits = [
        habit
        for habit in habits
        if habit.get("frequency") == "weekly"
    ]

    if not habits:
        empty_label = ttk.Label(
            habit_frame,
            text="You have not created any habits yet.",
            font=("Arial", 12)
        )
        empty_label.pack(pady=40)
        return

    display_section(
        habit_frame,
        "Daily Habits",
        daily_habits,
        habits
    )

    display_section(
        habit_frame,
        "Weekly Habits",
        weekly_habits,
        habits
    )

def open_add_habit_window(root, habit_frame, habits):
    add_window = tk.Toplevel(root)

    add_window.title("Add Habit")
    add_window.geometry("350x300")
    add_window.resizable(False, False)

    ttk.Label(
        add_window,
        text="Habit Name"
    ).pack(
        anchor=tk.W,
        padx=20,
        pady=(20, 5)
    )

    name_entry = ttk.Entry(add_window)
    name_entry.pack(
        fill=tk.X,
        padx=20
    )

    ttk.Label(
        add_window,
        text="Description"
    ).pack(
        anchor=tk.W,
        padx=20,
        pady=(15, 5)
    )

    description_entry = ttk.Entry(add_window)
    description_entry.pack(
        fill=tk.X,
        padx=20
    )

    ttk.Label(
        add_window,
        text="Frequency"
    ).pack(
        anchor=tk.W,
        padx=20,
        pady=(15, 5)
    )

    frequency_box = ttk.Combobox(
        add_window,
        values=["daily", "weekly"],
        state="readonly"
    )
    frequency_box.pack(
        fill=tk.X,
        padx=20
    )
    frequency_box.set("daily")

    def submit_habit():
        name = name_entry.get().strip()
        description = description_entry.get().strip()
        frequency = frequency_box.get()

        if not name:
            messagebox.showerror(
                "Missing Name",
                "Please enter a habit name."
            )
            return

        new_habit = create_habit(
            name,
            description,
            frequency
        )

        habits.append(new_habit)
        save_habits(habits)
        refresh_habits(habit_frame, habits)

        add_window.destroy()

    save_button = ttk.Button(
        add_window,
        text="Save Habit",
        command=submit_habit
    )
    save_button.pack(pady=25)

    name_entry.focus()

def main():
    habits = load_habits()

    if reset_habits(habits):
        save_habits(habits)

    root = tk.Tk()
    root.title("Habit Tracker")
    root.geometry("500x800")
    root.minsize(300, 300)

    title_label = ttk.Label(
        root,
        text="Habit Tracker",
        font=("Arial", 24, "bold")
    )
    title_label.pack(pady=(25, 10))

    habit_frame = ttk.Frame(
        root,
        padding=20
    )

    add_button = ttk.Button(
        root,
        text="+ Add Habit",
        command=lambda: open_add_habit_window(
            root,
            habit_frame,
            habits
        )
    )
    add_button.pack(pady=(0, 10))

    habit_frame.pack(
        fill=tk.BOTH,
        expand=True
    )

    refresh_habits(habit_frame, habits)

    root.mainloop()

if __name__ == "__main__":
    main()