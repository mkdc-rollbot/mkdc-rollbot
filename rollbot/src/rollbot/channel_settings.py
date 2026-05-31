import discord

class ChannelSettings:
    """
    Encapsulates information on a given discord channel.
    """
    DEFAULT_PREFIX = '~'
    DEFAULT_SYSTEM = None

    def __init__(self, prefix: str, system: str, guild_id: int, channel_id: int):
        self._channel = None
        self.prefix = prefix
        self.system = system
        self.characters = dict()
        self._guild_id = guild_id
        self._channel_id = channel_id

    @staticmethod
    def default_channel(guild_id, channel_id, channel):
        default = ChannelSettings(
                prefix=ChannelSettings.DEFAULT_PREFIX,
                system=ChannelSettings.DEFAULT_SYSTEM,
                guild_id=guild_id,
                channel_id=channel_id,
                )
        return default

    @staticmethod
    def from_db_model(db_channel):
        channel = ChannelSettings(
                prefix=db_channel.prefix,
                system=db_channel.system,
                guild_id=db_channel.guild_id,
                channel_id=db_channel.id,
                )

        return channel

    def set_channel(self, text_channel: discord.TextChannel):
        self._channel = text_channel

    def __repr__(self):
        return f'Channel {self._channel.name} in guild {self._channel.guild.name}'

    def send(self, *args, **kwargs):
        if not self._channel:
            raise ValueError
        return self._channel.send(*args, **kwargs)

    @property
    def id(self):
        return self._channel_id


