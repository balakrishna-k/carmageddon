import scenario_management.constants as ct
from scenario_management.scenario_definition.behaviours.behaviour import BehaviourTemplate
from scenario_management.scenario_manager.tracker import Tracker


class InRegionOfInterest(BehaviourTemplate):

    """
    This class contains the trigger region (conditions) of a scenario
    """

    def __init__(self, vehicle, min_x, max_x, min_y,
                 max_y, name="TriggerRegion"):
        """
            Setup trigger region (rectangle provided by
            [min_x,min_y] and [max_x,max_y]
        """
        super(InRegionOfInterest, self).__init__(name)
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
