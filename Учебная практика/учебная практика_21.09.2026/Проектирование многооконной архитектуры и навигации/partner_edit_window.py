import tkinter as tk

from style import BACKGROUND, FONT


class PartnerEditWindow(tk.Toplevel):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.title("CRM: Карточка партнера [Добавление]")
        self.geometry("700x600")
        self.configure(bg=BACKGROUND)
        self.protocol("WM_DELETE_WINDOW", self.go_back)

        back_button = tk.Button(self, text="Назад", font=(FONT, 12),
                                command=self.go_back)
        back_button.pack(side="bottom", anchor="e", padx=20, pady=20)

    def go_back(self):
        self.destroy()
        self.main_window.deiconify()
