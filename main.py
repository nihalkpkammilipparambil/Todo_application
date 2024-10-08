# importing required modules
import customtkinter as ctk
from sqlite3 import *
from PIL import Image

# application config
app = ctk.CTk()
app.title('Todo App')
app.geometry('600x400')
app.resizable(False, False)


# widgets
    # Logo
logo1 = ctk.CTkLabel(
    master=app,
    text='Todo',
    text_color='#949494',
    font=('Dangerless Liaisons', 35, 'bold')
)
logo1.place(x=35, y=25)

logo2 = ctk.CTkLabel(
    master=app,
    text='List',
    text_color='#FF0000',
    font=('Dangerless Liaisons', 35, 'bold')

)
logo2.place(x=90, y=25)

    # Task Entry
entry = ctk.CTkEntry(
    master=app,
    placeholder_text="Enter your your task here:",
    placeholder_text_color='#000000',
    font=('Comic Sans MS', 10, 'bold'),
    text_color='black',
    width=200, height=40,
    corner_radius=10,
    fg_color='#949494'
)
entry.place(x=150, y=120)

    # Add Button
        # load images
image_add = ctk.CTkImage(Image.open('./assets/icons8-add-button-96.png'), size=(35, 35))
add_btn = ctk.CTkButton(
    master=app,
    image=image_add,
    text='',
    width=0,
    height=0,
    fg_color='transparent',
)

add_btn.place(x=450, y=120)

app.mainloop()
