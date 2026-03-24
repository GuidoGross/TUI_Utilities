from .constants import _IN_GOOGLE_COLABORATORY
import ctypes
import locale
import sys
import os

def set_window_title(title):
    if in_google_colaboratory(): return
    if os.name == "nt": ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        sys.stdout.write(f"\033]0;{title}\007")
        sys.stdout.flush()

def maximize_window():
    if in_google_colaboratory() or os.name != "nt": return
    handle = ctypes.windll.kernel32.GetConsoleWindow()
    if handle and ctypes.windll.user32.IsWindowVisible(handle): ctypes.windll.user32.ShowWindow(handle, 3)

def set_locale(locale_identifier = "es_AR.UTF-8"): locale.setlocale(locale.LC_ALL, locale_identifier)

def get_resources_path(relative_path, base_path = None):
    if hasattr(sys, "_MEIPASS"): return os.path.join(sys._MEIPASS, relative_path)
    if base_path is None: base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def in_google_colaboratory(): return _IN_GOOGLE_COLABORATORY