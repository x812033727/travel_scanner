"""A small terminal screen, enough to read what a full-screen CLI shows.

The Antigravity CLI draws its pages with cursor moves rather than lines, so stripping the
escape sequences from its output runs words from different rows together. Feeding the
output through this grid and reading the rows back gives the text as it stands on the
screen. It knows the sequences such a program uses to place text (cursor moves, erases,
scrolling, the alternate screen) and skips everything else: colours, window titles,
hyperlinks, and the image and device-control strings some terminals accept. The agent runs
on the host's own python3, so this cannot come from a package.
"""

import re

_CSI = re.compile(r"\x1b\[([0-?]*)([ -/]*)([@-~])")
# OSC, DCS, APC, PM and SOS strings end with BEL or ST; none of them draws anything.
_STRING = re.compile(r"\x1b[\]P_^X].*?(?:\x07|\x1b\\)", re.DOTALL)


class Screen:
    def __init__(self, columns: int, rows: int) -> None:
        self.columns = columns
        self.rows = rows
        self._primary = self._blank()
        self._alternate = self._blank()
        self.grid = self._primary
        self.row = 0
        self.column = 0
        self._saved = (0, 0)
        self._pending = ""

    def _blank(self) -> list[list[str]]:
        return [[" "] * self.columns for _ in range(self.rows)]

    def _clamp(self) -> None:
        self.row = max(0, min(self.rows - 1, self.row))
        self.column = max(0, min(self.columns - 1, self.column))

    def _scroll(self) -> None:
        del self.grid[0]
        self.grid.append([" "] * self.columns)

    def _line_feed(self) -> None:
        if self.row == self.rows - 1:
            self._scroll()
        else:
            self.row += 1

    def _put(self, character: str) -> None:
        if self.column >= self.columns:
            self.column = 0
            self._line_feed()
        self.grid[self.row][self.column] = character
        self.column += 1

    def feed(self, text: str) -> None:
        """Apply more output; a sequence cut off at the end waits for the next call."""
        text = self._pending + text
        self._pending = ""
        text = _STRING.sub("", text)
        index = 0
        length = len(text)
        while index < length:
            character = text[index]
            if character == "\x1b":
                if index + 1 >= length:
                    self._pending = text[index:]
                    return
                follower = text[index + 1]
                if follower == "[":
                    match = _CSI.match(text, index)
                    if match is None:
                        if re.fullmatch(r"\x1b\[[0-?]*[ -/]*", text[index:]):
                            self._pending = text[index:]
                            return
                        index += 2
                        continue
                    self._control(match.group(1), match.group(3))
                    index = match.end()
                    continue
                if follower in "]P_^X":
                    # An unfinished string (its end has not arrived yet).
                    self._pending = text[index:]
                    return
                if follower in "()*+" and index + 2 < length:
                    index += 3  # Character set selection.
                    continue
                if follower == "7":
                    self._saved = (self.row, self.column)
                elif follower == "8":
                    self.row, self.column = self._saved
                elif follower == "D":
                    self._line_feed()
                elif follower == "E":
                    self.column = 0
                    self._line_feed()
                elif follower == "M":
                    if self.row == 0:
                        self.grid.insert(0, [" "] * self.columns)
                        del self.grid[-1]
                    else:
                        self.row -= 1
                elif follower == "c":
                    self.grid[:] = self._blank()
                    self.row = self.column = 0
                index += 2
                continue
            if character == "\r":
                self.column = 0
            elif character == "\n" or character in "\x0b\x0c":
                self._line_feed()
            elif character == "\b":
                self.column = max(0, self.column - 1)
            elif character == "\t":
                self.column = min(self.columns - 1, (self.column // 8 + 1) * 8)
            elif character >= " " and character != "\x7f":
                self._put(character)
            index += 1

    def _control(self, parameters: str, final: str) -> None:
        private = parameters.startswith("?")
        values = [
            int(part) if part.isdigit() else 0 for part in parameters.lstrip("?<>=").split(";")
        ]
        first = values[0] if values else 0
        count = max(1, first)
        if private:
            if final in "hl" and any(value in (47, 1047, 1049) for value in values):
                self.grid = self._alternate if final == "h" else self._primary
                if final == "h":
                    self._alternate[:] = self._blank()
            return
        if final in "Hf":
            self.row = count - 1
            self.column = (values[1] if len(values) > 1 and values[1] else 1) - 1
        elif final == "A":
            self.row -= count
        elif final in "Be":
            self.row += count
        elif final in "Ca":
            self.column += count
        elif final == "D":
            self.column -= count
        elif final == "E":
            self.row += count
            self.column = 0
        elif final == "F":
            self.row -= count
            self.column = 0
        elif final in "G`":
            self.column = count - 1
        elif final == "d":
            self.row = count - 1
        elif final == "J":
            self._erase_display(first)
        elif final == "K":
            self._erase_line(first)
        elif final == "X":
            end = min(self.columns, self.column + count)
            self.grid[self.row][self.column : end] = [" "] * (end - self.column)
        elif final == "P":
            line = self.grid[self.row]
            del line[self.column : self.column + count]
            line.extend([" "] * (self.columns - len(line)))
        elif final == "@":
            line = self.grid[self.row]
            line[self.column : self.column] = [" "] * count
            del line[self.columns :]
        elif final == "L":
            for _ in range(count):
                self.grid.insert(self.row, [" "] * self.columns)
                del self.grid[-1]
        elif final == "M":
            for _ in range(count):
                del self.grid[self.row]
                self.grid.append([" "] * self.columns)
        elif final == "S":
            for _ in range(count):
                self._scroll()
        elif final == "T":
            for _ in range(count):
                self.grid.insert(0, [" "] * self.columns)
                del self.grid[-1]
        elif final == "s":
            self._saved = (self.row, self.column)
        elif final == "u":
            self.row, self.column = self._saved
        self._clamp()

    def _erase_line(self, mode: int) -> None:
        line = self.grid[self.row]
        if mode == 0:
            line[self.column :] = [" "] * (self.columns - self.column)
        elif mode == 1:
            line[: self.column + 1] = [" "] * (self.column + 1)
        else:
            line[:] = [" "] * self.columns

    def _erase_display(self, mode: int) -> None:
        if mode == 0:
            self._erase_line(0)
            for row in range(self.row + 1, self.rows):
                self.grid[row] = [" "] * self.columns
        elif mode == 1:
            self._erase_line(1)
            for row in range(self.row):
                self.grid[row] = [" "] * self.columns
        else:
            self.grid[:] = self._blank()

    def lines(self) -> list[str]:
        """The rows that hold anything, right-trimmed, top to bottom."""
        rows = ("".join(row).rstrip() for row in self.grid)
        return [row for row in rows if row.strip()]

    def text(self) -> str:
        return "\n".join(self.lines())
