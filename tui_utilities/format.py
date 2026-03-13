def decimal_format(number, decimals = None):
    if isinstance(number, float) and number.is_integer(): number = int(number)
    if decimals is not None:
        formatted_number = f"{number:,.{decimals}f}"
        if "." in formatted_number: formatted_number = formatted_number.rstrip("0").rstrip(".")
    else: formatted_number = f"{number:,}"
    return formatted_number.replace(",", "X").replace(".", ",").replace("X", ".")

def datetime_format(datetime, include_year = "automatic", include_time = "automatic", include_second = "automatic"):
    day = datetime.day
    month = datetime.month
    year = decimal_format(datetime.year)
    hour = getattr(datetime, "hour", 0)
    minute = getattr(datetime, "minute", 0)
    second = getattr(datetime, "second", 0)
    if include_year == "automatic": include_year = True
    if include_time == "automatic": include_time = (hour != 0 or minute != 0 or second != 0)
    if include_second == "automatic": include_second = (second != 0)
    date = f"{day:02d}/{month:02d}"
    if include_year: date += f"/{year}"
    if include_time:
        time = f"{hour:02d}:{minute:02d}"
        if include_second: time += f":{second:02d}"
        return f"{date} - {time}"
    return date

def id_format(id):
    if "." in id: return id
    elif len(id) == 8: return f"{id[0:2]}.{id[2:5]}.{id[5:8]}"
    elif len(id) == 7: return f"{id[0:1]}.{id[1:4]}.{id[4:7]}"

def cellphone_number_format(cellphone_number):
    formatted_cellphone_number = "".join(filter(str.isdigit, cellphone_number))
    return f"{formatted_cellphone_number[0:4]} - {formatted_cellphone_number[4:10]}"

def convert_to_double(number): return float(str(number).replace(".", "").replace(",", "."))

def define_equality_symbol(number, number_rounded): return "=" if number == number_rounded else "≅"