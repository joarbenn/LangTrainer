from tkinter import *
from tkinter import ttk, filedialog, messagebox

import json
import random
import os
import sys

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

class View_Controller:
    def __init__(self, app):
        self.app = app

    def set_view(self, View):
        self.app.active_view.destroy()
        self.app.active_view = View(self.app, self)
        self.app.active_view.pack(pady=5)

class View_Default(Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller

class View_Navigation(Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller

        self.btn_play = ttk.Button(self, text="Play Deck", command=self.btn_play_click, width=10)
        self.btn_edit = ttk.Button(self, text="Edit Deck", command=self.btn_edit_click, width=10)

        self.btn_play.grid(row=0, column=0, columnspan=2, padx=2, ipady=1)
        self.btn_edit.grid(row=1, column=0, columnspan=2, padx=2, pady=2, ipady=1)

    def btn_play_click(self):
        self.controller.set_view(View_Play)

    def btn_edit_click(self):
        self.controller.set_view(View_Edit)

class View_Play(Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller

        self.deck_temp = controller.app.deck_current.copy()
        controller.app.lbl_status_wordcount["text"] = f"- word 1 of {len(controller.app.deck_current)}"
        controller.app.lbl_status_view["text"] = "- Playing"

        # Shuffle the deck to make sure word order is different each time
        random.shuffle(self.deck_temp)

        self.btn_cancel = ttk.Button(self, text="Back to Main", command=self.btn_back_click, width=15)
        self.btn_cancel.grid(row=0, column=0, columnspan=2, padx=2, ipady=1)

        self.lbl_word = ttk.Label(self, text=self.deck_temp[0].pol_words[0].capitalize(), font=("Calibri", 40))
        self.lbl_word.grid(row=3, column=0, columnspan=2, sticky="w")

        # Create list containing valid answers to the selected word
        self.answers = [x.lower() for x in self.deck_temp[0].eng_words]

        self.entry_word = ttk.Entry(self)
        self.entry_word.grid(row=4, column=0, columnspan=2, pady=4)
        self.entry_word.focus()

        self.controller.app.bind("<Escape>", lambda x: self.btn_back_click())
        self.entry_word.bind("<Return>", lambda x: self.checkword())

    def checkword(self):
        self.txt_correct = ttk.Label(self, font=("Calibri", 8))

        if self.entry_word.get().lower() in self.answers:
            self.entry_word["foreground"] = "Green"
            self.deck_temp.pop(0)
        else:
            self.txt_correct.grid(row=5, column=0, columnspan=2, pady=2)
            self.entry_word["foreground"] = "Red"
            self.txt_correct["text"] = f"Correct Answer: {self.answers[0]}"
            self.deck_temp.append(self.deck_temp.pop(0))

        if len(self.deck_temp) == 0:
            self.btn_nextword_click()
        else:
            self.btn_nextword = ttk.Button(self, text="Next", command="", width=5)
            self.btn_nextword.grid(row=6, column=0, columnspan=2)
            self.btn_nextword.focus()
            self.btn_nextword.bind("<Return>", lambda x: self.btn_nextword_click())

    def btn_nextword_click(self):
        self.btn_nextword.grid_forget()
        self.txt_correct.grid_forget()

        if len(self.deck_temp) == 0:
            self.lbl_done = ttk.Label(self, text="All words completed!")
            self.lbl_done.grid(row=7, column=0, columnspan=2)

            self.btn_cancel.focus()
            self.btn_cancel.bind("<Return>", lambda x: self.btn_back_click())
        else:
            self.entry_word["foreground"] = "Black"
            self.bind("<Return>", lambda x: self.checkword())
            self.controller.app.lbl_status_wordcount["text"] = f"- word {len(self.controller.app.deck_current) - len(self.deck_temp) + 1} of {len(self.controller.app.deck_current)}"

            self.entry_word.focus()
            self.lbl_word["text"] = self.deck_temp[0].pol_words[0].capitalize()
            self.answers = [x.lower() for x in self.deck_temp[0].eng_words]
            self.entry_word.delete(0, 'end')

    def btn_back_click(self):
        self.controller.app.lbl_status_wordcount["text"] = ""
        self.controller.app.lbl_status_view["text"] = ""
        self.controller.set_view(View_Navigation)

class View_Edit(Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        self.controller = controller
        self.deck_temp = self.controller.app.deck_current.copy()
        self.update_view()

    def update_view(self, vocableid=0):
        self.vocableid = vocableid

        for widget in self.winfo_children():
            widget.destroy()

        self.btn_cancel = ttk.Button(self, text="Back to Main", command=self.btn_back_click, width=15)
        self.btn_cancel.pack()
        # self.btn_cancel.grid(row=0, column=0, columnspan=2, padx=2, ipady=1)

        if self.vocableid > len(self.deck_temp) - 1:
            self.vocableid = len(self.deck_temp) - 1
        if self.vocableid < 0:
            self.vocableid = 0

        self.controller.app.lbl_status_view["text"] = "- Editing"
        self.controller.app.lbl_status_wordcount["text"] = f"- word {self.vocableid + 1} of {len(self.deck_temp)}"

        self.frm_vocable_words = Frame(self)
        self.frm_vocable_nav = Frame(self)

        self.entry_vars = [[], []]

        for idx, word in enumerate(self.deck_temp[self.vocableid].pol_words):
            self.entry_var = StringVar()
            self.entry_vars[0].append(self.entry_var)
            self.entry = ttk.Entry(self.frm_vocable_words, font=("Arial", 8), textvariable=self.entry_var)
            self.entry.insert(0, word)
            self.entry.grid(row=2 + idx, column=1, pady=1)
        for idx, word in enumerate(self.deck_temp[self.vocableid].eng_words):
            self.entry_var = StringVar()
            self.entry_vars[1].append(self.entry_var)
            self.entry = ttk.Entry(self.frm_vocable_words, font=("Arial", 8), textvariable=self.entry_var)
            self.entry.insert(0, word)
            self.entry.grid(row=2 + idx, column=2, padx=(2, 0), sticky="e")

        self.frm_vocable_words.pack(pady=20)
        self.frm_vocable_nav.pack(side="bottom", pady=20, padx=20)

        self.btn_prev = ttk.Button(
            self.frm_vocable_nav,
            text="Prev", width=8,
            command=lambda: self.update_view(self.vocableid - 1)
        )
        self.controller.app.bind("<Left>", lambda x: self.update_view(self.vocableid - 1))
        self.btn_prev.grid(row=0, column=0)

        self.btn_next = ttk.Button(
            self.frm_vocable_nav,
            text="Next", width=8,
            command=lambda: self.update_view(self.vocableid + 1)
        )
        self.controller.app.bind("<Right>", lambda x: self.update_view(self.vocableid + 1))
        self.btn_next.grid(row=0, column=1)

        self.controller.app.bind("<Escape>", lambda x: self.btn_back_click())

    def btn_back_click(self):
        self.controller.app.unbind("<Left>")
        self.controller.app.unbind("<Right>")
        self.controller.app.lbl_status_wordcount["text"] = ""
        self.controller.app.lbl_status_view["text"] = ""
        self.controller.set_view(View_Navigation)

class Vocable:
    def __init__(self, eng_words, pol_words):
        self.eng_words = eng_words
        self.pol_words = pol_words

if __name__ == "__main__":
    app = App("No deck selected - Polish Trainer", "400x240")
    app.mainloop()
