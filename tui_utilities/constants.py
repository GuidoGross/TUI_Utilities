from rich.console import Console
import sys

_IN_GOOGLE_COLABORATORY = "google.colab" in sys.modules or "ipykernel" in sys.modules
_CONSOLE = Console(width = 152 if _IN_GOOGLE_COLABORATORY else None)