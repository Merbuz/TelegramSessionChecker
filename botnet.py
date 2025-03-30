from checker.session import TSession
from checker.tdata import TData
from os.path import isfile
from typing import List
import os


class BotNet:
    @property
    def tdatas(self) -> List[TData]:
        return [TData(file) for file in os.listdir('tdatas') if isfile(f'tdatas/{file}')]  # noqa: E501s

    @property
    def sessions(self) -> List[TSession]:
        return [TSession(file) for file in os.listdir('sessions') if isfile(f'sessions/{file}')]  # noqa: E501

    async def convert_tdatas(self) -> None:
        for tdata in self.tdatas:
            await tdata.convert_to_session()

    async def join_channel(self, invite_link: str) -> None:
        for session in self.sessions:
            if await session.is_valid():
                await session.join_channel(invite_link)

    async def start_bot(self, bot_link: str) -> None:
        for session in self.sessions:
            if await session.is_valid():
                await session.start_bot(bot_link)

    async def click_button(self, bot_link: str, button_text: str) -> None:
        for session in self.sessions:
            if await session.is_valid():
                await session.click_button(bot_link, button_text)
