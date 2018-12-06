


class WorldState(object):

    def __init__(self,graph):
        self._graph=graph

    @property
    def graph(self):
        return self._graph

    @graph.setter
    def graph(self,new_g):
        self._graph = new_g

    def print_state(self):
        vertices_to_check=self.graph.vertices
        edges_to_check=self.graph.edges

        from beautifultable import BeautifulTable

        table = BeautifulTable()
        table.column_headers=['Vertex id', 'Shelter','People','Agents','Roads From<-->To(Weight)-Status']
        for v in vertices_to_check:
            if v.agents:
                agents = ''
                for agent in v.agents:
                    agents += ' agent_%d(%d), '%(agent.id,agent.number_of_people_carrying)
            else:
                agents="No Agents"

            current_vertex_edges=""
            for e in edges_to_check:
                if isinstance(e,list):
                    continue
                else:
                    if e.src==v.id or e.dest==v.id:
                        current_vertex_edges+="%d->%d(%d)-%s  "%(e.src,e.dest,e.weight,"Blocked" if e.is_blocked else "Free")\
                            if e.src==v.id else "%d->%d(%d)-%s  "%(e.dest,e.src,e.weight,"Blocked" if e.is_blocked else "Free")

            table.append_row([v.id,'V' if v.is_shelter else 'X',v.num_of_people,agents,current_vertex_edges])

        print(table)
