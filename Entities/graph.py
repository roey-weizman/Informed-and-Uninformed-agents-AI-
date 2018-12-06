class UndirectedGraph(object):

    """
    Representation of our world as a undirected graph
    """

    def __init__(self, num_of_vertices, vertices, edges):
        self._num_of_vertices = num_of_vertices
        self._vertices = vertices
        self._edges = edges
        self._num_of_people_at_start = 0
        self._shelters = []
        self._vertices_with_people_objects= []
        self.init()


    def init(self):
        for vertex in self._vertices:
            self._num_of_people_at_start += vertex.num_of_people
            if vertex.is_shelter:
                self._shelters.append(vertex.id)
            else:
                if vertex.num_of_people>0:
                    self._vertices_with_people_objects.append(vertex)

        self.fix_missing_vertices()


    @property
    def shelters(self):
        return self._shelters


    @property
    def vertices(self):
        return self._vertices

    @property
    def num_of_people_at_start(self):
        return self._num_of_people_at_start

    @num_of_people_at_start.setter
    def num_of_people_at_start(self, num_of_people_at_start):
        self._num_of_people_at_start = num_of_people_at_start

    @property
    def edges(self):
        return self._edges

    @edges.setter
    def edges(self,edges):
        self._edges=edges

    @vertices.setter
    def vertices(self, vertices):
        self._vertices=vertices

    @property
    def num_of_vertices(self):
        return self._num_of_vertices

    @num_of_vertices.setter
    def num_of_vertices(self,num):
        self._num_of_vertices = num

    @property
    def vertices_with_people_ids(self):
        return list(map(lambda v:v.id,self._vertices_with_people_objects))

    def contains_vertex(self,v):
         return 0<v<=self.num_of_vertices

    def get_vertex_byID(self,v):
        for vertex in self.vertices:
            if vertex.id==v:
                return vertex
        return None

    def get_neighbours_byID(self,v):
        l = []
        for u in self.vertices:
            if u.id == v:
                continue  # skip v
            if self.are_neighbours_byID(u,v):
                l.append(u.id)

        return l if len(l)>0 else None

    def get_valid_neighbours_byID(self, v):
        l = []
        for u in self.vertices:
            if u.id == v:
                continue
            if self.are_neighbours_byID(u.id, v) and not self.get_edge_byIDs(u.id,v).is_blocked:
                l.append(u.id)
        return l if len(l)>0 else None


    def get_edge_byIDs(self,src,dest):
        for e in self.edges:
            if (e.src == src and e.dest == dest) or (e.src == dest and e.dest == src):
                return e
        return None

    def fix_missing_vertices(self):
        """
            Fixing input errors
        """
        if len(self._vertices) < self._num_of_vertices:
            for i in range(1, self._num_of_vertices + 1):
                if not self.get_vertex_byID(i):
                    self._vertices.append(Vertex(i))

    def are_neighbours_byID(self,v1,v2):
        """

        Args:
            v1: A vertex Id to compare
            v2: A vertex Id to compare

        Returns: Weather v1 and v2 are neighbours in this graph

        """
        for edge in self.edges:
            if(edge.src == v1 and edge.dest == v2 ) or (edge.src == v2 and edge.dest == v1):
                return True
        return False

    def num_of_people_in_shelters(self):
        people = 0
        for v in self._vertices:
            if v.is_shelter:
                people += v.num_of_people
        return people

    def filter_again(self):
        for v in self._vertices_with_people_objects:
            if v.num_of_people==0:
                self._vertices_with_people_objects.remove(v)





class Vertex:

    def __init__(self,id, people=0, is_shelter=False):
        self._id=id
        self._is_shelter = is_shelter
        self._num_of_people = people
        self._agents = []
        self._prev = None

    @property
    def prev(self):
        return self._prev

    @property
    def is_shelter(self):
        return self._is_shelter

    @property
    def id(self):
        return self._id

    @property
    def num_of_people(self):
        return self._num_of_people

    @property
    def agents(self):
        return self._agents

    @prev.setter
    def prev(self, prev_vertex):
        self._prev = prev_vertex

    @agents.setter
    def agents(self,agents):
        self._agents=agents

    @is_shelter.setter
    def is_shelter(self,bool):
        self._is_shelter = bool

    @num_of_people.setter
    def num_of_people(self, num):
        self._num_of_people = num

    def append_agent(self,agent):
        if not self._agents:
            self._agents = []
        self._agents.append(agent)

    def remove_agent(self,agent):
        self._agents.remove(agent)
        if len(self._agents)==0:
            self._agents=None





class Edge:

    def __init__(self,v1, v2,weight, is_blocked=False):
        self._src=v1
        self._dest=v2
        self._weight=weight
        self._is_blocked=is_blocked

    @property
    def is_blocked(self):
        return self._is_blocked

    @property
    def src(self):
        return self._src

    @property
    def dest(self):
        return self._dest

    @property
    def weight(self):
        return self._weight

    @is_blocked.setter
    def is_blocked(self,boolean):
        self._is_blocked =boolean

    @weight.setter
    def weight(self,new_weight):
        self._weight = new_weight





