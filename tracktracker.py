import json
from datetime import datetime

def add_task():
    while True:
        add = input(" >> Add task: ")
        if not add.strip():
            print("⚠️ Task cannot be empty. Try again.")
            continue

        # Get current date and time
        now = datetime.now()
        current_date = now.strftime("%d-%m-%Y")
        current_time = now.strftime("%H:%M:%S")

        try:
            with open("data.json", "r") as file:
                tasks = json.load(file)
                if not isinstance(tasks, list):
                    tasks = []
        except (FileNotFoundError, json.JSONDecodeError):
            tasks = []

        # Generate unique ID
        new_id = max((task.get("id", 0) for task in tasks), default=0) + 1

        new_task = {
            "id": new_id,
            "task": add,
            "date_added": current_date,
            "time_added": current_time
        }

        tasks.append(new_task)

        with open("data.json", "w") as file:
            json.dump(tasks, file, indent=4)

        print(f">> ✅ Task added successfully [ID: {new_id}] on {current_date} at {current_time}")
        break  # Remove this `break` if you want to allow multiple task entries in one go


def update_task():
    try:
        with open("data.json", "r") as file:
            tasks = json.load(file)

        if not isinstance(tasks, list) or not tasks:
            print("📭 No tasks to update.")
            return

        # Display all tasks
        print("\n📝 All Tasks:")
        for task in tasks:
            print(f"ID: {task['id']} | 📅 {task['date_added']} | Task: {task['task']}")

        try:
            task_id = int(input("\nEnter the ID of the task you want to update: "))
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            return

        for task in tasks:
            if task["id"] == task_id:
                new_task_name = input("Enter the new task name: ")
                task["task"] = new_task_name
                print("✅ Task updated successfully.")
                break
        else:
            print(f"❌ Task with ID {task_id} not found.")
            return

        with open("data.json", "w") as file:
            json.dump(tasks, file, indent=4)

    except FileNotFoundError:
        print("❌ No task file found. Add a task first.")
    except json.JSONDecodeError:
        print("⚠️ Task file is corrupted.")

def delete_task():
    try:
        with open("data.json", "r") as file:
            tasks = json.load(file)
            if not isinstance(tasks, list):
                tasks = []

        if not tasks:
            print("⚠️ No tasks found to delete.")
            return

        print("\n📋 Current Tasks:")
        print("-" * 40)
        for task in tasks:
            print(f"🆔 ID: {task['id']} | 📝 Task: {task['task']} | 📅 Date: {task.get('date_added', 'N/A')} | ⏰ Time: {task.get('time_added', 'N/A')}")
        print("-" * 40)

        task_id = input("Enter the Task ID to delete: ")

        # Validate ID is an integer
        if not task_id.isdigit():
            print("❌ Invalid ID. Please enter a number.")
            return

        task_id = int(task_id)

        for i, task in enumerate(tasks):
            if task["id"] == task_id:
                removed_task = tasks.pop(i)
                with open("data.json", "w") as file:
                    json.dump(tasks, file, indent=4)
                print(f"🗑️ Task ID {task_id} ('{removed_task['task']}') deleted successfully.")
                break
        else:
            print(f"❌ Task with ID {task_id} not found.")

    except FileNotFoundError:
        print("❌ Task file not found. Please add a task first.")
    except json.JSONDecodeError:
        print("⚠️ Task file is corrupted.")

def mark_status():
    try:
        with open("data.json", "r") as file:
            tasks = json.load(file)
            if not isinstance(tasks, list):
                tasks = []

        if not tasks:
            print("⚠️ No tasks available to update.")
            return

        print("\n📋 All Tasks:")
        for task in tasks:
            task_id = task["id"]
            task_name = task["task"]
            current_status = task.get("status", "Not Marked")
            print(f"🆔 ID: {task_id} | 📝 Task: {task_name} | ✅ Current Status: {current_status}")

        print("\nNow mark each task as 'done' or 'not done'.")

        for task in tasks:
            while True:
                user_input = input(f"Is Task ID {task['id']} ('{task['task']}') done? (yes/no): ").strip().lower()
                if user_input in ['yes', 'y']:
                    task['status'] = 'Completed'
                    break
                elif user_input in ['no', 'n']:
                    task['status'] = 'Pending'
                    break
                else:
                    print("❌ Please enter 'yes' or 'no'.")

        with open("data.json", "w") as file:
            json.dump(tasks, file, indent=4)

        print("✅ All task statuses have been updated.")

    except FileNotFoundError:
        print("❌ Task file not found. Please add a task first.")
    except json.JSONDecodeError:
        print("⚠️ Task file is corrupted.")

        
