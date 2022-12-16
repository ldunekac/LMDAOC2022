import re
import networkx as nx
import matplotlib.pyplot as plt
from dataclasses import  dataclass, field
from queue import PriorityQueue

def make_graph(file):
    graph = nx.Graph()
    nodes = []
    flow_rates = []
    edges = []
    nodes_to_flow = {}
    with open(file) as f:
        for line in f:
            split_line = re.split(r"alve | has|=|;|, |\n|ves ", line.strip())
            node = split_line[1]
            flow_rate = int(split_line[3])
            paths_to = split_line[5:]
            nodes.append(node)
            flow_rates.append(flow_rate)
            for other_node in paths_to:
                edges.append((node, other_node))

            nodes_to_flow[node] = flow_rate

    graph.add_nodes_from([(n, {"flow_rate": fr}) for n, fr in zip(nodes, flow_rates)])
    graph.add_edges_from(edges)
    non_zero_nodes = [node for node, fl in zip(nodes, flow_rates) if fl > 0]
    return graph, non_zero_nodes, sum(flow_rates), nodes_to_flow

@dataclass(frozen=True, order=True)
class State:
    priority: int
    current_step: int = field(compare=False)
    pressure_being_released: int = field(compare=False)
    total_pressure_released: int = field(compare=False)
    valves_open: set = field(compare=False)
    current_loc: str = field(compare=False)


def simulate(graph, nodes, potential, node_to_flow):
    nodes = set(nodes)
    node_len = len(nodes)
    max_potential = 30 * potential

    queue = PriorityQueue()
    queue.put(State(0, 0, 0, 0, set(), "AA"))
    while True:
        if queue.empty():
            break
        item = queue.get()
        if item.current_step == 30 or  len(item.valves_open) == node_len:
            return item.total_pressure_released + potential * (30 - item.current_step)
        for valve_to_open in nodes - item.valves_open:
            steps_to_next_valve = len(nx.shortest_path(graph, source=item.current_loc, target=valve_to_open)) - 1
            if steps_to_next_valve == 0:
                print("NOOOOOOOOO")
                return
            if steps_to_next_valve + item.current_step >= 30:
                steps_walked = 30 - item.current_step
                total_pressure_released = item.pressure_being_released * steps_walked + item.total_pressure_released
                new_priority = max_potential - total_pressure_released
                queue.put(
                        State(new_priority, 30, item.pressure_being_released, total_pressure_released, item.valves_open, "")
                )
            else:
                pressure_released_during_walk_and_turning_on_valve = item.pressure_being_released * (steps_to_next_valve + 1)
                total_pressure_released = item.total_pressure_released + pressure_released_during_walk_and_turning_on_valve
                current_step = item.current_step + steps_to_next_valve + 1
                new_priority = max_potential - total_pressure_released - (30 - current_step)*potential
                valves_open = item.valves_open.copy()
                valves_open.add(valve_to_open)
                queue.put(
                    State(new_priority,
                          current_step,
                          item.pressure_being_released + node_to_flow[valve_to_open],
                          total_pressure_released,
                          valves_open,
                          valve_to_open)
                )



def solution1(file):
    graph, non_zero_nodes, potential, flow_dict = make_graph(file)
    return simulate(graph, non_zero_nodes, potential, flow_dict)
    # subax1 = plt.subplot(121)
    # nx.draw(graph, with_labels=True)
    # plt.show()
    # print(graph)


def main():
    ans = solution1("example.txt")
    print(f"Solution 1 for Example is: {ans}")
    ans = solution1("input.txt")
    print(f"Solution 1 for Input is: {ans}")

    # ans = solution2("example.txt", 20)
    # print(f"Solution 2 for Example is: {ans}")
    # ans = solution2("input.txt", 4000000)
    # print(f"Solution 2 for Input is: {ans}")


if __name__ == "__main__":
    main()
