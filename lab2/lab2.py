import copy
import heapq

# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
	raise NotImplementedError

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
	raise NotImplementedError


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
	agenda = [[start]]
	extended = set()

	while len(agenda) > 0:
		current_path = agenda.pop(0)
		current_node = current_path[len(current_path) - 1]
		extended.add(current_node)

		if current_node == goal:
			return current_path

		neighbors = graph.get_connected_nodes(current_node)
		neighbors = sorted(neighbors, reverse=True, key=lambda node: graph.get_heuristic(node, goal))
		for node in neighbors:
			if node not in extended:
				new_path = (copy.deepcopy(current_path))
				new_path.append(node)	
				agenda.insert(0, new_path)
	return [];

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
	agenda = [[start]]
	paths_to_next_level = []

	while len(agenda) > 0 or len(paths_to_next_level) > 0:
		if len(agenda) == 0:
			paths_to_next_level.sort(key=lambda path: graph.get_heuristic(path[len(path) - 1], goal))
			agenda = copy.deepcopy(paths_to_next_level[0:beam_width])
			paths_to_next_level = []

		current_path = agenda.pop(0)
		current_node = current_path[len(current_path) - 1]

		if current_node == goal:
			return current_path

		for node in graph.get_connected_nodes(current_node):
			if node not in current_path:
				new_path = (copy.deepcopy(current_path))
				new_path.append(node)	
				paths_to_next_level.append(new_path)

	return []; 

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
	node_one = node_names[0]
	node_two = None
	path_length = 0

	for node in node_names[1:]:
		node_two = node
		edge = graph.get_edge(node_one, node_two)
		path_length += edge.length
		node_one = node_two

	return path_length

def branch_and_bound(graph, start, goal):
	agenda = [(0, [start])]

	while len(agenda) > 0:
		current_path_length, current_path = heapq.heappop(agenda)
		current_node = current_path[len(current_path) - 1]

		if current_node == goal:
			return current_path

		neighbors = graph.get_connected_nodes(current_node)
		for node in neighbors:
			if node not in current_path:
				new_path = (copy.deepcopy(current_path))
				new_path.append(node)	
				heapq.heappush(agenda,(path_length(graph,new_path), new_path))

	return []

def a_star(graph, start, goal):
	agenda = [(0, [start])]
	extended_set = set()

	while len(agenda) > 0:
		current_path_length, current_path = heapq.heappop(agenda)
		current_node = current_path[len(current_path) - 1]
		extended_set.add(current_node)

		if current_node == goal:
			return current_path

		neighbors = graph.get_connected_nodes(current_node)
		for node in neighbors:
			if node not in extended_set:
				new_path = (copy.deepcopy(current_path))
				new_path.append(node)
				score = path_length	(graph, new_path) + graph.get_heuristic(node, goal)
				heapq.heappush(agenda,(score, new_path))

	return []


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
	for node in graph.nodes:
		shortest_path_to_goal = a_star(graph, node, goal)
		if path_length(graph, shortest_path_to_goal) < graph.get_heuristic(node, goal):
			return False
	return True

def is_consistent(graph, goal):
	for edge in graph.edges:
		node_one_heuristic = graph.get_heuristic(edge.node1, goal)
		node_two_heuristic = graph.get_heuristic(edge.node2, goal)
		if edge.length < abs(node_one_heuristic - node_two_heuristic):
			return False
	return True

HOW_MANY_HOURS_THIS_PSET_TOOK = 'nothing'
WHAT_I_FOUND_INTERESTING = 'everything'
WHAT_I_FOUND_BORING = 'nothing'
