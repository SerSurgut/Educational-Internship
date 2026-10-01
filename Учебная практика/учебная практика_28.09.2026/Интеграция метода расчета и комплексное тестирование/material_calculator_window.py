import tkinter as tk
from tkinter import messagebox

from material_calculator import calculate_material_quantity
from reference_mock import MATERIAL_DEFECT_PERCENTS
from reference_mock import PRODUCT_TYPE_COEFFICIENTS
from style import BACKGROUND, FONT, TEXT


def join_ids(reference):
    return ", ".join(str(type_id) for type_id in reference)


CALCULATION_ERROR = (
    "Не удалось рассчитать количество материала: введенные данные "
    "некорректны.\n\n"
    "Проверьте поля и повторите расчет:\n"
    "• ID типа продукции — одно из чисел "
    + join_ids(PRODUCT_TYPE_COEFFICIENTS) + ";\n"
    "• ID типа материала — одно из чисел "
    + join_ids(MATERIAL_DEFECT_PERCENTS) + ";\n"
    "• количество продукции — целое число больше нуля;\n"
    "• параметры 1 и 2 — положительные числа, например 2.5.")


def read_whole_number(entry):
    # Текст, который не читается как число, передается в расчет как None:
    # его отсекает проверка типов, и расчет возвращает -1.
    try:
        return int(entry.get().strip())
    except ValueError:
        return None


def read_number(entry):
    text = entry.get().strip().replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return None


class MaterialCalculatorWindow(tk.Toplevel):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.title("CRM: Калькулятор материалов")
        self.geometry("700x600")
        self.configure(bg=BACKGROUND)
        self.transient(main_window)
        self.grab_set()

        self.create_header(main_window.logo_image)
        self.create_form()
        self.create_result()
        self.create_buttons()

    def create_header(self, logo_image):
        header = tk.Frame(self, bg=BACKGROUND)
        header.pack(fill="x", padx=20, pady=(20, 10))
        logo = tk.Label(header, image=logo_image, bg=BACKGROUND)
        logo.pack(side="left")
        title = tk.Label(header, text="Расчет материалов",
                         font=(FONT, 20), bg=BACKGROUND, fg=TEXT)
        title.pack(side="left", padx=15)

    def create_entry(self, form, text, row):
        label = tk.Label(form, text=text, font=(FONT, 12),
                         bg=BACKGROUND, fg=TEXT)
        label.grid(row=row, column=0, sticky="w", padx=(0, 15), pady=5)
        entry = tk.Entry(form, font=(FONT, 12))
        entry.grid(row=row, column=1, sticky="ew", pady=5)
        return entry

    def create_form(self):
        form = tk.Frame(self, bg=BACKGROUND)
        form.pack(fill="x", padx=20, pady=10)
        form.columnconfigure(1, weight=1)

        self.product_type_entry = self.create_entry(
            form, "ID типа продукции", 0)
        self.material_type_entry = self.create_entry(
            form, "ID типа материала", 1)
        self.quantity_entry = self.create_entry(
            form, "Количество продукции (шт.)", 2)
        self.param_1_entry = self.create_entry(form, "Параметр 1", 3)
        self.param_2_entry = self.create_entry(form, "Параметр 2", 4)

    def create_result(self):
        self.result_label = tk.Label(self, font=(FONT, 16),
                                     bg=BACKGROUND, fg=TEXT)
        self.result_label.pack(anchor="w", padx=20, pady=10)
        self.show_result("—")

    def create_buttons(self):
        buttons = tk.Frame(self, bg=BACKGROUND)
        buttons.pack(side="bottom", anchor="e", padx=20, pady=20)
        calculate_button = tk.Button(buttons, text="Рассчитать",
                                     font=(FONT, 12),
                                     command=self.calculate)
        calculate_button.pack(side="left", padx=(0, 10))
        back_button = tk.Button(buttons, text="Назад", font=(FONT, 12),
                                command=self.destroy)
        back_button.pack(side="left")

    def show_result(self, value):
        self.result_label.configure(
            text=f"Количество материала с учетом брака: {value}")

    def calculate(self):
        result = calculate_material_quantity(
            read_whole_number(self.product_type_entry),
            read_whole_number(self.material_type_entry),
            read_whole_number(self.quantity_entry),
            read_number(self.param_1_entry),
            read_number(self.param_2_entry))
        if result == -1:
            self.show_result("—")
            messagebox.showerror("Ошибка расчета", CALCULATION_ERROR,
                                 parent=self)
            return
        self.show_result(result)
