Environment simulator and agents for the Hurricane Evacuation Problem
Implementing an environment simulator that runs a path optimization problem with agents that live in the environment and evaluate their performance.

Given a weighted graph,  the goal is (starting at a given vertex) to visit as many as possible out of a set of vertices, and reach a given goal vertex before a given deadline. However, unlike standard shortest path problems in graphs, which have easy known efficient solution methods (e.g. the Dijkstra algorithm), here the problem is that there are more than 2 vertices to visit, their order is not given, and even the number of visited vertices is not known in advance. This is a problem encountered in many real-world settings, such as when you are trying to evacuate people who are stuck at home with no transportation before the hurricane arrives.

Hurricane Evacuation problem environment
The environment consists of a weighted unidrected graph. Each vertex may contain a number of people to be evacuated, or a hurricane shelter. An agent (evacuation vehicle) at a vertex automatically picks up all the people at this vertex just before starting the next move, unless the vertex contains a hurricane shelter, in which case everybody in the vehicle is dropped off at the shelter (goal). It is also possible for edges (roads) to be blocked, assumnig complete knowledge such that all edges are initially unblocked.

An agent can only do no-op (taking 1 time unit) or traverse actions. The time for traverse actions is equal to: w(1+Kp), where w is the edge weight, p is the number of people in the vehicle, and K is a known global non-negative "slow-down" constant, determining how much the vehicle is slowed due to load. The action always succeeds, unless the time limit is breached.

The simulator should keep track of time, the number of actions done by each agent, and the total number of people successfully evacuated.

Implementation part I: simulator + simple agents
Initially Thera are several simple (non-AI) agents. The environment simulator start up by reading the graph from a file, as well as the contents of vertices and global constants, in a the given format(Worlds directory).

The simulator querying the user about the number of agents and what agent program to use for each of them, from a list defined below. Global constants and initialization parameters for each agent (initial position) are also to be queried from the user.

After the above initialization, the simulator running each agent in turn, performing the actions retured by the agents, and update the world accordingly. Additionally, the simulator is capable of displaying the state of the world after each step, with the appropriate state of the agents and their score.

Each agent program (a function) works as follows:
The agent is called by the simulator, together with a set of observations. The agent returns a move to be carried out in the current world state. The agent is allowed to keep an internal state if needed.
There are several agents:

A human agent- printing the state, read the next move from the user, and return it to the simulator. This is used for debugging and evaluating the program.
A greedy agent- the agent computing the shortest currently unblocked path to the next vertex with people to be rescued, or to a shelter if it is carrying people, and try to follow it. If there is no such path, doing no-op.
A vandal agent- it does V no-ops, and then blocks the lowest-cost edge adjacent to its current vertex (takes 1 time unit). Then it traverses a lowest-cost remaining edge, and this is repeated. Prefering the lowest-numbered node in case of ties. If there is no edge to block or traverse, do no-op.
At this stage, runing the environment with three agents participating in each run: one greedy agent, one vandal agent, and one other agent that can be chosen by the user. 
There isalso a part of intelligent agents that need to act in this environment. Each agent should assume that it is acting alone, regardless of whether it is true.
All the algorithms will use a heuristic evaluation function of your choice.

The agents working as follows:
A greedy search agent, that picks the move with best immediate heuristic value to expand next.
An agent using A* search, with the same heuristic.
An agent using a simplified version of real-time A*.
The performance measure will be composed of two parts: S, the agent's score, and N, the number of search expansion steps performed by the search algorithm. The performance of an agent will be:

   P = f * S + N
Clearly, a better agent will have P as small as possible.
The parameter f is a weight constant (can use with values of f: -1, -100, -10000)

