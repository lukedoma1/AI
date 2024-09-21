import heapq
import time

# Node class representing each state in the search tree
class Node:
    def __init__(self, vacuum_pos, dirty_squares, parent=None, action=None, path_cost=0):
        self.vacuum_pos = vacuum_pos  # (x, y) position of the vacuum
        self.dirty_squares = frozenset(dirty_squares)  # Remaining dirty squares
        self.parent = parent  # Parent node
        self.action = action  # Action taken to reach this node
        self.path_cost = path_cost  # Path cost to reach this node

    # Compare nodes based on path cost for the priority queue
    def __lt__(self, other):
        return self.path_cost < other.path_cost

# Uniform Cost Tree Search implementation
def uniform_cost_tree_search(start_pos, dirty_squares):
    start_node = Node(vacuum_pos=start_pos, dirty_squares=dirty_squares, path_cost=0)
    fringe = []
    heapq.heappush(fringe, (start_node.path_cost, start_node))  # Add start node with path cost 0

    expanded_nodes = []
    total_nodes_expanded = 0
    total_nodes_generated = 0
    start_time = time.time()  # Record the start time

    while fringe:
        # Expand the least-cost node from the fringe
        current_cost, current_node = heapq.heappop(fringe)
        expanded_nodes.append((current_node.vacuum_pos, current_node.dirty_squares))
        total_nodes_expanded += 1

        # If goal is achieved (no dirty squares left)
        if not current_node.dirty_squares:
            end_time = time.time()  # Record end time when solution is found
            total_time = end_time - start_time  # Total time taken
            solution_path = reconstruct_path(current_node)
            return (solution_path, total_time, total_nodes_expanded, total_nodes_generated, expanded_nodes)

        # Expand the current node and add its children to the fringe
        for action, result_state, action_cost in expand(current_node):
            new_vacuum_pos, new_dirty_squares = result_state
            new_node = Node(vacuum_pos=new_vacuum_pos, 
                            dirty_squares=new_dirty_squares, 
                            parent=current_node, 
                            action=action, 
                            path_cost=current_node.path_cost + action_cost)
            heapq.heappush(fringe, (new_node.path_cost, new_node))
            total_nodes_generated += 1

    return None, None, total_nodes_expanded, total_nodes_generated, expanded_nodes  # Return None if no solution is found

# Helper function to expand nodes and generate successors
def expand(node):
    successors = []
    x, y = node.vacuum_pos
    dirty_squares = node.dirty_squares

    # Define possible actions and their costs
    actions = {
        'UP': ((x-1, y), 0.8),
        'DOWN': ((x+1, y), 0.7),
        'LEFT': ((x, y-1), 1),
        'RIGHT': ((x, y+1), 0.9),
        'SUCK': (node.vacuum_pos, 0.6)
    }

    # Generate valid moves (ensure vacuum doesn't move out of bounds)
    for action, (new_pos, cost) in actions.items():
        new_x, new_y = new_pos
        # Check bounds (stay within the 4x5 grid)
        if action != 'SUCK' and (1 <= new_x <= 4 and 1 <= new_y <= 5):
            # Move to a valid position within the grid
            successors.append((action, (new_pos, dirty_squares), cost))
        elif action == 'SUCK' and node.vacuum_pos in dirty_squares:
            # Remove the dirty square if 'SUCK' is performed
            new_dirty_squares = dirty_squares - {node.vacuum_pos}
            successors.append((action, (new_pos, new_dirty_squares), cost))

    return successors

# Helper function to reconstruct the solution path from the goal node
def reconstruct_path(node):
    path = []
    while node:
        if node.action:
            path.append((node.action, node.vacuum_pos, node.path_cost))  # Include the path cost
        node = node.parent
    return path[::-1]  # Return reversed path (from start to goal)


# Function to run a test case
def run_test_case(start_pos, dirty_squares):
    print(f"Testing with initial vacuum position {start_pos} and dirty squares {dirty_squares}")
    result = uniform_cost_tree_search(start_pos, dirty_squares)

    if result[0]:
        solution, total_time, total_nodes_expanded, total_nodes_generated, expanded_nodes = result
        
        # Print the states of the first 5 expanded nodes
        print("First 5 expanded nodes (states):")
        for i, (vacuum_pos, dirty_squares) in enumerate(expanded_nodes[:5]):
            print(f"Node {i + 1}: Vacuum position {vacuum_pos}, Dirty squares {dirty_squares}")

        print(f"\nTotal nodes expanded: {total_nodes_expanded}")
        print(f"Total nodes generated: {total_nodes_generated}")
        print(f"Total CPU execution time: {total_time:.2f} seconds")

        # Print the solution path
        print("Solution path:")
        for step in solution:
            print(f"Action: {step[0]}, Vacuum position: {step[1]}")
        print(f"Number of moves: {len(solution)}")
        print(f"Cost of solution: {solution[-1][2]:.2f}")  # Get the cost from the last node
    else:
        print("No solution found.")
    print("=" * 50)


# Test Case 1: Initial agent location (2, 2) and dirty squares (1, 2), (2, 4), (3, 5)
run_test_case(start_pos=(2, 2), dirty_squares={(1, 2), (2, 4), (3, 5)})

# Test Case 2: Initial agent location (3, 2) and dirty squares (1, 2), (2, 1), (2, 4), (3, 3)
run_test_case(start_pos=(3, 2), dirty_squares={(1, 2), (2, 1), (2, 4), (3, 3)})
