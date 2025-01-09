from pathlib import Path
from typing import Callable

from pygame import mixer

from engine.audio.constants import SoundsPathEnum, SoundTypeEnum
from engine.metaclasses.singleton import SingletonMeta
from engine.cache import Cache


class Audio(metaclass=SingletonMeta):
    """Класс управления звуками и музыкой."""

    mixer.init()

    def __init__(self) -> None:
        """Инициализация аудио игрового процесса."""

        self._effects: dict[str, mixer.Sound] = {}
        self._voices: dict[str, mixer.Sound] = {}
        self._cache: Cache = Cache()

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
        sound = self._cache.get((path,), mixer.Sound, path)
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

    def load_voice(self, filename: str) -> mixer.Sound:
        """Загрузка звука голоса.

        Args:
            filename (str): название файла.

        Returns:
            Sound: звук голоса.
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


class Sound:
    """Класс представляющий sound.

    Attributes:
        _audio (Audio): объект для работы с аудио.
    """

    _map_get_sound: dict[SoundTypeEnum, Callable] = {
        SoundTypeEnum.EFFECT: lambda path: Audio().load_effect(path),
        SoundTypeEnum.VOICE: lambda path: Audio().load_voice(path),
    }

    def __init__(self, path: str | Path, sound_type: SoundTypeEnum, is_loop: bool = False) -> None:
        """Инициализация sound.

        Args:
            path (str | Path): путь до файла.
            sound_type (SoundTypeEnum): тип sound.
            is_loop (bool, optional):  зацикленный звук. По дефолту False.
        """
        self._sound: mixer.Sound = self._map_get_sound[sound_type](path)
        self._is_loop = -1 if is_loop else 0

    def stop(self) -> None:
        """Останавливает sound."""
        self._sound.stop()

    def play(self) -> None:
        """Запускает sound."""
        self._sound.play(loops=self._is_loop)

    def __deepcopy__(self, memo: dict) -> 'Sound':
        """При копировании возвращает сам себя.

        Args:
            memo (dict): словарь значений.

        Returns:
            Sound: Self.
        """
        return self
