import tkinter as tk
from tkinter import messagebox
import random
from math import floor

import pyperclip

from password_manager import PasswordManager
from password import Password

FONT_NAME = "Arial"
FONT_SIZE = 14

#-------------------- PASSWORD GENERATOR --------------------#


def generate_password(length=16, uppercase=True, lowercase=True, numbers=True, symbols=True):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    
    # arbitrarily decide to restrict to mostly characters
    nLettersFloor = floor(length * .66666)
    
    def get_n_chars(charset, length):
        nr_char = random.randint(1,length)
        if 'a' in charset:
            nr_char = max(nr_char, nLettersFloor)
        remaining_length = length - nr_char
        return (nr_char, remaining_length)
    
    nLetters, remaining_length = get_n_chars(letters, length) 
    nNumbers, nSymbols = get_n_chars(numbers, remaining_length) 

    password_list = [ random.choice(charset) for charset, n in zip([letters, numbers, symbols], [nLetters, nNumbers, nSymbols]) for _ in range(n) ]
    random.shuffle(password_list)
    password = "".join(password_list)

    password_entry.insert(0,password)
    pyperclip.copy(password)

#-------------------- SAVE PASSWORD --------------------#

global pm
pm = PasswordManager('mypass.db','passwords')

def get_values():
   website = website_entry.get()
   name = name_entry.get()
   username = username_entry.get()
   password = password_entry.get()
   notes = notes_entry.get('1.0', 'end-1c')

   if len(name) == 0 or username == 0 or password == 0:
        messagebox.showwarning(title='Empty fields', message='name, username, and password must be filled') 
        return 

   params =  {
       'website':website,
       'name':name,
       'username':username,
       'password':password,
       'notes':notes
   }
   return Password(params)

def save():
    password_object = get_values()
    if password_object:
        is_ok = messagebox.askokcancel(title="Review %s information"%password_object.website, message='Do you want to add this username/password?')
        if is_ok:
            pm.add_password(password_object)
            clear_entries()

def clear_entries():
   website_entry.delete(0, 'end')
   name_entry.delete(0, 'end')
   username_entry.delete(0, 'end')
   password_entry.delete(0, 'end')
   notes_entry.delete('1.0', 'end')


#-------------------- UI SETUP --------------------#


window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="white")

canvas = tk.Canvas(window, width=200, height=200, bg="white", highlightthickness=0)
image = tk.PhotoImage(file="logo.png")
canvas.create_image(140, 100, image=image)

canvas.grid(row=0, column=1)

# website lable and entry
website_label = tk.Label(text="Website:", fg="black", bg="white")
website_label.grid(row=1, column=0)

website_entry = tk.Entry(width=38, fg="black", bg="white", highlightbackground="lightblue")
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()

# name label and entry
name_label = tk.Label(text="Name:", fg="black", bg="white")
name_label.grid(row=2, column=0)

name_entry = tk.Entry(width=38, fg="black", bg="white", highlightbackground="lightblue")
name_entry.grid(row=2, column=1, columnspan=2)
#name_entry.insert(0, "fuzzy")

# username label and entry
username_label = tk.Label(text="Email/Username:", fg="black", bg="white")
username_label.grid(row=3, column=0)

username_entry = tk.Entry(width=38, fg="black", bg="white", highlightbackground="lightblue")
username_entry.grid(row=3, column=1, columnspan=2)
#username_entry.insert(0, "fuzzy")

# password label, entry, and gnerate password button
password_label = tk.Label(text="Password:", fg="black", bg="white", highlightbackground="lightblue")
password_label.grid(row=4, column=0)

password_entry = tk.Entry(width=21, fg="black", bg="white", highlightbackground="lightblue")
password_entry.grid(row=4, column=1)

generate_password_button = tk.Button(text="Generate Password", fg="black", highlightbackground="white", command=generate_password)
generate_password_button.grid(row=4, column=2)

# notes
notes_label = tk.Label(text="Notes:", fg="black", bg="white", highlightbackground="lightblue")
notes_label.grid(row=5, column=0)

notes_entry = tk.Text(width=38, height=5, fg="black", bg="white", highlightbackground="lightblue")
notes_entry.grid(row=5, column=1, rowspan=2, columnspan=2)

#add button
add_button = tk.Button(text="Add", fg="black", highlightbackground="white", width=36, command=save)
add_button.grid(row=7, column=1, columnspan=2)


window.mainloop()