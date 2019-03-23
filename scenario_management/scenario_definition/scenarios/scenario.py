

class Scenario(object):

    def generate_scenario_behaviour(self):
        raise NotImplementedError("Must implement method to generate behaviour")

    def generate_test_conditions(self):
        raise NotImplementedError("Must implement method to generate test conditions")
