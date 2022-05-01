from tkinter import *
from tkinter import ttk

from Scripts.views import ViewController, ViewDefault
from Scripts.menubar import MenuBar


class App(Tk):
    def __init__(self, title, geometry):
        super().__init__()

        self.title(title)
        self.geometry(geometry)
        self.config(bg="#FFFFFF")

        # Menubar
        self.menubar = MenuBar(self)
        self.config(menu=self.menubar)
        self.bind("<Control-o>", lambda _: self.menubar.deck_open())

        # Create View Controller and set the Active View to default
        self.view_controller = ViewController(self)
        self.active_view = ViewDefault(self, self.view_controller)

        # Default Styles
        self.style = ttk.Style(self)
        self.style.configure("TFrame", background="#FFFFFF")
        self.style.configure("TLabel", background="#FFFFFF")
        self.style.configure(
            "TButton",
            background="#FFF",
            borderwidth=1,
            foreground="#000",
            focusthickness=0,
            focuscolor='none',
            font=("Calibri", 10))
        self.style.configure("Delete.TButton", foreground="#F00")
        self.style.configure("Add.TButton", foreground="#00AA00")

        # Specific Styles
        self.style.configure("Statusbar.TFrame", background="#E6E6E6")
        self.style.configure("Statusbar.TLabel", background="#E6E6E6")

        # Status Bar
        self.status_bar = ttk.Frame(self, borderwidth=1, style="Statusbar.TFrame")
        self.status_bar.pack(side="bottom", fill="x")

        self.lbl_status_file = ttk.Label(
            self.status_bar,
            text="No Deck Selected",
            font=("Calibri", 8),
            style="Statusbar.TLabel"
        )
        self.lbl_status_file.grid(row=0, column=0)

        self.lbl_status_view = ttk.Label(self.status_bar, text="", font=("Calibri", 8), style="Statusbar.TLabel")
        self.lbl_status_view.grid(row=0, column=1)

        self.lbl_status_wordcount = ttk.Label(self.status_bar, text="", font=("Calibri", 8), style="Statusbar.TLabel")
        self.lbl_status_wordcount.grid(row=0, column=2)

        # Create empty deck list
        self.deck_current = []
