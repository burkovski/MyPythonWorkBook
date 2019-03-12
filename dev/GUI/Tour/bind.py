from tkinter import *


def show_pos_event(event):
    print("Widget={0.widget} X={0.x} Y={0.y}".format(event))


def show_all_event(event):
    print(event)
    for attr in dir(event):
        if not attr.startswith('__'):
            print(attr, '=>', getattr(event, attr))


def on_key_press(event):
    print('Got key pressed:', event.char)


def on_arrow_key(event):
    print('Got up arrow key pressed')


def on_return_key(event):
    print('Got return key pressed')


def on_left_click(event):
    print('Got left button mouse clicked:', end=' ')
    show_pos_event(event)


def on_right_click(event):
    print('Got right button mouse clicked:', end=' ')
    show_pos_event(event)


def on_middle_click(event):
    print('Got middle mouse button clicked:', end=' ')
    show_pos_event(event)
    show_all_event(event)


def on_left_drag(event):
    print('Got left mouse button drag', end=' ')
    show_pos_event(event)


def on_doubleleft_click(event):
    print('Got double left button clicked:', end=' ')
    show_pos_event(event)
    root.quit()


root = Tk()
labelfont = ('courier', 20, 'bold')
widget = Label(root, text='Hello bind world')
widget.config(bg='red', font=labelfont)
widget.config(height=5, width=20)
widget.pack(expand=YES, fill=BOTH)
widget.bind('<Button-1>', on_left_click)
widget.bind('<Button-3>', on_right_click)
widget.bind('<Button-2>', on_middle_click)
widget.bind('<Double-1>', on_doubleleft_click)
widget.bind('<B1-Motion>', on_left_drag)
widget.bind('<KeyPress>', on_key_press)
widget.bind('<Up>', on_arrow_key)
widget.bind('<Return>', on_return_key)
# widget.focus()


root.title('Click me')
root.mainloop()
