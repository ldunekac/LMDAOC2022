import re
import networkx as nx
import matplotlib.pyplot as plt
from dataclasses import  dataclass, field
from queue import PriorityQueue
import time

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
    order: tuple = field(compare=False)


def simulate(graph, nodes, potential, node_to_flow):
    nodes = set(nodes)
    node_len = len(nodes)
    max_minutes = 30
    max_potential = max_minutes * potential

    queue = PriorityQueue()
    queue.put(State(0, 0, 0, 0, set(), "AA", ()))
    while True:
        if queue.empty():
            break
        item = queue.get()
        if item.current_step == max_minutes or  len(item.valves_open) == node_len:
            print(item)
            return item.total_pressure_released + potential * (max_minutes - item.current_step)

        for valve_to_open in nodes - item.valves_open:
            steps_to_next_valve = len(nx.shortest_path(graph, source=item.current_loc, target=valve_to_open)) - 1
            if steps_to_next_valve == 0:
                print("NOOOOOOOOO")
                return
            if steps_to_next_valve + item.current_step >= max_minutes:
                steps_walked = max_minutes - item.current_step
                total_pressure_released = item.pressure_being_released * steps_walked + item.total_pressure_released
                new_priority = max_potential - total_pressure_released
                queue.put(
                        State(new_priority, max_minutes, item.pressure_being_released, total_pressure_released, item.valves_open, "", item.order)
                )
            else:
                pressure_released_during_walk_and_turning_on_valve = item.pressure_being_released * (steps_to_next_valve + 1)
                total_pressure_released = item.total_pressure_released + pressure_released_during_walk_and_turning_on_valve
                current_step = item.current_step + steps_to_next_valve + 1
                new_priority = max_potential - total_pressure_released - (max_minutes - current_step)*potential
                valves_open = item.valves_open.copy()
                valves_open.add(valve_to_open)
                queue.put(
                    State(new_priority,
                          current_step,
                          item.pressure_being_released + node_to_flow[valve_to_open],
                          total_pressure_released,
                          valves_open,
                          valve_to_open,
                          item.order + (valve_to_open,))
                )





@dataclass(frozen=True, order=True)
class State2:
    priority: int
    current_step: int
    pressure_being_released: int = field(compare=False)
    total_pressure_released: int = field(compare=False)
    valves_open: set = field(compare=False)
    current_loc: str = field(compare=False)
    elephant_current_loc: str = field(compare=False)
    #order: tuple = field(compare=False)
    you_in_route_to: str = field(compare=False)
    elephant_in_route_to: str = field(compare=False)


