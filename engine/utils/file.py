from typing import Iterable
from pathlib import Path


def validate_format_file(filename: str, formats: Iterable[str]) -> None:
    """Валидирует формат файла.

    Args:
        filename (str): название файла.
        formats (Iterable[str]): разрешённые форматы.
    """
    if Path(filename).suffix in formats:
        return
    raise ValueError(f'Файл не соответсвует форматам: {','.join(formats)}')
