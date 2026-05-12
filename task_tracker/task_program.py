import json
import os
from datetime import datetime

FILE_NAME = os.path.join(os.path.dirname(__file__), "tasks.json")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def format_datetime(iso_str):
    if not iso_str:
        return "Unknown"
    dt = datetime.fromisoformat(iso_str)
    return dt.strftime("%m/%d/%Y, %I:%M:%S %p")


def format_date(iso_str):
    if not iso_str:
        return "Unknown"
    dt = datetime.fromisoformat(iso_str)
    return dt.strftime("%m/%d/%Y")


def format_time(iso_str):
    if not iso_str:
        return "Unknown"
    dt = datetime.fromisoformat(iso_str)
    return dt.strftime("%I:%M %p")


def format_duration(seconds):
    if seconds is None:
        return "N/A"
    seconds = int(round(seconds))
    hours, rem = divmod(seconds, 3600)
    minutes, secs = divmod(rem, 60)

    if hours:
        return f"{hours}h {minutes}m"
    if minutes:
        return f"{minutes}m"
    return f"{secs}s"


def load_data():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            data = json.load(f)

        for task in data.values():
            if "created_at" not in task:
                task["created_at"] = None
            if "entries" not in task:
                task["entries"] = []

            for entry in task["entries"]:
                if "start_text" not in entry:
                    entry["start_text"] = ""
                if "start_time" not in entry:
                    entry["start_time"] = None
                if "end_text" not in entry:
                    entry["end_text"] = ""
                if "end_time" not in entry:
                    entry["end_time"] = None
                if "duration_seconds" not in entry:
                    entry["duration_seconds"] = None

        return data

    return {}


def save_data(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)


def get_active_entry(task):
    if task["entries"] and task["entries"][-1]["end_time"] is None:
        return task["entries"][-1]
    return None


def get_active_entry_elapsed(task):
    active = get_active_entry(task)
    if not active or not active["start_time"]:
        return None
    start_time = datetime.fromisoformat(active["start_time"])
    return (datetime.now() - start_time).total_seconds()


def new_task(data):
    name = input("Enter new task name: ").strip()
    if not name:
        print("Task name cannot be empty.")
        return

    if name in data:
        print("Task already exists.")
        return

    data[name] = {
        "created_at": datetime.now().isoformat(),
        "entries": []
    }

    print(f"Task '{name}' created.")


def start_entry(task):
    active = get_active_entry(task)
    if active:
        print("There is already an open entry for this task. End it before creating a new one.")
        return

    start_text = input("Start Entry Text: ").strip()
    now = datetime.now()

    task["entries"].append({
        "start_text": start_text,
        "start_time": now.isoformat(),
        "end_text": "",
        "end_time": None,
        "duration_seconds": None
    })

    print(f"Started entry at {format_datetime(now.isoformat())}")


def end_entry(task):
    active = get_active_entry(task)
    if not active:
        print("No open entry to close.")
        return

    end_text = input("End Entry Text (optional): ").strip()
    now = datetime.now()

    active["end_text"] = end_text
    active["end_time"] = now.isoformat()
    start_time = datetime.fromisoformat(active["start_time"])
    active["duration_seconds"] = (now - start_time).total_seconds()

    print(f"Closed entry at {format_datetime(now.isoformat())}")
    print(f"Total duration: {format_duration(active['duration_seconds'])}")


def delete_task(data, name):
    confirm = input(f"Delete task '{name}' and all entries? (y/n): ").strip().lower()
    if confirm == "y":
        del data[name]
        print(f"Task '{name}' deleted.")
        return True
    print("Delete cancelled.")
    return False


def get_total_task_time(task):
    """Calculate total time spent on a task across all entries."""
    total_seconds = 0
    for entry in task["entries"]:
        if entry["duration_seconds"]:
            total_seconds += entry["duration_seconds"]
    return total_seconds


def show_task_details(name, task):
    print(f"\n--- {name} ---")
    print(f"Created: {format_datetime(task['created_at'])}")
    active_entry = get_active_entry(task)
    active = "Open" if active_entry else "Closed"
    print(f"Status: {active}")

    if active_entry:
        elapsed = get_active_entry_elapsed(task)
        print(f"Current active entry elapsed: {format_duration(elapsed)}")

    total_time = get_total_task_time(task)
    print(f"Total time on task: {format_duration(total_time)}")
    print("")

    if not task["entries"]:
        print("No entries yet.")
        return

    for index, entry in enumerate(task["entries"], start=1):
        print(f"Start Entry {index}: {entry['start_text'] or '*No text*'}")
        print(f"Date: {format_date(entry['start_time'])}")
        print(f"Time: {format_time(entry['start_time'])}")
        print("--")
        print(f"End Entry {index}: {entry['end_text'] or '*Optional Text*'}")
        print(f"Time: {format_time(entry['end_time']) if entry['end_time'] else 'Not ended'}")
        print(
            f"Total time for this entry: {format_duration(entry['duration_seconds'])}"
            if entry["end_time"]
            else "Total time for this entry: Not ended"
        )
        print("---------------------")


def task_menu(data, name):
    while True:
        clear_screen()
        task = data[name]
        show_task_details(name, task)

        print("\n1. New start Entry")
        print("2. End current Entry")
        print("3. Delete current task")
        print("4. Back")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            start_entry(task)
            save_data(data)
        elif choice == "2":
            end_entry(task)
            save_data(data)
        elif choice == "3":
            if delete_task(data, name):
                save_data(data)
                break
        elif choice == "4":
            break
        else:
            print("Invalid input.")

        input("Press Enter to continue...")


def show_menu(data):
    clear_screen()
    print("\n--- Task Tracker ---")
    print("1. New Task")
    print("2. Exit")

    task_names = list(data.keys())
    for i, name in enumerate(task_names, start=3):
        task = data[name]
        active = "Open" if get_active_entry(task) else "Closed"
        print(f"{i}. {name} ({len(task['entries'])} entries, {active})")

    return task_names


def main():
    data = load_data()

    while True:
        task_names = show_menu(data)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            new_task(data)
            save_data(data)
        elif choice == "2":
            save_data(data)
            print("Saved. Goodbye.")
            break
        elif choice.isdigit() and int(choice) >= 3:
            index = int(choice) - 3
            if 0 <= index < len(task_names):
                task_menu(data, task_names[index])
            else:
                print("Invalid selection.")
                input("Press Enter to continue...")
        else:
            print("Invalid input.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()