class WorldParser(object):

    """
    Providing parsing capabilities and object building from the default representation of input
    """

    def __init__(self,filename):
        self.filename=filename
        self.num_of_vertices=0
        self.vertices= None
        self.edges=None
        self.deadline=0

    def vertex_exist(self,vertex_num):
        return vertex_num<=self.num_of_vertices

    def get_vertex(self,num):
        for v in self.vertices:
            if v.id==num:
                return v
        return

    def create_graph_object(self,args_map):

        """

        Args:
            args_map: A mapping from arg-key to arg-value as specified by the input

        Returns: A graph object (Vertex,Edge,Deadline)

        """

        from Entities.graph import Vertex, Edge

        if args_map['arg1']=='V':
            if len(args_map)>4:
                raise Exception("Too much arguments to Vertex_Builder")
            elif len(args_map)>2:
                if not self.vertex_exist(int(args_map['arg2'])):
                    raise Exception("Contradiction on Vertex_Builder")
                return Vertex(int(args_map['arg2']),is_shelter=True)if args_map['arg3']=='S' else Vertex(int(args_map['arg2']),people=int(args_map['arg4']))
            else:
                self.num_of_vertices=int(args_map['arg2'])
                return None



        elif args_map['arg1'] == 'E':
            if len(args_map)!=4:
                raise Exception("number of arguments in Edge_Builder is not compatible")
            if not self.vertex_exist(int(args_map['arg2'])) or not self.vertex_exist(int(args_map['arg3'])):
                raise Exception("Vertices v%d or v%d do not exist" % (int(args_map['arg2']),int(args_map['arg3'])))

            return Edge(int(args_map['arg2']), int(args_map['arg3']), int(args_map['arg4']))

        elif args_map['arg1']=='D':
            if len(args_map)!=2:
                raise Exception("number of arguments in Deadline_arg is not compatible")
            return int(args_map['arg2'])

    def build_graph_from_data(self):

        from Entities.graph import UndirectedGraph
        return UndirectedGraph(self.num_of_vertices,self.vertices,self.edges)

    def _parse_line(self, line):
        """

        Args:
            line: The current line to be processed from self.filename

        Returns:
            A graph object/entity to be build
        """
        from Utilities.utils import create_map_args

        normal_string = line.strip('#').split() if len(line.strip('#').split())>0 else ''
        args_map=create_map_args(*[c for c in normal_string])
        return self.create_graph_object(args_map)

    def parse_file(self):

        from Entities.graph import Vertex, Edge

        with open(self.filename, 'r') as file_object:
            lines = file_object.readlines()
            for line in lines:
               if not line or line.startswith('\n'):
                   continue
               elif not line.startswith('#'):
                   raise Exception("World format is not compatible!")
               else:
                   graph_object=self._parse_line(line)
                   if isinstance(graph_object,Vertex):
                       if self.vertices:
                           self.vertices.append(graph_object)
                       else:
                           self.vertices = [graph_object]
                   elif isinstance(graph_object,Edge):
                       if self.edges:
                           self.edges.append(graph_object)
                       else:
                           self.edges=[graph_object]
                   elif isinstance(graph_object,int):
                       self.deadline=graph_object
                   else:
                       pass

        file_object.close()
        return self.build_graph_from_data(), self.deadline



