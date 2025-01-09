class ManagementMixin:
    """Mixin старта, отстановки, перезапуска."""

    def _set_default_values(self) -> None:
        """Устанавливает дефолтные значения."""
        self._active_frame = 0
        self._elapsed = 0
        self.is_active = False
        if self._sound and self.is_loop:
            self._sound.stop()

    def restart(self) -> None:
        """Перезапускает."""
        self._set_default_values()
        self.is_active = True
        if self._sound:
            self._sound.play(loops=-1 if self.is_loop else 0)

    def start(self) -> None:
        """Запускает, если не активна."""
        if not self.is_active:
            self.restart()

    def stop(self) -> None:
        """Останавливает, если активна."""
        if self.is_active:
            self._set_default_values()

    def _update_elapsed(self) -> tuple[int, int]:
        """Обновление elapsed.

        Returns:
            tuple[int, int]: целая часть и остаток от деления _elapsed на time_between
        """
        self._elapsed += self._global_clock.frame_time
        return self._elapsed // self.time_between, self._elapsed % self.time_between
