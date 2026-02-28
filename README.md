# TUI Utilities

Personal-use console utilities library providing styled terminal interaction, structured menus, robust input validation, formatting helpers, and Spanish-oriented user experience.

---

## Purpose

This library is designed for console-based applications that need:

- Clean TUI

- Structured Spanish-language user interaction

- Robust validation

- Consistent formatting

---

## Dependencies

Standard library modules are used where possible; only external dependencies are listed:

- rich

- readchar

- requests

---

## Features

---

### Console Utilities (console)

Styled terminal interaction built on rich:

- print(): styled print function built on rich, supporting text styles, alignment, padding, and per-segment styling.

- input(): styled input function built on rich, supporting text styles and automatically trimming whitespaces.

- clear_console(): clears the terminal screen.

- wait_for_key(): pauses execution until the user presses a key.

---

### Structure Utilities (structure)

Tools for building structures in console applications:

- header(): prints a styled header, consisting of a title and a separator.

- menu(): creates interactive selection menus with header and automatic selection validation.

- confirmation_menu(): creates a confirmation dialog with custom message and options.

- confirm_exit(): creates a confirmation dialog that exits the program safely (uses confirmation_menu()).

- table(): creates personalized tables with easy introduction of fully-styled columns and rows.

- separator(): prints a fully-personalized visual separator line.

- error_message(): displays formatted error information including:

    - Custom message

    - Exception details

    - Full traceback

---

### Input Validation (validation)

Interactive validation utilities for user input.

- check_if_list_is_empty(): checks if a list is empty and displays an error screen if it is.

- validate_option(): validates user selection from a dictionary of options.

- validate_string(): ensures non-empty string input.

- validate_integer(): validates integers (uses Continental European numeric format).

- validate_double(): validates decimal numbers (uses Continental European numeric format).

- validate_datetime(): validates date and time input (uses Day–Month–Year date format with 24-hour time) with selectable year, time and second inclusion.

- validate_id(): validates Argentinian national ID numbers.

- validate_cellphone_number(): validates cellphone numbers (uses Argentinian format).

- validate_email(): validates e-mail addresses using an official TLDs list (from IANA's website) or syntax fallback (in case of not having an internet connection or a locally imported list of TLDs).

---

### Formatting Helpers (format)

Utilities for applying consistent formatting:

- decimal_format(): applies Continental European numeric formatting.

- datetime_format(): formats datetime objects (uses Day–Month–Year date format with 24-hour time) with automatic or custom year, time and second inclusion.

- id_format(): formats Argentinian national ID numbers.

- cellphone_number_format(): formats cellphone numbers (uses Argentinian format).

---

### System Utilities (system)

Helpers for interacting with the operating system console environment:

- set_window_title(): sets the console window title.

- maximize_window(): maximizes the console window.

- set_locale(): configures the process locale for number, date, and cultural formatting.

---

## Installation

pip install tui_utilities

---

## Update

pip install -U tui_utilities