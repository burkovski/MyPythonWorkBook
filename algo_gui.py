from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText
import os


class EmptyFileError(Exception):
    pass


class BigEndianCmd:
    def __init__(self, path=None):
        self.arrive = None
        self.path = path

    def __str__(self):
        return str(self.get_arrive(sort=True))

    def safe_openfile(self):
        reply = None
        try:
            self.openfile()
        except FileNotFoundError:
            reply = "No such file or directory '{}'!"
        except ValueError:
            reply = "Invalid data in file '{}'!"
        except EmptyFileError:
            reply = "Empty file '{}', no data for display!"
        if reply: return reply.format(os.path.abspath(self.path))

    def openfile(self):
        with open(self.path) as infile:
            line = infile.readline()
            if not line:
                raise EmptyFileError
            self.arrive = [int(item) for item in line.split()]
        return True

    def big_endian(self):
        return str(sorted(self.arrive))

    def get_arrive(self, *, sort=False):
        if not self.arrive:
            error_reply = self.safe_openfile()
            if error_reply: return error_reply
        return self.big_endian() if sort else self.arrive


class BigEndianGUI(BigEndianCmd):
    def __init__(self, root=None):
        super(BigEndianGUI, self).__init__()
        if not root:
            root = Tk()
        root.title("Big-Endian Arrive")
        root.minsize(width=640, height=480)
        # root.maxsize(width=480, height=360)
        root.iconbitmap(r".\py.ico")
        self.root = root
        self.file_path = StringVar(value='')
        self.file_text = False
        self.buttons_config = (
            ("Open...", self.on_open, LEFT),
            ("Show", self.on_show, LEFT),
            ("Clear", self.on_clear, LEFT),
            ("Quit", self.on_quit, LEFT)
        )
        self.buttons_width = max(len(text)+2 for text, *rest in self.buttons_config)
        self.text_area = None
        self.make_widgets()

    def make_widgets(self):
        box = Frame(self.root)
        toolbox = Frame(box)
        entry = Entry(toolbox, textvariable=self.file_path)
        entry.pack(side=LEFT, expand=YES, fill=X)
        for text, command, side in self.buttons_config:
            button = Button(toolbox, text=text, command=command, width=self.buttons_width)
            button.pack(side=side)
        toolbox.pack(side=TOP, anchor=N, fill=X)
        self.text_area = ScrolledText(box)
        self.text_area.pack(side=TOP, anchor=N, expand=YES, fill=BOTH)
        box.pack(side=TOP, expand=YES, fill=BOTH)

    def ask_clear(self,):
        if self.file_text:
            return askokcancel("Submit clear", "Are you sure want ot clear?")
        return True

    def on_open(self):
        if self.ask_clear():
            path = askopenfilename()
            if path:
                self.path = path
                reply = self.safe_openfile()
                if reply:
                    showerror("Error!", reply)
                else:
                    self.file_path.set(path)

    def on_show(self):
        if self.file_path.get():
            if self.text_area:
                if not self.on_clear():
                    return
            text = str(self)
            self.text_area.insert("1.0", text)
            self.file_text = True
        else:
            showerror("Error!", "You should enter file path before show!")

    def on_clear(self):
        if self.file_text:
            user_reply = askokcancel("Submit clear", "Are you sure want ot clear?")
            if user_reply:
                # self.file_path.set("")
                self.text_area.delete("1.0", END)
                self.file_text = False
            return user_reply
        return True

    def on_quit(self):
        if askyesno("Verify quit", "Are you sure want to quit?"):
            self.root.quit()


root = Tk()
win = BigEndianGUI(root)
root.mainloop()
