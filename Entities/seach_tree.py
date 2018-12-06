import queue
import copy
from Utilities.utils import  get_path_from_to,K,Losing_constant


class SearchTreeBuilder(object):

    def __init__(self,world,deadline,agent_first_location):
        '''The world instance given should be a one can be simulated (changed during tree construction)'''
        self._initial_world=world
        self._deadline=deadline
        self._agent_first_location=agent_first_location

    @property
    def initial_world(self):
        return self._initial_world

    @property
    def deadline(self):
        return self._deadline

    @property
    def agent_first_location(self):
        return self._agent_first_location

    def is_goal_state(self,state_node):
        return state_node.time_left<=0 or state_node.people_saved==self.initial_world.num_of_people_at_start

    def heuristic_computation(self,world,current_vertex,target_vertices,time,currently_carrying):

        """
        Represent minimal heuristic: heuristic will be computed as follows:
            compute the people I can not save *Losing_constant
        Admissible heuristic: compute shortest path from current_vertex to target_vertex
        and from to closest shelter

        Args:
            world: World which computation is computed
            current_vertex: source vertex
            target_vertex: destunation vertex
            time: deadline limit
        Returns: Heuristic function value
        """
        cost=0
        if len(target_vertices)>0:
            for target_vertex in target_vertices:
                people_to_be_saved=world.get_vertex_byID(target_vertex).num_of_people
                path_to_vertex_with_people=get_path_from_to(world,current_vertex,target_vertex,push_src=True)
                src_to_vertex_with_people_cost=self.compute_path_cost_with_people(world,path_to_vertex_with_people,target_vertices)
                vertex_with_people_to_shelter_cost=self.get_shortest_shelter_path(world,target_vertex,target_vertices)
                cost+=people_to_be_saved*Losing_constant if src_to_vertex_with_people_cost+vertex_with_people_to_shelter_cost>time else 0
        if currently_carrying:
            temp_target_vertices = copy.deepcopy(target_vertices)
            temp_target_vertices.append((current_vertex))
            vertex_with_people_to_shelter_cost = self.get_shortest_shelter_path(world,current_vertex,temp_target_vertices)
            cost+= currently_carrying*Losing_constant if vertex_with_people_to_shelter_cost>time else 0


        return cost

    def get_verices_with_people(self,world,curr):
       return list(filter(lambda x: x!=curr, world.vertices_with_people_ids))

    def get_shortest_shelter_path(self,world,src,target_vertices):
        """

        Args:
            world: instance of world
            src: source vertex

        Returns:The path from src to the least expensive shelter

        """
        shelters=world.shelters
        paths_to_shelters=[]
        costs=[]

        for shelter in shelters:
            paths_to_shelters.append(get_path_from_to(world,src,shelter,push_src=True))

        for path in paths_to_shelters:
            costs.append(self.compute_path_cost_with_people(world,path,target_vertices))

        min_path=float('inf')

        for i in range(len(costs)):
            if min_path>costs[i]:
                min_path=i

        return costs[min_path]


    def compute_path_cost_with_people(self,world,path,vertices_with_people):
        """
        NO change to the world
        """
        cost=0
        if not vertices_with_people:
            return cost
        people_carying=0
        for i in range(len(path)-1):
            curr_ver=world.get_vertex_byID(path[i])
            next_vet=world.get_vertex_byID(path[i+1])
            weight=world.get_edge_byIDs(path[i],path[i+1]).weight
            if not curr_ver.is_shelter and curr_ver.id in vertices_with_people:
                people_carying+=  curr_ver.num_of_people
            W=world.get_edge_byIDs(path[i],path[i+1]).weight
            cost+=W*(1+K*people_carying)

        return cost

    def create_next_states(self,state):
        states = []

        world = self.initial_world
        currently_carrying = state.num_of_people_carrying
        currrent_location_at_world = state.location
        neighbours = world.get_valid_neighbours_byID(currrent_location_at_world)


        for neighbour in neighbours:
            people_saved_until_now = state.people_saved
            neighbour_vertex = world.get_vertex_byID(neighbour)

            W = world.get_edge_byIDs(state.location, neighbour).weight
            next_state_carrying=currently_carrying
            taget_vertices=copy.deepcopy(state.vertices_with_people)

            if state.num_of_people_carrying>0 and neighbour_vertex.is_shelter:
                    people_saved_until_now+= currently_carrying
                    next_state_carrying=0

            if neighbour in state.vertices_with_people:
                next_state_carrying += neighbour_vertex.num_of_people
                taget_vertices.remove(neighbour)
                remove= True

            cost = W*(1 + K * currently_carrying)
            neighbour_time_left = state.time_left - cost
            if neighbour_time_left<0 and neighbour_vertex.is_shelter:
                people_saved_until_now-= currently_carrying
            hresult=self.heuristic_computation(world,neighbour,taget_vertices,neighbour_time_left,currently_carrying)

            '''Remove the neighbour after the heruristic calculation'''
            # if remove:
            #     taget_vertices.remove(neighbour)

            neighbour_state = StateTreeNode(neighbour, people_saved_until_now, neighbour_time_left, state, \
                                            next_state_carrying, vertices_with_people=taget_vertices,g=cost+state.g,
                                            h=hresult)

            '''reset h_value to 0 when state is goal state'''
            if self.is_goal_state(neighbour_state):
                neighbour_state.g+=neighbour_state.h
                neighbour_state.h=0
                neighbour_state.update_f()

            states.append(neighbour_state)

        return states

    def build_first_state(self):
        '''

        Returns: First State on Tree state

        '''
        agent_location=self.initial_world.get_vertex_byID(self.agent_first_location)
        num_of_people=agent_location.num_of_people
        target_vertices = self.get_verices_with_people(self.initial_world,self.agent_first_location)
        heur_result=self.heuristic_computation(self.initial_world,self.agent_first_location,target_vertices,self.deadline,None)

        return StateTreeNode(self.agent_first_location,0,self.deadline,None,num_of_people,vertices_with_people=target_vertices,h=heur_result)



    def build(self):

        """
        Building the search Tree
        constartins: Building it until leaves are goal state
        Goal State def: time exceeds or all people were saved

        :return: SearchTree Object
        """

        builder_queue = queue.Queue()
        first_state=self.build_first_state()
        '''a state int queue is a tuple of (child state, current world)'''
        builder_queue.put(first_state)

        while not builder_queue.empty():
            current_node=builder_queue.get()
            if not self.is_goal_state(current_node):
                next_states=self.create_next_states(current_node)
                for child_state in next_states:
                    current_node.append_child(child_state)
                    builder_queue.put(child_state)

        return first_state



