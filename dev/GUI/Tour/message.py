from tkinter import *


root = Tk()
msg = Message(root, text="Oh by the way, which one's Pink?")
msg.config(bg='Pink', font=('times', 16, 'italic'))
msg.pack(expand=YES, fill=X)
root.mainloop()
