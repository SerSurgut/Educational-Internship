import tkinter as tk
from pathlib import Path

RESOURCES = Path(__file__).parent / "resources"

FONT = "Segoe UI"
BACKGROUND = "#FFFFFF"
BORDER = "#8F8F8F"
TEXT = "#000000"

PARTNERS = [
    {
        "company_name": 'ООО "Логистик-Экспресс"',
        "contact_email": "info@logex.ru",
        "phone": "+79991112233",
        "rating": 4.8,
        "discount": 0,
    },
    {
        "company_name": "ИП Петров А.В.",
        "contact_email": "petrov_delivery@mail.ru",
        "phone": None,
        "rating": 4.2,
        "discount": 0,
    },
    {
        "company_name": 'ТК "Быстрый Путь"',
        "contact_email": "speedway@yandex.ru",
        "phone": "+78125554433",
        "rating": None,
        "discount": 0,
    },
]


def text_or_dash(value):
    if value is None:
        return "—"
    return str(value)


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

    name = create_label(card, partner["company_name"], 16)
    name.grid(row=0, column=0, sticky="w")
    discount = create_label(card, f"{partner['discount']}%", 16)
    discount.grid(row=0, column=1, sticky="e")
    email = create_label(card, partner["contact_email"], 12)
    email.grid(row=1, column=0, sticky="w")
    phone = create_label(card, text_or_dash(partner["phone"]), 12)
    phone.grid(row=2, column=0, sticky="w")
    rating = "Рейтинг: " + text_or_dash(partner["rating"])
    create_label(card, rating, 12).grid(row=3, column=0, sticky="w")


def create_partner_list(window, partners):
    partner_list = tk.Frame(window, bg=BACKGROUND, pady=5,
                            highlightthickness=1, highlightbackground=BORDER)
    partner_list.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    for partner in partners:
        create_partner_card(partner_list, partner)


if __name__ == "__main__":
    window = tk.Tk()
    window.title("CRM: Список партнеров и скидок")
    window.geometry("700x600")
    window.configure(bg=BACKGROUND)

    icon = tk.PhotoImage(file=str(RESOURCES / "icon.png"))
    window.iconphoto(True, icon)
    logo = tk.PhotoImage(file=str(RESOURCES / "logo.png"))

    create_header(window, logo)
    create_partner_list(window, PARTNERS)
    window.mainloop()