class SearchTree(object):

    def __init__(self, vertices, edges):
        self._vertices = vertices
        self._edges = edges

    @property
    def vertices(self):
        return self._vertices

    @property
    def edges(self):
        return self._edges



class StateTreeNode(object):

    id=0

    def __init__(self,location,people_saved,time_left,parent,num_of_people,vertices_with_people=0,g=0,h=0):

        '''vertex attribtes'''
        self.id=self.get_next_id()
        self._location=location
        self._people_saved=people_saved
        self._time_left=time_left
        self._parent=parent
        self._num_of_people_carrying=num_of_people
        self._h_value= h
        self._g_value = g
        self._f_value =self.get_f()
        self._vertices_with_people=vertices_with_people

        '''expanders'''
        self._children=None

    @classmethod
    def debug_state(cls,id,location,carrying,h,g,f,time,people_saved):
        print('''\n========DEBUG=======''')
        print(("%s with ID %d arrived to vertex %d carrying %d people  with H=%d G=%d anf F=%d, time left:%d") % (cls.__name__,id,location,carrying,h,g,f,time))
        # if time >=0:
        print(("People saved : %d\n") % (people_saved))


    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def update_f(self):
        self._f_value=self.get_f()

    def get_f(self):
        return   self._g_value+self._h_value

    @staticmethod
    def get_next_id():
        StateTreeNode.id += 1
        return StateTreeNode.id

    @property
    def location(self):
        return self._location

    @property
    def vertices_with_people(self):
        return self._vertices_with_people

    @property
    def people_saved(self):
        return self._people_saved

    @property
    def time_left(self):
        return self._time_left

    @property
    def f(self):
        return self._f_value

    @f.setter
    def f(self,f):
         self._f_value=f

    @property
    def g(self):
        return self._g_value

    @g.setter
    def g(self,g):
        self._g_value=g
    @property
    def h(self):
        return self._h_value

    @h.setter
    def h(self,h):
        self._h_value=h

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, c):
        self._children = c

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self,p):
        self._parent =p

    def append_child(self,child):
        if not self._children:
            self._children=[]
        self._children.append(child)

    @property
    def num_of_people_carrying(self):
        return self._num_of_people_carrying

    @num_of_people_carrying.setter
    def num_of_people_carrying(self, num):
        self._num_of_people_carrying = num


