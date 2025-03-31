from botnet import BotNet
import logging
import asyncio


def setup():
    # Setting up logging

    logger = logging.getLogger()

    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('logs.log', mode='w', encoding="utf-8")
    file_handler.setFormatter(
        logging.Formatter('"%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"')  # noqa: E501
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter('"%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"')  # noqa: E501
    )

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


async def main():
    setup()

    # Running CLI

    logging.info('Hello')

    botnet = BotNet()

    for session in await botnet.valid_sessions():
        await session.connect()

        try:
            session_me = await session.get_me()

            if session_me:
                logging.info(f'Session ID - {session_me.id}, @{session_me.username} - valid!')  # noqa: E501

        except Exception:
            logging.info('Session is valid!')

        session.disconnect()

    logging.info(f'Valid sessions - {len(await botnet.valid_sessions())}')

    while True:
        action = input('Select an action:\n1 - Subscribe to the channel\n2 - Go to the bot\n3 - Go to the bot and click\n4 - Close checker\n')  # noqa: E501

        match action:
            case '1':
                channel = input('Enter the link to the channel:\n')

                await botnet.join_channel(channel)

            case '2':
                bot = input('Enter the link to the bot:\n')

                await botnet.start_bot(bot)

            case '3':
                bot = input('Enter the link to the bot:\n')
                button_text = input('Enter the text of the button to click on:\n')  # noqa: E501

                await botnet.start_bot(bot)
                await asyncio.sleep(2)
                await botnet.click_button(bot, button_text)

            case '4':
                break

if __name__ == "__main__":
    asyncio.run(main())
