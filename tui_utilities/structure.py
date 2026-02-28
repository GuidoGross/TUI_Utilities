from .console import print, clear_console, wait_for_key, _CONSOLE
from rich.table import Table
from rich import box
import sys
import traceback

def _total_characters(object):
    if isinstance(object, str): return len(object)
    if isinstance(object, list): return sum(len(segment) for segment, _ in object)
    return len(str(object))

def _get_style_string(color, bold, italic, underline, strike, reverse):
    parts = [color] if color else []
    if bold: parts.append("bold")
    if italic: parts.append("italic")
    if underline: parts.append("underline")
    if strike: parts.append("strike")
    if reverse: parts.append("reverse")
    return " ".join(parts)

def header(
    title,
    title_color = "#ffffff",
    title_bold = True,
    title_italic = True,
    title_underline = False,
    title_strike = False,
    title_reverse = False,
    title_alignment = "center",
    title_padding = 0,
    title_top_padding = None,
    title_right_padding = None,
    title_bottom_padding = None,
    title_left_padding = None,
    separator_first_character = "\\",
    separator_separator_character = "-",
    separator_last_character = "/",
    separator_length = None,
    separator_color = "#ffffff",
    separator_aligment = "center",
    separator_padding = 0,
    separator_top_padding = None,
    separator_right_padding = None,
    separator_bottom_padding = 2,
    separator_left_padding = None
):
    clear_console()
    print(
        title,
        color = title_color,
        bold = title_bold,
        italic = title_italic,
        underline = title_underline,
        strike = title_strike,
        reverse = title_reverse,
        alignment = title_alignment,
        padding = title_padding,
        top_padding = title_top_padding,
        right_padding = title_right_padding,
        bottom_padding = title_bottom_padding,
        left_padding = title_left_padding
    )
    separator(
        first_character = separator_first_character,
        separator_character = separator_separator_character,
        last_character = separator_last_character,
        length = separator_length if separator_length else _total_characters(title) + 2,
        color = separator_color,
        aligment = separator_aligment,
        padding = separator_padding,
        top_padding = separator_top_padding,
        right_padding = separator_right_padding,
        bottom_padding = separator_bottom_padding,
        left_padding = separator_left_padding
    )

def menu(
    options,
    title = None,
    title_color = "#ffffff",
    title_bold = True,
    title_italic = True,
    title_underline = False,
    title_strike = False,
    title_reverse = False,
    title_alignment = "center",
    title_padding = 0,
    title_top_padding = None,
    title_right_padding = None,
    title_bottom_padding = None,
    title_left_padding = None,
    separator_first_character = "\\",
    separator_separator_character = "-",
    separator_last_character = "/",
    separator_length = None,
    separator_color = "#ffffff",
    separator_aligment = "center",
    separator_padding = 0,
    separator_top_padding = None,
    separator_right_padding = None,
    separator_bottom_padding = 2,
    separator_left_padding = None,
    message = "Seleccione una opción:",
    selection_text = "Su elección: ",
    invalid_error = "La opción ingresada no es válida, intente nuevamente"
):
    from .validation import validate_option
    if title:
        header(
            title = title,
            title_color = title_color,
            title_bold = title_bold,
            title_italic = title_italic,
            title_underline = title_underline,
            title_strike = title_strike,
            title_reverse = title_reverse,
            title_alignment = title_alignment,
            title_padding = title_padding,
            title_top_padding = title_top_padding,
            title_right_padding = title_right_padding,
            title_bottom_padding = title_bottom_padding,
            title_left_padding = title_left_padding,
            separator_first_character = separator_first_character,
            separator_separator_character = separator_separator_character,
            separator_last_character = separator_last_character,
            separator_length = separator_length,
            separator_color = separator_color,
            separator_aligment = separator_aligment,
            separator_padding = separator_padding,
            separator_top_padding = separator_top_padding,
            separator_right_padding = separator_right_padding,
            separator_bottom_padding = separator_bottom_padding,
            separator_left_padding = separator_left_padding
        )
    return validate_option(options, message, selection_text, invalid_error)

def confirmation_menu(
    message,
    selection_text = "Su elección: ",
    invalid_error = "La opción ingresada no es válida, intente nuevamente",
    options_text = ["Sí", "No"]
):
    from .validation import validate_option
    options = {
        "1": options_text[0],
        "2": options_text[1]
    }
    selection = validate_option(options, f"\n{message}", selection_text, invalid_error)
    return selection

def confirm_exit(
    message = "¿Está seguro de que desea salir?",
    selection_text = "Su elección: ",
    invalid_error = "La opción ingresada no es válida, intente nuevamente",
    options_text = ["Sí", "No"]
):
    selection = confirmation_menu(message, selection_text, invalid_error, options_text)
    if selection == "1": sys.exit()

