from opentele.td import TDesktop, API
import logging
import uuid


class TData:
    def __init__(self, path: str):
        self.path = path
        self.api = API.TelegramDesktop.Generate()
        self.tdesk = TDesktop(path, api=self.api)
        self.session = f'{uuid.uuid4()}.session'

    @property
    def is_valid(self) -> bool:
        return self.tdesk.isLoaded()

    async def convert_to_session(self) -> None:
        """Verifies the validity of the tdata and converts it to a session"""

        if self.is_valid:
            await self.tdesk.ToTelethon(session=f'sessions/{self.session}', api=self.api)  # noqa: E501

            logging.info(f'Successfuly created session {self.session} from tdata!')  # noqa: E501

        else:
            logging.info('Invalid tdata')
