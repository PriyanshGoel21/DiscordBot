from datetime import datetime
from typing import Any

import asyncpg
from discord.ext import commands


class DiscordBot(commands.AutoShardedBot):
    """A Subclass of `commands.Bot`."""

    prefixes: dict
    """List of prefixes per guild."""

    db_pool: asyncpg.Pool
    """Represent the database pool."""

    uptime: datetime = datetime.now()
    """Bot's uptime."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
