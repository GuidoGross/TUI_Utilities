import subprocess
import ctypes
import locale

def set_window_title(title): subprocess.run(f"title {title}", shell = True)

def maximize_window(): ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 3)

def set_locale(locale_identifier = "es_AR.UTF-8"): locale.setlocale(locale.LC_ALL, locale_identifier)