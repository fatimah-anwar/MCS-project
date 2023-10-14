import mesa
from enum import Enum

class State(Enum):
    HIGH = 1
    LOW = 0
    
class userAgent(mesa.Agent):
    
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