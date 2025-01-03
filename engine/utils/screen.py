from pygame.display import Info


def get_sreen_resolution() -> tuple[int, int]:
    """Отдаёт текущее разрешение экрана.

    Returns:
        tuple[int, int]: ширина и высота разрешения экрана.
    """
    display_info = Info()
    return display_info.current_w, display_info.current_h
