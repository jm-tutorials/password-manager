import tkinter as tk
from tkinter import messagebox
import random
from math import floor

import pyperclip

from password_manager import PasswordManager
from password import Password


class UiManager:

    def __init__(self):
        self.layout()
        self.pm = PasswordManager('mypass.db', 'passwords')

    def layout(self):
        # website label and entry
        self.website_label = tk.Label(text="Website:", fg="black", bg="white")
        self.website_label.grid(row=1, column=0)

        self.website_entry = tk.Entry(width=21, fg="black", bg="white", highlightbackground="lightblue")
        self.website_entry.grid(row=1, column=1)
        self.website_entry.focus()

        self.search_button = tk.Button(text="Search", fg="black", highlightbackground="white", command=self.search)
        self.search_button.grid(row=1, column=2)

        # name label and entry
        self.name_label = tk.Label(text="Name:", fg="black", bg="white")
        self.name_label.grid(row=2, column=0)

        self.name_entry = tk.Entry(width=38, fg="black", bg="white", highlightbackground="lightblue")
        self.name_entry.grid(row=2, column=1, columnspan=2)
        # name_entry.insert(0, "fuzzy")

        # username label and entry
        self.username_label = tk.Label(text="Email/Username:", fg="black", bg="white")
        self.username_label.grid(row=3, column=0)

        self.username_entry = tk.Entry(width=38, fg="black", bg="white", highlightbackground="lightblue")
        self.username_entry.grid(row=3, column=1, columnspan=2)
        # username_entry.insert(0, "fuzzy")

        # password label, entry, and gnerate password button
        self.password_label = tk.Label(text="Password:", fg="black", bg="white", highlightbackground="lightblue")
        self.password_label.grid(row=4, column=0)

        self.password_entry = tk.Entry(width=21, fg="black", bg="white", highlightbackground="lightblue")
        self.password_entry.grid(row=4, column=1)

        self.generate_password_button = tk.Button(text="Generate Password", fg="black", highlightbackground="white",
                                                  command=self.generate_password)
        self.generate_password_button.grid(row=4, column=2)

        # notes
        self.notes_label = tk.Label(text="Notes:", fg="black", bg="white", highlightbackground="lightblue")
        self.notes_label.grid(row=5, column=0)

        self.notes_entry = tk.Text(width=38, height=5, fg="black", bg="white", highlightbackground="lightblue")
        self.notes_entry.grid(row=5, column=1, rowspan=2, columnspan=2)

        # add button
        self.add_button = tk.Button(text="Add", fg="black", highlightbackground="white", width=36, command=self.save)
        self.add_button.grid(row=7, column=1, columnspan=2)

    def get_values(self):
        self.website = self.website_entry.get()
        self.name = self.name_entry.get()
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        self.notes = self.notes_entry.get('1.0', 'end-1c')

        self.params = {
           'website': self.website,
           'name': self.name,
           'username': self.username,
           'password': self.password,
           'notes': self.notes
        }

    def password_object_maker(self):
        self.get_values()
        if len(self.name) == 0 or self.username == 0 or self.password == 0:
            messagebox.showwarning(title='Empty fields', message='name, username, and password must be filled')
            return
        return Password(self.params)

    def save(self):
        password_object = self.password_object_maker()
        if password_object:
            is_ok = messagebox.askokcancel(title="Review %s information"%password_object.website, message='Do you want to add this username/password?')
            if is_ok:
                try:
                    self.pm.add_password(password_object)
                except Exception as e:
                    print(e)
                else:
                    self.clear_entries()

    def clear_entries(self):
        self.website_entry.delete(0, 'end')
        self.name_entry.delete(0, 'end')
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.notes_entry.delete('1.0', 'end')

    def search(self):
        self.get_values()
        if self.website or self.name or self.username:
            try:
                results = self.pm.search_for_password(self.params)
            except Exception as e:
                print("Error:", e)
            else:
                if results:
                    for result in results:
                        copy_password = messagebox.askyesno(message='website: {}\nname: {}\nusername/email: {}\n\nwould you like to copy the password to the clipboard?'
                                                            .format(result['website'], result['name'], result['username'],
                                                                    result['password']))
                        if copy_password:
                            pyperclip.copy(result['password'])

                else:
                    messagebox.showinfo(message='Nothings matches this search')

    def generate_password(self, length=16, uppercase=True, lowercase=True, numbers=True, symbols=True):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                   'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        # arbitrarily decide to restrict to mostly characters
        nLettersFloor = floor(length * .66666)

        def get_n_chars(charset, length):
            nr_char = random.randint(1, length)
            if 'a' in charset:
                nr_char = max(nr_char, nLettersFloor)
            remaining_length = length - nr_char
            return nr_char, remaining_length

        nLetters, remaining_length = get_n_chars(letters, length)
        nNumbers, nSymbols = get_n_chars(numbers, remaining_length)

        password_list = [random.choice(charset) for charset, n in
                         zip([letters, numbers, symbols], [nLetters, nNumbers, nSymbols]) for _ in range(n)]
        random.shuffle(password_list)
        password = "".join(password_list)

        self.password_entry.insert(0, password)
        pyperclip.copy(password)
