import mesa
import random
from enum import Enum

class State(Enum):
    MOVE = 1
    NO_MOVE = 0


class userAgent(mesa.Agent):
    '''
    Agents parameters 
        PT = peer trust
        R = risk sensitivty 
        B = rendency to share
        dt = risk tolerance threshold 
        
            value is -1 : randomly assigned from unifrom distribution 
            other values : all agents will share this value 
    '''
    
    def __init__( self, unique_id, model, PT, B, R, dt, pos, node):
        
        super().__init__(unique_id, model)
        
        self.physical_pos = pos
        self.online_node = node
        
        
        #1. opinion
        self.opinion = random.uniform(0, 1) 
#         self.old_opinion = self.opinion
    
        # 2. peer trust
        if PT == -1: 
            self.peer_trust = random.uniform(0, 1)
        else:
            self.peer_trust = PT
        
        # 3. tendency to share
        if B == -1:
            self.tendency_to_share = random.uniform(0, 1)
        else:
            self.tendency_to_share = B
        
        # 4. risk sensitivity
        if R == -1:
            temp = random.uniform(0, 1)
            if temp < 1.0/3.0:
                self.risk_sensitivity = 0 
            else:
                temp2 = random.uniform(0, 1)
                if temp2 < 0.5:
                    self.risk_sensitivity = 2 
                else:
                    self.risk_sensitivity = 1 
        else:
            self.risk_sensitivity = R
                
        # 5. risk tolerance threshold
        if dt == -1:
            self.decision_th = random.uniform(0, 1)
        else:
            self.decision_th = dt
            
        # 6. nighbours observed mobility
        self.moving_neighbors = 0
        self.observed_mobility_rate = 0
        
        # 7. final decision
        self.online_info = 0
        self.offline_info = 0
        self.combined_info = 0
        
        self.decision = random.randint(0, 1)
        self.old_decision = self.decision
            
            
        self.mobility_state = self.set_mobility_state(self.decision)
  

    def set_mobility_state(self, decision):

        if decision == 0:
            return State.NO_MOVE
        else:
            return State.MOVE
        
        
    def update_opinion(self):

        neighbors = self.model.online_space.get_neighborhood(self.online_node, include_center = False) 
        if len(neighbors) > 0:
            
            other_agent = self.random.choice(self.model.online_space.get_cell_list_contents(neighbors))
            saved_opinion = self.opinion
            
            # other agent speek
            speak_prob = other_agent.opinion ** (1.0 / other_agent.tendency_to_share)
            if random.uniform(0, 1) < speak_prob:
                self.opinion = self.opinion + self.peer_trust * (other_agent.opinion - self.opinion)

                if self.risk_sensitivity == 0:
                    self.opinion = self.opinion / 2.0
                elif self.risk_sensitivity == 2:
                    self.opinion = (1.0 + self.opinion) / 2.0
            
            # current agent speek
            speak_prob = saved_opinion ** (1.0 / self.tendency_to_share)
            if random.uniform(0, 1) < speak_prob:
                other_agent.opinion = other_agent.opinion + other_agent.peer_trust * (saved_opinion - other_agent.opinion)

                if other_agent.risk_sensitivity == 0:
                    other_agent.opinion = other_agent.opinion / 2.0
                elif other_agent.risk_sensitivity == 2:
                    other_agent.opinion = (1.0 + other_agent.opinion) / 2.0
    
   
    def get_nighbours_mobility_rate(self):
        
        cellmates = self.model.physical_space.get_cell_list_contents([self.physical_pos])
        if len(cellmates) > 1:
            self.moving_neighbors = sum(1 for a in cellmates if a.unique_id != self.unique_id and a.old_decision == 1)
            self.observed_mobility_rate = self.moving_neighbors / (len(cellmates)-1)
        
        
    def make_mobililty_decision(self, opinion):

        self.get_nighbours_mobility_rate()
        
        self.online_info = self.model.alpha * self.opinion
        # self.offline_info = self.model.beta * self.observed_mobility_rate
        self.offline_info = (1 - self.model.alpha) * (1 - self.observed_mobility_rate)
        
        self.combined_info = self.online_info + self.offline_info
    
        if self.combined_info < self.decision_th:
            self.decision = 1
        elif self.combined_info >= self.decision_th:
            self.decision = 0
            
        self.mobility_state = self.set_mobility_state(self.decision)
        
        # updtate opinion:
        self.opinion = self.combined_info
#         self.opinion = ( self.model.beta * self.opinion ) + ( (1 - self.model.beta) * self.combined_info )

        
    def step(self):
        self.make_mobililty_decision(self.opinion)
        self.update_opinion()
        
