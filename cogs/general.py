import random
import time

import aiohttp
import asyncpg
import discord
from discord import Webhook
from discord.ext import commands

from utillities.discordbot import DiscordBot


class General(commands.Cog, name="general"):
    def __init__(self, bot: DiscordBot) -> None:
        self.bot = bot
        self.temp1 = [
            "https://discord.com/api/webhooks/1010181670290342000/R6MTh2jJ4dWYvxWmWXdRevS1_qCGJAEscsjS-2cOlDUuhSTEiHBjekDv7EIkkE8kKZ23",
            "https://discord.com/api/webhooks/1010181793200214166/3QIwGlPY_-dZRVpoM1I4rAuu3Lokk3ZWMog0DJrSZee-lF5pXiBMU75CHyDkIi7tsySr",
        ]
        self.temp2 = [
            "https://discord.com/api/webhooks/1010182238517854258/V6l4-LOSmr70zzdFBvirYJzJwKKcpf0iCdVW8mpIb4esVp22Yo9RxKczQVMLh2JEgylO",
            "https://discord.com/api/webhooks/1010182274555318272/oRnTCAmfnGtoU7XsAfOBFXTvusTvxLVAlVO1xNfw5EpazvfCNafIjQsGiMyVGZCXqfV3",
        ]
        self.temp3 = [
            "https://discord.com/api/webhooks/1010182501311979600/QuUSTkfykl2z3bJia13FR-mcidUQ1qhlfdBmr4Z6SbbXMlURI1ozafEQsO9E2kJVL-qm",
            "https://discord.com/api/webhooks/1010182504826818702/-VI1xi9LpnU2LanQZK35lkdpZViUlNlSX1rI5ChRO0f8hE1TOgyoxZIkfZspv_m09pwc",
        ]

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.name.startswith("temp") and message.author.bot is False:
            await message.delete()
            async with aiohttp.ClientSession() as session:
                index = random.randint(0, 1)
                webhook1 = Webhook.from_url(
                    self.temp1[index],
                    session=session,
                )
                webhook2 = Webhook.from_url(
                    self.temp2[index],
                    session=session,
                )
                webhook3 = Webhook.from_url(
                    self.temp3[index],
                    session=session,
                )
                await webhook1.send(
                    message.content,
                    username=message.author.display_name,
                    avatar_url=message.author.display_avatar.url,
                    allowed_mentions=discord.AllowedMentions(everyone=False),
                )
                await webhook2.send(
                    message.content,
                    username=message.author.display_name,
                    avatar_url=message.author.display_avatar.url,
                    allowed_mentions=discord.AllowedMentions(everyone=False),
                )
                await webhook3.send(
                    message.content,
                    username=message.author.display_name,
                    avatar_url=message.author.display_avatar.url,
                    allowed_mentions=discord.AllowedMentions(everyone=False),
                )


async def setup(bot: DiscordBot):
    await bot.add_cog(General(bot))
