"""
Mykyta S.
pathfinding.py
Contains the methods for path finding for enemies
"""

from functools import total_ordering

# Implements a recursive merge sort (for use in BFS)
def merge_sort(unsorted_list, start=0, end=-1):

    if end == -1:
        end = len(unsorted_list)
    # If the list has only one element return
    if end - start < 2:
        return

    # Sort the two halves
    middle = (start + end) // 2
    merge_sort(unsorted_list, start, middle)
    merge_sort(unsorted_list, middle, end)

    min_1st_half = start
    min_2nd_half = middle

    # Merge the elements together in a new list
    sorted_list = []
    for i in range(start, end):
        if min_2nd_half >= end or \
                (unsorted_list[min_1st_half] <= unsorted_list[min_2nd_half]
                 and min_1st_half < middle):
            sorted_list.append(unsorted_list[min_1st_half])
            min_1st_half += 1
        else:
            sorted_list.append(unsorted_list[min_2nd_half])
            min_2nd_half += 1

    unsorted_list[start:end] = sorted_list
    return

# Implements a method for determining whether a character can go there
def can_pass_through(grid, position, enemy=None, avoid_spikes=False, avoid_switches=False):
    tile = grid.get_tile_at(*position)
    if "wall" in tile.name:
        return False
    if "spikes" in tile.name and (tile.is_armed or avoid_spikes):
        return False
    if "switch" in tile.name and avoid_switches:
        return False
    # Avoid other enemies
    if enemy:
        for e in grid.enemies:
            if e is not enemy and not e.is_dead and \
                    enemy.distance_to(e, position) < 0.7:
                return False
    return True


# Find distance between two positions
def distance_between(a, b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5


# Implements breath first search on the map
def breadth_first_search(grid, start_pos, end_pos, enemy=None):

    # Start from the beginning node
    queue = [Node(0, start_pos)]
    # A set of explored positions
    already_explored = set()
    # A variable for stored path
    found_path = None

    while len(queue) > 0:

        node = queue.pop(0)

        # If the destination was found, break from the loop
        if node.position == end_pos:
            found_path = node
            break

        # Check if it's already explored
        if node.position not in already_explored:

            already_explored.add(node.position)

            for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:

                new_position = direction[0] + node.position[0], \
                               direction[1] + node.position[1]

                # If the new position already explored, ignore it
                if new_position in already_explored:
                    continue

                # If the new position is impassible, ignore it
                if not can_pass_through(grid, new_position, enemy=enemy):
                    already_explored.add(new_position)
                    continue

                # Else go ahead and add it to the list to explore
                new_distance = node.distance + 1
                new_distance += distance_between(new_position, end_pos) * 0.01
                queue.append(Node(new_distance, new_position, node))

            # Sort the queue in order of increasing distance
            merge_sort(queue)

    if found_path is None:
        return None

    # Retrace path and make a list of steps
    path = []
    while found_path is not None:
        path.insert(0, found_path)
        found_path = found_path.previous_node

    return path

# A  class for Breadth First Search
@total_ordering
class Node:

    # Contains the node's distance from the origin, position and
    # the previous node it's connected to
    def __init__(self, distance, position, previous_node=None):
        self.distance = distance
        self.position = position
        self.previous_node = previous_node

    # Defines the comparison methods for sorting
    def __eq__(self, other):
        return self.distance == other.distance

    def __lt__(self, other):
        return self.distance < other.distance

    def __ne__(self, other):
        return self.distance != other.distance
