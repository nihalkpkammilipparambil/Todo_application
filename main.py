# importing required modules
import customtkinter as ctk
import sqlite3
from PIL import Image
from database import setup_database

global current_task_id

# Add task to database
def add_task(task):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
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
    for widget in scrolling_frame.winfo_children():
        widget.destroy()

    tasks = get_tasks()
    for task in tasks:
        # Display_frame
        display_frame = ctk.CTkFrame(
            master=scrolling_frame,
            width=300,
            height=50,
            fg_color='black',
            corner_radius=10,
            border_width=2,
            border_color='red'
        )

        display_frame.pack(pady=10)
        task_label = ctk.CTkLabel(display_frame, font=('Segoe UI', 20, 'bold'), bg_color='black', text_color='white', corner_radius=10, text=task[1])
        task_label.place(x=5, y=8)

        # Add delete button for each task
        delete_btn_image = ctk.CTkImage(Image.open('./assets/icons8-trash-48.png'), size=(30, 30))
        delete_button = ctk.CTkButton(display_frame, text="", image=delete_btn_image, height=1, width=1, fg_color='black', hover_color='black', command=lambda task_id=task[0]: delete_task(task_id))
        delete_button.place(x=250, y=5)

        # Add update button for each task
        update_btn_image = ctk.CTkImage(Image.open('./assets/icons8-edit-48.png'), size=(30, 30))
        update_button = ctk.CTkButton(display_frame, image=update_btn_image, text='', height=1, width=1, fg_color='black', hover_color='black', command=lambda task_id=task[0], task_name=task[1]: on_update_task(task_id, task_name))
        update_button.place(x=220, y=5)

# Update task from input
def on_update_task(task_id, task_name):
    #global current_task_id
    task_entry.delete(0, 'end')
    task_entry.insert(0, task_name)
    task_entry.configure(fg_color='green')  # Change color to indicate update mode
    current_task_id = task_id  # Store the ID of the task being updated
    update_task(task_id=task_id, new_task=task_name)

# Handle adding or updating tasks
def submit_task():
    task = task_entry.get()
    if task:
        if 'current_task_id' in globals() and current_task_id is not None:
            update_task(current_task_id, task)
            del current_task_id  # Clear the current task ID
        else:
            add_task(task)
        task_entry.delete(0, 'end')
        task_entry.configure(fg_color='#949494', placeholder_text='Enter your task here:', text_color='black', font=('Comic Sans MS', 12, 'bold'))  # Reset


# Update task in database
def update_task(task_id, new_task):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET task = ? WHERE id = ?', (new_task, task_id))
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
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


# start and setup database
setup_database()

# application config
app = ctk.CTk()
app.title('Todo App')
app.geometry('600x400')
app.resizable(False, False)
background_img = ctk.CTkImage()

# background
background_color = ctk.CTkFrame(
    master=app,
    fg_color='black',
    width=700,
    height=500
)
background_color.pack()

# widgets
    # Logo
logo1 = ctk.CTkLabel(
    master=app,
    text='Todo',
    text_color='#949494',
    font=('Dangerless Liaisons', 35, 'bold'),
    bg_color='black'
)
logo1.place(x=35, y=25)

logo2 = ctk.CTkLabel(
    master=app,
    text='List',
    text_color='#FF0000',
    font=('Dangerless Liaisons', 35, 'bold'),
    bg_color='black'

)
logo2.place(x=90, y=25)

    # Task Entry
task_entry = ctk.CTkEntry(
    master=app,
    placeholder_text="Enter your your task here:",
    placeholder_text_color='#000000',
    font=('Comic Sans MS', 12, 'bold'),
    text_color='black',
    width=300, height=40,
    corner_radius=10,
    fg_color='#949494',
    bg_color='black'
)
task_entry.place(x=150, y=120)

    # Add Button
        # load images
image_add_btn = ctk.CTkImage(Image.open('./assets/icons8-add-button-96.png'), size=(35, 35))
add_btn = ctk.CTkButton(
    master=app,
    image=image_add_btn,
    text='',
    width=1,
    height=1,
    fg_color='black',
    bg_color='black',
    hover_color='black',
    command=submit_task
)

add_btn.place(x=450, y=120)

    # Task diplay_frame
        # Scrolling_frame
scrolling_frame = ctk.CTkScrollableFrame(
    master=app,
    width=400,
    height=200,
    fg_color='black',
    bg_color='black',

)
scrolling_frame.place(x=95, y=200)

refresh_tasks()

# Run
app.mainloop()
