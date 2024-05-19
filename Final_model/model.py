import mesa
import random
import numpy as np
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
    return mobility_count(model) / model.num_agents



def get_communicatin_count(model):
    return model.communicatin_count

def communication_rate(model):
    return model.communicatin_count / model.num_agents



def get_start_moving_count(model):
    return model.start_moving_count

def get_stop_moving_count(model):
    return model.stop_moving_count

def start_moving_rate(model):
    return model.start_moving_count / model.num_agents

def stop_moving_rate(model):
    return model.stop_moving_count / model.num_agents



def get_updated_decision_count(model):
    return model.start_moving_count + model.stop_moving_count

def updated_decision_rate(model):
    return get_updated_decision_count(model) /model.num_agents


############################################
############################################


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
    def __init__(self, 
                 N = 10,  
                #  w = 1 , h = 1 , 
                 grid_dimensions = (5, 5),
                 network = "complete", 
                 net_var1_p = 0.1 , net_var2_m = 10,
                 alpha = 0.5 , 
                 PT = -1, B = -1, R = -1, dt = -1,
                 collect_agent_data = True, collect_model_data = True):
      
        
        self.num_agents = N

        # self.width = w
        # self.height = h
        self.height, self.width = grid_dimensions
        
        self.PT = PT
        self.B = B
        self.R = R
        self.dt = dt
        
        self.alpha = alpha # for determining the weights of the online and offline information in influencing the decision

        self.G = self.create_network(network, self.num_agents, net_var1_p , net_var2_m)
        
        self.collect_agent_data = collect_agent_data
        self.collect_model_data = collect_model_data

        # extra counters
        self.communicatin_count = 0
        self.start_moving_count = 0
        self.stop_moving_count = 0

        self.agents_initial_opinions = []
        self.agents_initial_decisions = []
        
        self.physical_space = mesa.space.MultiGrid(width = self.width , height = self.height, torus = True)
        self.online_space = mesa.space.NetworkGrid(g = self.G)
        self.schedule = mesa.time.RandomActivation(self)

        self.initialize_agents()  
        self.set_datacollector() 
          
        self.running = True
        self.datacollector.collect(self)        

    
    ####################################################


    def create_network(self, network_type, nodes_count, net_var1_p , net_var2_m):
        if network_type == "complete":
            network = nx.complete_graph(n = nodes_count)
                 
        # random network
        elif network_type == "random":
#             avg_node_degree = 5
#             prob = avg_node_degree / nodes_count
            network = nx.erdos_renyi_graph(n = nodes_count, p = net_var1_p)
       
        # regular lattice -> every node has m edges
        elif network_type == "regular":
            network = nx.random_regular_graph(n = nodes_count , d = net_var2_m)
 
        # Watts-Strogatz Small-World Network:
        elif network_type == "small_world":
            network = nx.watts_strogatz_graph(n = nodes_count, p = net_var1_p , k = net_var2_m) # takes to loong to converge
          
        # Barabási-Albert Scale-Free Network:
        elif network_type == "scale_free":
            network = nx.barabasi_albert_graph(n = nodes_count, m = net_var2_m) # I like this one

        return network
    


    def initialize_agents(self):
         for i in range(self.num_agents):
            x = random.randrange(self.physical_space.width)
            y = random.randrange(self.physical_space.height)
            
            physical_pos = (x , y)
            online_node = i
         
            a = userAgent(i, self, self.PT, self.B, self.R, self.dt, physical_pos, online_node)
            
            self.physical_space.place_agent(a, physical_pos)
            self.online_space.place_agent(a, online_node)
            
            self.schedule.add(a)
            
            self.agents_initial_opinions.append(a.opinion)
            self.agents_initial_decisions.append(a.decision)



    def reinitialize_agents(self):
        for a in self.online_space.get_all_cell_contents():
            i = a.unique_id
            a.opinion = a.old_opinion = self.agents_initial_opinions[i]
            a.decision = a.old_decision = self.agents_initial_decisions[i]

        self.set_datacollector()


    def set_alpha(self , new_alpha):
        self.alpha = new_alpha



    # def set_gamma(self, new_gamma):
    #     self.gamma = new_gamma


        
    def set_datacollector(self):

        model_reporters = {}
        if self.collect_model_data:
            model_reporters = {
                "op_avg": opinion_avg,
                "combined_info_avg": combined_info_avg,
                
                "moving" : mobility_count,
                "not_moving" : no_mobility_count,
                "mobility_rate" : mobility_rate,

                "start_moving_count" :  get_start_moving_count ,
                "stop_moving_count" : get_stop_moving_count ,
                "start_moving_rate" : start_moving_rate ,
                "stop_moving_rate" : stop_moving_rate,
            
                "updated_decision_count" : get_updated_decision_count,
                "updated_decision_rate" : updated_decision_rate,
                
                "communicatin_count" : get_communicatin_count,
                "communication_rate" : communication_rate,
            }
        
        agent_reporters = {}
        if self.collect_agent_data:
            agent_reporters = {
                "opinion" : "opinion", 
                "old_opinion" : "old_opinion",
                "physical_pos": "physical_pos",
                
                "peer_trust" : "peer_trust",
                "risk_sensitivity": "risk_sensitivity",
                "tendency_to_share" : "tendency_to_share",
                "offline_neighbors" : "offline_neighbors",
                "online_neighbors" : "online_neighbors",
                
                "moving_neighbors" : "moving_neighbors",
                "observed_mobility": "observed_mobility_rate",
                "online_info":"online_info",
                "offline_info" : "offline_info",
                "combined_info" : "combined_info",

                "decision_th" : "decision_th",
                "old_decision":"old_decision",
                "decision" : "decision",

                "move_counter" : "move_counter" ,
                "stop_move_counter" : "stop_move_counter",
                "speak_counter" : "speak_counter" ,
                "listen_counter" : "listen_counter" ,
            }

        self.datacollector = mesa.DataCollector(model_reporters = model_reporters , agent_reporters = agent_reporters)


    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)  
        
        for a in self.schedule.agents:
            a.old_decision = a.decision
            # a.old_opinion = a.opinion
        
        self.communicatin_count = 0
        self.start_moving_count = 0
        self.stop_moving_count = 0

            