import tkinter as tk
from tkinter import ttk

from style import BACKGROUND, FONT, HINT, TEXT

PHONE_HINT = "+7 900 123 45 67"
EMAIL_HINT = "info@company.ru"


def create_field_label(form, text, row):
    label = tk.Label(form, text=text, font=(FONT, 12),
                     bg=BACKGROUND, fg=TEXT)
    label.grid(row=row, column=0, sticky="w", padx=(0, 15), pady=5)


def create_entry(form, text, row):
    create_field_label(form, text, row)
    entry = tk.Entry(form, font=(FONT, 12))
    entry.grid(row=row, column=1, sticky="ew", pady=5)
    return entry


def add_placeholder(entry, hint):
    # Подсказка отличается от введённого текста только серым цветом:
    # при входе в поле она стирается, из пустого поля возвращается.
    def show_hint(event=None):
        if entry.get() == "":
            entry.insert(0, hint)
            entry.configure(fg=HINT)

    def hide_hint(event):
        if entry.cget("fg") == HINT:
            entry.delete(0, "end")
            entry.configure(fg=TEXT)

    entry.bind("<FocusIn>", hide_hint)
    entry.bind("<FocusOut>", show_hint)
    show_hint()


class PartnerEditWindow(tk.Toplevel):
    def __init__(self, main_window, partner_types):
        super().__init__(main_window)
        self.main_window = main_window
        self.title("CRM: Карточка партнера [Добавление]")
        self.geometry("700x600")
        self.configure(bg=BACKGROUND)
        # Крестик работает как «Назад», иначе спрятанное главное окно
        # так и останется невидимым.
        self.protocol("WM_DELETE_WINDOW", self.go_back)

        self.create_form(partner_types)

        back_button = tk.Button(self, text="Назад", font=(FONT, 12),
                                command=self.go_back)
        back_button.pack(side="bottom", anchor="e", padx=20, pady=20)

    def create_form(self, partner_types):
        form = tk.Frame(self, bg=BACKGROUND)
        form.pack(fill="x", padx=20, pady=20)
        form.columnconfigure(1, weight=1)

        self.name_entry = create_entry(form, "Наименование", 0)

        create_field_label(form, "Тип партнера", 1)
        # Значения — из справочника partner_types; readonly запрещает
        # вводить свой тип, можно только выбрать из списка.
        self.type_combobox = ttk.Combobox(form, values=partner_types,
                                          state="readonly",
                                          font=(FONT, 12))
        self.type_combobox.grid(row=1, column=1, sticky="ew", pady=5)

        create_field_label(form, "Рейтинг", 2)
        # Граница 10 та же, что в CHECK столбца rating.
        self.rating_spinbox = tk.Spinbox(form, from_=0, to=10,
                                         increment=1, width=5,
                                         font=(FONT, 12))
        self.rating_spinbox.grid(row=2, column=1, sticky="w", pady=5)

        self.address_entry = create_entry(form, "Адрес", 3)
        self.director_entry = create_entry(form, "ФИО директора", 4)

        self.phone_entry = create_entry(form, "Телефон", 5)
        add_placeholder(self.phone_entry, PHONE_HINT)
        self.email_entry = create_entry(form, "Email компании", 6)
        add_placeholder(self.email_entry, EMAIL_HINT)

    def go_back(self):
        self.destroy()
        self.main_window.deiconify()
