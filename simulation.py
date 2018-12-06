from Utilities.utils import   PrintingFormat,InfoObject
from Utilities.parser import WorldParser
from  Entities.seach_tree import SearchTreeBuilder
from  Entities.search import AStarSearchAgent,GreedySearchAgent,RealTimeAStarSearchAgent
from Utilities.state import WorldState
from beautifultable import BeautifulTable


class WorldSimulator(object):

    def __init__(self):
        self.running_agent=None


    def run(self):
        parser = WorldParser('Worlds\Initial_world.txt')

        K,V=self.get_inputs()


        world, deadline = parser.parse_file()
        self.world_info = InfoObject(deadline, K, V, world.num_of_people_at_start)

        option=int(input("Which kind of agents do you want to run? 0 to uninformed agents Any other number for search agents:\n"))
        if option==0:
            self.start_uninformed(world)

        else:
            self.start_informed(world, deadline)

    def start_informed(self,world, deadline):

        print("The type of agents are as follows:")
        table = BeautifulTable()
        table.column_headers = ['A* Search Agent', 'Greedy Search Agent', 'Real Time A* Search Agent']
        table.append_row(['1', '2', '3'])
        print(table)

        agent_type = int(input("Choose the type of search agent to activate:\n"))
        expands_for_RTA=6
        search_tree = SearchTreeBuilder(world, deadline, 1).build()

        location = int(input("where do you want the agent to start?\n"))

        perform_f = int(input("Please insert performance  f value\n"))
        selected_agent = AStarSearchAgent(location, self.world_info,search_tree) if agent_type == 1 \
            else GreedySearchAgent(location, self.world_info,search_tree)\
            if agent_type == 2 else \
            RealTimeAStarSearchAgent(location, self.world_info,search_tree,expands_for_RTA)

        goal_path=selected_agent.get_path_to_goal_state()

        for child in goal_path:
            child.debug_state(child.id,child.location,child.num_of_people_carrying,child.h,child.g,child.f,child.time_left,child.people_saved)
        _f = perform_f
        _n = selected_agent.n
        _s = goal_path[-1].people_saved
        _p = (_f * _s) +_n
        print("Performance are f=" +str(_f) +" N = " +str(_n) +" S= "+str(_s) + " P= "+str(_p))


        pass



    def start_uninformed(self,world):


        state=WorldState(world)

        agents_index=0
        STATE_NUMBER = 1
        agents=self.initialize_agents(world)



        while self.world_info.deadline>0:
            print(OKGREEN+"State No. %d:"+ENDC)% STATE_NUMBER
            print(Fail+"Time Remaining: %f"+ENDC+'\n')%self.world_info.deadline
            self.running_agent=agents[(self.running_agent.id-1)%len(agents)]
            self.running_agent.run(world,state)
            STATE_NUMBER=STATE_NUMBER+1
            agents_index+=1


        self.print_end(state,world)



    def initialize_agents(self,world):

        agent_count=self.present_agents_to_user()
        agents_objects=[]
        for i in range(0,agent_count):
            try:
                agent_type=int(input("What kind of agent will be agent No %d?\n"%i))
                if not 1<=agent_type<=3:
                    raise Exception("Invalid Choice, please retry!")
                location=int(input("Where do you want the agent to start?\n"))
                if not world.contains_vertex(location):
                    raise Exception("Invalid location, please retry!")

            except Exception as ex:
                print(ex.args[0])
                i-=i
                continue

            from Entities.agent import HumanAgent, GreedyAgent, VandalAgent

            selected_agent=HumanAgent(location,self.world_info)if agent_type==1 else GreedyAgent(location,self.world_info)if agent_type==2 else VandalAgent(location,self.world_info)
            agent_start_vertex_object = world.get_vertex_byID(location)
            agent_start_vertex_object.append_agent(selected_agent)
            agents_objects.append(selected_agent)

        '''Get the people in frist vertex if its not a shelter'''

        for agent in agents_objects:
            agent_vertex= world.get_vertex_byID(agent.location)
            if not agent_vertex.is_shelter:
                agent.number_of_people_carrying=agent_vertex.num_of_people
                agent_vertex.num_of_people=0


        return agents_objects

    def get_inputs(self):
        while True:
            try:
                K = float(input("With What 'K' do you want to influence time actions?\n"))
                if not 0 <= K <= 1:
                    raise ValueError("K must be a value between 0 to 1. Please Retry!")
            except ValueError as ex:
                print(ex.message)
                continue
            break

        while True:
            try:
                V = int(input("With What 'V' do you want to influence time actions?\n"))
                if V < 1:
                    raise Exception("K must be a value between 0 to 1. Please Retry!")
            except ValueError as ex:
                print(ex.message)
                continue
            break



        return K, V

    @staticmethod
    def present_agents_to_user():
        while True:
            try:
                agent_count=int(input("How many agents do you want to activate?\n"))
            except ValueError as ex:
                print(ex.message)
                continue
            break


        print("The type of agents are as follows:")
        table = BeautifulTable()
        table.column_headers=['Human','Greedy','Vandal']
        table.append_row(['1','2','3'])
        print(table)

        return agent_count

    def print_end(self,state,world):
        print ("\n"+WARNING + "Final State:" + ENDC+"\n")
        state.print_state()
        print("\n"+OKBLUE+"Number of people rescued: %d from %d "+ENDC) % (world.num_of_people_in_shelters(), world.num_of_people_at_start)

if __name__=='__main__':
   s=WorldSimulator().run()


