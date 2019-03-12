from tkinter import *


root = Tk()
m_button = Menubutton(root, text="Food")
picks = Menu(m_button)
m_button.config(menu=picks)

picks.add_command(label="spam", command=root.quit)
picks.add_command(label="eggs", command=root.quit)
picks.add_command(label="bacon", command=root.quit)

m_button.pack()
m_button.config(bg="white", bd=4, relief=RAISED)
root.mainloop()
