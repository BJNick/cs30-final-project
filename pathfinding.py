"""
Mykyta S.
pathfinding.py

A module that contains functions for path finding (for enemies). The grid is
represented as a graph with empty tiles connected to one another.
BFSNode is used by the breadth first search algorithm to store node data.
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


# Implements a quick binary search for checking if the element is in the list
# Returns a tuple whether the value is found, index where it could be placed in
def binary_search(sorted_list, value):
    # If the list is empty return -1
    if len(sorted_list) == 0:
        return False, 0
    # If the only number is not the result return -1
    if len(sorted_list) == 1:
        return value == sorted_list[0], (1 if value >= sorted_list[0] else 0)

    # Split in the middle
    middle = len(sorted_list) // 2
    if sorted_list[middle] == value:
        return True, middle

    # Search in either half
    if sorted_list[middle] > value:
        result, sub_index = binary_search(sorted_list[:middle], value)
    else:
        result, index = binary_search(sorted_list[middle:], value)
        sub_index = index + middle

    return result, sub_index


# Implements a method for determining whether a character can go there
def can_pass_through(grid, position, enemy=None, avoid_spikes=False,
                     avoid_switches=False):
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
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


# A node class for Breadth First Search
@total_ordering
class BFSNode:

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


# Implements breath first search on the map
# It attempts to find the shortest path between start_ and end_pos on the grid
def breadth_first_search(grid, start_pos, end_pos, enemy=None):
    # Start from the beginning node
    queue = [BFSNode(0, start_pos)]
    # A list of already explored coordinates
    already_explored = []
    # A variable for the discovered path
    found_path = None

    while len(queue) > 0:

        node = queue.pop(0)

        # If the destination was found, break from the loop
        if node.position == end_pos:
            found_path = node
            break

        # Check if it's already explored
        is_explored, list_index = \
            binary_search(already_explored, node.position)
        if not is_explored:

            # Add the location to the list at the specified position,
            # keeping the list sorted
            already_explored.insert(list_index, node.position)

            for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:

                new_position = direction[0] + node.position[0], \
                               direction[1] + node.position[1]

                # If the new position already explored, ignore it
                if new_position in already_explored:
                    continue

                # If the new position is impassible, ignore it
                if not can_pass_through(grid, new_position, enemy=enemy):
                    already_explored.append(new_position)
                    continue

                # Else go ahead and add it to the list to explore
                new_distance = node.distance + 1
                new_distance += distance_between(new_position, end_pos) * 0.01
                queue.append(BFSNode(new_distance, new_position, node))

            # Re-sort the queue in order of increasing distance
            merge_sort(queue)

    # If no path is found, return None
    if found_path is None:
        return None

    # Otherwise, retrace path and make a list of steps
    path = []
    while found_path is not None:
        path.insert(0, found_path)
        found_path = found_path.previous_node

    # Return a list of steps for the enemy to take
    return path
