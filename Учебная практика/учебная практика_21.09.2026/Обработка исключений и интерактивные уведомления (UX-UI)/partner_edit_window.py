import tkinter as tk
from tkinter import messagebox, ttk

import psycopg2

from partner_service import add_partner, update_partner
from style import BACKGROUND, FONT, HINT, TEXT

PHONE_HINT = "+7 900 123 45 67"
EMAIL_HINT = "info@company.ru"

DATABASE_ERROR = ("Не удалось связаться с базой данных.\n\n"
                  "Проверьте, что сервер PostgreSQL запущен, "
                  "и перезапустите приложение.")


def show_database_error(parent):
    messagebox.showerror("Ошибка базы данных", DATABASE_ERROR,
                         parent=parent)


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


def fill_entry(entry, value):
    if value is None:
        return
    entry.delete(0, "end")
    entry.insert(0, value)
    entry.configure(fg=TEXT)


def read_entry(entry):
    if entry.cget("fg") == HINT:
        return None
    text = entry.get().strip()
    if text == "":
        return None
    return text


def check_required(value, field_name):
    if value is None:
        raise ValueError(f"Поле «{field_name}» не заполнено.\n\n"
                         "Пожалуйста, заполните его и повторите попытку.")
    return value


def check_rating(text):
    try:
        rating = int(text)
    except ValueError:
        raise ValueError("Рейтинг должен быть целым числом от 0 до 10.\n\n"
                         "Пожалуйста, удалите буквы и знаки препинания "
                         "и повторите попытку.")
    if rating < 0 or rating > 10:
        raise ValueError("Рейтинг должен быть целым числом от 0 до 10.\n\n"
                         "Пожалуйста, введите число из этого диапазона "
                         "и повторите попытку.")
    return rating


class PartnerEditWindow(tk.Toplevel):
    def __init__(self, main_window, partner_types, partner=None):
        super().__init__(main_window)
        self.main_window = main_window
        self.partner_id = None
        if partner is None:
            self.title("CRM: Карточка партнера [Добавление]")
        else:
            self.partner_id = partner["partner_id"]
            self.title("CRM: Карточка партнера [Редактирование]")
        self.geometry("700x600")
        self.configure(bg=BACKGROUND)
        # Карточка модальная: главное окно остаётся на экране под ней,
        # но не реагирует на клики, пока карточка открыта.
        self.transient(main_window)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.go_back)

        self.create_form(partner_types)
        if partner is not None:
            self.fill_form(partner)
        self.create_buttons()
        self.start_fields = self.read_fields()

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

    def create_buttons(self):
        buttons = tk.Frame(self, bg=BACKGROUND)
        buttons.pack(side="bottom", anchor="e", padx=20, pady=20)
        save_button = tk.Button(buttons, text="Сохранить", font=(FONT, 12),
                                command=self.save)
        save_button.pack(side="left", padx=(0, 10))
        back_button = tk.Button(buttons, text="Назад", font=(FONT, 12),
                                command=self.go_back)
        back_button.pack(side="left")

    def fill_form(self, partner):
        fill_entry(self.name_entry, partner["company_name"])
        if partner["partner_type"] is not None:
            self.type_combobox.set(partner["partner_type"])
        if partner["rating"] is not None:
            self.rating_spinbox.delete(0, "end")
            self.rating_spinbox.insert(0, partner["rating"])
        fill_entry(self.address_entry, partner["address"])
        fill_entry(self.director_entry, partner["director_name"])
        fill_entry(self.phone_entry, partner["phone"])
        fill_entry(self.email_entry, partner["contact_email"])

    def read_fields(self):
        return [read_entry(self.name_entry), self.type_combobox.get(),
                self.rating_spinbox.get(), read_entry(self.address_entry),
                read_entry(self.director_entry), read_entry(self.phone_entry),
                read_entry(self.email_entry)]

    def read_form(self):
        company_name = check_required(read_entry(self.name_entry),
                                      "Наименование")
        rating = check_rating(self.rating_spinbox.get())
        contact_email = check_required(read_entry(self.email_entry),
                                       "Email компании")
        partner_type = self.type_combobox.get()
        if partner_type == "":
            partner_type = None
        phone = read_entry(self.phone_entry)
        if phone is not None:
            phone = phone.replace(" ", "")
        return {
            "company_name": company_name,
            "partner_type": partner_type,
            "rating": rating,
            "address": read_entry(self.address_entry),
            "director_name": read_entry(self.director_entry),
            "phone": phone,
            "contact_email": contact_email,
        }

    def save(self):
        try:
            partner = self.read_form()
        except ValueError as error:
            messagebox.showerror("Ошибка ввода", str(error), parent=self)
            return

        connection = self.main_window.connection
        try:
            if self.partner_id is None:
                add_partner(connection, partner)
                message = "Партнер добавлен в базу."
            else:
                update_partner(connection, self.partner_id, partner)
                message = "Изменения партнера сохранены в базе."
            self.main_window.refresh_partner_list()
        except ValueError as error:
            messagebox.showerror("Ошибка сохранения", str(error),
                                 parent=self)
            return
        except psycopg2.IntegrityError:
            messagebox.showerror("Ошибка сохранения",
                                 "Партнер с таким email уже есть в базе."
                                 "\n\nПожалуйста, укажите другой email "
                                 "и повторите попытку.", parent=self)
            return
        except psycopg2.Error:
            show_database_error(self)
            return

        messagebox.showinfo("Партнер сохранен", message, parent=self)
        self.destroy()

    def go_back(self):
        if self.read_fields() != self.start_fields:
            close = messagebox.askyesno(
                "Несохраненные изменения",
                "Изменения в карточке не сохранены и будут потеряны "
                "безвозвратно.\n\nЗакрыть карточку без сохранения?",
                icon="warning", default="no", parent=self)
            if not close:
                return
        self.destroy()
