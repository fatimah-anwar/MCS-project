import mesa
import networkx as nx 
import numpy as np
from enum import Enum


class State(Enum):
    HIGH = 1
    LOW = 0
    
def state_count(model, state):
    return sum(1 for a in model.grid.get_all_cell_contents() if a.opinion_state is state)


def high_opinions_count(model):
    return state_count(model, State.HIGH)
    
    
def low_opinions_count(model):
    return state_count(model, State.LOW)


class myAgent(mesa.Agent):
    
    def __init__( self, unique_id, model, init_opinion, update_opinion_prob):
        
        super().__init__(unique_id, model)
        
        self.opinion = init_opinion
        self.opinion_state = self.set_opinion_state(self.opinion)
        self.update_opinion_prob = update_opinion_prob

    
    def set_opinion_state(self, opinion):
        if opinion <= 0.5:
            return State.LOW
        else:
            return State.HIGH
    
    
    def update_opinion(self):
        if(self.random.random() < self.update_opinion_prob):
            neighbors = self.model.grid.get_neighborhood(self.pos, include_center=True)
            if len(neighbors) > 0:
                self.opinion = sum(a.opinion for a in self.model.grid.get_cell_list_contents(neighbors))/ len(neighbors)
                self.opinion_state = self.set_opinion_state(self.opinion)
    
    def step(self):
        self.update_opinion()


class simpleOD_Model(mesa.Model):
    
    def __init__(self, N = 10, avg_node_degree = 3, opinion_update_prob = 0.3):
        
        self.num_agents = N
        
        # random network structure based on the specified average node degree and the total number of nodes
        prob = avg_node_degree / self.num_agents
        self.G = nx.erdos_renyi_graph(n=self.num_agents, p=prob)
#         self.G = nx.complete_graph(n=self.num_agents)
        
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
            a = myAgent(i, self, inital_opinions[i], self.opinion_update_prob)
            self.schedule.add(a)
            self.grid.place_agent(a, node)
            
        self.running = True
        self.datacollector.collect(self)

        
    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    def run_model(self, n):
        for i in range(n):
            self.step()