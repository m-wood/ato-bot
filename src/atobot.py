"""
Bot library for a Discord bot


Bot account:
    ato-bot#7075
Contact:
    atokymat#0529

Michael Wood
"""

from datetime import datetime, timedelta
import os
import random
import discord

ato_bot_id = 1031330737720397945

time_responses = [
    "time", "WYSI", "727!1!?!"
]
not_time_responses = [
    "not time",
    "it's literally not time",
    "I don't see it",
    "😐",
]

not_time_special_response_probability = 0.08
timeout_probability = 0.25
not_time_special_responses = ["osuplayerswhentheyseeit"]


def read_new_special_responses():
    global not_time_special_responses
    try:
        with open('responses/secret_not_time_responses.txt', 'r', encoding='utf-8') as secret_responses:
            for response in secret_responses.readlines():
                response_clean = response.strip()
                if response_clean not in not_time_special_responses:
                    not_time_special_responses.append(response_clean)
    except FileNotFoundError:
        # Additional secret responses not checked into git can be put into ./responses/secret_not_time_responses.txt
        pass


def write_new_special_responses(responses: list[str]):
    # Make sure file is up-to-date
    read_new_special_responses()
    try:
        with open('responses/secret_not_time_responses.txt', mode='a', encoding='utf-8') as secret_responses:
            for response in responses:
                if response not in not_time_special_responses:
                    secret_responses.write(f"\n{response}")
                    not_time_special_responses.append(response)
    except FileNotFoundError:
        # Additional secret responses not checked into git can be put into ./responses/secret_not_time_responses.txt
        pass


read_new_special_responses()

not_time_responses_mean = [
    "you are braindamaged", "keep yourself safe"
]
time_27_responses = [
    "wrong timezone bud", "I do not see it", "tryhard"
]


class AtoBotClient(discord.Client):

    def __init__(self, intents: discord.Intents) -> None:
        super().__init__(intents=intents)

        self.bot_id: int = None
        self.ato_guild: discord.Guild = None

        self.peko_cum_emote: discord.Emoji = None
        self.bedge_madge_emote: discord.Emoji = None
        self.alvin_emote: discord.Emoji = None

        self.is_in_shutdown = False

    async def on_ready(self) -> None:
        self.bot_id = self.user.id

        # ato-bot#7075 will always be a member of my server
        self.ato_guild = self.get_guild(346089839508324353)

        # And I will keep these emotes uploaded
        self.peko_cum_emote = await self.ato_guild.fetch_emoji(931375103365754951)
        self.bedge_madge_emote = await self.ato_guild.fetch_emoji(886081565770285056)
        self.alvin_emote = await self.ato_guild.fetch_emoji(1027788302411116584)

    async def on_message(self, message: discord.Message) -> None:
        # print(f'Message from {message.author}: {message.content}')

        # Ignore messages from self
        if message.author.id == self.bot_id:
            return

        # For debugging: only allow atokymat🌈#0529 to run anything
        # if message.author.id != 346089198991704065:
        #     return

        # Give atokymat🌈#0529 special commands
        if message.author.id == 346089198991704065:
            await self.atokymat_command(message)

        clean_message = message.content.lower().strip()

        if "time" in clean_message:
            await self.parse_time_response(message)

        elif self.user in message.mentions:
            await self.respond_to_ping(message)

        elif clean_message.startswith(">rs") or clean_message.startswith("<r"):
            await self.congratulate_recent(message)

        elif clean_message.startswith(">c") or clean_message.startswith("<c"):
            await self.shame_compare(message)

        elif clean_message.startswith(">gap"):
            # Why did ouf have to teach me about this command
            await message.channel.send(
                f"{message.author.mention} ill shove this dick in your gap if you keep doing that")
            await message.add_reaction("🖕")

    async def atokymat_command(self, message: discord.Message) -> None:
        """Lets me not run the bot 24/7 while I'm at work if I don't want to"""

        # To log off the bot
        if message.content == "ato!logoff":
            await message.channel.send("See you next time!")
            quit(0)
            return

        # To restart the bot
        if message.content == "ato!restart":
            await message.channel.send("Bot will restart")
            os.system("bot-restart.bat")
            quit(0)

        if message.content.startswith("ato!add"):
            lines = message.content[8:].split(", ")
            write_new_special_responses(lines)
            return

        if message.content == "ato!secrets":
            bots_chan = await self.ato_guild.fetch_channel(941195122039742504)
            await bots_chan.send(", ".join([funny for funny in not_time_special_responses]))
            return

    async def shame_compare(self, message: discord.Message) -> None:
        await message.reply(f"keep your ego in check")
        if message.author.id == 193412336881500160 and self.alvin_emote is not None:
            await message.add_reaction(self.alvin_emote)
        elif self.bedge_madge_emote is not None:
            await message.add_reaction(self.bedge_madge_emote)

    async def congratulate_recent(self, message: discord.Message) -> None:
        await message.channel.send("good job bro")

        if message.author.id == 193412336881500160 and self.alvin_emote is not None:
            await message.add_reaction(self.alvin_emote)
        elif self.peko_cum_emote is not None:
            await message.add_reaction(self.peko_cum_emote)

    async def respond_to_ping(self, message: discord.Message) -> None:
        clean_message = message.content.lower().strip()

        context = 0
        context += clean_message.count("good bot")
        for angry_context in (clean_message.count(mean_msg) for mean_msg in ["bad bot", "fuck you", "🖕"]):
            context -= angry_context

        if context > 0:
            await message.channel.send("thanks")
        elif context == 0:
            await message.channel.send("erm")
        else:
            await message.channel.send("what did I do")

    async def parse_time_response(self, message: discord.Message) -> None:
        current_time = datetime.now()

        # bully Alvin
        if message.author.id == 193412336881500160:
            return await self.send_angry_time_response(message, current_time)

        # tease anyone else
        if current_time.hour in {7, 19} and current_time.minute == 27:
            await self.send_time_response(message)

        # send special messages at other XX:27
        elif current_time.minute == 27:
            await self.send_hour_27_response(message)

        # it's literally not time stop pinging the bot
        else:
            await self.send_not_time_response(message)

    async def send_not_time_response(self, message: discord.Message) -> None:
        if not_time_special_responses and random.random() < not_time_special_response_probability:
            # Read new responses just in time
            read_new_special_responses()
            await message.reply(f"{random.choice(not_time_special_responses)}")
        else:
            await message.reply(f"{random.choice(not_time_responses)}")

        # Don't timeout atokymat🌈#0529
        if message.author.id != 346089198991704065:
            # Time out anyone else so I don't get rate limited kekw
            if random.random() < timeout_probability:
                await message.author.timeout(timedelta(seconds=60))

    async def send_hour_27_response(self, message: discord.Message) -> None:
        await message.reply(f"{random.choice(time_27_responses)}")
        # Allow spam at XX:27; no timeouts

    async def send_time_response(self, message: discord.Message) -> None:
        await message.channel.send(f"{message.author.mention} {random.choice(time_responses)}")
        if self.ato_guild is not None:
            # send time in #general in category General
            await self.ato_guild.get_channel(944096756755464213).send(
                f"@/everyone {message.author.display_name} says time"
            )
        # Allow spam at time; no timeouts

    async def send_angry_time_response(self, message: discord.Message, current_time: datetime) -> None:
        if current_time.hour in {7, 19} and current_time.minute == 27:
            await message.channel.send(f"{message.author.mention} kys")
        else:
            await message.reply(f"{random.choice(not_time_responses_mean)}")
            await message.channel.send(self.alvin_emote)
            await message.author.timeout(timedelta(seconds=180))
