from re import I, sub
from typing import Any, Tuple, Union, Annotated

from nonebot import on_regex, get_driver, on_command
from nonebot.log import logger
from nonebot.rule import to_me
from nonebot.params import Command, RegexGroup
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import (GROUP, PRIVATE_FRIEND, Bot, Event,
                                         Message, MessageSegment,
                                         GroupMessageEvent,
                                         PrivateMessageEvent)

from .rules import rule, plugin_rule
from .config import Config
from .get_picture import GetPicture

global_config = get_driver().config
config = Config.parse_obj(global_config)


change_plugin_state = on_command(('Ba图', '开启'), rule=to_me(), aliases={('Ba图', '禁用')},
                                 permission=SUPERUSER)
save_picture_state = on_command(('Ba图保存功能', '开启'), rule=to_me(), aliases={('Ba图保存功能', '关闭')},
                                permission=SUPERUSER)
give_me_picture = on_regex(r'^(来点Ba图)\s?([x|X|*]?\d+[张|个|份]?)?\s?(.*)?',
                           rule=plugin_rule, flags=I,
                           permission=PRIVATE_FRIEND | GROUP)


@change_plugin_state.handle()
async def _(cmd: Tuple[str, str] = Command()):
    _, action = cmd
    if action == '开启':
        config.plugin_enabled = True
    elif action == '禁用':
        config.plugin_enabled = False
    await change_plugin_state.finish(f'Ba图插件已{action}')


@save_picture_state.handle()
async def _(cmd: Tuple[str, str] = Command()):
    _, action = cmd
    if action == '开启':
        config.save_enabled = True
    elif action == '关闭':
        config.save_enabled = False
    await save_picture_state.finish(f'Ba图插件保存功能已{action}')


@give_me_picture.handle()
async def _(bot: Bot, event: Union[PrivateMessageEvent, GroupMessageEvent],
            regex_group: Annotated[tuple[Any, ...], RegexGroup()]):
    args = list(regex_group)
    logger.debug(f'args={args}')
    num = args[1]
    tag = args[2]
    #处理数据
    num = int(sub(r'\D', '', num)) if num else 1
    num = min(num, config.max_picture)
    tag = tag if tag else ''
    image_urls = GetPicture(pic_num=num, user_tag=tag, save=config.save_enabled).get_picture()
    for url in image_urls:
        try:
            await bot.send(event, MessageSegment.image(url))
        except:
            await bot.send(event, MessageSegment.text('发送图片失败……'))
            logger.error('发送图片失败……')
    await give_me_picture.finish()
