import heapq
import time

# Define the costs
LEFT = 1.0
RIGHT = 0.9
UP = 0.8
DOWN = 0.7
SUCK = 0.6

# Location class to represent agent or dirt locations
class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):  
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __repr__(self):
        return f"({self.x},{self.y})"

# State class to represent a snapshot of the environment
class State:
    def __init__(self, agent_location, dirty_rooms):
        self.agent_location = agent_location
        self.dirty_rooms = dirty_rooms.copy()

    def __eq__(self, other):
        return self.agent_location == other.agent_location and set(self.dirty_rooms) == set(other.dirty_rooms)

    def __hash__(self):
        return hash((self.agent_location, tuple(sorted(self.dirty_rooms))))

    def __repr__(self):
        return f"Agent at {self.agent_location}, Dirt at {self.dirty_rooms}"

# Function to test whether the goal has been achieved (i.e., no dirty rooms)
def goal_test(state):
    return len(state.dirty_rooms) == 0

# Function to expand a node and generate its successors
def expand(node):
    successors = []
    current_state = node.state
    agent = current_state.agent_location
    dirty_rooms = current_state.dirty_rooms

    # Helper function to create a new node
    def create_node(new_location, action_cost, action_taken):
        new_state = State(new_location, dirty_rooms)
        return Node(new_state, node, node.path_cost + action_cost, action_taken)

    # Move left
    if agent.y > 1:
        new_location = Location(agent.x, agent.y - 1)
        successors.append(create_node(new_location, LEFT, 'Left'))
    
    # Move right
    if agent.y < 5:
        new_location = Location(agent.x, agent.y + 1)
        successors.append(create_node(new_location, RIGHT, 'Right'))
    
    # Move up
    if agent.x > 1:
        new_location = Location(agent.x - 1, agent.y)
        successors.append(create_node(new_location, UP, 'Up'))
    
    # Move down
    if agent.x < 4:
        new_location = Location(agent.x + 1, agent.y)
        successors.append(create_node(new_location, DOWN, 'Down'))
    
    # Suck dirt (if the current location is dirty)
    if agent in dirty_rooms:
        new_dirty_rooms = [room for room in dirty_rooms if room != agent]
        new_state = State(agent, new_dirty_rooms)
        successors.append(Node(new_state, node, node.path_cost + SUCK, 'Suck'))

    return successors

# Node class to represent each node in the search tree
class Node:
    def __init__(self, state, parent=None, path_cost=0, action_taken=None):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost
        self.action_taken = action_taken

    # Less-than for priority queue to compare by path cost
    def __lt__(self, other):
        return self.path_cost < other.path_cost

# Function to reconstruct the solution path from the goal node to the root node
def reconstruct_solution(node):
    actions = []
    current = node
    while current.parent is not None:
        actions.append((current.state, current.action_taken))
        current = current.parent
    actions.reverse()
    return actions

# Uniform Cost Graph Search implementation
def uniform_cost_graph_search(problem):
    start_time = time.time()

    # Initial state and node
    start_state = State(problem['agent_location'], problem['dirty_rooms'])
    root = Node(start_state)
    
    # Priority queue (fringe) for uniform cost search
    fringe = []
    heapq.heappush(fringe, (root.path_cost, root))
    
    # Closed set to track visited states
    closed_set = set()

    nodes_expanded = 0
    nodes_generated = 0
    first_five_nodes = []

    while fringe:
        _, node = heapq.heappop(fringe)
        
        # Record first 5 expanded nodes
        if nodes_expanded < 5:
            first_five_nodes.append(node.state)

        # Goal test
        if goal_test(node.state):
            solution = reconstruct_solution(node)
            total_time = time.time() - start_time
            return {
                'solution': solution,
                'cost': node.path_cost,
                'nodes_expanded': nodes_expanded,
                'nodes_generated': nodes_generated,
                'cpu_time': total_time,
                'first_five_nodes': first_five_nodes
            }
        
        # If state has already been visited, skip
        if node.state in closed_set:
            continue

        closed_set.add(node.state)
        nodes_expanded += 1
        
        # Expand the node and generate successors
        successors = expand(node)
        nodes_generated += len(successors)
        for successor in successors:
            if successor.state not in closed_set:
                heapq.heappush(fringe, (successor.path_cost, successor))

    # If no solution found, return failure
    return None

# Problem instances
problem1 = {
    'agent_location': Location(2, 2),
    'dirty_rooms': [Location(1, 2), Location(2, 4), Location(3, 5)]
}

problem2 = {
    'agent_location': Location(3, 2),
    'dirty_rooms': [Location(1, 2), Location(2, 1), Location(2, 4), Location(3, 3)]
}

# Testing the first problem
print("Testing Problem 1:")
result1 = uniform_cost_graph_search(problem1)
if result1:
    # Print first 5 search nodes
    print("First 5 search nodes (states) expanded:")
    for state in result1['first_five_nodes']:
        print(state)
    
    # Print solution
    print("\nSolution steps:")
    for step in result1['solution']:
        state, action = step
        print(f"State: {state}, Action: {action}")
    
    print(f"\nCost: {round(result1['cost'], 2)}")
    print(f"Nodes expanded: {result1['nodes_expanded']}")
    print(f"Nodes generated: {result1['nodes_generated']}")
    print(f"CPU time: {result1['cpu_time']} seconds")

# Testing the second problem
print("\nTesting Problem 2:")
result2 = uniform_cost_graph_search(problem2)
if result2:
    # Print first 5 search nodes
    print("First 5 search nodes (states) expanded:")
    for state in result2['first_five_nodes']:
        print(state)
    
    # Print solution
    print("\nSolution steps:")
    for step in result2['solution']:
        state, action = step
        print(f"State: {state}, Action: {action}")
    
    print(f"\nCost: {round(result2['cost'], 2)}")
    print(f"Nodes expanded: {result2['nodes_expanded']}")
    print(f"Nodes generated: {result2['nodes_generated']}")
    print(f"CPU time: {result2['cpu_time']} seconds")

input("Press Enter to exit...")