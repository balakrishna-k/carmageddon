import scenario_management.constants as ct
import py_trees

from scenario_management.scenario_manager.tracker import Tracker


class InRegion(py_trees.behaviour.Behaviour):

    """
    This class contains the trigger region (tests) of a scenario
    """

    def __init__(self, vehicle, min_x, max_x, min_y,
                 max_y, name="TriggerRegion"):
        """
            Setup trigger region (rectangle provided by
            [min_x,min_y] and [max_x,max_y]
        """
        super(InRegion, self).__init__(name)
        self._vehicle = vehicle
        self._min_x = min_x
        self._max_x = max_x
        self._min_y = min_y
        self._max_y = max_y

    def update(self):
        """
        Check if the _vehicle location is within trigger region
        """
        new_status = ct.STATUS.RUNNING

        location = Tracker.get_location(self._vehicle)

        if location is None:
            return new_status

        not_in_region = (location.x < self._min_x or location.x > self._max_x) or (
            location.y < self._min_y or location.y > self._max_y)
        if not not_in_region:
            new_status = ct.STATUS.SUCCESS

        return new_status


class DistanceToVehicle(py_trees.behaviour.Behaviour):

    """
    This class contains the trigger distance (condition) between to vehicles
    of a scenario
    """

    def __init__(self, other_vehicle, ego_vehicle, distance,
                 name="DistanceToVehicle"):
        """
        Setup trigger distance
        """
        super(DistanceToVehicle, self).__init__(name)
        self._other_vehicle = other_vehicle
        self._ego_vehicle = ego_vehicle
        self._distance = distance

    def update(self):
        """
        Check if the ego vehicle is within trigger distance to other vehicle
        """
        new_status = py_trees.common.Status.RUNNING

        ego_location = Tracker.get_location(self._ego_vehicle)
        other_location = Tracker.get_location(self._other_vehicle)

        if ego_location is None or other_location is None:
            return new_status

        if ego_location.distance(other_location) < self._distance:
            new_status = py_trees.common.Status.SUCCESS

        return new_status

