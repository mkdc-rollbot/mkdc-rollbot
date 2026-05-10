from src.db.models import Guild

def get_or_create_guild(session, guild_id):
    guild = session.get(Guild, guild_id)
    
    if not guild:
        guild = Guild(id=guild_id)

        session.add(guild)

    return guild

