from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import Channel, User, Message
from telethon.tl.functions.messages import (
    ImportChatInviteRequest,
    StartBotRequest
)
from telethon import TelegramClient
from checker.models import Session
from typing import Optional
import logging


class TSession:
    def __init__(self, path: str):
        self.path = path
        self.session = path.split("/")[-1]
        self.client = TelegramClient(
            session=path,
            api_id=1,
            api_hash='1',
            system_version='4.16.30-vxCUSTOM'
        )

    async def is_valid(self) -> bool:
        if not self.client.is_connected():
            await self.client.connect()

        return await self.client.is_user_authorized()

    async def get_me(self) -> Optional[Session]:
        """Returns user id and username"""

        me = await self.client.get_me()

        if isinstance(me, User):
            return Session(id=me.id, username=me.username)

    async def join_channel(self, invite_link: str) -> None:
        """Connects the user to a private or public Telegram channel

        Args:
            invite_link (str): link to the Telegram channel
        """

        channel_name = invite_link.split('/')[-1].replace('+', '')
        account = await self.get_me()

        if account:
            try:
                if isinstance(await self.client.get_entity(channel_name), Channel):  # type: ignore # noqa: E501
                    await self.client(JoinChannelRequest(channel_name))  # type: ignore # noqa: E501

                    logging.info(f'The account @{account.username}, ID - {account.id} joined to channel!')  # type: ignore # noqa: E501

                else:
                    logging.error('The specified link does not lead to the channel')  # noqa: E501

            except ValueError:
                try:
                    await self.client(ImportChatInviteRequest(channel_name))  # noqa: E501

                    logging.info(f'The account @{account.username}, ID - {account.id} joined to channel!')  # type: ignore # noqa: E501

                except Exception:
                    logging.error('The channel was not found, or the user has already joined')  # noqa: E501

    async def start_bot(self, bot_link: str) -> None:
        """Sends /start to the Telegram bot

        Args:
            bot_link (str): link to the bot in Telegram
        """

        bot_name = bot_link.split('/')[-1]
        account = await self.get_me()

        if account:
            try:
                bot = await self.client.get_entity(bot_name)

                if isinstance(bot, User) and bot.bot:
                    await self.client(StartBotRequest(bot_name, bot_name, '1'))  # type: ignore # noqa: E501

                    logging.info(f'The account @{account.username}, ID - {account.id} launched the bot!')  # noqa: E501

                else:
                    logging.error('The specified link does not lead to the bot')  # noqa: E501

            except Exception:
                logging.error('The specified bot was not found')

    async def click_button(self, bot_link: str, button_text: str) -> None:
        """Clicks on the approximate text in the button

        Args:
            bot_link (str): link to the bot in Telegram
            button_text (str): approximate text in the button
        """

        bot_name = bot_link.split('/')[-1]
        account = await self.get_me()

        if account:
            try:
                bot = await self.client.get_entity(bot_name)

                if isinstance(bot, User) and bot.bot:
                    messages = await self.client.get_messages(bot_name)

                    if isinstance(messages, list) and isinstance(messages[0], Message):  # noqa: E501
                        message: Message = messages[0]

                        if message.reply_markup:
                            logging.info(message)

                            for row in message.reply_markup.rows:  # type: ignore # noqa: E501
                                for button in row.buttons:
                                    if button_text in button.text:
                                        await message.click(text=button.text)  # type: ignore # noqa: E501

                                        logging.info(f'The account @{account.username}, ID - {account.id} clicked \'{button.text}\' button!')  # noqa: E501

                                else:
                                    logging.warning('Button not found')

                        logging.warning('Reply markup not found')
                else:
                    logging.error('The specified link does not lead to the bot')  # noqa: E501

            except Exception:
                logging.error('The specified bot was not found')

    async def disconnect(self) -> None:
        """Closes the session"""

        await self.disconnect()
