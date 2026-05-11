import discord
import logging

from collections import namedtuple

from src.db.session import SessionLocal
from src.db.models import Channel as ChannelModel
from src.db.repositories.guilds import get_or_create_guild
from src.db.repositories.channels import get_or_create_channel, update_channel_settings
from src.db.repositories.characters import create_character


Command = namedtuple('Command', ['description', 'function'])

SYSTEMS = {'dnd5e': None}


def initialize_logger():
    logger = logging.getLogger('rollbot')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s : %(name)s : %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


class ChannelSettings:
    """
    Encapsulates information on a given discord channel.
    """
    DEFAULT_PREFIX = '~'
    DEFAULT_SYSTEM = None

    def __init__(self, channel: discord.TextChannel, prefix: str, system: str, guild_id: int, channel_id: int):
        self._channel = channel
        self.prefix = prefix
        self.system = system
        self.characters = dict()
        self._guild_id = guild_id
        self._channel_id = channel_id

    @staticmethod
    def default_channel(guild_id, channel_id, channel):
        default = ChannelSettings(
                channel=channel,
                prefix=ChannelSettings.DEFAULT_PREFIX,
                system=ChannelSettings.DEFAULT_SYSTEM,
                guild_id=guild_id,
                channel_id=channel_id,
                )
        return default

    @staticmethod
    def from_db_model(db_channel: ChannelModel, text_channel: discord.TextChannel):
        channel = ChannelSettings(
                channel=text_channel,
                prefix=db_channel.prefix,
                system=db_channel.system,
                guild_id=db_channel.guild_id,
                channel_id=db_channel.id,
                )

        return channel

    def __repr__(self):
        return f'Channel {self._channel.name} in guild {self._channel.guild.name}'

    def send(self, *args, **kwargs):
        return self._channel.send(*args, **kwargs)

    def update(self, session):
        update_channel_settings(session, self._channel_id, self.prefix, self.system)
        session.commit()


class DiscordBot:
    def __init__(self):
        self._logger = initialize_logger()
        self._commands: dict[str: Command] = {
            'prefix': Command(f'Changes assigned prefix. default is {ChannelSettings.DEFAULT_PREFIX}.', self.set_prefix),
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
        channel = self._validate_channel(guild_id, channel_id, message.channel)
        prefix = channel.prefix

        # If message is not a rollbot command, stop message handling.
        if not message.content.startswith(prefix):
            return

        # Handle message
        parsed_message = message.content[len(prefix):].split(' ')
        author = message.author
        command_key = parsed_message.pop(0)
        command = self._commands.get(command_key)
        if not command:
            raise ValueError(f'Unknown command \"{command_key}\"')
        await command.function(channel, parsed_message, author)

    def _validate_channel(self, guild_id: int, channel_id: int, channel_obj: discord.TextChannel):
        with SessionLocal() as session:
            guild = get_or_create_guild(session, guild_id)
            channel_db = get_or_create_channel(session, guild_id, channel_id)
            text_channel = self._client.get_channel(channel_id)
            channel_settings = ChannelSettings.from_db_model(channel_db, text_channel)
            session.commit()
        return channel_settings

    def run(self, token):
        """
        Logs rollbot in.
        """
        self._client.run(token)

    async def set_prefix(self, channel_settings: ChannelSettings, parsed_message: list[str], _):
        """
        Changes the message prefix for the given channel.
        """
        prefix = parsed_message[0]
        self._logger.info(f'Changing prefix of {channel_settings} to {prefix}')
        channel_settings.prefix = prefix
        with SessionLocal() as session:
            channel_settings.update(session)
        await channel_settings.send(f'Changed prefix to {prefix}')

    async def set_system(self, channel_settings: ChannelSettings, parsed_message: list[str], _):
        """
        Sets the roleplaying system for given channel.
        """
        system_key = parsed_message[0]
        channel_settings.system = SYSTEMS[system_key]()
        self._logger.info(f'{channel_settings} is set for {system_key}.')
        with SessionLocal() as session:
            channel_settings.update(session)
        await channel_settings.send(f'This is now a {system_key} channel.')

    async def character(self, channel_settings: ChannelSettings, parsed_message: list[str], author: str):
        """
        Creates a character sheet for a player
        """
        try:
            assert channel_settings.system is not None
        except AssertionError:
            await channel_settings.send('Can\'t create character before selecting a roleplaying system.')
            return

        character_sheet, name = channel_settings.system.character_sheet(parsed_message)
        with SessionLocal() as session:
            create_character(session, author, name, character_sheet)
        self._logger.info(f'Created character for {author}.')
        await channel_settings.send(f'{author}, your character is {name}')

    async def my_character(self, channel_settings: ChannelSettings, parsed_message: list[str], author: str):
        character = channel_settings.characters[author]
        await channel_settings.send(character)

    async def check(self, channel_settings: ChannelSettings, parsed_message: list[str], author: str):
        character = channel_settings.characters[author]
        roll = channel_settings.system.parse(character, *parsed_message)
        await channel_settings.send(f'You rolled {roll}')

    async def help_str(self, channel_settings: ChannelSettings, *_):
        """
        Sends a help message to the requesting channel, containing a list of commands.
        """
        help_str = "List of available commands:\n"
        for command, function in self._commands.items():
            if function:
                help_str += f'{command}: {function.description}\n'
        await channel_settings.send(help_str)
