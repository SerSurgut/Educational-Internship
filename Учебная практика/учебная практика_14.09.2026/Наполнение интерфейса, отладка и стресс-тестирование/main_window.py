import tkinter as tk
from pathlib import Path

import psycopg2

from partner_service import get_partners_with_discount

RESOURCES = Path(__file__).parent / "resources"

FONT = "Segoe UI"
BACKGROUND = "#FFFFFF"
BORDER = "#8F8F8F"
TEXT = "#000000"


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


def create_header(window, logo):
    header = tk.Frame(window, bg=BACKGROUND)
    header.pack(fill="x", padx=20, pady=(20, 10))
    tk.Label(header, image=logo, bg=BACKGROUND).pack(side="left")
    title = create_label(header, "Список партнеров и скидок", 20)
    title.pack(side="left", padx=15)


def create_partner_card(parent, partner):
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


def create_partner_list(window, partners):
    border = tk.Frame(window, highlightthickness=1,
                      highlightbackground=BORDER)
    border.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    canvas = tk.Canvas(border, bg=BACKGROUND, highlightthickness=0)
    scrollbar = tk.Scrollbar(border, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    partner_list = tk.Frame(canvas, bg=BACKGROUND, pady=5)
    list_id = canvas.create_window(0, 0, window=partner_list, anchor="nw")
    for partner in partners:
        create_partner_card(partner_list, partner)

    def update_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def stretch_list(event):
        canvas.itemconfigure(list_id, width=event.width)

    partner_list.bind("<Configure>", update_scroll_region)
    canvas.bind("<Configure>", stretch_list)


if __name__ == "__main__":
    connection = psycopg2.connect(dbname="partners_db", host="localhost")
    partners = get_partners_with_discount(connection)
    connection.close()

    window = tk.Tk()
    window.title("CRM: Список партнеров и скидок")
    window.geometry("700x600")
    window.configure(bg=BACKGROUND)

    icon = tk.PhotoImage(file=str(RESOURCES / "icon.png"))
    window.iconphoto(True, icon)
    logo = tk.PhotoImage(file=str(RESOURCES / "logo.png"))

    create_header(window, logo)
    create_partner_list(window, partners)
    window.mainloop()
