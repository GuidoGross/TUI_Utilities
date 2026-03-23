from rich.console import Console
import sys

_CONSOLE = Console()
_IN_GOOGLE_COLABORATORY = "google.colab" in sys.modules or "ipykernel" in sys.modules