def table(
    columns,
    rows,
    title = None,
    title_color = "#ffffff",
    title_bold = True,
    title_italic = True,
    title_underline = False,
    title_strike = False,
    title_reverse = False,
    title_justify = "center",
    color = "#ffffff",
    bold = False,
    italic = False,
    underline = False,
    strike = False,
    reverse = False,
    row_colors = None,
    row_bolds = None,
    row_italics = None,
    row_underlines = None,
    row_strikes = None,
    row_reverses = None,
    show_lines = True,
    box = box.HEAVY_HEAD,
    safe_box = None,
    border_color = "#ffffff",
    border_bold = False,
    border_italic = False,
    border_underline = False,
    border_strike = False,
    border_reverse = False,
    show_header = True,
    header_color = "#ffffff",
    header_bold = True,
    header_italic = False,
    header_underline = False,
    header_strike = False,
    header_reverse = False,
    show_footer = False,
    footer_color = "#ffffff",
    footer_bold = False,
    footer_italic = False,
    footer_underline = False,
    footer_strike = False,
    footer_reverse = False,
    caption = None,
    caption_color = "#ffffff",
    caption_bold = False,
    caption_italic = False,
    caption_underline = False,
    caption_strike = False,
    caption_reverse = False,
    caption_justify = "center",
    show_edge = True,
    padding_edge = True,
    highlight = False,
    alignment = "center",
    padding = None,
    top_padding = None,
    right_padding = None,
    bottom_padding = 1,
    left_padding = None,
    padding_table = (0, 1),
    leading = 0,
    collapse_padding = False,
    width = None,
    minimum_width = None,
    expand = False
):
    title_style = _get_style_string(title_color, title_bold, title_italic, title_underline, title_strike, title_reverse)
    style = _get_style_string(color, bold, italic, underline, strike, reverse)
    caption_style = _get_style_string(caption_color, caption_bold, caption_italic, caption_underline, caption_strike, caption_reverse)
    header_style = _get_style_string(header_color, header_bold, header_italic, header_underline, header_strike, header_reverse)
    footer_style = _get_style_string(footer_color, footer_bold, footer_italic, footer_underline, footer_strike, footer_reverse)
    border_style = _get_style_string(border_color, border_bold, border_italic, border_underline, border_strike, border_reverse)
    row_styles = None
    if row_colors or row_bolds or row_italics or row_underlines or row_strikes or row_reverses:
        from itertools import zip_longest
        row_styles = []
        list_colors = row_colors if row_colors else []
        list_bolds = row_bolds if row_bolds else []
        list_italics = row_italics if row_italics else []
        list_underlines = row_underlines if row_underlines else []
        list_strikes = row_strikes if row_strikes else []
        list_reverses = row_reverses if row_reverses else []
        for color, bold, italic, underline, strike, reverse in zip_longest(
            list_colors,
            list_bolds,
            list_italics,
            list_underlines,
            list_strikes,
            list_reverses
        ):
            row_styles.append(_get_style_string(color, bold, italic, underline, strike, reverse))
    table_instance = Table(
        title = title,
        caption = caption,
        width = width,
        min_width = minimum_width,
        box = box,
        safe_box = safe_box,
        padding = padding_table,
        collapse_padding = collapse_padding,
        pad_edge = padding_edge,
        expand = expand,
        show_header = show_header,
        show_footer = show_footer,
        show_edge = show_edge,
        show_lines = show_lines,
        leading = leading,
        style = style,
        row_styles = row_styles,
        header_style = header_style,
        footer_style = footer_style,
        border_style = border_style,
        title_style = title_style,
        caption_style = caption_style,
        title_justify = title_justify,
        caption_justify = caption_justify,
        highlight = highlight
    )
    for column in columns:
        column_color = column.pop("color", None)
        column_bold = column.pop("bold", None)
        column_italic = column.pop("italic", None)
        column_underline = column.pop("underline", None)
        column_strike = column.pop("strike", None)
        column_reverse = column.pop("reverse", None)
        column_style = _get_style_string(
            column_color,
            column_bold,
            column_italic,
            column_underline,
            column_strike,
            column_reverse
        )
        column["style"] = column_style if column_style.strip() else style
        table_instance.add_column(**column)
    for row in rows: table_instance.add_row(*row)
    print(
        table_instance,
        alignment = alignment,
        padding = padding,
        top_padding = top_padding,
        right_padding = right_padding,
        bottom_padding = bottom_padding,
        left_padding = left_padding
    )

def separator(
    first_character = "/",
    separator_character = "-",
    last_character = "/",
    length = None,
    color = "#ffffff",
    aligment = "left",
    padding = 0,
    top_padding = None,
    right_padding = None,
    bottom_padding = None,
    left_padding = None
):
    if not length: length = _CONSOLE.width
    print(
        first_character + separator_character * (length - 2) + last_character,
        color = color,
        bold = True,
        alignment = aligment,
        padding = padding,
        top_padding = top_padding,
        right_padding = right_padding,
        bottom_padding = bottom_padding,
        left_padding = left_padding
    )

def error_message(
    message,
    error = None,
    separator_first_character = "/",
    separator_separator_character = "-",
    separator_last_character = "/",
    separator_length = None,
    separator_color = "#ffffff",
    separator_aligment = "left",
    separator_padding = 0,
    separator_top_padding = None,
    separator_right_padding = None,
    separator_bottom_padding = None,
    separator_left_padding = None
):
    header("Error")
    print(message, color = "#ff0000", bold = True, bottom_padding = 1 if error else 0)
    if error:
        separator(
            first_character = separator_first_character,
            separator_character = separator_separator_character,
            last_character = separator_last_character,
            length = separator_length,
            color = separator_color,
            aligment = separator_aligment,
            padding = separator_padding,
            top_padding = separator_top_padding,
            right_padding = separator_right_padding,
            bottom_padding = separator_bottom_padding,
            left_padding = separator_left_padding
        )
        print([("Error: ", {"bold": True}), (f"{error}", {"color": "#00bfff"})], bottom_padding = 1)
        print([("Detalles: ", {"bold": True}), (traceback.format_exc(), {"color": "#00bfff"})], end = "")
        separator(
            first_character = separator_first_character,
            separator_character = separator_separator_character,
            last_character = separator_last_character,
            length = separator_length,
            color = separator_color,
            aligment = separator_aligment,
            padding = separator_padding,
            top_padding = separator_top_padding,
            right_padding = separator_right_padding,
            bottom_padding = separator_bottom_padding,
            left_padding = separator_left_padding
        )
    wait_for_key()

def success_message(message):
    header("Éxito")
    print(message, color = "#00ff00", bold = True)
    wait_for_key()