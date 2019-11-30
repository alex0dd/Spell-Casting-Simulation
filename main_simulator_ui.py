from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
import os
import random as random

from game_model import player, ability
from game_model.model import GameModel
import game_events.game_events as events
from game_events.game_event_emitters import AbilityCastEventEmitter, EveryoneRestoreEventEmitter
from simulation.simulation import DiscreteEventsSimulation
from game_visualizers.textual_visualizer import TextualVisualizer
from game_utils.utils import load_abilities

abilities = load_abilities('game_data/abilities_db.json')
print(abilities)

player_1_abilities = [abilities[1]]
boss_abilities = [abilities[2]]

player_1 = player.Player(500, 1000, abilities=player_1_abilities, health_per_unit_time=1, mana_per_unit_time=1, name="Alex", game_class="Mage")
boss_player = player.Player(1000, 100, abilities=boss_abilities, name="Boss", game_class="Warrior")

players_list = [player_1]
enemies_list = [boss_player]

game_model = GameModel(players_list+enemies_list)

everyone_restore_emitter = EveryoneRestoreEventEmitter(game_model)
player_1_cast_emitter = AbilityCastEventEmitter(player_1)
boss_cast_emitter = AbilityCastEventEmitter(boss_player)

game_simulation = DiscreteEventsSimulation(
    game_model, 
    event_emitters=[
        everyone_restore_emitter, player_1_cast_emitter, boss_cast_emitter
    ], 
    visualizers=[TextualVisualizer()]
)

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
        self.player_health_bars = []
        for player in self.model.players:
            player_heal_button = QPushButton()
            player_health_bar = QProgressBar()
            player_heal_button.pressed.connect(lambda player=player: self.send_heal(player))
            self.player_health_bars.append(player_health_bar)
            self.player_heal_buttons.append(player_heal_button)
            layout.addWidget(player_health_bar)
            layout.addWidget(player_heal_button)

        
        
        # widget
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.setBaseSize(400, 200)

    def _update_player_health_buttons(self):
        for player_heal_button, player_health_bar, player in zip(
            self.player_heal_buttons, self.player_health_bars, self.model.players
        ):
            if player.health > 0:
                current_health_percentage = int((player.health / player.max_health) * 100)
                # update bar
                player_health_bar.setFormat("%p%")
                player_health_bar.setValue(current_health_percentage)
                # update button
                player_heal_button.setText("{}\n{}/{}".format(player.name, player.health, player.max_health))
            else:
                player_health_bar.setFormat("Dead")
                player_health_bar.setValue(0)
                player_heal_button.setText("{}\nDead".format(player.name))

    def send_heal(self, player):
        self.simulation.dispatch_event(events.AbilityCastStarted(self.model.god, {"target": player, "ability": abilities[3]}))

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