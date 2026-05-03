from db.models import Channel

def get_channel(session, channel_id):
    return session.get(Channel, channel_id)
