from Utilities.utils import operation_dec,get_path_from_to, PrintingFormat
class Agent(object):

    id = 0

    def __init__(self,location,info):
        self.id = self.get_next_id()
        self.number_of_people_carrying = 0
        self.location = location  # TODO: treat a case when location is invalid
        self.last_move_edge = 0
        self.world_info=info

    @classmethod
    def debug_agent(cls,id,from_ver,to_ver):
        print('''\n========DEBUG=======''')
        print("%s with ID %d traversed from vertex %d to %d\n" % (cls.__name__,id,from_ver,to_ver))

    @staticmethod
    def get_next_id():
        Agent.id += 1
        return Agent.id

    '''abstract method -needs implementation'''
    def next_move(self,observations):
        pass

    def no_op(self):
        '''
        Updating time for operation
        :return: True if time has passed
        '''
        deadline_to_be = self.world_info.deadline - 1
        self.world_info.deadline= 0 if deadline_to_be < 0 else deadline_to_be
        return self.world_info.deadline==0

    '''update people in next_vertex and current_vertex'''
    def take_it_or_leave_it(self,next_place_vertex_object,observations):
        if next_place_vertex_object.is_shelter:
            next_place_vertex_object.num_of_people+=self.number_of_people_carrying
            self.number_of_people_carrying=0
            if observations.num_of_people_in_shelters()==observations.num_of_people_at_start:
                print(OKGREEN+"Goal reached! Time left: %f"+ENDC)%self.world_info.deadline
                self.world_info.deadline=0
        else:
            self.number_of_people_carrying += next_place_vertex_object.num_of_people
            next_place_vertex_object.num_of_people=0

    '''Updating time for operation'''
    def update_time(self,edge_to_next_place_weight):
        W = edge_to_next_place_weight
        K = self.world_info.k
        P = 0 if type(self)==VandalAgent else self.number_of_people_carrying

        deadline_to_be = self.world_info.deadline - W * (1 + K * P)

        return False if deadline_to_be<0 else True,deadline_to_be

    '''Update agent location'''
    def update_agent_location(self,current_location_vertex_object,next_location_vertex_object):
        current_location_vertex_object.remove_agent(self)
        next_location_vertex_object.append_agent(self)
        self.location = next_location_vertex_object.id


    def run(self,observations,state):
        state.print_state()
        self.next_move(observations)

    '''Combine changes after traverse action of agent'''

    def change_the_world(self, next_place_vertex_object, current_location_vertex_object, edge_to_next_place_weight,observations):
        self.update_agent_location(current_location_vertex_object, next_place_vertex_object)
        pred,new_deadline=self.update_time(edge_to_next_place_weight)

        if not pred:
            self.world_info.deadline=0
            print(Fail + "%s could not complete the move due to time limits!" + ENDC + '\n') % type(self).__name__
        else:
            self.world_info.deadline=new_deadline
            self.take_it_or_leave_it(next_place_vertex_object,observations)


class HumanAgent(Agent):

    def __init__(self,location,info):
        super(HumanAgent,self).__init__(location,info)



    @operation_dec
    def next_move(self,observations):

        while True:
            try:
                next_place = int(input(HumanAgent.__name__+" with id %d Asks: Where do you want me to go?" % self.id))
            except ValueError as e:
                print (e.args[0]+" Please retry!")
                continue
            try:
                if next_place == 0:
                    return {'op':self.no_op}

                if not observations.contains_vertex(next_place):
                    raise Exception("There is no such Place, Please retry!")
                if not observations.are_neighbours_byID(self.location,next_place):
                    raise Exception("There is no Road between %d and %d ,Please retry!"%(self.location,next_place))

                edge_to_next_place=observations.get_edge_byIDs(self.location,next_place)

                if edge_to_next_place and edge_to_next_place.is_blocked:
                    raise Exception("The Road from This way is BLOCKED!")

                    '''In case of success ,replace agent location'''

            except Exception as ex:
                print(ex.message)
                continue


            break

        return {'op':self.traverse,'world':observations,'next_edge':edge_to_next_place,'next_vertex':next_place}






    def traverse(self,observations,edge_to_next_place,next_place):
        """

        Args:
            observations: The world represented by a UndirectedGraph
            edge_to_next_place: the edge that leads to next vertex
            next_place: the next vertex to traverse
        """

        current_location_vertex = observations.get_vertex_byID(self.location)
        next_location_vertex = observations.get_vertex_byID(next_place)
        self.last_move_edge = edge_to_next_place

        HumanAgent.debug_agent(self.id,self.location,next_place)

        self.change_the_world(next_location_vertex,current_location_vertex,edge_to_next_place.weight,observations)


