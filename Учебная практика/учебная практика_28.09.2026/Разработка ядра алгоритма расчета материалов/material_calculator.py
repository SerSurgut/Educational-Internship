import math

from reference_mock import MATERIAL_DEFECT_PERCENTS
from reference_mock import PRODUCT_TYPE_COEFFICIENTS


def get_product_type_coefficient(product_type_id: int):
    return PRODUCT_TYPE_COEFFICIENTS.get(product_type_id)


def get_material_defect_percent(material_type_id: int):
    return MATERIAL_DEFECT_PERCENTS.get(material_type_id)


def calculate_material_quantity(product_type_id: int, material_type_id: int,
                                quantity: int, param_1: float,
                                param_2: float) -> int:
    coefficient = get_product_type_coefficient(product_type_id)
    defect_percent = get_material_defect_percent(material_type_id)
    if coefficient is None or defect_percent is None:
        return -1
    if quantity <= 0 or param_1 <= 0 or param_2 <= 0:
        return -1
    base_per_unit = param_1 * param_2 * coefficient
    net_total = base_per_unit * quantity
    total_with_defect = net_total * (1 + defect_percent / 100)
    return math.ceil(total_with_defect)


if __name__ == "__main__":
    print(calculate_material_quantity(1, 1, 10, 2.0, 3.0))
    print(calculate_material_quantity(9, 1, 10, 2.0, 3.0))
    print(calculate_material_quantity(1, 1, 10, -2.0, 3.0))
