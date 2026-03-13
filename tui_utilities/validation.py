from .console import print, input, wait_for_key
from .structure import error_message
from importlib.resources import files
import math
import requests
import re
from datetime import datetime

_TLDS_LIST = files("tui_utilities._tlds").joinpath("tlds.txt")

_MATHEMATICAL_CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
    "phi": (1 + 5 ** 0.5) / 2
}
_value_pattern = r"(?:-?infinity|-?pi|-?e|-?tau|-?phi|-?\d+(?:\.\d+)?(?:,\d+)?(?:/-?\d+(?:\.\d+)?(?:,\d+)?)?)"
_interval_pattern = rf"[\[\(]{_value_pattern}; {_value_pattern}[\]\)]"
_range_item_pattern = rf"(?:{_interval_pattern}|{_value_pattern})"
_numeric_range_pattern = re.compile(rf"^{_range_item_pattern}(?: \| {_range_item_pattern})*$")
_extraction_pattern = re.compile(rf"(?P<left_type>[\[\(])(?P<left_value>{_value_pattern}); (?P<right_value>{_value_pattern})(?P<right_type>[\]\)])")
_email_pattern = None

def _parse_value(raw_value):
    if raw_value.startswith("-"):
        sign = -1
        raw_value = raw_value[1:]
    else: sign = 1
    if raw_value == "infinity": return sign * float("inf")
    if raw_value in _MATHEMATICAL_CONSTANTS: return sign * _MATHEMATICAL_CONSTANTS[raw_value]
    if "/" in raw_value:
        parts = raw_value.split("/")
        return sign * (_parse_value(parts[0]) / _parse_value(parts[1]))
    return sign * float(raw_value.replace(".", "").replace(",", "."))

def _check_range_consistency(range_string):
    if not range_string: return True
    items = []
    intervals = range_string.split(" | ")
    for item_string in intervals:
        match = _extraction_pattern.match(item_string)
        if match:
            items.append({
                "type": "interval",
                "left": _parse_value(match.group("left_value")),
                "right": _parse_value(match.group("right_value")),
                "left_inclusive": match.group("left_type") == "[",
                "right_inclusive": match.group("right_type") == "]"
            })
        else:
            items.append({
                "type": "value",
                "value": _parse_value(item_string)
            })
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            item_1 = items[i]
            item_2 = items[j]
            if item_1["type"] == "value" and item_2["type"] == "value":
                if item_1["value"] == item_2["value"]: return False
            elif item_1["type"] == "value" or item_2["type"] == "value":
                value_item = item_1 if item_1["type"] == "value" else item_2
                interval_item = item_2 if item_1["type"] == "value" else item_1
                value = value_item["value"]
                in_left = (value >= interval_item["left"]) if interval_item["left_inclusive"] else (value > interval_item["left"])
                in_right = (value <= interval_item["right"]) if interval_item["right_inclusive"] else (value < interval_item["right"])
                if in_left and in_right: return False
            else:
                if item_1["right"] < item_2["left"]: continue
                if item_1["right"] == item_2["left"] and not (item_1["right_inclusive"] and item_2["left_inclusive"]): continue
                if item_2["right"] < item_1["left"]: continue
                if item_2["right"] == item_1["left"] and not (item_2["right_inclusive"] and item_1["left_inclusive"]): continue
                return False
    return True

def _is_in_range(value, range):
    if not range: return True
    if not _numeric_range_pattern.match(range) or not _check_range_consistency(range): return False
    intervals = range.split(" | ")
    for interval in intervals:
        match = _extraction_pattern.match(interval)
        if not match:
            if value == _parse_value(interval): return True
            continue
        left_type = match.group("left_type")
        right_type = match.group("right_type")
        left_raw_value = match.group("left_value")
        right_raw_value = match.group("right_value")
        left_value = _parse_value(left_raw_value)
        right_value = _parse_value(right_raw_value)
        if left_value > right_value: continue
        if left_raw_value == "-infinity" and left_type == "[": continue
        if right_raw_value == "infinity" and right_type == "]": continue
        in_left = (value >= left_value) if left_type == "[" else (value > left_value)
        in_right = (value <= right_value) if right_type == "]" else (value < right_value)
        if in_left and in_right: return True
    return False

