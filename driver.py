import logging
import typing
from types import ModuleType

import pandas as pd

from . import graph

logger = logging.getLogger(__name__)


class Driver(object):
    def __init__(self, module: ModuleType):
        self.graph = graph.FunctionGraph(module)

    def validate_inputs(self, user_nodes: typing.Collection[graph.Node], inputs: typing.Dict[str, typing.Any]):
        """Validates that inputs meet our expectations.

        :param user_nodes: The required nodes we need for computation.
        :param inputs: the user inputs provided.
        """
        # validate inputs
        for user_node in user_nodes:
            if user_node.name not in inputs:
                raise ValueError(f'Error: Required input {user_node.name} not provided.')
            elif not isinstance(inputs[user_node.name], user_node.type):
                raise ValueError(f'Error: Type requirement mistmatch. Expected {user_node.name}:{user_node.type} '
                                 f'got {inputs[user_node.name]} instead.')

    def execute(self, final_vars: typing.List[str],
                inputs: typing.Dict[str, typing.Any],
                display_graph: bool = False) -> pd.DataFrame:
        """Executes computation.

        :param final_vars: the final list of variables we want in the data frame.
        :param inputs: the user defined input variables.
        :param display_graph: whether we want to display the graph being computed.
        :return: a data frame consisting of the variables requested.
        """
        nodes, user_nodes = self.graph.get_required_functions(final_vars)
        self.validate_inputs(user_nodes, inputs)
        if display_graph:
            # TODO: fix path.
            self.graph.display(output_file_path='test-output/execute.gv')

        memoized_computation = dict()  # memoized storage
        self.graph.execute(nodes, inputs, memoized_computation)
        columns = {c: memoized_computation[c] for c in final_vars}  # only want request variables in df.
        del memoized_computation  # trying to cleanup some memory
        # TODO: figure out how to fill in columns?
        # TODO: if we have dataframes as computations, we will likely have to skip them (cause we want identity functions
        #  to be used off of them) or do some special combining logic.
        return pd.DataFrame(columns)

    def list_available_variables(self) -> typing.List[str]:
        """Returns available variables.

        :return: list of available variables.
        """
        return [node.name for node in self.graph.get_nodes()]

    def display_all_functions(self):
        """Displays the graph."""
        self.graph.display()


if __name__ == '__main__':
    import sys

    formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(name)s(%(lineno)s): %(message)s')
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)
    # df = execute(['D_SHIFT_FUNC', 'D_TWO_WEEKS_BEFORE_HALLOWEEN'], {'DATE': x.to_series(), 'RANDOM': 4})
    x = pd.date_range('2019-01-05', '2020-12-31', freq='7D')  # TODO figure out saturday to start from.
    x.index = x
    # df = execute(['D_THANKSGIVING'], {'DATE': x.to_series(), 'RANDOM': 4}, display_graph=True)
    # print(df)
    df = execute(['DATE', 'M_DISPLAY_SPEND_TF', 'D_WEEK_AFTER_MOTHERSDAY'],
                 {'DATE': x.to_series(), 'VERSION': 'womens', 'AS_OF': '2019-06-01'},
                 display_graph=True)
    print(df)
