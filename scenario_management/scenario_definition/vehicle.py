import sys
import random

import carla
from scenario_management.scenario_manager.tracker import Tracker


class Vehicle(object):
    _world = None
    _vehicle_model = None
    _spawn_point = None
    _type = None
    _vehicle = None

    def __init__(self, world, model, spawn_point):
        self._world = world
        self._vehicle_model = model
        self._spawn_point = spawn_point

    def spawn(self):
        blueprints = self._world.get_blueprint_library()

        # If you give it the exact name, then obviously not going to be a random selection
        blueprint = random.choice(blueprints.filter(self._vehicle_model))
        blueprint.set_attribute('role_name', self._type)

        location = carla.Location(x=self._spawn_point.x, y=self._spawn_point.y, z=self._spawn_point.z)
        self._spawn_point = carla.Transform(location, carla.Rotation(yaw=0))

        vehicle = self._world.try_spawn_actor(blueprint, self._spawn_point)

        if vehicle is None:
            sys.exit("Cannot spawn {} at {}".format(self._vehicle_model, self._spawn_point))

        vehicle.set_autopilot(False)

        _vehicle = vehicle
        Tracker.track_vehicle(vehicle)

        return vehicle


class EgoVehicle(Vehicle):
    _type = 'hero'

    def __init__(self, world, model, spawn_point):
        super(EgoVehicle, self).__init__(world, model, spawn_point)


class OtherVehicle(Vehicle):
    _type = 'scenario'

    def __init__(self, world, model, spawn_point):
        super(OtherVehicle, self).__init__(world, model, spawn_point)

