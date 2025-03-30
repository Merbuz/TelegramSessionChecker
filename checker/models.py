from typing import Optional
from attrs import define


@define
class Session:
    id: int
    username: Optional[str]