def simulateWithElephant(graph, nodes, potential, node_to_flow):
    max_minutes = 26
    nodes = set(nodes)
    node_len = len(nodes)
    max_potential = max_minutes * potential

    queue = PriorityQueue()
    queue.put(State2(0, 0, 0, 0, set(), "AA", "AA", "AA", "AA"))
    while True:
        if queue.empty():
            break
        item = queue.get()
        if item.current_step == max_minutes or  len(item.valves_open) == node_len+1:
            print(item)
            return item.total_pressure_released + potential * (max_minutes - item.current_step + 1)

        you_at_dest_valve = item.current_loc == item.you_in_route_to
        elephant_at_dest_valve = item.elephant_current_loc == item.elephant_in_route_to

        updated_pressure_being_released = item.pressure_being_released
        you_next_pos = item.current_loc
        elephant_next_pos = item.elephant_current_loc
        valves_open = item.valves_open.copy()
        total_pressure_released = item.total_pressure_released + item.pressure_being_released
        if not you_at_dest_valve:
            you_next_pos = nx.shortest_path(graph, source=item.current_loc, target=item.you_in_route_to)[1]
        else:
            if not item.current_loc in valves_open:
                updated_pressure_being_released += node_to_flow[item.current_loc]
                valves_open.add(item.current_loc)

        if not elephant_at_dest_valve:
            elephant_next_pos = nx.shortest_path(graph, source=item.elephant_current_loc, target=item.elephant_in_route_to)[1]
        else:
            if not item.elephant_current_loc in valves_open:
                updated_pressure_being_released += node_to_flow[item.elephant_current_loc]
                valves_open.add(item.elephant_current_loc)

        remaining_valves = nodes - item.valves_open
        if you_at_dest_valve and elephant_at_dest_valve:
            for you_next_valve in remaining_valves:
                for elephant_next_valve in remaining_valves:
                    new_priority = max_potential - total_pressure_released - (max_minutes - item.current_step - 1) * potential
                    queue.put(
                        State2(
                            new_priority,
                            item.current_step + 1,
                            updated_pressure_being_released,
                            total_pressure_released,
                            valves_open,
                            item.current_loc,
                            item.elephant_current_loc,
                            you_next_valve,
                            elephant_next_valve
                        ))
        elif you_at_dest_valve:
            for you_next_valve in remaining_valves:
                new_priority = max_potential - total_pressure_released - (
                            max_minutes - item.current_step - 1) * potential
                queue.put(
                    State2(
                        new_priority,
                        item.current_step + 1,
                        updated_pressure_being_released,
                        total_pressure_released,
                        valves_open,
                        you_next_pos,
                        elephant_next_pos,
                        you_next_valve,
                        item.elephant_in_route_to
                    )
                )
        else:
            for elephant_next_valve in remaining_valves:
                new_priority = max_potential - total_pressure_released - (
                        max_minutes - item.current_step - 1) * potential
                queue.put(
                    State2(
                        new_priority,
                        item.current_step + 1,
                        updated_pressure_being_released,
                        total_pressure_released,
                        valves_open,
                        you_next_pos,
                        elephant_next_pos,
                        item.you_in_route_to,
                        elephant_next_valve
                    )
                )



def simulateWithElephant2(graph, nodes, potential, node_to_flow):
    max_minutes = 30 # TODO change back
    nodes = set(nodes)
    node_len = len(nodes)
    max_potential = max_minutes * potential

    queue = PriorityQueue()
    queue.put(State2(-max_potential, 0, 0, 0, set(), "AA", "AA", "AA", "AA"))
    while True:
        if queue.empty():
            break
        item = queue.get()
        if item.current_step > max_minutes:
            print(item)
            return item.total_pressure_released

        if item.current_step == max_minutes:
            total = item.total_pressure_released + item.pressure_being_released
            new_priority = max_potential - total
            queue.put(
                State2(
                new_priority,
                max_minutes + 1,
                item.pressure_being_released,
                total,
                item.valves_open,
                "",
                "",
                "",
                ""
            ))
            return item.total_pressure_released

        if len(item.valves_open) == node_len:
            assert item.pressure_being_released == potential
            total_pressure_released = item.total_pressure_released +  item.pressure_being_released * (max_minutes - item.current_step)
            assert total_pressure_released < max_potential
            queue.put(State2(
                -total_pressure_released,
                max_minutes,
                item.pressure_being_released,
                total_pressure_released,
                item.valves_open,
                "",
                "",
                "",
                ""
            ))
            continue

        ## Case you and elephant both at stops
        if item.current_loc == item.elephant_current_loc:
            # unlock the valves
            # go one step forward updating the total_pressure_released
            total_pressure_released = item.total_pressure_released + item.pressure_being_released
            assert total_pressure_released < max_potential

            current_open_valves = item.valves_open.copy()
            if item.current_loc in current_open_valves or item.elephant_current_loc in current_open_valves:
                # When we come to an open valve we are not on the optimal path anymore
                continue
            # assert not item.current_loc in current_open_valves
            # assert not item.elephant_current_loc in current_open_valves

            current_open_valves.add(item.current_loc) if not item.current_loc == 'AA' else None
            current_open_valves.add(item.elephant_current_loc) if not item.elephant_current_loc == 'AA' else None

            current_open_pressure = item.pressure_being_released
            if item.current_loc == item.elephant_current_loc:
                current_open_pressure = item.pressure_being_released + node_to_flow[item.current_loc]
                assert current_open_pressure == sum(node_to_flow[x] for x in current_open_valves)
            else:
                current_open_pressure = item.pressure_being_released + node_to_flow[item.current_loc] + node_to_flow[elephant_current_loc]
                assert current_open_pressure == sum(node_to_flow[x] for x in current_open_valves)
            
            valves_remaining = nodes - current_open_valves
            if len(valves_remaining) == 0:
                # No more valves
                assert sum(node_to_flow[x] for x in valves_remaining.union(current_open_valves)) == 81
                new_priority = (-total_pressure_released_after_steps) - ((max_minutes - item.current_step - 1)* potential)
                assert new_priority >= -2106
                queue.put(State2(
                    new_priority,
                    item.current_step+1,
                    current_open_pressure,
                    total_pressure_released,
                    current_open_valves,
                    "",
                    "",
                    "",
                    ""
                ))
            else:
                assert sum(node_to_flow[x] for x in valves_remaining.union(current_open_valves)) == 81
                for you_new_dest in valves_remaining:
                    for elephant_new_dest in valves_remaining:
                        you_path = nx.shortest_path(graph, item.current_loc, you_new_dest)
                        elephant_path = nx.shortest_path(graph, item.elephant_current_loc, elephant_new_dest)
                        num_steps = min(
                            len(you_path) - 1,
                            len(elephant_path) - 1
                        )
                        total_pressure_released_after_steps = total_pressure_released + (num_steps*current_open_pressure)
                        steps_taken = item.current_step + num_steps + 1 # 1 for opening the valve
                        new_priority = (-total_pressure_released_after_steps) - ((max_minutes - steps_taken)* potential)
                        assert new_priority >= -max_potential
                        assert steps_taken <= max_minutes
                        assert total_pressure_released_after_steps <= max_potential
                        queue.put(
                            State2(
                                new_priority,
                                steps_taken,
                                current_open_pressure,
                                total_pressure_released_after_steps,
                                current_open_valves,
                                you_path[num_steps],
                                elephant_path[num_steps],
                                you_path[-1],
                                elephant_path[-1],
                            )
                        )



