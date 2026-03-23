from .constants import _IN_GOOGLE_COLABORATORY, _CONSOLE
import os
from rich.console import RenderableType
from rich.text import Text
from rich.align import Align
from rich.padding import Padding
import subprocess
import readchar

if _IN_GOOGLE_COLABORATORY: os.environ["COLUMNS"] = "152"

def _style(
    object,
    color = "#ffffff",
    bold = False,
    italic = False,
    underline = False,
    strike = False,
    reverse = False,
    alignment = None,
    padding = None,
    top_padding = None,
    right_padding = None,
    bottom_padding = None,
    left_padding = None
):
    def apply_text_styles(object):
        styleable = Text()
        if isinstance(object, str):
            style_parts = [color]
            if bold: style_parts.append("bold")
            if italic: style_parts.append("italic")
            if underline: style_parts.append("underline")
            if strike: style_parts.append("strike")
            if reverse: style_parts.append("reverse")
            style = " ".join(style_parts)
            current_segment = ""
            for character in object:
                if character == " ":
                    if current_segment:
                        styleable.append(current_segment, style = style)
                        current_segment = ""
                    styleable.append(" ")
                else: current_segment += character
            if current_segment: styleable.append(current_segment, style = style)
            return styleable
        elif isinstance(object, list):
            for segment, segment_style in object:
                style_parts = [segment_style.get("color", color)]
                if segment_style.get("bold"): style_parts.append("bold")
                if segment_style.get("italic"): style_parts.append("italic")
                if segment_style.get("underline"): style_parts.append("underline")
                if segment_style.get("strike"): style_parts.append("strike")
                if segment_style.get("reverse"): style_parts.append("reverse")
                style = " ".join(style_parts)
                current_segment = ""
                for character in segment:
                    if character == " ":
                        if current_segment:
                            styleable.append(current_segment, style = style)
                            current_segment = ""
                        styleable.append(" ")
                    else: current_segment += character
                if current_segment: styleable.append(current_segment, style = style)
            return styleable
    
    def apply_alignment(renderable): return Align(renderable, alignment) if alignment else renderable
    
    def apply_padding(renderable):
        if not needs_padding: return renderable
        base = padding or 0
        final_padding = (
            top_padding if top_padding else base,
            (right_padding if right_padding else base) * 2,
            bottom_padding if bottom_padding else base,
            (left_padding if left_padding else base) * 2
        )
        return Padding(renderable, final_padding)
    
    needs_alignment = alignment is not None
    needs_padding = (padding or top_padding or right_padding or bottom_padding or left_padding)
    needs_layout = needs_alignment or needs_padding
    if isinstance(object, (str, list)):
        styled = apply_text_styles(object)
        if not needs_layout: return styled
        return apply_padding(apply_alignment(styled))
    if isinstance(object, RenderableType):
        if not needs_layout: return object
        return apply_padding(apply_alignment(object))
    styled = apply_text_styles(str(object))
    aligned = apply_alignment(styled)
    padded = apply_padding(aligned)
    return padded

def print(
    *objects,
    color = "#ffffff",
    bold = False,
    italic = False,
    underline = False,
    strike = False,
    reverse = False,
    alignment = None,
    padding = None,
    top_padding = None,
    right_padding = None,
    bottom_padding = None,
    left_padding = None,
    separator = " ",
    end = "\n",
    **kwargs
):
    renderables = []
    for object in objects:
        renderables.append(_style(
            object = object,
            color = color,
            bold = bold,
            italic = italic,
            underline = underline,
            strike = strike,
            reverse = reverse,
            alignment = alignment,
            padding = padding,
            top_padding = top_padding,
            right_padding = right_padding,
            bottom_padding = bottom_padding,
            left_padding = left_padding
        ))
    _CONSOLE.print(*renderables, sep = separator, end = end, **kwargs)

def input(
    text = "",
    color = "#ffffff",
    bold = False,
    italic = False,
    underline = False,
    strike = False,
    reverse = False
):
    if _IN_GOOGLE_COLABORATORY:
        while text.startswith("\n"):
            print(" ")
            text = text[1:]
    return _CONSOLE.input(_style(
        object = text,
        color = color,
        bold = bold,
        italic = italic,
        underline = underline,
        strike = strike,
        reverse = reverse
    )).strip()

def clear_console():
    if _IN_GOOGLE_COLABORATORY:
        from IPython.display import clear_output
        clear_output(wait = True)
    else: subprocess.run("cls" if os.name == "nt" else "clear", shell = True)

def wait_for_key(
    text = "Pulse cualquier tecla para continuar...",
    color = "#ffffff",
    bold = True,
    italic = True,
    underline = False,
    strike = False,
    reverse = False,
    alignment = None,
    padding = None,
    top_padding = None,
    right_padding = None,
    bottom_padding = None,
    left_padding = None
):
    print(
        f"\n{text}",
        color = color,
        bold = bold,
        italic = italic,
        underline = underline,
        strike = strike,
        reverse = reverse,
        alignment = alignment,
        padding = padding,
        top_padding = top_padding,
        right_padding = right_padding,
        bottom_padding = bottom_padding,
        left_padding = left_padding,
        end = ""
    )
    if _IN_GOOGLE_COLABORATORY:
        import builtins
        import time
        time.sleep(0.1)
        builtins.input()
    else: readchar.readkey()