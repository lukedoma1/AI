import time

# Node class representing each state in the search tree
class Node:
    def __init__(self, vacuum_pos, dirty_squares, parent=None, action=None, path_cost=0, depth=0):
        self.vacuum_pos = vacuum_pos  # (x, y) position of the vacuum
        self.dirty_squares = set(dirty_squares)  # Remaining dirty squares
        self.parent = parent  # Parent node
        self.action = action  # Action taken to reach this node
        self.path_cost = path_cost  # Total path cost accumulated so far
        self.depth = depth  # Depth to search

# Runs limited DFS with increasing depth
def iterative_deepening_tree_search(start_pos, dirty_squares): 
    depth_limit = 0
    total_nodes_expanded = 0
    total_nodes_generated = 0
    expanded_nodes = []
    start_time = time.time()

    while True:
        # Repeatedly call limited DFS, increasing the depth limit with each iteration
        result = depth_limited_search(start_pos, dirty_squares, depth_limit, expanded_nodes)
        # solution_path = result[0]
        total_nodes_expanded += result[1]
        total_nodes_generated += result[2]
        # path_cost = result[3]

        # If solution is found, return all the necessary information
        if result[0]:
            #print(result[0])
            end_time = time.time()
            total_time = end_time - start_time
            return result[0], total_time, total_nodes_expanded, total_nodes_generated, expanded_nodes, result[3]
        depth_limit += 1

# Depth first search with a limit
def depth_limited_search(start_pos, dirty_squares, depth_limit, expanded_nodes):
    start_node = Node(vacuum_pos=start_pos, dirty_squares=dirty_squares, depth=0, path_cost=0)
    fringe = [start_node]  # Stack for DFS
    total_nodes_expanded = 0
    total_nodes_generated = 0

    # Iterate through nodes in the fringe
    while fringe:
        # LIFO: grab the node from the back of the fringe (stack)
        current_node = fringe.pop()
        expanded_nodes.append((current_node.vacuum_pos, current_node.dirty_squares))
        total_nodes_expanded += 1

        # If no dirty squares left, return the path. Success!
        if not current_node.dirty_squares:
            solution_path = reconstruct_path(current_node)
            return solution_path, total_nodes_expanded, total_nodes_generated, current_node.path_cost

        # Expand the current node if within the depth limit
        if current_node.depth < depth_limit:
            for action, result_state, action_cost in expand(current_node):
                new_vacuum_pos, new_dirty_squares = result_state
                new_node = Node(vacuum_pos=new_vacuum_pos,
                                dirty_squares=new_dirty_squares,
                                parent=current_node,
                                action=action,
                                path_cost=current_node.path_cost + action_cost,
                                depth=current_node.depth + 1)
                # Add new node to the back of the fringe
                fringe.append(new_node)
                total_nodes_generated += 1

    return None, total_nodes_expanded, total_nodes_generated, 0  # Return None if no solution is found

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
            path.append((node.action, node.vacuum_pos, node.path_cost))  # Include path cost in each step
        node = node.parent
    return path[::-1]  # Return reversed path (from start to goal)

# Function to run a test case
def run_test_case(start_pos, dirty_squares):
    print(f"Testing with initial vacuum position {start_pos} and dirty squares {dirty_squares}")
    result = iterative_deepening_tree_search(start_pos, dirty_squares)

    if result[0]:
        solution, total_time, total_nodes_expanded, total_nodes_generated, expanded_nodes, total_path_cost = result
        
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
            print(f"Action: {step[0]}, Vacuum position: {step[1]}, Path cost: {step[2]:.2f}")
        print(f"Number of moves: {len(solution)}")
        print(f"Total cost of solution: {total_path_cost:.2f}")  # Output the total path cost at the end
    else:
        print("No solution found.")
    print("=" * 50)

# Test Case 1: Initial agent location (2, 2) and dirty squares (1, 2), (2, 4), (3, 5)
run_test_case(start_pos=(2, 2), dirty_squares={(1, 2), (2, 4), (3, 5)})

# Test Case 2: Initial agent location (3, 2) and dirty squares (1, 2), (2, 1), (2, 4), (3, 3)
run_test_case(start_pos=(3, 2), dirty_squares={(1, 2), (2, 1), (2, 4), (3, 3)})
