import re
from tkinter import *
from tkinter.messagebox import *


class InvalidInfixForm(Exception):
    pass


class InvalidNotation(Exception):
    pass


class PolishNotation:
    def __init__(self, any_str=""):
        self.in_str = any_str
        self.out_str = None
        self.operator = None
        self.operands = []
        self.notations = {"postfix": self.postfix_notation,
                          "prefix": self.prefix_notation}
        self.operator_patt = re.compile(r"[+\-*/]")
        self.item_patt = re.compile(r"-?\d+")
        self.spaces_patt = re.compile(r"\s+")
        self.polish_notation_patt = re.compile(r"^-?\d+\s+[+\-*/]\s+-?\d+$")

    def __str__(self):
        return self.out_str or "No string yet! Inner string: '{}'".format(self.in_str)

    def verify_str(self):
        return self.polish_notation_patt.match(self.in_str)

    def is_operator(self, token):
        return self.operator_patt.match(token)

    def is_operand(self, token):
        return self.item_patt.match(token)

    def is_spaces(self, token):
        return self.spaces_patt.match(token)

    def conversion(self):
        self.operands.clear()
        if self.verify_str():
            for token in re.split(self.spaces_patt, self.in_str):
                if self.is_operand(token):
                    if token.startswith('-'):
                        token = "({})".format(token)
                    self.operands.append(token)
                elif self.is_operator(token):
                    self.operator = token
        else:
            raise InvalidInfixForm("Invalid string!")

    def prefix_notation(self):
        self.conversion()
        return [item for item in [self.operator] + self.operands]

    def postfix_notation(self):
        self.conversion()
        return [item for item in self.operands + [self.operator]]

    def reply(self, *, notation_type):
        if notation_type not in self.notations:
            raise InvalidNotation("Invalid notation: '{}'!".format(notation_type))
        expression = self.notations[notation_type]()
        self.out_str = ' '.join(expression)
        return self.out_str


class PolishNotationGUI(PolishNotation):
    def __init__(self, root=None):
        super(PolishNotationGUI, self).__init__()
        if not root:
            root = Tk()
        root.title("PolishNotation")
        root.iconbitmap(r'.\py.ico')
        self.root = root
        self.fields = ["Infix form"]
        self.fields.extend(("{} form".format(form.capitalize())
                            for form in self.notations))
        self.variables = []
        self.make_widgets()
        # assert len(self.fields) == len(self.notations) + 1 == len(self.variables)
        self.root.bind("<Return>", lambda event: self.on_conversion())
        self.root.bind("<Escape>", lambda event: self.on_quit())

    def make_widgets(self):
        frame = Frame(self.root)
        for field in self.fields:
            row = Frame(frame)
            lab = Label(row, text=field, width=max(map(len, self.fields)) + 1)
            row.pack()
            ent = Entry(row)
            var = StringVar()
            self.variables.append(var)
            ent.config(textvariable=var)
            row.pack(side=TOP, fill=X)  # прикрепить к верхнему краю
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
        Button(frame, text="Conversion", command=self.on_conversion).pack(expand=YES, fill=X)
        row = Frame(frame)
        btns_config = (("Clear", self.on_clear, LEFT), ("Quit", self.on_quit, RIGHT))
        for text, command, side in btns_config:
            Button(row, text=text, command=command).pack(side=side, expand=YES, fill=X)
        row.pack(side=TOP, fill=X)
        frame.pack(side=TOP, expand=YES, fill=X, anchor=N)

    def on_conversion(self):
        to_read, *to_set = self.variables
        self.in_str = to_read.get()
        try:
            responses = [self.reply(notation_type=n)
                         for n in self.notations]
        except InvalidInfixForm as exc:
            showerror("Error!", exc)
        else:
            for var, resp in zip(to_set, responses):
                var.set(resp)

    @staticmethod
    def question(title, text):
        return askyesno(title, text)

    def on_clear(self):
        if any(var.get() for var in self.variables):
            if self.question("Verify clear", "Are you sure want ot clear?"):
                for var in self.variables:
                    var.set("")
                self.operands.clear()
                self.operator = None
        else:
            showinfo("Clear unsuccessfully!", "No fields to clear!")

    def on_quit(self):
        if self.question("Verify quit", "Are you sure want to quit?"):
            self.root.quit()


if __name__ == "__main__":
    root = Tk()
    pn_gui = PolishNotationGUI(root)
    root.mainloop()
