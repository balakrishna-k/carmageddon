import py_trees

from scenario_management.scenario_definition.scenarios import scenario as sc


class STATUS:
    RUNNING = py_trees.common.Status.RUNNING
    SUCCESS = py_trees.common.Status.SUCCESS
    INVALID = py_trees.common.Status.INVALID
    FAILURE = py_trees.common.Status.FAILURE


class POLICY:
    SUCCESS_ON_ONE = py_trees.common.ParallelPolicy.SUCCESS_ON_ONE
    SUCCESS_ON_ALL = py_trees.common.ParallelPolicy.SUCCESS_ON_ALL


SCENARIOS = {
    "LVD": sc.LVD
}
