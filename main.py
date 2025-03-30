from checker.session import TSession, TelegramClient
import logging
import asyncio


def setup():
    # Setting up logging

    logger = logging.getLogger()

    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('logs.log', mode='w')
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

if __name__ == "__main__":
    asyncio.run(main())
