import tkinter as tk

from ui_manager import UiManager

FONT_NAME = "Arial"
FONT_SIZE = 14

#-------------------- UI SETUP --------------------#

window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="white")

canvas = tk.Canvas(window, width=200, height=200, bg="white", highlightthickness=0)
image = tk.PhotoImage(file="logo.png")
canvas.create_image(140, 100, image=image)
canvas.grid(row=0, column=1)

ui = UiManager()

window.mainloop()