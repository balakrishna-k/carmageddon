import carla
import py_trees

from scenario_management.scenario_manager.tracker import Tracker

TOLERANCE = 0.001


class CheckVelocity(py_trees.behaviour.Behaviour):

    """
    This class contains the trigger velocity (condition) of a scenario
    """

    def __init__(self, vehicle, target_velocity, name="CheckVelocity"):
        """
        Setup trigger velocity
        """
        super(CheckVelocity, self).__init__(name)
        self._vehicle = vehicle
        self._target_velocity = target_velocity

    def update(self):
        """
        Check if the vehicle has the trigger velocity
        """
        new_status = py_trees.common.Status.RUNNING

        delta_velocity = Tracker.get_velocity(
            self._vehicle) - self._target_velocity
        if delta_velocity < TOLERANCE:
            new_status = py_trees.common.Status.SUCCESS

        return new_status
