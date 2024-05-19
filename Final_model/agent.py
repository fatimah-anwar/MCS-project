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

        pos = location of the agent in the offline grid
        node = location of the agent in the online network
    '''
    
    def __init__( self, unique_id, model, PT, B, R, dt, pos, node):
    # def __init__( self, unique_id, model, O, PT, B, R, dt, pos, node):
        
        super().__init__(unique_id, model)
        
        # agent's locations in the offline and online environments
        self.physical_pos = pos
        self.online_node = node
         
        #1. opinion
        self.opinion = random.uniform(0, 1) 
        self.old_opinion = self.opinion
    
        # 2. peer trust
        if PT == -1:           
            self.peer_trust = random.uniform(0, 1)  # unifrom distibution between 0 and 1 
        elif PT == "low":
            self.peer_trust = random.uniform(0, 0.3)  # unifrom distibution of low values
        elif PT == "mid":
            self.peer_trust = random.uniform(0.3, 0.7) # unifrom distibution of mid values
        elif PT == "high":
            self.peer_trust = random.uniform(0.7, 1) # unifrom distibution of high values
        else:
            self.peer_trust = PT  # all agent will have the same value
        
        # 3. tendency to share
        if B == -1:
            self.tendency_to_share = random.uniform(0, 1)  # unifrom distibution between 0 and 1 
        elif B == "low":
            self.tendency_to_share = random.uniform(0, 0.3)  # unifrom distibution of low values
        elif B == "mid":
            self.tendency_to_share = random.uniform(0.3, 0.7) # unifrom distibution of mid values
        elif B == "high":
            self.tendency_to_share = random.uniform(0.7, 1) # unifrom distibution of high values
        else:
            self.tendency_to_share = B  # all agent will have the same value
        
        # 4. risk sensitivity
        if R == -1:
            temp = random.uniform(0, 1)  # unifrom distibution  
            if temp < 1.0/3.0:
                self.risk_sensitivity = 0 
            else:
                temp2 = random.uniform(0, 1)
                if temp2 < 0.5:
                    self.risk_sensitivity = 2 
                else:
                    self.risk_sensitivity = 1 
        else:
            self.risk_sensitivity = R   # all agent will have the same value
                
        # 5. risk tolerance threshold
        if dt == -1:
            self.decision_th = random.uniform(0, 1)   # unifrom distibution between 0 and 1 
        elif dt == "low":
            self.decision_th = random.uniform(0, 0.3)  # unifrom distibution of low values
        elif dt == "mid":
            self.decision_th = random.uniform(0.3, 0.7) # unifrom distibution of mid values
        elif dt == "high":
            self.decision_th = random.uniform(0.7, 1) # unifrom distibution of high values
        else:
            self.decision_th = dt   # all agent will have the same value
            
        
        # 6. final decision
        # self.decision = random.randint(0, 1)
        # self.decision = self.get_decision(self.opinion)

        if self.opinion < self.decision_th:
            self.decision = 1 # move
        elif self.opinion >= self.decision_th:
            self.decision = 0 # doen't move
                    
        self.old_decision = self.decision
        self.mobility_state = self.set_mobility_state()

        # decision making extra variables
        self.offline_neighbors = 0
        self.online_neighbors = 0
        self.moving_neighbors = 0
        self.observed_mobility_rate = 0
        
        self.online_info = 0
        self.offline_info = 0
        self.combined_info = 0

        # extra counters
        self.move_counter = 0  # count number of times the agent change its behavior to moving 
        self.stop_move_counter = 0 # count number of times the agent change its behavior to adopt to lock-down 
        self.speak_counter = 0 # count number of times the agent deside to speak and share its opinion online
        self.listen_counter = 0 # count number of times the agent deside to listen and update its opinion online
        

    ####################################################


    def set_mobility_state(self):

        if self.decision == 0:
            return State.NO_MOVE
        else:
            return State.MOVE    



    def update_opinion(self):

        if self.model.alpha > 0:

            neighbors = self.model.online_space.get_neighborhood(self.online_node, include_center = False) 
            self.online_neighbors = len(neighbors)

            if len(neighbors) > 0:
                
                other_agent = self.random.choice(self.model.online_space.get_cell_list_contents(neighbors))
                saved_opinion = self.opinion
                
                # other agent speek
                speak_prob = other_agent.opinion ** (1.0 / other_agent.tendency_to_share)

                if random.uniform(0, 1) < speak_prob:

                    other_agent.speak_counter += 1
                    self.listen_counter += 1

                    self.model.communicatin_count += 1

                    self.opinion = self.opinion + self.peer_trust * (other_agent.opinion - self.opinion)

                    if self.risk_sensitivity == 0:
                        self.opinion = self.opinion / 2.0
                    elif self.risk_sensitivity == 2:
                        self.opinion = (1.0 + self.opinion) / 2.0
                
                # current agent speek
                speak_prob = saved_opinion ** (1.0 / self.tendency_to_share)

                if random.uniform(0, 1) < speak_prob:

                    self.speak_counter += 1
                    other_agent.listen_counter +=1

                    self.model.communicatin_count += 1

                    other_agent.opinion = other_agent.opinion + other_agent.peer_trust * (saved_opinion - other_agent.opinion)

                    if other_agent.risk_sensitivity == 0:
                        other_agent.opinion = other_agent.opinion / 2.0
                    elif other_agent.risk_sensitivity == 2:
                        other_agent.opinion = (1.0 + other_agent.opinion) / 2.0

          
   
    def get_nighbours_mobility_rate(self):
        
        neighbors = self.model.physical_space.get_cell_list_contents([self.physical_pos])
        self.offline_neighbors = len(neighbors) - 1

        if self.offline_neighbors > 0:
            self.moving_neighbors = sum(1 for a in neighbors if a.unique_id != self.unique_id and a.old_decision == 1)
            self.observed_mobility_rate = self.moving_neighbors / self.offline_neighbors
          


    def make_mobililty_decision(self):

        # observe the neighbors behavior
        self.get_nighbours_mobility_rate()
        
        # combine online discussion and offline observation to construct a new relization about the risk 
        self.old_opinion = self.opinion
        self.online_info = self.model.alpha * self.opinion
        self.offline_info = (1 - self.model.alpha) * (1 - self.observed_mobility_rate)
        
        self.combined_info = self.online_info + self.offline_info
    
        # make a decision
        if self.combined_info < self.decision_th:
            self.decision = 1
        elif self.combined_info >= self.decision_th:
            self.decision = 0
            
        self.mobility_state = self.set_mobility_state()
        

        if self.decision != self.old_decision:
            # update the movement status counters
            if self.decision == 1:
                self.move_counter += 1
                self.model.start_moving_count += 1

            else:
                self.stop_move_counter += 1 
                self.model.stop_moving_count += 1

        # update the opinion
        self.opinion = self.combined_info


        # updtate opinion:
        # if self.model.last_step == 1:
        #     self.opinion = self.combined_info
        # elif self.model.last_step == 2:
        #     self.opinion = ( self.model.gamma * self.opinion ) + ( (1 - self.model.gamma) * self.combined_info )

        # when gamma = 0 -> O = I
        # when gamma = 1 -> O = O
        # self.opinion = ( self.model.gamma * self.opinion ) + ( (1 - self.model.gamma) * self.combined_info )


   
    def step(self):
        self.update_opinion()
        self.make_mobililty_decision()
        
        
