import ctypes
import locale

def set_window_title(title): ctypes.windll.kernel32.SetConsoleTitleW(title)

def maximize_window():
    handle = ctypes.windll.kernel32.GetConsoleWindow()
    if handle and ctypes.windll.user32.IsWindowVisible(handle): ctypes.windll.user32.ShowWindow(handle, 3)

def set_locale(locale_identifier = "es_AR.UTF-8"): locale.setlocale(locale.LC_ALL, locale_identifier)