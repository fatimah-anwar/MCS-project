import mesa
import random
import networkx as nx   
from agent import userAgent, State


def opinion_avg(model):
    return sum(a.opinion for a in model.online_space.get_all_cell_contents())/model.num_agents

def combined_info_avg(model):
    return sum(a.combined_info for a in model.online_space.get_all_cell_contents())/model.num_agents

def mobility_count(model):
    return sum(1 for a in model.online_space.get_all_cell_contents() if a.mobility_state is State.MOVE)
    
def no_mobility_count(model):
    return sum(1 for a in model.online_space.get_all_cell_contents() if a.mobility_state is State.NO_MOVE)

def mobility_rate(model):
    return mobility_count(model)/model.num_agents


class myModel(mesa.Model): 
    '''
    Model parameters:
        N = population size
        alpha = the weight of the opinions in influencing the constructed decisions
        beta = the weight of the observed mobility in influencing the constructed decisions
        h = the height of the physical grid
        w = the width of the pysical grid
        
    Agents parameters 
        PT = peer trust
        R = risk sensitivty 
        B = rendency to share
        dt = risk tolerance threshold 
        
            value is -1 : randomly assigned from unifrom distribution 
            other values : all agents will share this value 
    '''
    def __init__(self, N = 10, w = 10 , h = 10 , alpha = 0.5 , beta = 0.5, PT = -1, B = -1, R = -1, dt = -1):
      
        
        self.num_agents = N
        self.width = w
        self.height = h
        
        self.PT = PT
        self.B = B
        self.R = R
        self.dt = dt
        
        self.alpha = alpha
        self.beta = beta

        self.G = nx.complete_graph(n = self.num_agents)

        # self.agents = []
        
#         avg_node_degree = 5
#         prob = avg_node_degree / self.num_agents
#         self.G = nx.erdos_renyi_graph(n=self.num_agents, p=prob)
        
        self.datacollector = mesa.DataCollector(
            model_reporters = {
                "op_avg": opinion_avg,
                "combined_info_avg": combined_info_avg,
#                 "moving" : mobility_count,
#                 "not_moving" : no_mobility_count,
                "mobility_rate" : mobility_rate,
            },
            agent_reporters = {
                "opinion" : "opinion", 
#                 "physical_pos": "physical_pos",
#                 "peer_trust" : "peer_trust",
#                 "risk_sensitivity": "risk_sensitivity",
#                 "tendency_to_share" : "tendency_to_share",
#                 "moving_neighbors" : "moving_neighbors",
                "observed_mobility": "observed_mobility_rate",
                
                "online_info":"online_info",
                "offline_info" : "offline_info",
                "combined_info" : "combined_info",
                "decision_th" : "decision_th",
                "old_decision":"old_decision",
                "decision" : "decision",
#                 "mobility_state" : "mobility_state",
            }
        )

        self.physical_space = mesa.space.MultiGrid(width = self.width , height = self.height, torus = True)
        self.online_space = mesa.space.NetworkGrid(g = self.G)
        
        self.schedule = mesa.time.RandomActivation(self)
                
        for i in range(self.num_agents):
            x = random.randrange(self.physical_space.width)
            y = random.randrange(self.physical_space.height)
            
            physical_pos = (x , y)
            online_node = i
                        
            a = userAgent(i, self, self.PT, self.B, self.R, self.dt, physical_pos, online_node)
            
            self.physical_space.place_agent(a, physical_pos)
            self.online_space.place_agent(a, online_node)
            
            self.schedule.add(a)

        # self.initialize_agents()   
          
        self.datacollector.collect(self)        

    # def initialize_agents(self):
    #      for i in range(self.num_agents):
    #         x = random.randrange(self.physical_space.width)
    #         y = random.randrange(self.physical_space.height)
            
    #         physical_pos = (x , y)
    #         online_node = i
                        
    #         a = userAgent(i, self, self.PT, self.B, self.R, self.dt, physical_pos, online_node)
            
    #         self.physical_space.place_agent(a, physical_pos)
    #         self.online_space.place_agent(a, online_node)
            
    #         self.schedule.add(a)
    #         self.agents.append(a)


    # def reinitialize_agents(self):
    #     for i in range(self.num_agents):
    #         a = self.agents[i]
           
    # def step(self, alpha):
    def step(self):
        # self.alpha = alpha

        self.schedule.step()
        self.datacollector.collect(self)  
        
        for a in self.schedule.agents:
            a.old_decision = a.decision
            