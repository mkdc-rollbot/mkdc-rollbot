import discord
import logging

from collections import namedtuple

from src.rollbot.channel_settings import ChannelSettings
from src.rollbot.api_client import APIClient
from src.rollbot.dummy_system import DummySystem

Command = namedtuple('Command', ['description', 'function'])

SYSTEMS = {'dnd5e': None, 'dummy': DummySystem}


def initialize_logger():
    logger = logging.getLogger('discord_client')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s : %(name)s : %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger

class DiscordBot:
    def __init__(self):
        self._logger = initialize_logger()
        self._commands: dict[str: Command] = {
            'prefix': Command(f'Changes assigned prefix. default is {ChannelSettings.DEFAULT_PREFIX}.', self.set_prefix),
            'help': Command('Get available commands.', self.help_str),
            'system': Command(f'Set the roleplaying system for this channel. Available systems are: {"\n\t".join(SYSTEMS.keys())}', self.set_system),
            'character': Command('Create character sheet', self.create_character),
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

        self._discord_client = client
        self._api_client = APIClient()

    async def _handle_message(self, message: discord.Message):
        """
        Handles every received message.
        """
        message_metadata = message.to_message_reference_dict()
        guild_id, channel_id = message_metadata['guild_id'], message_metadata['channel_id']
        channel = await self._validate_channel(guild_id, channel_id, message.channel)
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

    async def _validate_channel(self, guild_id: int, channel_id: int, channel_obj: discord.TextChannel):
        channel_data = await self._api_client.validate_guild_and_channel(guild_id, channel_id)
        channel_settings = ChannelSettings(**channel_data)
        text_channel = self._discord_client.get_channel(channel_id)
        channel_settings.set_channel(text_channel)
        return channel_settings

    def run(self, token):
        """
        Logs rollbot in.
        """
        self._discord_client.run(token)

    async def set_prefix(self, channel_settings: ChannelSettings, parsed_message: list[str], _):
        """
        Changes the message prefix for the given channel.
        """
        prefix = parsed_message[0]
        self._logger.info(f'Changing prefix of {channel_settings} to {prefix}')
        channel_id = str(channel_settings.id)
        # Send channel settings to api client for update
        await self._api_client.update_channel_settings(channel_id, prefix, None)
        await channel_settings.send(f'Changed prefix to {prefix}')

    async def set_system(self, channel_settings: ChannelSettings, parsed_message: list[str], _):
        """
        Sets the roleplaying system for given channel.
        """
        system_key = parsed_message[0]
        if system_key not in SYSTEMS.keys():
            raise ValueError(f'No such system {system_key}')
        channel_settings.system = SYSTEMS[system_key]()
        self._logger.info(f'{channel_settings} is set for {system_key}.')
        # Send channel settings to api client for update
        channel_id = channel_settings.id
        response = await self._api_client.update_channel_settings(channel_id, None, system_key)
        self._logger.info(response)
        await channel_settings.send(f'This is now a {system_key} channel.')

    async def create_character(self, channel_settings: ChannelSettings, parsed_message: list[str], author):
        """
        Creates a character sheet for a player
        """
        try:
            assert channel_settings.system is not None
        except AssertionError:
            await channel_settings.send('Can\'t create character before selecting a roleplaying system.')
            return

        # Have the system module parse the message into a character sheet.
        system = SYSTEMS[channel_settings.system]
        author_id = author.id
        character_sheet, name = system().character_sheet(parsed_message)
        # Commit character to DB
        character_id = await self._api_client.create_character(author_id, name, character_sheet, channel_settings.id)
        await channel_settings.send(f'{author}, your character is {name}')

    async def get_player_character(self, channel_settings, author):
        characters = await self._api_client.get_characters_for_channel(channel_settings.id)
        if not characters or all([len(c) == 0 for c in characters]):
            return None
        author_character = [character for character in characters if character['player'] == author.id][0]
        character = author_character['sheet_data']
        return character


    async def my_character(self, channel_settings: ChannelSettings, parsed_message: list[str], author):
        character = await self.get_player_character(channel_settings, author)
        if not character:
            message = f'You don\'t have a character yet. Create one with `{channel_settings.prefix}character.`'
        else:
            message = character
        await channel_settings.send(message)

    async def check(self, channel_settings: ChannelSettings, parsed_message: list[str], author: str):
        character = self.get_player_character(channel_settings, author)
        system = SYSTEMS[channel_settings.system]
        roll = system().parse(character, *parsed_message)
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
