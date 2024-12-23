from pygame import mixer

from engine.audio.constants import SoundsPathEnum
from engine.metaclasses.singleton import SingletonMeta


class Audio(metaclass=SingletonMeta):
    """Класс управления звуками и музыкой."""

    def __init__(self) -> None:
        """Инициализация аудио игрового процесса."""
        mixer.init()
        self._effects: dict[str, mixer.Sound] = {}
        self._voices: dict[str, mixer.Sound] = {}

    def start_music(self) -> None:
        """Запускает воспроизведение музыки."""
        mixer.music.play(-1)

    def stop_music(self) -> None:
        """Останавливает воспроизведение музыки."""
        mixer.music.stop()

    def fadeout_music(self, time: int = 200) -> None:
        """Затухание музыки.

        Args:
            time (int, optional): время затухания музыки(в мс). По дефолту 200.
        """
        mixer.music.fadeout(time)

    def _load(self, path: str, volume: float, sounds: dict[str, mixer.Sound]) -> None:
        """Загружает файл звука.

        Args:
            path (str): путь до файла.
            volume (float): громкость.
            sounds (dict[str, mixer.Sound]): звуки.

        Returns:
            mixer.Sound: звук.
        """
        if sound := sounds.get(path):
            return sound
        sound = mixer.Sound(path)
        sound.set_volume(volume)
        sounds[path] = sound
        return sound

    def load_music(self, filename: str) -> None:
        """Загрузка музыки.

        Args:
            filename (str): название файла.
        """
        path = str(SoundsPathEnum.MUSICS.value / filename)
        mixer.music.load(path)

    def load_effect(self, filename: str) -> mixer.Sound:
        """Загрузка звука эффекта.

        Args:
            filename (str): название файла.

        Returns:
            mixer.Sound: звук эффекта.
        """
        path = str(SoundsPathEnum.EFFECTS.value / filename)
        return self._load(path, self.effects_volume, self._effects)

    def load_voices(self, filename: str) -> mixer.Sound:
        """Загрузка звука голоса.

        Args:
            filename (str): название файла.

        Returns:
            mixer.Sound: звук голоса.
        """
        path = str(SoundsPathEnum.VOICES.value / filename)
        return self._load(path, self.voices_volume, self._voices)

    def _volume(self, attrname: str, volume: float, sounds: dict[str, mixer.Sound]) -> None:
        """Устанавливает громкость звукам.

        Args:
            attrname (str): название атрибута громкости.
            volume (float): громкость.
            sounds (dict[str, mixer.Sound]): звуки.
        """
        setattr(self, attrname, volume)
        for sound in sounds.values():
            sound.set_volume(volume)

    @property
    def music_volume(self) -> float:
        """Громкость музыки.

        Returns:
            float: громкость музыки.
        """
        return self._music_volume

    @property
    def effects_volume(self) -> float:
        """Громкость эффектов.

        Returns:
            float: громкость эффектов.
        """
        return self._effects_volume

    @property
    def voices_volume(self) -> float:
        """Громкость голоса.

        Returns:
            float: громкость голоса.
        """
        return self._voices_volume

    @music_volume.setter
    def music_volume(self, volume: float) -> None:
        """Устанавливает громкость музыке.

        Args:
            volume (float): громкость.
        """
        setattr(self, '_music_volume', volume)
        mixer.music.set_volume(volume)

    @effects_volume.setter
    def effects_volume(self, volume: float) -> None:
        """Устанавливает громкость эффектам.

        Args:
            volume (float): громкость.
        """
        self._volume('_effects_volume', volume, self._effects)

    @voices_volume.setter
    def voices_volume(self, volume: float) -> None:
        """Устанавливает громкость голосу.

        Args:
            volume (float): громкость.
        """
        self._volume('_voices_volume', volume, self._voices)
