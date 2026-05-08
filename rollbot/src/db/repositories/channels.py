from src.db.models import Channel, Guild

def get_channel(session, channel_id):
    return session.get(Channel, channel_id)


def get_or_create_channel(session, guild_id, channel_id):
    guild = session.get(Guild, guild_id)

    if not guild:
        guild = Guild(id=guild_id)
        session.add(guild)


    channel = get_channel(session, channel_id)

    if not channel:
        channel = Channel(
            id=channel_id,
            guild_id=guild_id,
            prefix="~",
            system=None
        )
        session.add(channel)
        session.commit()

    return channel
