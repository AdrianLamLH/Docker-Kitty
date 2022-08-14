import tkinter as tk
root = tk.Tk()
root.withdraw()
root.geometry('400x300')
root.config(bg='#84BF04')

message ='''
Dear Reader,

    Thank you for giving your
    Love and Support to PythonGuides.
    PythonGuides is now available on 
    YouTube with the same name.

Thanks & Regards,
Team PythonGuides '''

text_box = Text(
    root,
    height=12,
    width=40
)
text_box.pack(expand=True)
text_box.insert('end', message)
text_box.config(state='disabled')

root.mainloop()