def _get_tlds():
    url = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"
    try:
        response = requests.get(url, timeout = 10)
        response.raise_for_status()
        tlds = [tld.lower() for tld in response.text.splitlines()[1:]]
        if tlds: _export_tlds(tlds)
        return tlds
    except requests.RequestException as error:
        error_message(
            "Error al obtener la lista de TLDs actualizada. Se intentará importar la lista de TLDs guardada localmente, de existir una:",
            error
        )
        wait_for_key()
        return _import_tlds()

def _import_tlds():
    try:
        with _TLDS_LIST.open("r", encoding = "utf-8") as saved_tlds: return [tld.strip() for tld in saved_tlds]
    except Exception as error:
        error_message(
            "Error al importar la lista de TLDs guardada localmente. No se podrá verificar la validez de las TLDs en los correos electrónicos, sino tan solo su sintaxis:",
            error
        )
        wait_for_key()
        return []

def _export_tlds(tlds):
    try:
        with _TLDS_LIST.open("w", encoding = "utf-8") as saved_tlds: saved_tlds.write("\n".join(tlds))
    except Exception as error:
        error_message("Error al exportar la lista de TLDs:", error)
        wait_for_key()

def _build_email_pattern():
    global _email_pattern
    if _email_pattern is not None: return _email_pattern
    tlds = _get_tlds()
    if tlds: tld_pattern = "|".join(sorted(tlds, key = len, reverse = True))
    else: tld_pattern = r"[a-zA-Z]{2,63}"
    _email_pattern = re.compile(
        r"^(?P<local>[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+"
        r"(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*)@"
        r"(?P<dominio>(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+"
        r"(?:" + tld_pattern + r"))$",
        re.IGNORECASE
    )
    return _email_pattern

def check_if_list_is_empty(list, blank_error = "La lista está vacía"):
    if not list:
        error_message(blank_error)
        return True
    return False

def validate_option(
    options,
    message = "Seleccione una opción:",
    selection_text = "Su elección: ",
    invalid_error = "La opción ingresada no es válida, intente nuevamente",
):
    print(message, bold = True, bottom_padding = 1)
    for key, option in options.items(): print([(f"{key}:", {"bold": True}), (f" {option}", {})])
    selection = input(f"\n{selection_text}", bold = True).upper()
    while selection not in options:
        print(f"\n{invalid_error}", color = "#ff0000")
        selection = input(f"\n{selection_text}", bold = True).upper()
    return selection

def validate_string(
    message = "Ingrese un texto: ",
    blank_error = "El texto no puede estar vacío, intente nuevamente"
):
    while True:
        string = input(text = message, bold = True)
        if string: return string
        print(f"\n{blank_error}\n", color = "#ff0000")

def validate_integer(
    message = "Ingrese un número: ",
    range = None,
    blank_error = "El número no puede estar vacío",
    invalid_error = "El número ingresado no es válido, intente nuevamente",
    range_error = "El número ingresado no se encuentra dentro del rango permitido, intente nuevamente"
):
    pattern = re.compile(r"^-?(?:\d{1,3}(?:\.\d{3})*|\d+)$")
    while True:
        integer = input(text = message, bold = True)
        if not integer:
            print(f"\n{blank_error}\n", color = "#ff0000")
            continue
        if pattern.match(integer):
            unformatted_integer = integer.replace(".", "")
            value = int(unformatted_integer)
            if not _is_in_range(value, range):
                print(f"\n{range_error}\n", color = "#ff0000")
                continue
            return value
        print(f"\n{invalid_error}\n", color = "#ff0000")

