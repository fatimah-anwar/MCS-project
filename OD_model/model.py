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



class opinionsModel(mesa.Model):
    
    def __init__(self, N = 10, avg_node_degree = 3, opinion_update_prob = 0.3):
        
        self.num_agents = N
        
        # random network structure based on the specified average node degree and the total number of nodes
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
        # self.G = nx.complete_graph(n=self.num_agents)
        # Barabási-Albert Scale-Free Network:
        self.G = nx.barabasi_albert_graph(n=self.num_agents, m=2) # I like this one
        # Watts-Strogatz Small-World Network:
        # self.G = nx.watts_strogatz_graph(n=self.num_agents, k=4, p=0.1) # takes to loong to converge
        # Grid Graph:
        # self.G = nx.grid_2d_graph(int(np.sqrt(self.num_agents)), int(np.sqrt(self.num_agents))) # not sure what it is

        
        self.grid = mesa.space.NetworkGrid(self.G)
        self.schedule = mesa.time.RandomActivation(self)
        self.opinion_update_prob = opinion_update_prob

        inital_opinions = np.random.normal(0.5, 0.2, self.num_agents)

        self.datacollector = mesa.DataCollector(
            {
                "high" : high_opinions_count,
                "low" : low_opinions_count,
            }
        )
        
        
        for i, node in enumerate(self.G.nodes()): 
            a = userAgent(i, self, inital_opinions[i], self.opinion_update_prob)
            self.schedule.add(a)
            self.grid.place_agent(a, node)
            
        self.running = True
        self.datacollector.collect(self)

    def get_current_step(self):
        if high_opinions_count(self) == self.G.number_of_nodes() or low_opinions_count(self) == self.G.number_of_nodes():
        # if high_opinions_count(self) == self.largest_component_size or low_opinions_count(self) == self.largest_component_size:
            return self.schedule.steps
        else:
            return None
        
    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

        # stop if the model reached convergence
        if high_opinions_count(self) == self.G.number_of_nodes() or low_opinions_count(self) == self.G.number_of_nodes():
        # if high_opinions_count(self) == self.largest_component_size or low_opinions_count(self) == self.largest_component_size:
            self.running = False
            
        


    # def run_model(self, n):
    #     for i in range(n):
    #         self.step()