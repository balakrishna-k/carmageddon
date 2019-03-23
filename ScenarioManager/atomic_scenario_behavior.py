import py_trees
import carla

from ScenarioManager.carla_data_provider import CarlaDataProvider

TOLERANCE = 0.001


class AtomicBehavior(py_trees.behaviour.Behaviour):

    """
    Base class for all atomic behaviors used to setup a scenario

    Important parameters:
    - name: Name of the atomic behavior
    """

    def __init__(self, name):
        super(AtomicBehavior, self).__init__(name)
        self.name = name

    def setup(self, unused_timeout=15):
        return True

    def initialise(self):
        pass

    def terminate(self, new_status):
        pass


class InTriggerDistanceToVehicle(AtomicBehavior):

    """
    This class contains the trigger distance (condition) between to vehicles
    of a scenario
    """

    def __init__(self, other_vehicle, ego_vehicle, distance,
                 name="TriggerDistanceToVehicle"):
        """
        Setup trigger distance
        """
        super(InTriggerDistanceToVehicle, self).__init__(name)
        self._other_vehicle = other_vehicle
        self._ego_vehicle = ego_vehicle
        self._distance = distance

    def update(self):
        """
        Check if the ego vehicle is within trigger distance to other vehicle
        """
        new_status = py_trees.common.Status.RUNNING

        ego_location = CarlaDataProvider.get_location(self._ego_vehicle)
        other_location = CarlaDataProvider.get_location(self._other_vehicle)

        if ego_location is None or other_location is None:
            return new_status

        if calculate_distance(ego_location, other_location) < self._distance:
            new_status = py_trees.common.Status.SUCCESS

        return new_status


class TriggerVelocity(AtomicBehavior):

    """
    This class contains the trigger velocity (condition) of a scenario
    """

    def __init__(self, vehicle, target_velocity, name="TriggerVelocity"):
        """
        Setup trigger velocity
        """
        super(TriggerVelocity, self).__init__(name)

        self._vehicle = vehicle
        self._target_velocity = target_velocity

    def update(self):
        """
        Check if the vehicle has the trigger velocity
        """
        new_status = py_trees.common.Status.RUNNING

        delta_velocity = CarlaDataProvider.get_velocity(
            self._vehicle) - self._target_velocity

        if delta_velocity < TOLERANCE:
            new_status = py_trees.common.Status.SUCCESS

        return new_status


class InTimeToArrivalToLocation(AtomicBehavior):

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

        self._vehicle = vehicle
        self._time = time
        self._target_location = location

    def update(self):
        """
        Check if the vehicle can arrive at target_location within time
        """
        new_status = py_trees.common.Status.RUNNING

        current_location = CarlaDataProvider.get_location(self._vehicle)

        if current_location is None:
            return new_status

        distance = calculate_distance(current_location, self._target_location)
        velocity = CarlaDataProvider.get_velocity(self._vehicle)

        # if velocity is too small, simply use a large time to arrival
        time_to_arrival = self._max_time_to_arrival
        if velocity > TOLERANCE:
            time_to_arrival = distance / velocity

        if time_to_arrival < self._time:
            new_status = py_trees.common.Status.SUCCESS

        return new_status


class KeepVelocity(AtomicBehavior):

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
        self._control = carla.VehicleControl()
        self._vehicle = vehicle
        self._target_velocity = target_velocity

        self._control.steering = 0

    def update(self):
        """
        Set throttle to throttle_value, as long as velocity is < target_velocity
        """
        new_status = py_trees.common.Status.RUNNING

        if CarlaDataProvider.get_velocity(
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


class DriveDistance(AtomicBehavior):

    """
    This class contains an atomic behavior to drive a certain distance.
    """

    def __init__(self, vehicle, distance, name="DriveDistance"):
        """
        Setup parameters
        """
        super(DriveDistance, self).__init__(name)

        self._target_distance = distance
        self._distance = 0
        self._location = None
        self._vehicle = vehicle

    def initialise(self):
        self._location = CarlaDataProvider.get_location(self._vehicle)
        super(DriveDistance, self).initialise()

    def update(self):
        """
        Check driven distance
        """
        new_status = py_trees.common.Status.RUNNING

        new_location = CarlaDataProvider.get_location(self._vehicle)
        self._distance += calculate_distance(self._location, new_location)
        self._location = new_location

        if self._distance > self._target_distance:
            new_status = py_trees.common.Status.SUCCESS

        return new_status


class StopVehicle(AtomicBehavior):

    """
    This class contains an atomic stopping behavior. The controlled traffic
    participant will decelerate with _bake_value_ until reaching a full stop.
    """

    def __init__(self, vehicle, brake_value, name="Stopping"):
        """
        Setup _vehicle and maximum braking value
        """
        super(StopVehicle, self).__init__(name)

        self._control = carla.VehicleControl()
        self._vehicle = vehicle
        self._brake_value = brake_value

        self._control.steering = 0

    def update(self):
        """
        Set brake to brake_value until reaching full stop
        """
        new_status = py_trees.common.Status.RUNNING

        if CarlaDataProvider.get_velocity(self._vehicle) > TOLERANCE:
            self._control.brake = self._brake_value
        else:
            new_status = py_trees.common.Status.SUCCESS
            self._control.brake = 0

        self._vehicle.apply_control(self._control)

        return new_status

def calculate_distance(location, other_location):
    return location.distance(other_location)