def simulateWithElephant3(graph, nodes, potential, node_to_flow):
    max_minutes = 26
    nodes = set(nodes)
    node_len = len(nodes)
    max_potential = max_minutes * potential

    queue = PriorityQueue()
    queue.put(State2(0, 0, 0, 0, set(), "AA", "AA", "AA", "AA"))
    count = 0
    max_state = State2(0, 0, 0, 0, set(), "AA", "AA", "AA", "AA")
    while True:
        count += 1
        if queue.empty():
            break
        item = queue.get()
        # if count % 100000 == 0:
        #     print(item)
        if item.current_step == max_minutes:
            print(item)
            return item.total_pressure_released + item.pressure_being_released

        if len(item.valves_open) == node_len+1:
            print(item)
            return item.total_pressure_released + potential * (max_minutes - item.current_step + 1)

        if item.current_step > max_state.current_step and item.pressure_being_released > max_state.pressure_being_released and item.total_pressure_released > max_state.total_pressure_released:
            max_state = item

        if 0 < item.pressure_being_released < max_state.pressure_being_released:
            # if they have a lower rate
            rate_diff = max_state.pressure_being_released - item.pressure_being_released
            toat_diff = max_state.total_pressure_released - item.total_pressure_released
            num_step_diff = toat_diff // rate_diff
            num_step_diff += max_state.current_step - item.current_step
            if num_step_diff >= 3:
                continue

        you_at_dest_valve = item.current_loc == item.you_in_route_to
        elephant_at_dest_valve = item.elephant_current_loc == item.elephant_in_route_to

        updated_pressure_being_released = item.pressure_being_released
        you_next_pos = item.current_loc
        elephant_next_pos = item.elephant_current_loc
        valves_open = item.valves_open.copy()
        total_pressure_released = item.total_pressure_released + item.pressure_being_released
        if not you_at_dest_valve:
            you_next_pos = nx.shortest_path(graph, source=item.current_loc, target=item.you_in_route_to)[1]
        else:
            if not item.current_loc in valves_open:
                updated_pressure_being_released += node_to_flow[item.current_loc]
                valves_open.add(item.current_loc)

        if not elephant_at_dest_valve:
            elephant_next_pos = nx.shortest_path(graph, source=item.elephant_current_loc, target=item.elephant_in_route_to)[1]
        else:
            if not item.elephant_current_loc in valves_open:
                updated_pressure_being_released += node_to_flow[item.elephant_current_loc]
                valves_open.add(item.elephant_current_loc)

        remaining_valves = nodes - item.valves_open
        if you_at_dest_valve and elephant_at_dest_valve:
            pairs = set()
            for you_next_valve in remaining_valves:
                for elephant_next_valve in remaining_valves:
                    if item.current_loc == item.elephant_current_loc:
                        # don't mirror the same path
                        if (you_next_valve, elephant_next_valve) in pairs or (elephant_next_valve, you_next_valve) in pairs:
                            continue
                        pairs.add((you_next_valve, elephant_next_valve))
                        pairs.add((elephant_next_valve, you_next_valve))
                    new_priority = max_potential - total_pressure_released - (max_minutes - item.current_step - 1) * potential
                    queue.put(
                        State2(
                            new_priority,
                            item.current_step + 1,
                            updated_pressure_being_released,
                            total_pressure_released,
                            valves_open,
                            item.current_loc,
                            item.elephant_current_loc,
                            you_next_valve,
                            elephant_next_valve
                        ))
        elif you_at_dest_valve:
            for you_next_valve in remaining_valves:
                new_priority = max_potential - total_pressure_released - (
                            max_minutes - item.current_step - 1) * potential
                queue.put(
                    State2(
                        new_priority,
                        item.current_step + 1,
                        updated_pressure_being_released,
                        total_pressure_released,
                        valves_open,
                        you_next_pos,
                        elephant_next_pos,
                        you_next_valve,
                        item.elephant_in_route_to
                    )
                )
        elif elephant_at_dest_valve:
            for elephant_next_valve in remaining_valves:
                new_priority = max_potential - total_pressure_released - (
                        max_minutes - item.current_step - 1) * potential
                queue.put(
                    State2(
                        new_priority,
                        item.current_step + 1,
                        updated_pressure_being_released,
                        total_pressure_released,
                        valves_open,
                        you_next_pos,
                        elephant_next_pos,
                        item.you_in_route_to,
                        elephant_next_valve
                    )
                )
        else: # No one has reached their goal
            # you_next_steps = nx.shortest_path(graph, source=item.current_loc, target=item.you_in_route_to)
            # elephant_next_steps = nx.shortest_path(graph, source=item.elephant_current_loc, target=item.elephant_in_route_to)
            # steps_to_go = min(
            #     len(you_next_steps) - 1,
            #     len(elephant_next_steps) - 1
            # )
            # total_pressure_released = item.total_pressure_released + (item.pressure_being_released * steps_to_go)
            new_priority = max_potential - total_pressure_released - (
                    max_minutes - item.current_step - 1) * potential
            queue.put(
                State2(
                    new_priority,
                    item.current_step + 1,
                    updated_pressure_being_released,
                    total_pressure_released,
                    valves_open,
                    you_next_pos,
                    elephant_next_pos,
                    item.you_in_route_to,
                    item.elephant_in_route_to
                )
            )




def solution1(file):
    graph, non_zero_nodes, potential, flow_dict = make_graph(file)
    return simulate(graph, non_zero_nodes, potential, flow_dict)
    subax1 = plt.subplot(121)
    nx.draw(graph, with_labels=True)
    plt.show()
    print(graph)


def solution2(file):
    graph, non_zero_nodes, potential, flow_dict = make_graph(file)
    return simulateWithElephant3(graph, non_zero_nodes, potential, flow_dict)


def main():
    ans = solution1("example.txt")
    print(f"Solution 1 for Example is: {ans}")

    ans = solution1("input.txt")
    print(f"Solution 1 for Input is: {ans}")

    ans = solution2("example.txt")
    print(f"Solution 2 for Example is: {ans}")

    start = time.perf_counter()
    ans = solution2("input.txt")
    print(f"Solution 2 for Input is: {ans}")
    end = time.perf_counter()
    print(f"Time elapsed: {end-start}")

if __name__ == "__main__":
    main()
