from heapq import *

class PrintingFormat():
    '''Printing formatting'''
    ENDC = '\033[0m'
    BOLD = "\033[1m"
    Fail = '\033[91m'
    WARNING = '\033[93m'
    OKGREEN = '\033[92m'
    OKBLUE = '\033[94m'

'''Tree building constants'''
K=1
Losing_constant=100


def was_already(state,states):

    for other in states:
        if other==state:
            return True

    return False

def arg_gen():
    """

    Returns: yielded generator arg-string

    """
    x=0
    while True:
      x+=1
      yield 'arg%d'%x


def create_map_args(*args):
    gen = arg_gen()
    return {next(gen): arg for arg in args}




def dijkstra(graph, source):
    dist = {source: 0}
    prev = {}
    used = []
    q = []
    heappush(q, (0, source))
    for v in graph.vertices:
        if v.id != source:
            dist[v.id] = float("inf")
            prev[v.id] = -1
            heappush(q, (float('inf'), v.id))

    for i in range(0, len(dist.items())):
        v_dist, v_id = heappop(q)
        used.append(v_id)
        neighbours = graph.get_valid_neighbours_byID(v_id)
        for u in neighbours:
            edge = graph.get_edge_byIDs(v_id, u)
            alt = v_dist + edge.weight
            if alt < dist[u]:
                dist[u] = alt
                prev[u] = v_id
                for item in q:
                    if item[1] == u:
                        q.remove(item)
                heappush(q, (dist[u], u))
                heapify(q)


    return dist,prev

def get_path_from_to(graph, source, target,push_src=False):

    ''' return empty list for the cost method(searc tree)'''
    if source==target:
        return []
    dist,prev = dijkstra(graph,source)
    path = []
    u = target
    while u != source:
        if prev[u] == -1: #not possible to reach that vertex
            return None
        path.insert(0,u)
        u = graph.get_vertex_byID(prev[u]).id

    if push_src:
        path.insert(0,source)

    return path

def operation_dec(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result['op'].__name__ =='traverse':
            result['op'](result['world'],result['next_edge'],result['next_vertex'])
        else:
            result['op']()

    return wrapper

class InfoObject(object):

    def __init__(self,d,k,v,start_people):
        self._deadline=d
        self._k=k
        self._latelyBlocked = False
        self._start_people=start_people
        self._num_of_no_ops=v
        self._latelyBlocked = False

    def latelyBlocked(self):
        return self._latelyBlocked

    @property
    def deadline(self):
        return self._deadline

    @property
    def start_people(self):
        return self._start_people

    @property
    def latelyBlocked(self):
        return self._latelyBlocked

    @property
    def num_of_no_ops(self):
        return self._num_of_no_ops
    @property
    def k(self):
        return self._k

    @deadline.setter
    def deadline(self,d):
        self._deadline=d

    @latelyBlocked.setter
    def latelyBlocked(self, state):
        self._latelyBlocked = state



def draw_graph():
    from networkx.drawing.nx_agraph import write_dot, graphviz_layout
    import networkx as nx
    G = nx.Graph()
    import queue
    builder_queue = queue.Queue()
    builder_queue.put(root)

    while not builder_queue.empty():
        current = builder_queue.get()
        G.add_node(current.id)
        if current.children:
            for child in current.children:
                builder_queue.put(child)

    builder_queue.put(root)

    while not builder_queue.empty():
        current = builder_queue.get()
        if current.children:
            for child in current.children:
                G.add_edge(current.id, child.id)
                builder_queue.put(child)

    write_dot(G, 'test.dot')

    # same layout using matplotlib with no labels
    plt.title('draw_networkx')
    pos = graphviz_layout(G, prog='dot')
    nx.draw(G, pos, with_labels=False, arrows=True)
    plt.savefig('nx_test.png')
    # nx.draw(G)

    import matplotlib.pyplot as plt

    plt.show()
