from tkinter import *
from tkinter import ttk, messagebox
from copy import deepcopy

import random
import functools
import jsonpickle

from Scripts.vocable import Vocable

class View_Controller:
    def __init__(self, app):
        self.app = app

    def set_view(self, View):
        self.app.active_view.destroy()
        self.app.active_view = View(self.app, self)
        self.app.active_view.pack(pady=5)

class View_Default(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller

class View_Navigation(ttk.Frame):
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

class View_Play(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller

        self.deck_temp = list(controller.app.deck_current)
        controller.app.lbl_status_wordcount["text"] = f"- word 1 of {len(controller.app.deck_current)}"
        controller.app.lbl_status_view["text"] = "- Playing"

        # Shuffle the deck to make sure word order is different each time
        random.shuffle(self.deck_temp)

        self.btn_cancel = ttk.Button(self, text="Back to Main", command=self.btn_back_click, width=15)
        self.btn_cancel.grid(row=0, column=0, columnspan=2, padx=2, ipady=1)

        self.lbl_word = ttk.Label(self, text=self.deck_temp[0].words[0][0], font=("Calibri", 40))
        self.lbl_word.grid(row=3, column=0, columnspan=2, sticky="w")

        # Create list containing valid answers to the selected word
        self.answers = [x.lower() for x in self.deck_temp[0].words[1]]

        self.entry_word = ttk.Entry(self)
        self.entry_word.grid(row=4, column=0, columnspan=2, pady=4)
        self.entry_word.focus()

        # Pre-create widgets that are gridded later
        self.txt_correct = ttk.Label(self, font=("Calibri", 8))
        self.btn_nextword = ttk.Button(self, text="Next", command="", width=5)
        self.lbl_done = ttk.Label(self, text="All words completed!")

        self.controller.app.bind("<Escape>", lambda x: self.btn_back_click())
        self.entry_word.bind("<Return>", lambda x: self.checkword())

    def checkword(self):
        if self.entry_word.get().lower().strip() in self.answers:
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
            self.btn_nextword.grid(row=6, column=0, columnspan=2)
            self.btn_nextword.focus()
            self.btn_nextword.bind("<Return>", lambda x: self.btn_nextword_click())

    def btn_nextword_click(self):
        self.btn_nextword.grid_forget()
        self.txt_correct.grid_forget()

        if len(self.deck_temp) == 0:
            self.lbl_done.grid(row=7, column=0, columnspan=2)

            self.btn_cancel.focus()
            self.btn_cancel.bind("<Return>", lambda x: self.btn_back_click())
        else:
            self.entry_word["foreground"] = "Black"
            self.bind("<Return>", lambda x: self.checkword())
            self.controller.app.lbl_status_wordcount["text"] = f"- word {len(self.controller.app.deck_current) - len(self.deck_temp) + 1} of {len(self.controller.app.deck_current)}"

            self.entry_word.focus()
            self.lbl_word["text"] = self.deck_temp[0].words[0][0].capitalize()
            self.answers = [x.lower() for x in self.deck_temp[0].words[1]]
            self.entry_word.delete(0, 'end')

    def btn_back_click(self):
        self.controller.app.lbl_status_wordcount["text"] = ""
        self.controller.app.lbl_status_view["text"] = ""
        self.controller.set_view(View_Navigation)

class View_Edit(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        self.controller = controller
        self.deck_temp = deepcopy(self.controller.app.deck_current)
        self.update_view()

    def update_view(self, vocableid=0):
        self.vocableid = vocableid

        for widget in self.winfo_children():
            widget.destroy()

        self.btn_cancel = ttk.Button(self, text="Back to Main", command=self.btn_back_click, width=15)
        self.btn_cancel.pack()
        # self.btn_cancel.grid(row=0, column=0, columnspan=2, padx=2, ipady=1)

        if self.vocableid > len(self.deck_temp) - 1:
            self.vocableid = 0
        if self.vocableid < 0:
            self.vocableid = len(self.deck_temp) - 1

        self.controller.app.lbl_status_view["text"] = "- Editing"
        self.controller.app.lbl_status_wordcount["text"] = f"- word {self.vocableid + 1} of {len(self.deck_temp)}"

        self.frm_vocable_words = ttk.Frame(self)
        self.frm_vocable_nav = ttk.Frame(self)

        self.entry_vars = [[], []]

        self.btn_addvocable = ttk.Button(
            self.frm_vocable_words,
            text="Add",
            width=8,
            style="Add.TButton",
            command=self.btn_add_vocable
        )

        self.btn_removevocable = ttk.Button(
            self.frm_vocable_words,
            text="Delete",
            width=8,
            style="Delete.TButton",
            command=self.btn_delete_vocable
        )
        self.btn_addvocable.grid(row=0, column=1, columnspan=4, pady=2)
        self.btn_removevocable.grid(row=1, column=1, columnspan=4, pady=(0, 10))

        for idx, word in enumerate(self.deck_temp[self.vocableid].words[0]):
            self.entry_var = StringVar()
            self.entry_vars[0].append(self.entry_var)
            self.entry = ttk.Entry(self.frm_vocable_words, font=("Arial", 8), textvariable=self.entry_var)
            self.entry.insert(0, word)
            self.entry.grid(row=2 + idx, column=1, pady=1)

            self.btn_removeword = ttk.Button(
                self.frm_vocable_words,
                text="-",
                width=2,
                style="Delete.TButton",
                command=functools.partial(self.btn_delete_word, langid=0, row=idx)
            )
            self.btn_removeword.grid(row=2 + idx, column = 2)
        for idx, word in enumerate(self.deck_temp[self.vocableid].words[1]):
            self.entry_var = StringVar()
            self.entry_vars[1].append(self.entry_var)
            self.entry = ttk.Entry(self.frm_vocable_words, font=("Arial", 8), textvariable=self.entry_var)
            self.entry.insert(0, word)
            self.entry.grid(row=2 + idx, column=3, padx=(2, 0), sticky="e")

            self.btn_removeword = ttk.Button(
                self.frm_vocable_words,
                text="-",
                width=2,
                style="Delete.TButton",
                command=functools.partial(self.btn_delete_word, langid=1, row=idx)
            )
            self.btn_removeword.grid(row=2 + idx, column=4)

        self.btn_addword = ttk.Button(
            self.frm_vocable_words,
            text="+",
            width=2,
            style="Add.TButton",
            command=lambda: self.btn_add_word(0)
        )
        self.btn_addword.grid(row=2 + len(self.deck_temp[self.vocableid].words[0]), column=1)

        self.btn_addword = ttk.Button(
            self.frm_vocable_words,
            text="+",
            width=2,
            style="Add.TButton",
            command=lambda: self.btn_add_word(1)
        )
        self.btn_addword.grid(row=2 + len(self.deck_temp[self.vocableid].words[1]), column=3)

        self.frm_vocable_words.pack(pady=20)
        self.frm_vocable_nav.pack(side="bottom", pady=20)

        self.btn_prev = ttk.Button(
            self.frm_vocable_nav,
            text="Prev", width=8,
            command=lambda: self.switch_vocable(self.vocableid - 1)
        )
        self.controller.app.bind("<Left>", lambda x: self.switch_vocable(self.vocableid - 1))
        self.btn_prev.grid(row=0, column=0)

        self.btn_next = ttk.Button(
            self.frm_vocable_nav,
            text="Next", width=8,
            command=lambda: self.switch_vocable(self.vocableid + 1)
        )
        self.controller.app.bind("<Right>", lambda x: self.switch_vocable(self.vocableid + 1))
        self.btn_next.grid(row=0, column=1)

        self.controller.app.bind("<Escape>", lambda x: self.btn_back_click())

    def switch_vocable(self, vocable):
        self.update_deck_list()
        self.update_view(vocable)

    def update_deck_list(self):
        self.deck_temp[self.vocableid].words[0] = []
        self.deck_temp[self.vocableid].words[1] = []

        for ev in self.entry_vars[0]:
            self.deck_temp[self.vocableid].words[0].append(ev.get())
        for ev in self.entry_vars[1]:
            self.deck_temp[self.vocableid].words[1].append(ev.get())

    def btn_add_word(self, langid):
        self.update_deck_list()
        if langid == 0:
            self.deck_temp[self.vocableid].words[0].append("")
            self.update_view(self.vocableid)
        if langid == 1:
            self.deck_temp[self.vocableid].words[1].append("")
            self.update_view(self.vocableid)

    def btn_delete_word(self, langid, row):
        self.update_deck_list()
        if langid == 0:
            if len(self.deck_temp[self.vocableid].words[0]) > 1:
                self.deck_temp[self.vocableid].words[0].pop(row)
                self.update_view(self.vocableid)
            else:
                messagebox.showerror(title="Error", message="Cannot remove last word from a vocable.")
        if langid == 1:
            if len(self.deck_temp[self.vocableid].words[1]) > 1:
                self.deck_temp[self.vocableid].words[1].pop(row)
                self.update_view(self.vocableid)
            else:
                messagebox.showerror(title="Error", message="Cannot remove last word from a vocable.")

    def btn_add_vocable(self):
        self.update_deck_list()
        v = Vocable([""], [""])
        self.deck_temp.insert(0, v)
        self.update_view(0)

    def btn_delete_vocable(self):
        if len(self.deck_temp) > 1:
            self.update_deck_list()
            self.deck_temp.pop(self.vocableid)
            self.update_view(self.vocableid)
        else:
            self.update_deck_list()
            self.deck_temp.pop(self.vocableid)
            self.btn_back_click()

    def btn_back_click(self):
        self.update_deck_list()
        self.save = messagebox.askyesnocancel(title="Save changes", message="Do you want to save your changes?")

        if self.save != None:
            if self.save == True:
                self.controller.app.deck_current = deepcopy(self.deck_temp)
                jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)
                vocable_json = jsonpickle.encode(self.deck_temp, unpicklable=False)

                with open(self.controller.app.menubar.fp, "w") as f:
                    f.truncate(0)
                    f.write(vocable_json)

            self.controller.app.unbind("<Left>")
            self.controller.app.unbind("<Right>")
            self.controller.app.lbl_status_wordcount["text"] = ""
            self.controller.app.lbl_status_view["text"] = ""
            self.controller.set_view(View_Navigation)