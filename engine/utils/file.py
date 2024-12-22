from typing import Iterable


def validate_format_file(filename: str, formats: Iterable[str]) -> None:
    """Валидирует формат файла.

    Args:
        filename (str): название файла.
        formats (Iterable[str]): разрешённые форматы.
    """
    filename = filename.split('.')
    file_format = filename[-1]
    if len(filename) > 1 and file_format in formats:
        return
    raise ValueError(f'Файл не соответсвует форматам: {','.join(formats)}')
