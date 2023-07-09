from pydantic import Extra, BaseModel, validator


class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    save_enabled: bool = False
    plugin_enabled: bool = True
    max_picture: int = 2

    @validator('save_enabled')
    def _(cls, v):
        if isinstance(v, bool):
            return v
        raise ValueError('save_enabled must be a boolean value!')
