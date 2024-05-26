import mesa
import networkx as nx 
import numpy as np

from .agent import userAgent, State

def state_count(model, state):
    return sum(1 for a in model.grid.get_all_cell_contents() if a.opinion_state is state)

def high_opinions_count(model):
    return state_count(model, State.HIGH)   
    
def low_opinions_count(model):
    return state_count(model, State.LOW)

def opinion_avg(model):
    return sum(a.opinion for a in model.grid.get_all_cell_contents())/model.num_agents

def tendency_to_share_avg(model):
    return sum(a.tendency_to_share for a in model.grid.get_all_cell_contents())/model.num_agents

def risk_avg(model):
    return sum(a.risk_sensitivity for a in model.grid.get_all_cell_contents())/model.num_agents

def inst_trust_avg(model):
    return sum(a.inst_trust for a in model.grid.get_all_cell_contents())/model.num_agents

def peer_trust_avg(model):
    return sum(a.peer_trust for a in model.grid.get_all_cell_contents())/model.num_agents

def sharing_count(model):
    return sum(a.sahring for a in model.grid.get_all_cell_contents())

def sharing_percentage(model):
    return sharing_count(model)/model.num_agents

def get_current_step(model):
    return model.schedule.steps


class opinionsModel(mesa.Model):
    
    def __init__(self, N = 100 , inst_info = -1):
    # def __init__(self, N = 100, avg_node_degree = 5, inst_info = -1, update_opinion_prob = 0.3):
        
        self.prev_avg = 0.0
        self.new_avg = 0.0

        self.num_agents = N

        self.G = nx.complete_graph(n = self.num_agents)
        
        # random network structure based on the specified average node degree and the total number of nodes
        # avg_node_degree = 5
        # prob = avg_node_degree / self.num_agents
        # self.G = nx.erdos_renyi_graph(n=self.num_agents, p=prob)

        # self.largest_component_size = len(max(nx.connected_components(self.G), key=len))
        
        # focus on the latgest connected sub-graph
        # components = list(nx.connected_components(graph))
        # largest_component = max(components, key=len)
        # self.G = graph.subgraph(largest_component)

        # Create the initial random graph
        # initial_G = nx.erdos_renyi_graph(n=self.num_agents, p=prob)

        # Extract the largest connected component
        # largest_component = max(nx.connected_components(initial_G), key=len)
        # self.G = initial_G.subgraph(largest_component).copy()

        # ______________________________________
        # Other network structures 
        # ______________________________________
        # Barabási-Albert Scale-Free Network:
        # self.G = nx.barabasi_albert_graph(n=self.num_agents, m=2) # I like this one
        # Watts-Strogatz Small-World Network:
        # self.G = nx.watts_strogatz_graph(n=self.num_agents, k=4, p=0.1) # takes to loong to converge
        # Grid Graph:
        # self.G = nx.grid_2d_graph(int(np.sqrt(self.num_agents)), int(np.sqrt(self.num_agents))) # not sure what it is

        self.datacollector = mesa.DataCollector(
            model_reporters = {
                "op_avg": opinion_avg,
                "risk_avg" : risk_avg,
                "tendency_to_share_avg" : tendency_to_share_avg, 
                "peer_trust_avg" : peer_trust_avg,

                # "inst_trust_avg" : inst_trust_avg,
                # "sharing_count" : sharing_count,
                # "sharing_avg" : sharing_percentage,
                # "high" : high_opinions_count,
                # "low" : low_opinions_count,
            },
            agent_reporters = {
                "opinion" : "opinion", 
                "risk_sensitivity" : "risk_sensitivity",
                "tendency_to_share" : "tendency_to_share",
                "peer_trust" : "peer_trust",
               
                # "inst_trust" : "inst_trust",
                # "shared" : "shared",
                # "updated" : "updated",
                # "other_opinion" : "other_opinion",
                # "other_agent_ID" : "other_agent_ID",
            }
        )

        self.grid = mesa.space.NetworkGrid(self.G)
        self.schedule = mesa.time.RandomActivation(self)

        for i, node in enumerate(self.G.nodes()):           
            a = userAgent(i, self, inst_info)
            # a = userAgent(i, self, inst_info, update_opinion_prob)
            
            self.schedule.add(a)
            self.grid.place_agent(a, node)
            
        self.running = True
        self.datacollector.collect(self)


    # Not used
    def get_current_step(self):
        if high_opinions_count(self) == self.G.number_of_nodes() or low_opinions_count(self) == self.G.number_of_nodes():
        # if high_opinions_count(self) == self.largest_component_size or low_opinions_count(self) == self.largest_component_size:
            return self.schedule.steps
        else:
            return None

        
    def step(self):

        self.prev_avg = opinion_avg(self)
        self.schedule.step()
        self.new_avg = opinion_avg(self)

        self.datacollector.collect(self)
        
        # stop if the model reached convergence
        # if self.new_avg == self.prev_avg:
        if abs(self.new_avg - self.prev_avg) < 0.001:
            self.running = False
            
        # if high_opinions_count(self) == self.G.number_of_nodes() or low_opinions_count(self) == self.G.number_of_nodes():
        # if high_opinions_count(self) == self.largest_component_size or low_opinions_count(self) == self.largest_component_size:
            # self.running = False

        # stop if the model reached convergence
        # if high_opinions_count(self) == self.G.number_of_nodes() or low_opinions_count(self) == self.G.number_of_nodes():
      