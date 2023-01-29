import asyncio
from datetime import datetime

import logging
import operator
import re
from typing import Any
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram_dialog import (Dialog, DialogManager, DialogRegistry, Window, StartMode)
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Multiselect, Cancel, Start, Url, Radio, Group, Row
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from db import get_info_from_db

with open('token_test.txt', 'r') as file:
    token = file.read().strip()


class DialogSG(StatesGroup):
    main_menu = State()
    users = State()


# async def get_data(dialog_manager: DialogManager, **kwargs):
#     dialog_data = dialog_manager.current_context().dialog_data
#     return {
#         "text": await get_info_from_db(),
#     }
#
#
async def to_users(c: CallbackQuery, dialog: Dialog, manager: DialogManager):
    await c.message.answer(f'{await get_info_from_db()}')
    #await c.answer(f"users: {await get_info_from_db()}")
    await manager.switch_to(state=DialogSG.users)

async def to_main(c: CallbackQuery, dialog: Dialog, dialog_manager: DialogManager):
    dialog_data = dialog_manager.current_context().dialog_data
    #await c.message.answer(f'{await get_info_from_db()}')
    #await c.answer(f"users: {await get_info_from_db()}")
    await dialog_manager.switch_to(state=DialogSG.main_menu)

dialog = Dialog(
    Window(
        Format("Пересылка данных"),
        Button(Const("users"), id="sec4", on_click=to_users),
        state=DialogSG.main_menu,
        #getter=get_data,
    ),
    Window(
        Format("users"),
        Button(Const("main"), id="sec4", on_click=to_main),
        state=DialogSG.users,
        # getter=get_data,
    ),
)


async def main():
    logging.basicConfig(level=logging.INFO)
    storage = MemoryStorage()
    bot = Bot(token=token)
    dp = Dispatcher(bot, storage=storage)
    registry = DialogRegistry(dp)
    registry.register_start_handler(DialogSG.main_menu)
    registry.register(dialog)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
