import textwrap
from dataclasses import dataclass, field


class TextMenu:

    @dataclass
    class Section:
        title: str
        lines: list[str] = field(default_factory=list)

        def add_line(self, line: str):
            self.lines.append(line)

        def get_length_of_longest_line(self):
            return max(self.lines, key=lambda line: len(line))

    def __init__(
        self,
        max_width: int = -1,
        horizontal_padding_spaces: int = 3,
        vertical_padding_lines: int = 1,
    ):
        self.max_width = max_width
        self.horizontal_padding_spaces = horizontal_padding_spaces
        self.vertical_padding_lines = vertical_padding_lines
        self._sections = {}

    def add_section(self, title: str, name: str = ""):
        identifier = name if name else title.replace(" ", "_").lower()

        if not identifier.isidentifier():
            raise ValueError("section was not given a valid identifier")

        section = self.Section(title=title)
        self._sections[identifier] = section
        setattr(self, identifier, section)

    def _calculate_width(self):
        if self.max_width > 0:
            return self.max_width

        longest_line_length = max(
            self._sections.values(),
            key=lambda section: section.get_length_of_longest_line(),
        )
        total_padding_length = 2 * (self.horizontal_padding_spaces + 1)

        return longest_line_length + total_padding_length

    def _format_line(self, text, width):
        padding = " " * self.horizontal_padding_spaces
        content_width = width - 2 * (self.horizontal_padding_spaces + 1)

        return f"|{padding}{text.ljust(content_width)}{padding}|"

    def _format_section_title(self, title: str, width: int):
        title_with_spaces = f" {title} "
        padded_title_with_spaces = title_with_spaces.center(width - 2, "=")

        return f"+{padded_title_with_spaces}+"

    def __str__(self):
        total_width = self._calculate_width()
        content_width = (
            total_width
            if self.max_width < 0
            else total_width - 2 * (self.horizontal_padding_spaces + 1)
        )

        actual_lines = []
        vertical_padding_line = self._format_line("", total_width)
        bottom_line = f"+{"=" * (total_width - 2)}+"

        for section in self._sections.values():
            actual_lines.append(self._format_section_title(section.title, total_width))
            actual_lines.extend([vertical_padding_line] * self.vertical_padding_lines)

            for line in section.lines:
                wrapped_line = textwrap.wrap(line, content_width)

                for sub_line in wrapped_line:
                    actual_lines.append(
                        self._format_line(sub_line.center(content_width), total_width)
                    )

            actual_lines.extend([vertical_padding_line] * self.vertical_padding_lines)

        actual_lines.append(bottom_line)

        return "\n".join(actual_lines)

    def to_bytes(self) -> bytes:
        return str(self).encode()
