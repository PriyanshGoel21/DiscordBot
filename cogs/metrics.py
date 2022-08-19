import time

import asyncpg
import discord
from discord.ext import commands

from utillities.discordbot import DiscordBot
from utillities import bot_has_permissions


class Metrics(commands.Cog, name="metrics"):
    def __init__(self, bot: DiscordBot) -> None:
        self.bot = bot

    async def load(self, channel: discord.TextChannel):
        async with self.bot.db_pool.acquire() as connection:
            connection: asyncpg.Connection
            created_at = await connection.fetchval(
                """
                SELECT created_at 
                FROM messages 
                WHERE channel_id = $1
                ORDER BY created_at DESC
                """,
                channel.id,
            )
        async for message in channel.history(
            limit=None, oldest_first=True, after=created_at
        ):
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
                        f"============\n{channel.mention}\n============\n{str(E)}"
                    )
        log_channel: discord.TextChannel = self.bot.get_channel(952424006928175114)
        await log_channel.send(f"Done {channel.mention}")

    @commands.Cog.listener()
    async def on_ready(self):
        guild: discord.Guild = self.bot.get_guild(987324781881884702)
        for text_channel in guild.text_channels:
            self.bot.loop.create_task(self.load(text_channel))


async def setup(bot: DiscordBot):
    await bot.add_cog(Metrics(bot))
