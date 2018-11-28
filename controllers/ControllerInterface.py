from abc import ABC
from abc import abstractmethod

import carla.libcarla as carla

"""
    1. Abstract Class has implemented methods to tell Carla how to move the car. 
    2. The controller should have to redefine the methods that tell carla when to perform a certain action
"""


class Controller(ABC):

    def __init__(self, start_in_autopilot, world, clock):
        self._autopilot_enabled = start_in_autopilot
        self._control = carla.VehicleControl()
        self._steer_cache = 0.0
        self._world = world
        self._clock = clock
        world.vehicle.set_autopilot(self._autopilot_enabled)
        world.hud.notification("Press 'H' or '?' for help.", seconds=4.0)

    @abstractmethod
    def throttle(self, events):
        pass

    @abstractmethod
    def apply_brake(self, events):
        pass

    @abstractmethod
    def apply_hand_brake(self, events):
        pass

    @abstractmethod
    def steer(self, events):
        pass

    @abstractmethod
    def reverse(self, events):
        pass

    def _throttle_car(self, apply):
        self._control.throttle = 1.0 if apply else 0.0

    def _brake(self, apply):
        self._control.brake = 1.0 if apply or apply else 0.0

    def _hand_brake(self, apply):
        self._control.hand_brake = apply

    def _steer_left(self, apply, milliseconds):
        pass

    def _steer_right(self, apply, milliseconds):
        pass

    def _reverse(self):
        self._control.reverse = not self._control.reverse


