import ctypes
import locale
import sys
import os

def set_window_title(title): ctypes.windll.kernel32.SetConsoleTitleW(title)

def maximize_window():
    handle = ctypes.windll.kernel32.GetConsoleWindow()
    if handle and ctypes.windll.user32.IsWindowVisible(handle): ctypes.windll.user32.ShowWindow(handle, 3)

def set_locale(locale_identifier = "es_AR.UTF-8"): locale.setlocale(locale_identifier)

def get_resources_path(relative_path):
    if hasattr(sys, "_MEIPASS"): return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)