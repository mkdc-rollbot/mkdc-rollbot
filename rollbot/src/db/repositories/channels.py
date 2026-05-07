from db.models import Channel

def get_channel(session, channel_id):
    return session.get(Channel, channel_id)


def get_or_create_channel(session, guild_id, channel_id):
    channel = get_channel(session, channel_id)

    if not channel:
        channel = ChannelModel(
            id=channel_id,
            guild_id=guild_id,
            prefix="~",
            system=None
        )
        session.add(channel)
        session.commit()

    return channel
