import threading


class Orchestrator(object):
    scenario_tree = None
    ego_vehicle = None
    other_vehicles = None

    def __init__(self, world):
        self._world = world
        self._run_in_parallel = False
        self._thread_lock = threading.Lock()
        world.on_tick(self.update_scenario)

    def setup_scenario(self):
        pass

    def start_scenario(self):
        pass

    def end_scenario(self):
        pass

    def update_scenario(self):
        pass

    def generate_metrics(self):
        pass

    def __generate_scenario_tree(self):
        pass
