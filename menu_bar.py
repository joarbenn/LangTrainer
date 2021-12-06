from tkinter import *
from tkinter import filedialog, messagebox

import json
import os
import sys

from views import View_Default, View_Navigation
from vocable import Vocable

class Menu_Bar(Menu):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.menu_file = Menu(self, tearoff=False)
        self.menu_file.add_command(label="Open... (Ctrl+O)", command=self.deck_open)
        self.menu_file.add_command(label="Close...", command=self.deck_close, state=DISABLED)

        self.menu_file.add_separator()
        self.menu_file.add_command(label="Exit", command=self.exit)

        self.menu_help = Menu(self, tearoff=False)
        self.menu_help.add_command(label="About", command=self.about)

        self.add_cascade(label="File", menu=self.menu_file)
        self.add_cascade(label="Help", menu=self.menu_help)

    def deck_open(self):
        fp = filedialog.askopenfilename(
            title="Open Deck",
            initialdir=os.getcwd(),
            filetypes=[
                ("json files", "*.json")
            ]
        )

        if fp:
            fn = os.path.split(fp)[1]
            try:
                self.menu_file.entryconfigure("Close...", state=NORMAL)

                with open(fp, encoding="UTF-8") as f:
                    data = json.load(f)
                    self.parent.deck_current = []
                    for item in data["words"]:
                        v = Vocable(item["english"], item["polish"])
                        self.parent.deck_current.append(v)
                    self.parent.title(f"{fn} - Polish Trainer")
                    self.parent.lbl_status_file["text"] = fn
                    self.parent.view_controller.set_view(View_Navigation)
            except:
                error_msg = f"{fp}\nPolish Trainer cannot read this file.\n"\
                            "This is not a valid json file, or the format is incorrect"
                messagebox.showerror(title="Polish Trainer", message=error_msg)

    def deck_close(self):
        self.menu_file.entryconfigure("Close...", state=DISABLED)
        self.parent.deck_current = []

        self.parent.title("No deck selected - Polish Trainer")
        self.parent.lbl_status_file["text"] = "No deck selected"
        self.parent.lbl_status_view["text"] = ""
        self.parent.lbl_status_wordcount["text"] = ""

        self.parent.view_controller.set_view(View_Default)

    @staticmethod
    def exit():
        sys.exit()

    @staticmethod
    def about():
        messagebox.showinfo(title="About", message="Polish Trainer v0.3")