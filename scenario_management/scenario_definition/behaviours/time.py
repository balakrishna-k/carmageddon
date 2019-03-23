import py_trees
from scenario_management.scenario_manager.tracker import Tracker

TOLERANCE = 0.001


class InTimeToArrivalToLocation(py_trees.behaviour.Behaviour):

    """
    This class contains a check if a vehicle arrives within a given time
    at a given location.
    """

    _max_time_to_arrival = float('inf')  # time to arrival in seconds

    def __init__(self, vehicle, time, location, name="TimeToArrival"):
        """
        Setup parameters
        """
        super(InTimeToArrivalToLocation, self).__init__(name)
        self.logger.debug("%s.__init__()" % (self.__class__.__name__))
        self._vehicle = vehicle
        self._time = time
        self._target_location = location

    def update(self):
        """
        Check if the vehicle can arrive at target_location within time
        """
        new_status = py_trees.common.Status.RUNNING

        current_location = Tracker.get_location(self._vehicle)

        if current_location is None:
            return new_status

        distance = current_location.distance(self._target_location)
        velocity = Tracker.get_velocity(self._vehicle)

        # if velocity is too small, simply use a large time to arrival
        time_to_arrival = self._max_time_to_arrival
        if velocity > TOLERANCE:
            time_to_arrival = distance / velocity

        if time_to_arrival < self._time:
            new_status = py_trees.common.Status.SUCCESS

        self.logger.debug("%s.update()[%s->%s]" %
                          (self.__class__.__name__, self.status, new_status))

        return new_status

