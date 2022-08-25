import asyncpg
import discord
from discord.ext import commands

from utillities.discordbot import DiscordBot


class Metrics(commands.Cog, name="metrics"):
    def __init__(self, bot: DiscordBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        try:
            async with self.bot.db_pool.acquire() as connection:
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
        except asyncpg.UniqueViolationError:
            ...


async def setup(bot: DiscordBot):
    await bot.add_cog(Metrics(bot))
