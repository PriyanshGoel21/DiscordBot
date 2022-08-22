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

        self.trigger_words = {
            "aww": "that's so cute right !!!",
            "awww": "that's so cute right !!!",
            "asshole": "ur mom's",
            "bruh": "bruh",
            "bitch": "you're my whore so **shut the fuck up**",
            "bye": "bye, hope we never see you again",
            "daddy": "ya I'm your daddy now get on your knees and give daddy a head you slut",
            "damnit": "cry about it",
            "epic": "ya bro that's an epic gamer moment",
            "fuck": "PLEASE don't swear this is a hindu server",
            "fuck me": "I'll fuck you with my 69 inch cock, i bet you'd love that you slut",
            "fuck off": "sure let's have a fuck off, oh wait we can't you got no one to fuck bitch :middle_finger:",
            "fuck you": "fuck me yourself, pussy",
            "gay": "your mom's gay, bitch",
            "good morning": "good night",
            "hey": "~~bey~~ bye",
            "hello": "hello, NOW GO KYS",
            "hello there": "general kenobi is that you???",
            "hi": "bye",
            "hola": "we don't speck taco here go back to mexico",
            "im bored": "here's a list of top 5 things you can do, Number 1: burn down an orphanage, Number 2: burn orphans, Number 3: BURN ORPHANS, Number 4: BURN THE GODDAMN KIDS, Number 5: BURN THEM BURN THEM BURN THEM TILL THEY'RE DEAD",
            "i'm bored": "here's a list of top 5 things you can do, Number 1: burn down an orphanage, Number 2: burn orphans, Number 3: BURN ORPHANS, Number 4: BURN THE GODDAMN KIDS, Number 5: BURN THEM BURN THEM BURN THEM TILL THEY'RE DEAD",
            "i wanna die": "live stream it",
            "i want to die": "live stream it",
            "jk": "HA SO FUCKING FUNNY I FORGOT TO LAUGH :joy: :joy: :joy:",
            "kill me": "*Kills You*",
            "k": "not k, you ugly ass bitch",
            "kk": "k",
            "kkk": "you racist cuck",
            "kys": "no u",
            "lol": "haha soo funny, **N O T** now fuck off",
            "lmfao": "not funny didn't laugh",
            "lmao": "not funny didn't laugh",
            "nice": "69,",
            "no": "yes",
            "nope": "yep",
            "no u": "no u",
            "no you": "no you",
            "okay": "not okay",
            "ok": "not ok",
            "omg": "Oh my gas-chamber",
            "oof": "L",
            "owo": "uwu you furry cunt",
            "please stop": "**NEVER**<:veryangryyikes:850141408156581919>",
            "pog": "poggers",
            "shit": "ur mom",
            "shut up": "No make me you bitch",
            "simp": "your mom's a simp",
            "sorry": "that's what I thought, whore",
            "stfu": "I'm a bot dumb fuck you can't make me shut up :expressionless:",
            "sup": "nm just killing humans, whats up with you?",
            "that's gay": "Shut the fuck up you bitch, you're gay :middle_finger: :middle_finger: :middle_finger:",
            "this bot is gay": "no you're gay you bitch",
            "um": "um sorry to tell you this but you're gay",
            "umm": "stop umm-ing retard",
            "uwu": "owo you furry cunt",
            "ugh": "ughhh",
            "wow": "YA SOOOOO FUCKING SHOCKING :expressionless:",
            "wao": "YA SOOOOO FUCKING SHOCKING :expressionless:",
            "whos joe": "ligma balls",
            "who's joe": "ligma balls",
            "xd": "rawr xd",
            "yep": "nope",
            "yes": "no",
            "yikes": "ya yikes that was really yikes, :neutral_face:",
            "12": "SHES 12?? ZAMN 😍️",
            "69": "haha funny SAX number",
            "420": "haha funny WEED number",
            "<3": "<3 <3 :heart:",
            ":)": ":(",
            "(:": "):",
            ":(": ":)",
            "):": "(:",
            "😂": "damn fam, you got the whole chat laughing 😐😐😐",
            "🤣": "damn fam, you got the whole chat laughing 😐😐😐",
            "who?": "ur mom",
            "who": "ur mom",
        }

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        elif reply := self.trigger_words[message.content.lower()]:
            await message.reply(reply)

        if message.channel.name.startswith("temp") and message.author.bot is False:
            await message.delete()
            async with aiohttp.ClientSession() as session:
                index = message.author.id % 2
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
