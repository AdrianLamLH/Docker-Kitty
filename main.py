from tkinter import *
import tkinter as tk

# Tkinter window screen setup
root = tk.Tk()
root.title("Tamagoch-deez")
root.resizable(False, False) # so Window cannot be resized
root.geometry(f'{root.winfo_screenwidth()-10}x{root.winfo_screenheight()-72}+0+0')
root.wm_attributes('-transparentcolor','#add123')


# Running App loop
root.mainloop()