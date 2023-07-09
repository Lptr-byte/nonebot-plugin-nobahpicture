from nonebot import get_driver
from nonebot.rule import Rule, to_me

from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)  # type: ignore


async def plugin_is_enable() -> bool:
    return config.plugin_enabled

plugin_rule = Rule(plugin_is_enable)    # type: ignore
rule = to_me() & plugin_rule
