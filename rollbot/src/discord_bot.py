from rollbot.src.system.system_base import RolePlayingSystem
from rollbot.src.system.dnd5e import Dnd5e
from collections import namedtuple

import discord
import logging


Command = namedtuple('Command', ['description', 'function'])

SYSTEMS = {'Dnd5e': Dnd5e}


def initialize_logger():
    logger = logging.getLogger('rollbot')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s : %(name)s : %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


class Channel:
    """
    Encapsulates information on a given discord channel.
    """
    DEFAULT_PREFIX = '~'
    DEFAULT_SYSTEM = None

    def __init__(self, channel: discord.TextChannel, prefix: str, system: RolePlayingSystem, guild_id: int, channel_id: int):
        self._channel = channel
        self.prefix = prefix
        self.system = system
        self.characters = dict()
        self._guild_id = guild_id
        self._channel_id = channel_id

    @staticmethod
    def default_channel(guild_id, channel_id, channel):
        default = Channel(channel,
                          Channel.DEFAULT_PREFIX,
                          Channel.DEFAULT_SYSTEM,
                          guild_id,
                          channel_id
                          )
        return default

    def __repr__(self):
        return f'Channel {self._channel.name} in guild {self._channel.guild.name}'

    def send(self, *args, **kwargs):
        return self._channel.send(*args, **kwargs)


class DiscordBot:
    def __init__(self):
        self._guilds: dict[str: dict[str: Channel]] = dict()
        self._logger = initialize_logger()
        self._commands: dict[str: Command] = {
            'prefix': Command(f'Changes assigned prefix. default is {Channel.DEFAULT_PREFIX}.', self.set_prefix),
            'help': Command('Get available commands.', self.help_str),
            'system': Command(f'Set the roleplaying system for this channel. Available systems are: {"\n\t".join(SYSTEMS.keys())}', self.set_system),
            'character': Command('Create character sheet', self.character),
            'my_character': Command('Print your character sheet', self.my_character),
            'check': Command('Performs a skill check', self.check)
        }
        self._initialize_client()

    def _initialize_client(self):
        """
        Initializes a discord bot and defines its events.
        See discord.py
        """
        intents = discord.Intents.default()
        intents.message_content = True

        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            self._logger.info(f'Bot logged in as {client.user}')

        @client.event
        async def on_message(message):
            if message.author == client.user:
                return
            try:
                await self._handle_message(message)
            except ValueError as e:
                self._logger.info(f'Couldn\'t handle message {message.content}: {e}')
                await message.channel.send(f'Sorry, ran into an error: {e}')

        self._client = client

    async def _handle_message(self, message: discord.Message):
        """
        Handles every received message.
        """
        message_metadata = message.to_message_reference_dict()
        guild_id, channel_id = message_metadata['guild_id'], message_metadata['channel_id']
        channel_settings = self._validate_channel(guild_id, channel_id, message.channel)

        # If message is not a rollbot command, stop message handling.
        if not message.content.startswith(channel_settings.prefix):
            return

        # Handle message
        parsed_message = message.content[len(channel_settings.prefix):].split(' ')
        author = message.author
        command_key = parsed_message.pop(0)
        command = self._commands.get(command_key)
        if not command:
            raise ValueError(f'Unknown command \"{command_key}\"')
        await command.function(channel_settings, parsed_message, author)

    def _validate_channel(self, guild_id: int, channel_id: int, channel_obj: discord.TextChannel):
        # Ensure the message comes from a known channel
        if guild_id not in self._guilds.keys():
            # Handle joining a guild
            self.join_guild(guild_id, channel_id, channel_obj)
        elif channel_id not in self._guilds[guild_id].keys():
            # Handle joining a new channel in an existing server
            self.join_channel(guild_id, channel_id, channel_obj)
        return self._guilds[guild_id][channel_id]

    def join_guild(self, guild_id: int, channel_id: int, channel: discord.TextChannel):
        """
        Adds a guild to the list of known guilds, as well as adding a channel.
        """
        self._guilds[guild_id] = dict()
        self._logger.info(f'Entered new guild with id {guild_id}')
        self.join_channel(guild_id, channel_id, channel)

    def join_channel(self, guild_id: int, channel_id: int, channel: discord.TextChannel):
        """
        Initializes the default settings for a new channel.
        """
        self._guilds[guild_id][channel_id] = Channel.default_channel(guild_id, channel_id, channel)
        self._logger.info(f'Entered new channel in guild {guild_id} with id {channel_id}')

    def run(self, token):
        """
        Logs rollbot in.
        """
        self._client.run(token)

    async def set_prefix(self, channel_settings: Channel, parsed_message: list[str], _):
        """
        Changes the message prefix for the given channel.
        """
        prefix = parsed_message[0]
        self._logger.info(f'Changing prefix of {channel_settings} to {prefix}')
        channel_settings.prefix = prefix
        await channel_settings.send(f'Changed prefix to {prefix}')

    async def set_system(self, channel_settings: Channel, parsed_message: list[str], _):
        """
        Sets the roleplaying system for given channel.
        """
        system_key = parsed_message[0]
        channel_settings.system = SYSTEMS[system_key]()
        self._logger.info(f'{channel_settings} is set for {system_key}.')
        await channel_settings.send(f'This is now a {system_key} channel.')

    async def character(self, channel_settings: Channel, parsed_message: list[str], author: str):
        """
        Creates a character sheet for a player
        """
        try:
            assert channel_settings.system is not None
        except AssertionError:
            await channel_settings.send('Can\'t create character before selecting a roleplaying system.')
            return
        channel_settings.characters[author] = channel_settings.system.character_sheet(parsed_message)
        self._logger.info(f'Created character for {author}.')
        await channel_settings.send(f'{author}, your character is {channel_settings.characters[author].name}')

    async def my_character(self, channel_settings: Channel, parsed_message: list[str], author: str):
        character = channel_settings.characters[author]
        await channel_settings.send(character)

    async def check(self, channel_settings: Channel, parsed_message: list[str], author: str):
        character = channel_settings.characters[author]
        roll = channel_settings.system.check(character, *parsed_message)
        await channel_settings.send(f'You rolled {roll}')

    async def help_str(self, channel_settings: Channel, *_):
        """
        Sends a help message to the requesting channel, containing a list of commands.
        """
        help_str = "List of available commands:\n"
        for command, function in self._commands.items():
            if function:
                help_str += f'{command}: {function.description}\n'
        await channel_settings.send(help_str)
