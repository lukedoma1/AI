import time

class Node:
    def __init__(self, vacuum_pos, dirty_squares, parent=None, action=None, path_cost=0, depth=0):
        self.vacuum_pos = vacuum_pos  # Position x,y
        self.dirty_squares = set(dirty_squares)  # Set of dirty squares left
        self.parent = parent  # Previous node
        self.action = action  # Action to get to the node
        self.path_cost = path_cost  # Path cost to this node
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
            solution_path = find_solution_path(current_node)
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

# Generate successors by expanding the current node.
def expand(node):
    x, y = node.vacuum_pos
    dirty_squares = node.dirty_squares

    actions = {
        'UP': ((x - 1, y), 0.8),
        'DOWN': ((x + 1, y), 0.7),
        'LEFT': ((x, y - 1), 1),
        'RIGHT': ((x, y + 1), 0.9),
        'SUCK': (node.vacuum_pos, 0.6)
    }

    # Check for valid moves
    valid_moves = [
        (action, (new_pos, dirty_squares), cost) for action, (new_pos, cost) in actions.items()
        if (action != 'SUCK' and 1 <= new_pos[0] <= 4 and 1 <= new_pos[1] <= 5)
        or (action == 'SUCK' and node.vacuum_pos in dirty_squares)
    ]

    if 'SUCK' in [move[0] for move in valid_moves]:
        # Perform 'SUCK' action, getting rid of the dirty square
        valid_moves = [
            (action, (new_pos, dirty_squares - {node.vacuum_pos}) if action == 'SUCK' else (new_pos, dirty_squares), cost)
            for action, (new_pos, dirty_squares), cost in valid_moves
        ]

    return valid_moves


# Helps to find the solution path from the goal node
def find_solution_path(node):
    path = []  # Use a list and insert steps in reverse order while traversing
    while node:
        if node.action:
            path.insert(0, (node.action, node.vacuum_pos, node.path_cost))
        node = node.parent
    return path


# Function to run a test case
def run_test_case(start_pos, dirty_squares):
    print(f"Starting Test with Vacuum at {start_pos} and Dirty Squares at {dirty_squares}")
    solution, total_time, total_nodes_expanded, total_nodes_generated, expanded_nodes, total_path_cost = iterative_deepening_tree_search(start_pos, dirty_squares)

    if solution:
        # Displaying expanded node details
        print(f"Nodes Expanded: {total_nodes_expanded}, Nodes Generated: {total_nodes_generated}")
        print(f"Execution Time: {total_time:.3f} seconds")
        
        # Showing details for first few expanded nodes
        print("\nInitial Expanded Nodes:")
        for idx, (vacuum_pos, dirty_squares) in enumerate(expanded_nodes[:5], start=1):
            print(f"  {idx}: Vacuum at {vacuum_pos}, Remaining Dirt: {dirty_squares}")

        # Printing the solution path with formatting for each step
        print("\nSolution Path:")
        for i, (action, pos, cost) in enumerate(solution, start=1):
            print(f"  Step {i}: Action: {action}, Position: {pos}, Cumulative Cost: {cost:.2f}")

        print(f"Total Moves: {len(solution)}, Total Cost: {total_path_cost:.2f}")
    else:
        print("No solution was found.")
    print("-" * 60)


# Test Case 1: Initial agent location (2, 2) and dirty squares (1, 2), (2, 4), (3, 5)
run_test_case(start_pos=(2, 2), dirty_squares={(1, 2), (2, 4), (3, 5)})

# Test Case 2: Initial agent location (3, 2) and dirty squares (1, 2), (2, 1), (2, 4), (3, 3)
run_test_case(start_pos=(3, 2), dirty_squares={(1, 2), (2, 1), (2, 4), (3, 3)})
