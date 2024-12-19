from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.settings.schemas import GraphicsSettingsSchema, AudioSettingsSchema, EngineSettingsSchema


type TYPES_SETTINGS = str | int | float | bool | tuple[int, int] | None
type SETTINGS_SCHEMAS = AudioSettingsSchema | GraphicsSettingsSchema | EngineSettingsSchema
