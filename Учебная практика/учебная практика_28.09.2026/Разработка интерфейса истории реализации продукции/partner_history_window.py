import tkinter as tk
from tkinter import ttk

from partner_service import get_partner, get_sales_history
from style import BACKGROUND, BORDER, FONT, TEXT


def format_date(sale_date):
    return sale_date.strftime("%d.%m.%Y")


class PartnerHistoryWindow(tk.Toplevel):
    def __init__(self, main_window, partner_id):
        partner = get_partner(main_window.connection, partner_id)
        sales = get_sales_history(main_window.connection, partner_id)

        super().__init__(main_window)
        self.title("CRM: История реализации продукции — "
                   + partner["company_name"])
        self.geometry("700x600")
        self.configure(bg=BACKGROUND)
        self.transient(main_window)
        self.grab_set()

        self.create_header(main_window.logo_image, partner)
        self.create_back_button()
        if len(sales) == 0:
            self.create_empty_message()
        else:
            self.create_sales_table(sales)

    def create_header(self, logo_image, partner):
        header = tk.Frame(self, bg=BACKGROUND)
        header.pack(fill="x", padx=20, pady=(20, 10))
        logo = tk.Label(header, image=logo_image, bg=BACKGROUND)
        logo.pack(side="left")

        titles = tk.Frame(header, bg=BACKGROUND)
        titles.pack(side="left", padx=15)
        title = tk.Label(titles, text="История реализации продукции",
                         font=(FONT, 20), bg=BACKGROUND, fg=TEXT)
        title.pack(anchor="w")
        partner_type = partner["partner_type"]
        if partner_type is None:
            partner_type = "—"
        name = tk.Label(titles,
                        text=partner_type + " | " + partner["company_name"],
                        font=(FONT, 16), bg=BACKGROUND, fg=TEXT)
        name.pack(anchor="w")

    def create_back_button(self):
        back_button = tk.Button(self, text="Назад", font=(FONT, 12),
                                command=self.destroy)
        back_button.pack(side="bottom", anchor="e", padx=20, pady=(0, 20))

    def create_empty_message(self):
        message = tk.Label(self, text="У партнера пока нет продаж.",
                           font=(FONT, 12), bg=BACKGROUND, fg=TEXT)
        message.pack(anchor="w", padx=20, pady=10)

    def create_sales_table(self, sales):
        style = ttk.Style(self)
        style.configure("Treeview", font=(FONT, 12), rowheight=28,
                        background=BACKGROUND, fieldbackground=BACKGROUND,
                        foreground=TEXT)
        style.configure("Treeview.Heading", font=(FONT, 12))

        border = tk.Frame(self, highlightthickness=1,
                          highlightbackground=BORDER)
        border.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        columns = ("product", "quantity", "date")
        table = ttk.Treeview(border, columns=columns, show="headings")
        table.heading("product", text="Наименование продукции")
        table.heading("quantity", text="Количество (шт.)")
        table.heading("date", text="Дата продажи")
        table.column("product", width=320)
        table.column("quantity", width=160, anchor="e")
        table.column("date", width=150, anchor="center")

        scrollbar = tk.Scrollbar(border, command=table.yview)
        table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        table.pack(side="left", fill="both", expand=True)

        for sale in sales:
            table.insert("", "end", values=(sale["product_name"],
                                            sale["quantity"],
                                            format_date(sale["sale_date"])))
