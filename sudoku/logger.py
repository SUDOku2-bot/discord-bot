from pathlib import Path
from typing import IO


class Logger:
    _log_file: IO

    def __init__(self, path: str):
        Path(path).mkdir(parents=True, exist_ok=True)
        self._log_file = open(f"{path}/sudoku.log", 'a+')

    def error(self, message):
        self._log_file.write(f"[ ERROR ] : {message}")

    def warning(self, message):
        self._log_file.write(f"[ WARN ] : {message}")
