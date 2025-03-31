from checker.session import TSession
from os.path import isfile
from typing import List
import os


class BotNet:
    @property
    def sessions(self) -> List[TSession]:
        return [TSession(f'sessions/{file}') for file in os.listdir('sessions') if isfile(f'sessions/{file}')]  # noqa: E501

    async def valid_sessions(self) -> List[TSession]:
        return [session for session in self.sessions if await session.is_valid() and not session.disconnect()]  # noqa: E501

    async def join_channel(self, invite_link: str) -> None:
        for session in await self.valid_sessions():
            await session.connect()
            await session.join_channel(invite_link)
            session.disconnect()

    async def start_bot(self, bot_link: str) -> None:
        for session in await self.valid_sessions():
            await session.connect()
            await session.start_bot(bot_link)
            session.disconnect()

    async def click_button(self, bot_link: str, button_text: str) -> None:
        for session in await self.valid_sessions():
            await session.connect()
            await session.click_button(bot_link, button_text)
            session.disconnect()
