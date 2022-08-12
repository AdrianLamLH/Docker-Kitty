from tkinter import *
import tkinter as tk

# Tkinter window screen setup
root = tk.Tk()
root.title("Tamagoch-deez")
root.resizable(False, False) # so Window cannot be resized
root.geometry(f'{root.winfo_screenwidth()-10}x{root.winfo_screenheight()-72}+0+0') # fit to window screen
# window is in front of all apps always and fullscreen i.e. no window topbar
root.attributes('-topmost',1)
root.wm_attributes('-fullscreen', 'True')

label= Label(root, text="This is a New Line Text", font= ('Helvetica 14 bold'), foreground= "red3")
label.place(relx = 0.5, rely = 0.5, anchor ='center')

# Make the window transparent
root.config(bg = '#add123')
root.wm_attributes('-transparentcolor','#add123')

# Running App loop
root.mainloop()