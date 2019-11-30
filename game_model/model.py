from game_model.player import Player

class GameModel:
    
    def __init__(self, players):
        self.players = players
        self.god = Player(10**10, 10**10, health_per_unit_time=10**10, mana_per_unit_time=10**10, name="God", is_god=True)

    def get_god_player(self):
        return self.god

    def add_player(self, player):
        if player not in players:
            self.players.append(player)

    def health_and_resources_restore(self):
        """
        Restores health and resources for every player
        """
        for player in self.players:
            player.restore_health_and_mana(player.health_per_unit_time, player.mana_per_unit_time)
