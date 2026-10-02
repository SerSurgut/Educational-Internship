import math

from reference_mock import MATERIAL_DEFECT_PERCENTS
from reference_mock import PRODUCT_TYPE_COEFFICIENTS


def get_product_type_coefficient(product_type_id: int):
    # get отдаёт None для несуществующего id, а не бросает KeyError.
    return PRODUCT_TYPE_COEFFICIENTS.get(product_type_id)


def get_material_defect_percent(material_type_id: int):
    return MATERIAL_DEFECT_PERCENTS.get(material_type_id)


def is_whole_number(value) -> bool:
    # bool — подкласс int: без этой проверки True прошёл бы как 1.
    return isinstance(value, int) and not isinstance(value, bool)


def is_positive_number(value) -> bool:
    if isinstance(value, bool):
        return False
    if not isinstance(value, (int, float)):
        return False
    # nan не больше и не меньше нуля, поэтому отсекается до сравнения.
    if isinstance(value, float) and not math.isfinite(value):
        return False
    return value > 0


def calculate_material_quantity(product_type_id: int, material_type_id: int,
                                quantity: int, param_1: float,
                                param_2: float) -> int:
    if not is_whole_number(product_type_id):
        return -1
    if not is_whole_number(material_type_id):
        return -1
    if not is_whole_number(quantity) or quantity <= 0:
        return -1
    if not is_positive_number(param_1) or not is_positive_number(param_2):
        return -1
    coefficient = get_product_type_coefficient(product_type_id)
    defect_percent = get_material_defect_percent(material_type_id)
    if coefficient is None or defect_percent is None:
        return -1
    # При огромных параметрах произведение уходит в inf,
    # и math.ceil бросает OverflowError.
    try:
        base_per_unit = param_1 * param_2 * coefficient
        net_total = base_per_unit * quantity
        total_with_defect = net_total * (1 + defect_percent / 100)
        return math.ceil(total_with_defect)
    except ArithmeticError:
        return -1
