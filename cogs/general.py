import random
import time

import aiohttp
import discord
from discord import Webhook
from discord.ext import commands

from utillities import bot_has_permissions
from utillities.discordbot import DiscordBot


class General(commands.Cog, name="general"):
    def __init__(self, bot: DiscordBot) -> None:
        self.bot = bot
        self.webhooks = [
            [
                "https://discord.com/api/webhooks/1010181670290342000/R6MTh2jJ4dWYvxWmWXdRevS1_qCGJAEscsjS-2cOlDUuhSTEiHBjekDv7EIkkE8kKZ23",
                "https://discord.com/api/webhooks/1010181793200214166/3QIwGlPY_-dZRVpoM1I4rAuu3Lokk3ZWMog0DJrSZee-lF5pXiBMU75CHyDkIi7tsySr",
            ],
            [
                "https://discord.com/api/webhooks/1010182238517854258/V6l4-LOSmr70zzdFBvirYJzJwKKcpf0iCdVW8mpIb4esVp22Yo9RxKczQVMLh2JEgylO",
                "https://discord.com/api/webhooks/1010182274555318272/oRnTCAmfnGtoU7XsAfOBFXTvusTvxLVAlVO1xNfw5EpazvfCNafIjQsGiMyVGZCXqfV3",
            ],
            [
                "https://discord.com/api/webhooks/1010182501311979600/QuUSTkfykl2z3bJia13FR-mcidUQ1qhlfdBmr4Z6SbbXMlURI1ozafEQsO9E2kJVL-qm",
                "https://discord.com/api/webhooks/1010182504826818702/-VI1xi9LpnU2LanQZK35lkdpZViUlNlSX1rI5ChRO0f8hE1TOgyoxZIkfZspv_m09pwc",
            ],
        ]

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if self.bot.user in message.mentions:
            await message.reply(
                "Looks like you tagged the wrong Epsilon smh. <@890650629201076224>"
            )

        if message.author.id == 490458548422311937:
            if random.randint(1, 100) == 69:
                await message.reply("Neet results when?")

        if message.channel.name.startswith("temp") and message.author.bot is False:
            await message.delete()
            async with aiohttp.ClientSession() as session:
                for webhook in self.webhooks:
                    await Webhook.from_url(
                        webhook[message.author.id % 2],
                        session=session,
                    ).send(
                        message.content,
                        username=message.author.display_name,
                        avatar_url=message.author.display_avatar.url,
                        allowed_mentions=discord.AllowedMentions(everyone=False),
                    )

    @bot_has_permissions(send_messages=True)
    @commands.hybrid_command(name="ping", description="Ping the bot.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx: commands.Context):
        """Show latency in seconds & milliseconds"""
        before = time.monotonic()
        message = await ctx.send(":ping_pong: Pong!")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f":ping_pong: Pong! in {int(ping)}ms")


async def setup(bot: DiscordBot):
    await bot.add_cog(General(bot))
