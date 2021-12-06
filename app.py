from tkinter import *

from views import View_Controller, View_Default
from menu_bar import Menu_Bar

class App(Tk):
    def __init__(self, title, geometry):
        super().__init__()

        self.title(title)
        self.geometry(geometry)

        # Menubar
        self.menubar = Menu_Bar(self)
        self.config(menu=self.menubar)
        self.bind("<Control-o>", lambda _: self.menubar.deck_open())

        # Create View Controller and set the Active View to default
        self.view_controller = View_Controller(self)
        self.active_view = View_Default(self, self.view_controller)

        # Status Bar
        self.status_bar = Frame(self, bd=1, relief="sunken", bg="#DFDFDF")
        self.status_bar.pack(side="bottom", fill="x")

        self.lbl_status_file = Label(self.status_bar, text="No Deck Selected", bg="#DFDFDF", font=("Arial", 8))
        self.lbl_status_file.grid(row=0, column=0)

        self.lbl_status_view = Label(self.status_bar, text="", bg="#DFDFDF", font=("Arial", 8))
        self.lbl_status_view.grid(row=0, column=1)

        self.lbl_status_wordcount = Label(self.status_bar, text="", bg="#DFDFDF", font=("Arial", 8))
        self.lbl_status_wordcount.grid(row=0, column=2)

        # Create empty deck list
        self.deck_current = []