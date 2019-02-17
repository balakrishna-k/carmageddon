import math

"""
    The Tracker serves to provide ready and convenient access to data about vehicles in the scenario. 
    
    Most of the functions (for now) are akin to wrapper functions. 
    These should be "enhanced" to provide added functionality in the future.
"""


class Tracker(object):

    """
        Tracker consists of static methods to register vehicles to start tracking, constantly update
        the state information corresponding to the following:

            1. Velocity of the vehicle
            2. Location of the vehicle

    """

    vehicle_map = dict()

    @staticmethod
    def track_vehicle(vehicle):
        """
        Add new vehicle to dictionaries
        If vehicle already exists, throw an exception
        """

        init_location = None
        init_velocity = 0.0

        if vehicle in Tracker.vehicle_map:
            pass
        else:
            Tracker.vehicle_map[vehicle] = (init_location, init_velocity)

    @staticmethod
    def track_vehicles(vehicles):
        """
        Add new set of vehicles to dictionaries
        """
        for vehicle in vehicles:
            Tracker.track_vehicle(vehicle)

    @staticmethod
    def on_update():
        """
            Keeps track of changed variables when the time 'ticks'
        """

        for vehicle in Tracker.vehicle_map:
            if vehicle is not None and vehicle.is_alive:
                location = vehicle.get_location()
                velocity = calculate_velocity(vehicle)

                Tracker.vehicle_map[vehicle] = (location, velocity)

    @staticmethod
    def get_velocity(vehicle):
        """
        returns the absolute velocity for the given vehicle
        """
        if vehicle not in Tracker.vehicle_map.keys():
            return 0.0
        else:
            (loc, vel) = Tracker.vehicle_map[vehicle]
            return vel

    @staticmethod
    def get_location(vehicle):
        """
        returns the location for the given vehicle
        """
        if vehicle not in Tracker.vehicle_map.keys():
            return None
        else:
            (loc, vel) = Tracker.vehicle_map[vehicle]
            return loc

    @staticmethod
    def reset():
        """
            Cleanup and remove all entries from all dictionaries
        """
        Tracker.vehicle_map.clear()


def calculate_velocity(vehicle):
    """
    Returns the magnitude of the velocity of the vehicle passed in
    """
    velocity = vehicle.get_velocity()
    sq_velocity = velocity.x**2 + velocity.y**2

    return math.sqrt(sq_velocity)
