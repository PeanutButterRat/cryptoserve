from io import StringIO

from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text


def prettify(sections: list[tuple], width: int = 80, menu_title: str = "Error Report"):
    """Generate a formatted, stylized string report using Rich panels.

    Args:
        sections: A list of tuples, where each tuple contains
            (title: str, body: str, color: str). Each tuple represents a section
            of the report to be rendered as an individual panel.
        width: The total width of the output. Defaults to 80.
        menu_title: The title displayed at the top of the entire
            report. Defaults to "Error Report".

    Returns:
        str: A single string containing the stylized report, suitable for
        terminal display or logging.
    """
    panels = []

    for title, body, color in sections:
        panel = Panel(
            Align.center(Text(body), style=color),
            title=f" {title} ",
            title_align="center",
            border_style=color,
            box=box.ROUNDED,
            padding=(1, 1),
        )
        panels.append(panel)

    message = Panel(
        Align.center(Group(*panels)),
        title=f" {menu_title} ",
        title_align="center",
        border_style="bright_black",
        box=box.ROUNDED,
        padding=(1, 1),
    )

    buffer = StringIO()
    console = Console(file=buffer, force_terminal=True, width=width)
    console.print(message)

    string = buffer.getvalue()
    buffer.close()

    return string
