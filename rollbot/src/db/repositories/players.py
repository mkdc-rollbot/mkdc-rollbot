from src.db.models import Player

def get_or_create_player(session, player_id):
    player = session.get(Player, player_id)

    if not player:
        player = Player(id=player_id)
        session.add(player)
    
    return player