class GreedyAgent(Agent):
      def __init__(self,location,info):
        super(GreedyAgent,self).__init__(location,info)
        self.pathToShelter = None
        self.pathToShelterLength = float('inf')


      def next_move(self,observations):

          next_place = 0
          edge_to_next_place = 0

          if self.number_of_people_carrying > 0: #go to nearest shelter
            if self.world_info.latelyBlocked is True or not self.pathToShelter:
                self.world_info.latelyBlocked =False
                self.pathToShelter=[]
                for shelter in observations.shelters:
                    current_shelter_path = get_path_from_to(observations,self.location,shelter)
                    if current_shelter_path is None: #not reachable from source to target
                        continue
                    elif len(current_shelter_path) < self.pathToShelterLength:
                        self.pathToShelter = current_shelter_path
                        self.pathToShelterLength = len(current_shelter_path)
                    #dont forget if all shelters are not reachable do no op
                if len(self.pathToShelter) == float('inf'):
                        next_place = -1 #will do no-op
                else:
                    next_place=self.pathToShelter.pop(0)
                    if len(self.pathToShelter) == 0:
                        self.pathToShelter = None
                        self.pathToShelterLength = float('inf')
            else:
                next_place = self.pathToShelter.pop(0)
                if len(self.pathToShelter)==0:
                    self.pathToShelter=None
                    self.pathToShelterLength = float('inf')
                edge_to_next_place = observations.get_edge_byIDs(next_place,self.location)

            '''Going to rescue people from oother vertex'''
          else:

                path_to_vertex_with_people = None
                path_length_to_vertex_with_people = float('inf')



                '''Update if the "vertices with people" list'''
                observations.filter_again()

                for v in observations.vertices_with_people_objects:
                    current_vertex_with_people_path = get_path_from_to(observations,self.location,v.id)
                    if len(current_vertex_with_people_path) < path_length_to_vertex_with_people:
                        path_to_vertex_with_people = current_vertex_with_people_path
                        path_length_to_vertex_with_people = len(current_vertex_with_people_path)

                #TODO: dont forget if all verteices with people are not reachable or no vertices with people do no-op
                if path_length_to_vertex_with_people == float('inf') or len(observations.vertices_with_people_objects) == 0:
                      next_place = -1
                else:
                    next_place = path_to_vertex_with_people.pop(0)
                    edge_to_next_place = observations.get_edge_byIDs(next_place,self.location)


          if next_place == -1:
              GreedyAgent.debug_agent(self.id,self.location,self.location)
              print("Ive just done no-op")
              self.no_op()
          else:
              next_place_vertex_object = observations.get_vertex_byID(next_place)
              current_location_vertex_object = observations.get_vertex_byID(self.location)
              edge_to_next_place = observations.get_edge_byIDs(self.location,next_place)
              GreedyAgent.debug_agent(self.id, self.location, next_place)
              self.change_the_world(next_place_vertex_object, current_location_vertex_object, edge_to_next_place.weight,observations)




class VandalAgent(Agent):
    def __init__(self,location,info):
        super(VandalAgent,self).__init__(location,info)
        self.num_of_no_ops=info.num_of_no_ops

    def next_move(self,observations):

        if self.num_of_no_ops>0:
            self.no_op()
            self.num_of_no_ops-=1
            return

        neighbours_ver_1=observations.get_valid_neighbours_byID(self.location)

        '''Block edges logic'''
        if neighbours_ver_1:
            current_neighbour_weight=float('inf')
            edge_to_block=None
            for neighbour in neighbours_ver_1:
                current_edge=observations.get_edge_byIDs(self.location,neighbour)
                if current_edge.weight<current_neighbour_weight:
                        edge_to_block=tuple([current_edge,neighbour])
                        current_neighbour_weight = current_edge.weight
                elif current_edge.weight==current_neighbour_weight:
                        if edge_to_block[1].id<neighbour:
                            edge_to_block = tuple([current_edge, neighbour])
                            current_neighbour_weight = current_edge.weight
                else:
                    continue

            '''Updating World - with **FAKE** no-op'''
            if not self.no_op():
                edge_to_block[0].is_blocked=True
                self.world_info.latelyBlocked=True
            else:
                return
        else:
            self.no_op()
            self.num_of_no_ops=self.world_info.num_of_no_ops
            return

        '''Traverse edges logic'''
        neighbours_ver_2 = observations.get_valid_neighbours_byID(self.location)

        if neighbours_ver_2:
            current_neighbour_weight=float('inf')
            edge_to_traverse=None
            for neighbour in neighbours_ver_2:
                current_edge=observations.get_edge_byIDs(self.location,neighbour)
                if current_edge.weight<current_neighbour_weight:
                    edge_to_traverse=tuple([current_edge,neighbour])
                    current_neighbour_weight=current_edge.weight
                elif current_edge.weight==current_neighbour_weight:
                        if edge_to_traverse[1].id<neighbour:
                            edge_to_traverse = tuple([current_edge, neighbour])
                            current_neighbour_weight = current_edge.weight
                else:
                    continue


            next_place= edge_to_traverse[1]
            current_location_vertex = observations.get_vertex_byID(self.location)
            next_location_vertex = observations.get_vertex_byID(next_place)

            VandalAgent.debug_agent(self.id, self.location,next_place)

            '''End traverse action'''
            self.change_the_world(next_location_vertex,current_location_vertex,current_neighbour_weight,observations)

        else:
            self.no_op()

        self.num_of_no_ops = self.world_info.num_of_no_ops
        return








