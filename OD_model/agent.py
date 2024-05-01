import random
import mesa
from enum import Enum

class State(Enum):
    HIGH = 1
    LOW = 0
    
class userAgent(mesa.Agent):
    
    def __init__( self, unique_id, model, inst_info):
    # def __init__( self, unique_id, model, inst_info, update_opinion_prob):

        
        super().__init__(unique_id, model)

        # self.shared = 0
        # self.updated = 0
        # self.sahring = 0
        # self.other_opinion = 0
        # self.other_agent_ID = 0
        
        # self.update_opinion_prob = update_opinion_prob

        self.opinion = random.uniform(0, 1) # initial opinion

        self.tendency_to_share = random.uniform(0, 1)
        self.inst_trust = random.uniform(0, 1)
        self.peer_trust = 1 - self.inst_trust
        
        temp = random.uniform(0, 1)
        if temp < 1.0/3.0:
            self.risk_sensitivity = 0 # low risk sensitivity
        else:
            temp2 = random.uniform(0, 1)
            if temp2 < 0.5:
                self.risk_sensitivity = 2 # high risk sensitivity
            else:
                self.risk_sensitivity = 1 # medium risk sensitivity

        # temp = random.uniform(0, 1)
        # if temp < 0.5:
        #     self.inst_trust = 0.5 * random.uniform(0, 1) + 0.5
        # else:
        #     self.inst_trust = 0.5 * random.uniform(0, 1)

        # processing institutional information
        # if inst_info > -1:
        #     self.inst_listen_prop = random.uniform(0, 1)
        #     self.inst_info = inst_info # institutional information

        #     if random.uniform(0 , 1) < self.inst_listen_prop:
        #         self.opinion = self.opinion + 1.0 * self.inst_trust * (inst_info - self.opinion)

        #         if self.risk_sensitivity == 0:
        #             self.opinion = self.opinion / 2.0
        #         elif self.risk_sensitivity == 2:
        #             self.opinion = (1.0 + self.opinion) / 2.0
 
        # set the state of the initial opinion
        self.opinion_state = self.set_opinion_state(self.opinion)


    '''
    A method to set the satet of the current opinion
    '''
    def set_opinion_state(self, opinion):
        if opinion <= 0.5:
            return State.LOW
        else:
            return State.HIGH
    

    '''
    A method to update the agent opinion based on trust and risk sensitivity 
    '''
    # def update_opinion(self, old_opinion, information , trust, listen_prop):
        
    #     if self.random.random() < listen_prop:
    #         # update the opinion based on trust
    #         new_opinion = old_opinion + trust * (information - old_opinion)

    #         # update the opinion based on risk sensitivity 
    #         if self.risk_sensitivity < 0:
    #             new_opinion = 0.5 * (1 + new_opinion)
    #         elif self.risk_sensitivity > 0:
    #             new_opinion = 0.5 * new_opinion

    #         self.opinion = new_opinion

    #         # update the opinion state
    #         self.opinion_state = self.set_opinion_state(self.opinion)

    '''
    This function perform the simplist version of the opinion update process (taking the average of all neighbors)
    '''    
    # def update_opinion_basic_DeGroot(self):
    #     # if(self.random.random() < self.update_opinion_prob):
    #     neighbors = self.model.grid.get_neighborhood(self.pos, include_center = True)
        
    #     if len(neighbors) > 1:
    #         # self.sahring = 1
    #         # Update opinion following DeGroot (weighted avergae of neighbors opinions)
    #         self.opinion = sum(a.opinion for a in self.model.grid.get_cell_list_contents(neighbors))/ len(neighbors)
    #         self.opinion_state = self.set_opinion_state(self.opinion)

    #     # else:
    #     #     self.sahring = 0


    '''
    The original Deffuant update function
    '''
    # def original_Deffuant(self):
    #     neighbors = self.model.grid.get_neighborhood(self.pos, include_center = False) 
    #     # select another agent randomly
    #     if len(neighbors) > 0:
    #         other_agent = self.random.choice(self.model.grid.get_cell_list_contents(neighbors))

    #         if abs(self.opinion - other_agent.opinion) < 0.5:
    #             saved_opinion = self.opinion
    #             self.opinion = self.opinion + self.peer_trust * (other_agent.opinion - self.opinion)
    #             other_agent.opinion = other_agent.opinion + other_agent.peer_trust * (saved_opinion - other_agent.opinion)

    '''
    This function is for simple opinion update process using only peer trust
    ''' 
    # def update_opinion_simple_Deffuant(self):
    #     # get all the connected neighbors
    #     neighbors = self.model.grid.get_neighborhood(self.pos, include_center = False) 
    #     # select another agent randomly
    #     if len(neighbors) > 0:
    #         other_agent = self.random.choice(self.model.grid.get_cell_list_contents(neighbors))
    #         saved_opinion = self.opinion
    #         self.opinion = self.opinion + self.peer_trust * (other_agent.opinion - self.opinion)
    #         other_agent.opinion = other_agent.opinion + other_agent.peer_trust * (saved_opinion - other_agent.opinion)


    '''
    This function is for opinion update process using peer trust - risk sensitivity 
    ''' 
    # def update_opinion_Deffuant_with_risk(self):
    #     # get all the connected neighbors
    #     neighbors = self.model.grid.get_neighborhood(self.pos, include_center = False) 
    #     # select another agent randomly
    #     if len(neighbors) > 0:
    #         other_agent = self.random.choice(self.model.grid.get_cell_list_contents(neighbors))
    #         saved_opinion = self.opinion
            
    #         self.opinion = self.opinion + self.peer_trust * (other_agent.opinion - self.opinion)

    #         if self.risk_sensitivity == 0:
    #             self.opinion = self.opinion / 2.0
    #         elif self.risk_sensitivity == 2:
    #             self.opinion = (1.0 + self.opinion) / 2.0

    #         other_agent.opinion = other_agent.opinion + other_agent.peer_trust * (saved_opinion - other_agent.opinion)

    #         if other_agent.risk_sensitivity == 0:
    #             other_agent.opinion = other_agent.opinion / 2.0
    #         elif other_agent.risk_sensitivity == 2:
    #             other_agent.opinion = (1.0 + other_agent.opinion) / 2.0


    
    # def update_opinion_Deffuant_with_risk2(self):
    #     # get all the connected neighbors
    #     neighbors = self.model.grid.get_neighborhood(self.pos, include_center = False) 
    #     # select another agent randomly
    #     if len(neighbors) > 0:
    #         other_agent = self.random.choice(self.model.grid.get_cell_list_contents(neighbors))
    #         saved_opinion = self.opinion

    #         if self.risk_sensitivity == 0:
    #             self.opinion = self.opinion / 2.0
    #         elif self.risk_sensitivity == 2:
    #             self.opinion = (1.0 + self.opinion) / 2.0

    #         self.opinion = self.opinion + self.peer_trust * (other_agent.opinion - self.opinion)

    #         if other_agent.risk_sensitivity == 0:
    #             other_agent.opinion = other_agent.opinion / 2.0
    #         elif other_agent.risk_sensitivity == 2:
    #             other_agent.opinion = (1.0 + other_agent.opinion) / 2.0

    #         other_agent.opinion = other_agent.opinion + other_agent.peer_trust * (saved_opinion - other_agent.opinion)


    '''
    This function is for opinion update process using all agent varibales (peer trust - risk sensitivity - tendency to share)
    '''
    def update_opinion_Deffuant_with_R_and_B(self):

        # self.updated = 0
        # self.shared = 0

        # self.other_opinion = 0
        # self.other_agent_ID = 0
        
        # get all the connected neighbors
        neighbors = self.model.grid.get_neighborhood(self.pos, include_center = False) 
        # select another agent randomly
        if len(neighbors) > 0:
            
            other_agent = self.random.choice(self.model.grid.get_cell_list_contents(neighbors))
            saved_opinion = self.opinion

            # self.other_opinion = other_agent.opinion
            # self.other_agent_ID = other_agent.unique_id

            
            # other_agent.updated = 0
            # other_agent.shared = 0
            
            # other agent speek
            speak_prob = other_agent.opinion ** (1.0 / other_agent.tendency_to_share)
            if random.uniform(0, 1) < speak_prob:
                self.opinion = self.opinion + self.peer_trust * (other_agent.opinion - self.opinion)

                if self.risk_sensitivity == 0:
                    self.opinion = self.opinion / 2.0
                elif self.risk_sensitivity == 2:
                    self.opinion = (1.0 + self.opinion) / 2.0

                # self.updated = 1
                # other_agent.shared = 1

                self.opinion_state = self.set_opinion_state(self.opinion)
             

            # current agent speek
            speak_prob = self.opinion ** (1.0 / self.tendency_to_share)
            if random.uniform(0, 1) < speak_prob:
                other_agent.opinion = other_agent.opinion + other_agent.peer_trust * (saved_opinion - other_agent.opinion)

                if other_agent.risk_sensitivity == 0:
                    other_agent.opinion = other_agent.opinion / 2.0
                elif other_agent.risk_sensitivity == 2:
                    other_agent.opinion = (1.0 + other_agent.opinion) / 2.0

                # self.shared = 1
                # other_agent.updated = 1

                other_agent.opinion_state = other_agent.set_opinion_state(other_agent.opinion)


    '''
    This function is for opinion update process using all agent varibales (peer trust - risk sensitivity - tendency to share)
    with changing the order of steps
    '''
    # def update_opinion_Deffuant_change_order(self):

    #     # get all the connected neighbors
    #     neighbors = self.model.grid.get_neighborhood(self.pos, include_center = False) 
    #     # select another agent randomly
    #     if len(neighbors) > 0:
            
    #         other_agent = self.random.choice(self.model.grid.get_cell_list_contents(neighbors))
    #         saved_opinion = self.opinion

    #         # other agent speek
    #         speak_prob = other_agent.opinion ** (1.0 / other_agent.tendency_to_share)
    #         if random.uniform(0, 1) < speak_prob:

    #             if self.risk_sensitivity == 0:
    #                 self.opinion = self.opinion / 2.0
    #             elif self.risk_sensitivity == 2:
    #                 self.opinion = (1.0 + self.opinion) / 2.0

    #             self.opinion = self.opinion + self.peer_trust * (other_agent.opinion - self.opinion)

    #         # current agent speek
    #         speak_prob = self.opinion ** (1.0 / self.tendency_to_share)
    #         if random.uniform(0, 1) < speak_prob:
                
    #             if other_agent.risk_sensitivity == 0:
    #                 other_agent.opinion = other_agent.opinion / 2.0
    #             elif other_agent.risk_sensitivity == 2:
    #                 other_agent.opinion = (1.0 + other_agent.opinion) / 2.0

    #             other_agent.opinion = other_agent.opinion + other_agent.peer_trust * (saved_opinion - other_agent.opinion)


    '''
    A method for executing the peer-to-peer communication based on the destials provided in the C code file 
    '''
    # def communicate(self):
    #     # get all the connected neighbors
    #     neighbors = self.model.grid.get_neighborhood(self.pos, include_center = False)        
    
    #     # select another agent randomly
    #     if len(neighbors) > 0:
    #         other_agent = self.random.choice(self.model.grid.get_cell_list_contents(neighbors))

    #         # save the opinion of the other agent
    #         other_saved_opinion = other_agent.opinion

    #         # the current agent speaks
    #         speak_prob = self.opinion ** (1.0 / self.tendency_to_share)
    #         if random.uniform(0, 1) < speak_prob:
    #             other_agent.opinion = other_agent.opinion + other_agent.peer_trust * (self.opinion - other_agent.opinion)

    #             if self.risk_sensitivity == 2: # alarmist speaker
    #                 if other_agent.risk_sensitivity == 2 and self.opinion >= 0.5: # both agents are alarmist
    #                     other_agent.opinion = (1.0 + other_agent.opinion) / 2.0 # listener increase alarmism
    #                 if self.opinion < 0.5: 
    #                     other_agent.opinion = other_agent.opinion / 2.0 # listener decrease alarmism

    #             else: # not alarmist spreaker
    #                 if self.opinion > 0.5:
    #                     other_agent.opinion = (1.0 + other_agent.opinion) / 2.0

    #         # the other agent speaks
    #         other_speak_prob = other_saved_opinion ** (1.0 / other_agent.tendency_to_share)
    #         if random.uniform(0, 1) < other_speak_prob:
    #             self.opinion = self.opinion + 1.0 * self.peer_trust * (other_saved_opinion - self.opinion)

    #             if other_agent.risk_sensitivity == 2: 
    #                 if self.risk_sensitivity == 2 and other_saved_opinion >= 0.5:
    #                     self.opinion = (1.0 + self.opinion) / 2.0
    #                 if other_saved_opinion < 0.5:
    #                     self.opinion = self.opinion / 2.0

    #             else:
    #                 if other_saved_opinion > 0.5:
    #                     self.opinion = (1.0 + self.opinion) / 2.0


    #         self.opinion_state = self.set_opinion_state(self.opinion)
    #         other_agent.opinion_state = other_agent.set_opinion_state(other_agent.opinion)
        
             
    
    def step(self):
        # This is the finctions for the complete communication process for the ruplicated model
        # self.communicate()
        
        # ******************************
        # Following are the functions calls for the incrementally extended model 
        # ******************************

        # self.update_opinion_basic_DeGroot()
        
        # self.update_opinion_simple_Deffuant()
        # self.update_opinion_Deffuant_with_risk()
        # self.update_opinion_Deffuant_with_risk2()
        self.update_opinion_Deffuant_with_R_and_B()
        # self.update_opinion_Deffuant_change_order()

        # self.original_Deffuant()
        
        # self.communicate()
