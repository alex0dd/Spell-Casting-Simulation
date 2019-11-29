from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
import os

from game_model import player, ability
from game_model.model import GameModel
import game_events.game_events as events
from game_events.game_event_emitters import AbilityCastEventEmitter
from simulation.simulation import DiscreteEventsSimulation
from game_visualizers.textual_visualizer import TextualVisualizer
import random as random


frost_bolt_spell = ability.DamagingAbility(100, 200, cast_time=5, name="Frost Bolt")
melee_attack_ability = ability.DamagingAbility(50, 1, cast_time=1, name="Melee Attack")

player_1_abilities = [frost_bolt_spell]
boss_abilities = [melee_attack_ability]

player_1 = player.Player(500, 1000, abilities=player_1_abilities, health_per_unit_time=1, mana_per_unit_time=1, name="Alex", game_class="Mage")
boss_player = player.Player(1000, 100, abilities=boss_abilities, name="Boss", game_class="Warrior")

players_list = [player_1]
enemies_list = [boss_player]

game_model = GameModel(players_list+enemies_list)

player_1_cast_emitter = AbilityCastEventEmitter(player_1)
boss_cast_emitter = AbilityCastEventEmitter(boss_player)

game_simulation = DiscreteEventsSimulation(
    game_model, 
    event_emitters=[
        player_1_cast_emitter, boss_cast_emitter
    ], 
    visualizers=[TextualVisualizer()]
)

# manually dispatch some events
# dispatch initial event that starts health and resources restoration for everyone
game_simulation.event_queue.dispatch_event(events.EveryoneRestoreHealthAndResources(game_model), 0)
game_simulation.event_queue.dispatch_event(events.AbilityCastStarted(player_1, {"ability": frost_bolt_spell, "target": boss_player}), 2)
game_simulation.event_queue.dispatch_event(events.AbilityCastStarted(boss_player, {"ability": melee_attack_ability, "target": player_1}), 2)
game_simulation.event_queue.dispatch_event(events.AbilityCastStarted(player_1, {"ability": frost_bolt_spell, "target": boss_player}), 4)

class SimulationWindow(QMainWindow):
    
    def __init__(self, simulation, simulation_speed=1000, *args, **kwargs):
        """
        simulation: simulation object
        simulation_speed: milliseconds corresponding to one game tick
        """
        super(SimulationWindow, self).__init__(*args, **kwargs)

        self.simulation = simulation
        self.model = self.simulation.model
        self.simulation_speed = simulation_speed

        self.init_functionality(simulation_speed)
        self.init_ui()




        #layout = QHBoxLayout()

        #for n in range(10):
        #    btn = QPushButton(str(n))
        #    btn.pressed.connect(lambda n=n: print(n))
        #    layout.addWidget(btn)

    def init_functionality(self, simulation_speed):
        self.timer = QTimer()
        self.timer.timeout.connect(self.simulator_tick)
        self.timer.start(simulation_speed)

    def init_ui(self):
        self.setWindowTitle("Application")

        # layout
        layout = QVBoxLayout()

        # components
        self.simulation_time_label = QLabel()
        layout.addWidget(self.simulation_time_label)

        # players heal buttons
        self.player_heal_buttons = []
        for player in self.model.players:
            player_heal_button = QPushButton()
            self.player_heal_buttons.append(player_heal_button)
            layout.addWidget(player_heal_button)

        
        
        # widget
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.setBaseSize(400, 200)

    def _update_player_health_buttons(self):
        for player_heal_button, player in zip(
            self.player_heal_buttons, self.model.players
        ):
            player_heal_button.setText("{}\n{}/{}".format(player.name, player.health, player.max_health))

    def simulator_tick(self):
        self.simulation_time_label.setText(
            "Current simulation time: {}".format(self.simulation.current_time)
        )
        self._update_player_health_buttons()
        # step forward into the simulation
        game_simulation.step()

app = QApplication(sys.argv)

window = SimulationWindow(game_simulation, simulation_speed=500)
window.show()

app.exec_()