from .agent import Agent
import copy
from Utilities.utils import was_already




class SearchAgent(Agent):

    """
    A general search agent
    """
    def __init__(self,location,info,search_tree):
        super(SearchAgent, self).__init__(location, info)
        self.tree=search_tree
        self.expands_limit = float('inf')
        self.n = 0

    def compute_f(self):
        return

    def is_goal_state(self, state_node):
        return state_node.time_left <= 0 or state_node.people_saved == self.world_info.start_people
    @classmethod
    def find_min_child(cls, children):
        cls.find_min_child(children)


    def get_path_to_goal_state(self):
        current_node = self.tree
        path = []
        # states=[]
        fringe=[current_node]
        while True and self.expands_limit>0:
            if self.is_goal_state(current_node):
                break
            fringe.remove(current_node)
            self.n += 1
            fringe.extend(current_node.children)
            current_node = self.find_min_child(fringe)
            # states.append(copy.deepcopy(current_node))
            self.expands_limit-=1


        while current_node:
            path.append(current_node)
            current_node=current_node.parent

        path=path[::-1]

        return path


class GreedySearchAgent(SearchAgent):
    """
        A gready search agent
        Purpose: get the first goal state he sees
    """
    def __init__(self,location,info,search_tree):
        super(GreedySearchAgent, self).__init__(location, info,search_tree)
        self.expands_limit = float('inf')



    def find_min_child(self,children):
        index = 0
        min_h=float('inf')
        for  i in range(len(children)):
            if min_h > children[i].h:
                min_h = children[i].h
                index = i

        return children[index]

class AStarSearchAgent(SearchAgent):
    """
           A* search agent
           Purpose: get the goal state according to minimal cost(dependent of f)
    """
    def __init__(self,location,info,search_tree):
        super(AStarSearchAgent, self).__init__(location, info,search_tree)
        self._expands_limit = float('inf')

    def find_min_child(self,children):

        index=0
        min_f=float('inf')
        for  i in range(len(children)):
            if min_f == children[i].f:
                index =i if children[i].people_saved>=children[index].people_saved else index
            if min_f > children[i].f:
                min_f = children[i].f
                index=i

        return children[index]




class RealTimeAStarSearchAgent(AStarSearchAgent):
    """
               RTA* search agent
               Purpose: get the goal state according to minimal cost(dependent of f) with constaraind on expands limit
        """
    def __init__(self,location,info,search_tree,expands):
        super(AStarSearchAgent, self).__init__(location, info,search_tree)
        self.expands_limit=expands