def view_task():
    try:
        with open("data.json", "r") as file:
            tasks = json.load(file)

            if not tasks:
                print("📭 No tasks found.")
                return

        while True:
            print("\n=== VIEW TASK MENU ===")
            print("2.1 View All Tasks")
            print("2.2 View Completed Tasks")
            print("2.3 View Pending Tasks")
            print("2.4 Back to Main Menu")
            choice = input("Choose your option [2.1, 2.2, 2.3, 2.4]: \n")

            if choice == "2.1":
                print("\n📋 All Tasks:")
                print("-" * 50)
                for i, task in enumerate(tasks, start=1):
                    date = task.get("date_added", "Unknown date")
                    name = task.get("task", "Unnamed task")
                    status = task.get("status", "Not Marked")
                    print(f"{i}. 📅 {date} | 📝 {name} | ✅ Status: {status}")
                print("-" * 50)

            elif choice == "2.2":
                completed = [task for task in tasks if task.get("status") == "Completed"]
                if not completed:
                    print("✅ No completed tasks found.")
                else:
                    print("\n✅ Completed Tasks:")
                    print("-" * 50)
                    for i, task in enumerate(completed, start=1):
                        date = task.get("date_added", "Unknown date")
                        name = task.get("task", "Unnamed task")
                        print(f"{i}. 📅 {date} | 📝 {name} | ✅ Status: Completed")
                    print("-" * 50)

            elif choice == "2.3":
                pending = [task for task in tasks if task.get("status") != "Completed"]
                if not pending:
                    print("🕒 No pending tasks found.")
                else:
                    print("\n🕒 Pending Tasks:")
                    print("-" * 50)
                    for i, task in enumerate(pending, start=1):
                        date = task.get("date_added", "Unknown date")
                        name = task.get("task", "Unnamed task")
                        status = task.get("status", "Pending")
                        print(f"{i}. 📅 {date} | 📝 {name} | ✅ Status: {status}")
                    print("-" * 50)

            elif choice == "2.4":
                break

            else:
                print("❌ Invalid option. Please choose 2.1, 2.2, 2.3, or 2.4.")

    except FileNotFoundError:
        print("❌ No task file found. Add a task first.")
    except ValueError:
        print("⚠️ Task file is corrupted or empty.")
    except json.JSONDecodeError:
        print("⚠️ Invalid JSON format.")

  
        

def task_management():
    while True:
        print("\n=== Task Management ===\n")
        print("1.1. Add a new task")
        print("1.2. Update your task")
        print("1.3. Delete your task")
        print("1.4. Mark task Status")
        print("1.5 Back to main menu")
        choice = input("Choose your option [1.1, 1.2, 1.3, 1.4, 1.5] : \n")
        if choice == "1.1":
            add_task()
        elif choice == "1.2":
            update_task()
        elif choice == "1.3":
            delete_task()
        elif choice == "1.4":
            mark_status()
        elif choice == "1.5":
            first_menu()
        else:
            print("Invalid operation")
            break

#main function 1
def first_menu():
    while True:
        print("\n=== FIRST MENU === ")
        print("\n")
        print("1. Task Management")
        print("2. View Task")
        print("3. Exit")
        choice = input("Choose your option [1, 2, 3] : ")
        if choice == "1":
            task_management()
        elif choice == "2":
            view_task()
        elif choice == "3":
            print("Exiting the program")
            break
first_menu()

