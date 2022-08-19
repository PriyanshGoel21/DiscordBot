import time

import asyncpg
import discord
from discord.ext import commands

from utillities.discordbot import DiscordBot
from utillities import bot_has_permissions


class Metrics(commands.Cog, name="metrics"):
    def __init__(self, bot: DiscordBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        async with self.bot.db_pool.acquire() as connection:
            try:
                await connection.execute(
                    """
                    INSERT INTO messages(message_id, channel_id, author_id, guild_id, created_at, bot) 
                    VALUES ($1, $2, $3, $4, $5, $6)
                    """,
                    message.id,
                    message.channel.id,
                    message.author.id,
                    message.guild.id,
                    message.created_at,
                    message.author.bot,
                )
            except Exception as E:
                log_channel: discord.TextChannel = self.bot.get_channel(
                    952424006928175114
                )
                await log_channel.send(
                    f"============\n{message.channel.mention}\n============\n{str(E)}"
                )


async def setup(bot: DiscordBot):
    await bot.add_cog(Metrics(bot))
