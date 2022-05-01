from tkinter import *
from tkinter import filedialog, messagebox

import json
import os
import sys

from Scripts.views import ViewDefault, ViewNavigation
from Scripts.vocable import Vocable


class MenuBar(Menu):
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
        self.fp = filedialog.askopenfilename(
            title="Open Deck",
            initialdir=os.getcwd(),
            filetypes=[
                ("json files", "*.json")
            ]
        )

        if self.fp:
            fn = os.path.split(self.fp)[1]
            try:
                with open(self.fp, encoding="UTF-8") as f:
                    data = json.load(f)
                    self.parent.deck_current = []
                    for item in data:
                        v = Vocable(item["words"][0], item["words"][1])
                        self.parent.deck_current.append(v)

                    self.parent.title(f"{fn} - Polish Trainer")
                    self.parent.lbl_status_file["text"] = fn
                    self.parent.view_controller.set_view(ViewNavigation)

                    self.menu_file.entryconfigure("Close...", state=NORMAL)
            except:
                error_msg = f"{self.fp}\nPolish Trainer cannot read this file.\n"\
                            "This is not a valid json file, or the format is incorrect"
                messagebox.showerror(title="Polish Trainer", message=error_msg)

    def deck_close(self):
        self.close = messagebox.askyesno(
            title="Close Deck",
            message="Are you sure you want to close the current deck?\nAny unsaved changes will be lost."
        )
        if self.close:
            self.menu_file.entryconfigure("Close...", state=DISABLED)
            self.parent.deck_current = []

            self.parent.title("No deck selected - Polish Trainer")
            self.parent.lbl_status_file["text"] = "No deck selected"
            self.parent.lbl_status_view["text"] = ""
            self.parent.lbl_status_wordcount["text"] = ""

            self.parent.view_controller.set_view(ViewDefault)

    @staticmethod
    def exit():
        sys.exit()

    @staticmethod
    def about():
        messagebox.showinfo(title="About", message="Polish Trainer v0.3")