def validate_double(
    message = "Ingrese un número: ",
    blank_error = "El número no puede estar vacío",
    invalid_error = "El número ingresado no es válido, intente nuevamente",
    range = None,
    range_error = "El número ingresado no se encuentra dentro del rango permitido, intente nuevamente"
):
    pattern = re.compile(rf"^{_value_pattern}$")
    while True:
        double = input(text = message, bold = True)
        if not double:
            print(f"\n{blank_error}\n", color = "#ff0000")
            continue
        if pattern.match(double):
            value = _parse_value(double)
            if not _is_in_range(value, range):
                print(f"\n{range_error}\n", color = "#ff0000")
                continue
            return value
        print(f"\n{invalid_error}\n", color = "#ff0000")

def validate_datetime(
    message = "Ingrese una fecha: ",
    blank_error = "La fecha no puede estar vacía",
    invalid_error = "La fecha ingresada no es válida, intente nuevamente",
    include_year = True,
    include_time = True,
    include_second = True
):
    date_pattern = r"(0[1-9]|[12]\d|3[01])/(0[1-9]|1[0-2])"
    if include_year: date_pattern += r"/(\d{4}|\d{1,2}\.\d{3})"
    time_pattern = r"([01]\d|2[0-3]):[0-5]\d"
    if include_second: time_pattern += r"(?::[0-5]\d)?"
    pattern = re.compile(rf"^{date_pattern}(?: - {time_pattern})?$" if include_time else rf"^{date_pattern}$")
    while True:
        datetime_string = input(text = message, bold = True)
        if not datetime_string:
            print(f"\n{blank_error}\n", color = "#ff0000")
            continue
        if pattern.match(datetime_string):
            cleaned_datetime = datetime_string.replace(".", "")
            if " - " in cleaned_datetime:
                if cleaned_datetime.count(":") == 2:
                    current_format = "%d/%m/%Y - %H:%M:%S" if include_year else "%d/%m - %H:%M:%S"
                else: current_format = "%d/%m/%Y - %H:%M" if include_year else "%d/%m - %H:%M"
            else: current_format = "%d/%m/%Y" if include_year else "%d/%m"
            return datetime.strptime(cleaned_datetime, current_format)
        print(f"\n{invalid_error}\n", color = "#ff0000")

def validate_id(
    message = "Ingrese un número de D.N.I.: ",
    blank_error = "El número de D.N.I. no puede estar vacío",
    invalid_error = "El número de D.N.I. ingresado no es válido, intente nuevamente"
):
    pattern = re.compile(r"^(?:\d{8}|(?:\d{1,2}\.\d{3}\.\d{3}))$")
    while True:
        id = input(text = message, bold = True)
        if not id:
            print(f"\n{blank_error}\n", color = "#ff0000")
            continue
        if pattern.match(id): return id
        print(f"\n{invalid_error}\n", color = "#ff0000")

def validate_cellphone_number(
    message = "Ingrese un número telefónico: ",
    blank_error = "El número telefónico no puede estar vacío",
    invalid_error = "El número telefónico ingresado no es válido, intente nuevamente"
):
    pattern = re.compile(r"^\d{4}\s*-?\s*\d{6}$")
    while True:
        cellphone_number = input(text = message, bold = True)
        if not cellphone_number:
            print(f"\n{blank_error}\n", color = "#ff0000")
            continue
        if pattern.match(cellphone_number): return cellphone_number
        print(f"\n{invalid_error}\n", color = "#ff0000")

def validate_email(
    message = "Ingrese el correo electrónico: ",
    blank_error = "El correo electrónico no puede estar vacío",
    invalid_error = "El correo electrónico ingresado no es válido, intente nuevamente"
):
    pattern = _build_email_pattern()
    while True:
        email = input(text = message, bold = True)
        if not email:
            print(f"\n{blank_error}\n", color = "#ff0000")
            continue
        if pattern.match(email): return email
        print(f"\n{invalid_error}\n", color = "#ff0000")