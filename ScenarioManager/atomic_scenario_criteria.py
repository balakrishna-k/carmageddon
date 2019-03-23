import weakref

import py_trees
import carla

from ScenarioManager.carla_data_provider import CarlaDataProvider
from ScenarioManager.timer import GameTime


class Criterion(py_trees.behaviour.Behaviour):
    def __init__(self,
                 name,
                 vehicle,
                 expected_value_success,
                 expected_value_acceptable=None,
                 optional=False):
        super(Criterion, self).__init__(name)
        self._terminate_on_failure = False

        self.name = name
        self.vehicle = vehicle
        self.test_status = "INIT"
        self.expected_value_success = expected_value_success
        self.expected_value_acceptable = expected_value_acceptable
        self.actual_value = 0
        self.optional = optional

class MaxVelocityTest(Criterion):

    """
    This class contains an atomic test for maximum velocity.
    """

    def __init__(self, vehicle, max_velocity_allowed, optional=False, name="CheckMaximumVelocity"):
        """
        Setup vehicle and maximum allowed velovity
        """
        super(MaxVelocityTest, self).__init__(
            name, vehicle, max_velocity_allowed, None, optional)

    def update(self):
        """
        Check velocity
        """
        new_status = py_trees.common.Status.RUNNING

        if self.vehicle is None:
            return new_status

        velocity = CarlaDataProvider.get_velocity(self.vehicle)

        self.actual_value = max(velocity, self.actual_value)

        if velocity > self.expected_value_success:
            self.test_status = "FAILURE"
        else:
            self.test_status = "SUCCESS"

        if self._terminate_on_failure and (self.test_status == "FAILURE"):
            new_status = py_trees.common.Status.FAILURE

        return new_status


class DrivenDistanceTest(Criterion):

    """
    This class contains an atomic test to check the driven distance
    """

    def __init__(self,
                 vehicle,
                 distance_success,
                 distance_acceptable=None,
                 optional=False,
                 name="CheckDrivenDistance"):
        """
        Setup vehicle
        """
        super(DrivenDistanceTest, self).__init__(
            name, vehicle, distance_success, distance_acceptable, optional)
        self._last_location = None

    def initialise(self):
        self._last_location = CarlaDataProvider.get_location(self.vehicle)
        super(DrivenDistanceTest, self).initialise()

    def update(self):
        """
        Check distance
        """
        new_status = py_trees.common.Status.RUNNING

        if self.vehicle is None:
            return new_status

        location = CarlaDataProvider.get_location(self.vehicle)

        if location is None:
            return new_status

        if self._last_location is None:
            self._last_location = location
            return new_status

        self.actual_value += location.distance(self._last_location)
        self._last_location = location

        if self.actual_value > self.expected_value_success:
            self.test_status = "SUCCESS"
        elif (self.expected_value_acceptable is not None and
              self.actual_value > self.expected_value_acceptable):
            self.test_status = "ACCEPTABLE"
        else:
            self.test_status = "RUNNING"

        if self._terminate_on_failure and (self.test_status == "FAILURE"):
            new_status = py_trees.common.Status.FAILURE

        return new_status


class AverageVelocityTest(Criterion):

    """
    This class contains an atomic test for average velocity.
    """

    def __init__(self,
                 vehicle,
                 avg_velocity_success,
                 avg_velocity_acceptable=None,
                 optional=False,
                 name="CheckAverageVelocity"):
        """
        Setup vehicle and average velovity expected
        """
        super(AverageVelocityTest, self).__init__(name, vehicle,
                                                  avg_velocity_success,
                                                  avg_velocity_acceptable,
                                                  optional)
        self._last_location = None
        self._distance = 0.0

    def initialise(self):
        self._last_location = CarlaDataProvider.get_location(self.vehicle)
        super(AverageVelocityTest, self).initialise()

    def update(self):
        """
        Check velocity
        """
        new_status = py_trees.common.Status.RUNNING

        if self.vehicle is None:
            return new_status

        location = CarlaDataProvider.get_location(self.vehicle)

        if location is None:
            return new_status

        if self._last_location is None:
            self._last_location = location
            return new_status

        self._distance += location.distance(self._last_location)
        self._last_location = location

        elapsed_time = GameTime.get_time()
        if elapsed_time > 0.0:
            self.actual_value = self._distance / elapsed_time

        if self.actual_value > self.expected_value_success:
            self.test_status = "SUCCESS"
        elif (self.expected_value_acceptable is not None and
              self.actual_value > self.expected_value_acceptable):
            self.test_status = "ACCEPTABLE"
        else:
            self.test_status = "RUNNING"

        if self._terminate_on_failure and (self.test_status == "FAILURE"):
            new_status = py_trees.common.Status.FAILURE

        return new_status


class CollisionTest(Criterion):

    """
    This class contains an atomic test for collisions.
    """

    def __init__(self, vehicle, optional=False, name="CheckCollisions"):
        """
        Construction with sensor setup
        """
        super(CollisionTest, self).__init__(name, vehicle, 0, None, optional)

        world = self.vehicle.get_world()
        blueprint = world.get_blueprint_library().find('sensor.other.collision')
        self._collision_sensor = world.spawn_actor(
            blueprint, carla.Transform(), attach_to=self.vehicle)
        self._collision_sensor.listen(
            lambda event: self._count_collisions(weakref.ref(self), event))

    def update(self):
        """
        Check collision count
        """
        new_status = py_trees.common.Status.RUNNING

        if self.actual_value > 0:
            self.test_status = "FAILURE"
        else:
            self.test_status = "SUCCESS"

        if self._terminate_on_failure and (self.test_status == "FAILURE"):
            new_status = py_trees.common.Status.FAILURE

        return new_status

    def terminate(self, new_status):
        """
        Cleanup sensor
        """
        if self._collision_sensor is not None:
            self._collision_sensor.destroy()
        self._collision_sensor = None
        super(CollisionTest, self).terminate(new_status)

    @staticmethod
    def _count_collisions(weak_self, event):
        """
        Callback to update collision count
        """
        self = weak_self()
        if not self:
            return
        self.actual_value += 1


class KeepLaneTest(Criterion):

    """
    This class contains an atomic test for keeping lane.
    """

    def __init__(self, vehicle, optional=False, name="CheckKeepLane"):
        """
        Construction with sensor setup
        """
        super(KeepLaneTest, self).__init__(name, vehicle, 0, None, optional)

        world = self.vehicle.get_world()
        blueprint = world.get_blueprint_library().find(
            'sensor.other.lane_detector')
        self._lane_sensor = world.spawn_actor(
            blueprint, carla.Transform(), attach_to=self.vehicle)
        self._lane_sensor.listen(
            lambda event: self._count_lane_invasion(weakref.ref(self), event))

    def update(self):
        """
        Check lane invasion count
        """
        new_status = py_trees.common.Status.RUNNING

        if self.actual_value > 0:
            self.test_status = "FAILURE"
        else:
            self.test_status = "SUCCESS"

        if self._terminate_on_failure and (self.test_status == "FAILURE"):
            new_status = py_trees.common.Status.FAILURE

        return new_status

    def terminate(self, new_status):
        """
        Cleanup sensor
        """
        if self._lane_sensor is not None:
            self._lane_sensor.destroy()
        self._lane_sensor = None
        super(KeepLaneTest, self).terminate(new_status)

    @staticmethod
    def _count_lane_invasion(weak_self, event):
        """
        Callback to update lane invasion count
        """
        self = weak_self()
        if not self:
            return
        self.actual_value += 1
