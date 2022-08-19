from datetime import datetime

import asyncpg
from discord.ext import commands
from typing import Any


class DiscordBot(commands.Bot):
    """A Subclass of `commands.Bot`."""

    prefixes: dict
    """List of prefixes per guild."""

    db_pool: asyncpg.Pool
    """Represent the database pool."""

    uptime: datetime = datetime.now()
    """Bot's uptime."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
