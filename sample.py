import sqlite3
import customtkinter as ctk
from database import setup_database

# global variables
global current_task_id

# Add task to database
def add_task(task):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
    conn.commit()
    conn.close()
    refresh_tasks()

# Delete task from database
def delete_task(task_id):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    refresh_tasks()

# Update task in database
def update_task(task_id, new_task):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET task = ? WHERE id = ?', (new_task, task_id))
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    refresh_tasks()

# Retrieve tasks from database
def get_tasks():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# Refresh task list in GUI
def refresh_tasks():
    for widget in task_frame.winfo_children():
        widget.destroy()

    tasks = get_tasks()
    for task in tasks:
        task_label = ctk.CTkLabel(task_frame, text=task[1])
        task_label.pack(side='left', padx=5)

        # Add delete button for each task
        delete_button = ctk.CTkButton(task_frame, text="Delete", command=lambda task_id=task[0]: delete_task(task_id))
        delete_button.pack(side='left', padx=5)

        # Add update button for each task
        update_button = ctk.CTkButton(task_frame, text="Update", command=lambda task_id=task[0], task_name=task[1]: on_update_task(task_id, task_name))
        update_button.pack(side='left', padx=5)

# Update task from input
def on_update_task(task_id, task_name):
    #global current_task_id
    task_entry.delete(0, 'end')
    task_entry.insert(0, task_name)
    task_entry.configure(fg_color='yellow')  # Change color to indicate update mode
    current_task_id = task_id  # Store the ID of the task being updated
    update_task(task_id=task_id, new_task=task_name)



# Handle adding or updating tasks
def submit_task():
    task = task_entry.get()
    if task:
        if 'current_task_id' in globals() and current_task_id is not None:
            update_task(current_task_id, task)
            task_entry.configure(fg_color='white')  # Reset color
            del current_task_id  # Clear the current task ID
        else:
            add_task(task)
        task_entry.delete(0, 'end')


# Setting up the main application window
setup_database()

app = ctk.CTk()
app.title("Todo App")

# Input frame
input_frame = ctk.CTkFrame(app)
input_frame.pack(pady=10)

task_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter task...")
task_entry.pack(side='left', padx=5)

submit_task_button = ctk.CTkButton(input_frame, text="Add/Update Task", command=submit_task)
submit_task_button.pack(side='left', padx=5)

# Task display frame
task_frame = ctk.CTkFrame(app)
task_frame.pack(pady=10)

refresh_tasks()

app.mainloop()
