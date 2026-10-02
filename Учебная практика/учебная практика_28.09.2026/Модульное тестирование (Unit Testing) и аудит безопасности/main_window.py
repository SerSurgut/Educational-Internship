import tkinter as tk
from pathlib import Path
from tkinter import messagebox

import psycopg2

from app_log import log_error, setup_logging
from material_calculator_window import MaterialCalculatorWindow
from partner_edit_window import (DATABASE_ERROR, PartnerEditWindow,
                                 show_database_error)
from partner_history_window import PartnerHistoryWindow
from partner_service import (get_partner, get_partner_types,
                             get_partners_with_discount)
from style import BACKGROUND, BORDER, FONT, SELECTED, TEXT

RESOURCES = Path(__file__).parent / "resources"


def text_or_dash(value):
    if value is None:
        return "—"
    return str(value)


def format_phone(phone):
    if phone is None:
        return "—"
    return (f"{phone[:2]} {phone[2:5]} {phone[5:8]} "
            f"{phone[8:10]} {phone[10:]}")


def create_label(parent, text, size):
    return tk.Label(parent, text=text, font=(FONT, size),
                    bg=BACKGROUND, fg=TEXT)


def paint_card(card, color):
    card.configure(bg=color)
    for label in card.winfo_children():
        label.configure(bg=color)


def create_partner_card(parent, partner, select_partner, open_partner):
    card = tk.Frame(parent, bg=BACKGROUND, padx=25, pady=10,
                    highlightthickness=1, highlightbackground=BORDER)
    card.pack(fill="x", padx=20, pady=(15, 0))
    card.columnconfigure(0, weight=1)

    title = (text_or_dash(partner["partner_type"]) + " | "
             + partner["company_name"])
    create_label(card, title, 16).grid(row=0, column=0, sticky="w")
    discount = create_label(card, f"{partner['discount']}%", 16)
    discount.grid(row=0, column=1, sticky="e")
    director = create_label(card, text_or_dash(partner["director_name"]), 12)
    director.grid(row=1, column=0, sticky="w")
    phone = create_label(card, format_phone(partner["phone"]), 12)
    phone.grid(row=2, column=0, sticky="w")
    rating = "Рейтинг: " + text_or_dash(partner["rating"])
    create_label(card, rating, 12).grid(row=3, column=0, sticky="w")

    def on_click(event):
        select_partner(card, partner["partner_id"])

    def on_double_click(event):
        open_partner(partner["partner_id"])

    card.bind("<Button-1>", on_click)
    card.bind("<Double-Button-1>", on_double_click)
    for label in card.winfo_children():
        label.bind("<Button-1>", on_click)
        label.bind("<Double-Button-1>", on_double_click)


class MainWindow(tk.Tk):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        # Типы загружаются из базы один раз при запуске и передаются
        # в каждую открытую карточку.
        self.partner_types = get_partner_types(connection)
        self.selected_card = None
        self.selected_partner_id = None
        self.title("CRM: Реестр партнеров")
        self.geometry("700x600")
        self.configure(bg=BACKGROUND)

        self.icon_image = tk.PhotoImage(file=str(RESOURCES / "icon.png"))
        self.iconphoto(True, self.icon_image)
        self.logo_image = tk.PhotoImage(file=str(RESOURCES / "logo.png"))

        self.create_header()
        self.create_buttons()
        self.create_partner_list()

    def create_header(self):
        header = tk.Frame(self, bg=BACKGROUND)
        header.pack(fill="x", padx=20, pady=(20, 10))
        logo = tk.Label(header, image=self.logo_image, bg=BACKGROUND)
        logo.pack(side="left")
        title = create_label(header, "Список партнеров и скидок", 20)
        title.pack(side="left", padx=15)

    def create_buttons(self):
        buttons = tk.Frame(self, bg=BACKGROUND)
        buttons.pack(side="bottom", anchor="e", padx=20, pady=(0, 20))
        calculator_button = tk.Button(buttons, text="Расчет материалов",
                                      font=(FONT, 12),
                                      command=self.open_calculator_window)
        calculator_button.pack(side="left", padx=(0, 10))
        history_button = tk.Button(buttons, text="История продаж",
                                   font=(FONT, 12),
                                   command=self.open_history_window)
        history_button.pack(side="left", padx=(0, 10))
        add_button = tk.Button(buttons, text="Добавить партнера",
                               font=(FONT, 12),
                               command=self.open_partner_edit_window)
        add_button.pack(side="left")

    def create_partner_list(self):
        border = tk.Frame(self, highlightthickness=1,
                          highlightbackground=BORDER)
        border.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        canvas = tk.Canvas(border, bg=BACKGROUND, highlightthickness=0)
        scrollbar = tk.Scrollbar(border, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        partner_list = tk.Frame(canvas, bg=BACKGROUND, pady=5)
        list_id = canvas.create_window(0, 0, window=partner_list,
                                       anchor="nw")
        self.partner_list = partner_list
        self.refresh_partner_list()

        def update_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def stretch_list(event):
            canvas.itemconfigure(list_id, width=event.width)

        partner_list.bind("<Configure>", update_scroll_region)
        canvas.bind("<Configure>", stretch_list)

    def refresh_partner_list(self):
        self.selected_card = None
        self.selected_partner_id = None
        for card in self.partner_list.winfo_children():
            card.destroy()
        for partner in get_partners_with_discount(self.connection):
            create_partner_card(self.partner_list, partner,
                                self.select_partner,
                                self.open_partner_edit_window)

    def select_partner(self, card, partner_id):
        if self.selected_card is not None:
            paint_card(self.selected_card, BACKGROUND)
        paint_card(card, SELECTED)
        self.selected_card = card
        self.selected_partner_id = partner_id

    def open_history_window(self):
        if self.selected_partner_id is None:
            messagebox.showwarning("Партнер не выбран",
                                   "Выберите партнера в списке щелчком "
                                   "по его карточке и нажмите "
                                   "«История продаж» еще раз.", parent=self)
            return
        try:
            PartnerHistoryWindow(self, self.selected_partner_id)
        except psycopg2.Error as error:
            log_error("Не удалось загрузить историю продаж партнера", error)
            show_database_error(self)

    def open_calculator_window(self):
        MaterialCalculatorWindow(self)

    def open_partner_edit_window(self, partner_id=None):
        if partner_id is None:
            PartnerEditWindow(self, self.partner_types)
        else:
            try:
                partner = get_partner(self.connection, partner_id)
            except psycopg2.Error as error:
                log_error("Не удалось загрузить карточку партнера", error)
                show_database_error(self)
                return
            PartnerEditWindow(self, self.partner_types, partner)


def show_start_error():
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Ошибка подключения к базе данных", DATABASE_ERROR,
                         parent=root)
    root.destroy()


if __name__ == "__main__":
    setup_logging()
    try:
        connection = psycopg2.connect(dbname="partners_db",
                                      host="localhost")
    except psycopg2.OperationalError as error:
        log_error("Не удалось подключиться к базе данных", error)
        show_start_error()
    else:
        window = MainWindow(connection)
        window.mainloop()
        connection.close()
