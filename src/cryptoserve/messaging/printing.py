from io import StringIO

from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text


def prettify(sections: list[tuple], width: int = 80, menu_title: str = "Error Report"):
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
