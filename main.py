import asyncio
import logging
import logging.handlers
import os
from os import listdir

import asyncpg
import discord
from discord.ext import commands

from utillities.discordbot import DiscordBot


class Bot(DiscordBot):
    def __init__(
        self,
        db_pool: asyncpg.Pool,
    ):
        self.db_pool = db_pool
        super().__init__(
            allowed_mentions=discord.AllowedMentions(everyone=False),
            case_insensitive=True,
            command_prefix=self.__get_prefix,
            intents=discord.Intents.all(),
        )

    def __get_prefix(self, client: DiscordBot, message: discord.Message):
        guild_id = message.guild.id
        if guild_id in self.prefixes:
            prefix = self.prefixes[guild_id]
        else:
            prefix = "!"
        return commands.when_mentioned_or(prefix)(client, message)

    async def on_ready(self):
        print(f"{self.user} has started")

    async def setup_hook(self):
        """Initialize the db, prefixes & cogs."""

        self.prefixes = dict()

        for filename in listdir("cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")

        if os.getenv("TESTING_GUILD_ID"):
            guild = discord.Object(int(os.getenv("TESTING_GUILD_ID")))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()


async def main():
    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)
    async with asyncpg.create_pool(dsn=os.getenv("DATABASE_DSN")) as pool:
        async with Bot(db_pool=pool) as bot:
            await bot.start(os.getenv("TOKEN"))


asyncio.run(main())
