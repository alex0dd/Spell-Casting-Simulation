class GameModel:
    
    def __init__(self, players):
        self.players = players

    def add_player(self, player):
        if player not in players:
            self.players.append(player)

    def health_and_resources_restore(self):
        """
        Restores health and resources for every player
        """
        for player in self.players:
            player.restore_health_and_mana(player.health_per_unit_time, player.mana_per_unit_time)
