import carla
import py_trees

from scenario_management.scenario_manager.tracker import Tracker

TOLERANCE = 0.001


class VehicleBehaviour(py_trees.behaviour.Behaviour):
    _control = carla.VehicleControl()
    _vehicle = None

    def __init__(self, name):
        super(VehicleBehaviour, self).__init__(name)


class StopVehicle(VehicleBehaviour):

    """
    This class contains an atomic stopping behavior. The controlled traffic
    participant will decelerate with _bake_value_ until reaching a full stop.
    """

    def __init__(self, vehicle, brake_value, name="Stopping"):
        """
        Setup _vehicle and maximum braking value
        """
        super(StopVehicle, self).__init__(name)
        self._vehicle = vehicle
        self._brake_value = brake_value

        self._control.steering = 0

    def update(self):
        """
        Set brake to brake_value until reaching full stop
        """
        new_status = py_trees.common.Status.RUNNING

        if Tracker.get_velocity(self._vehicle) > TOLERANCE:
            self._control.brake = self._brake_value
        else:
            new_status = py_trees.common.Status.SUCCESS
            self._control.brake = 0

        self._vehicle.apply_control(self._control)

        return new_status


class DrivenDistance(py_trees.behaviour.Behaviour):

    """
    This class contains an atomic behavior to drive a certain distance.
    """

    def __init__(self, vehicle, distance, name="CheckDrivenDistance"):
        """
        Setup parameters
        """
        super(DrivenDistance, self).__init__(name)
        self._target_distance = distance
        self._distance = 0
        self._location = None
        self._vehicle = vehicle

    def initialise(self):
        self._location = Tracker.get_location(self._vehicle)
        super(DrivenDistance, self).initialise()

    def update(self):
        """
        Check driven distance
        """
        new_status = py_trees.common.Status.RUNNING

        new_location = Tracker.get_location(self._vehicle)
        self._distance += self._location.distance(new_location)
        self._location = new_location

        if self._distance > self._target_distance:
            new_status = py_trees.common.Status.SUCCESS

        return new_status


class KeepVelocity(VehicleBehaviour):

    """
    This class contains an atomic behavior to keep the provided velocity.
    The controlled traffic participant will accelerate as fast as possible
    until reaching a given _target_velocity_, which is then maintained for
    as long as this behavior is active.

    Note: In parallel to this behavior a termination behavior has to be used
          to keep the velocity either for a certain duration, or for a certain
          distance, etc.
    """

    def __init__(self, vehicle, target_velocity, name="KeepVelocity"):
        """
        Setup parameters including acceleration value (via throttle_value)
        and target velocity
        """
        super(KeepVelocity, self).__init__(name)
        self._vehicle = vehicle
        self._target_velocity = target_velocity

        self._control.steering = 0

    def update(self):
        """
        Set throttle to throttle_value, as long as velocity is < target_velocity
        """
        new_status = py_trees.common.Status.RUNNING

        if Tracker.get_velocity(
                self._vehicle) < self._target_velocity:
            self._control.throttle = 1.0
        else:
            self._control.throttle = 0.0

        self._vehicle.apply_control(self._control)

        return new_status

    def terminate(self, new_status):
        """
        On termination of this behavior, the throttle should be set back to 0.,
        to avoid further acceleration.
        """
        self._control.throttle = 0.0
        self._vehicle.apply_control(self._control)
        super(KeepVelocity, self).terminate(new_status)

