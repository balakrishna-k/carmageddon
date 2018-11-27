from abc import ABC
from abc import abstractmethod

import carla.libcarla as carla


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
    def parse_events(self, events):
        pass

    @abstractmethod
    def apply_brake(self, events):
        pass

    @abstractmethod
    def apply_hand_brake(self, events):
        pass

    @abstractmethod
    def steer_left(self, events):
        pass

    @abstractmethod
    def steer_right(self, events):
        pass

    @abstractmethod
    def throttle(self, events):
        pass

    @abstractmethod
    def toggle_reverse(self, events):
        pass


