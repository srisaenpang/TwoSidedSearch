import string
import re
import random
import Strategy
import config
import math

class Agent:
    def __init__(self, ID, strategy):
        self.ID = ID
        self.attractiveness = round(random.uniform(config.attractiveness_min,config.attractiveness_max),config.random_decimal_point)
        self.interest = [round(random.uniform(config.interest_min,config.interest_max),config.random_decimal_point) for i in range(config.category_of_interest)]
        self.matched = 0
        self.strategy = strategy
        self.opponent = None
        self.ideal_opponent = None
        self.ideal_opponent_left = None
        self.ideal_opponent_right = None
        self.rank = None
        self.parameters = {}
        self.meeting_history = {i+1: [] for i in range(config.simulation_repeated)}
        self.reward_history = {i+1: [] for i in range(config.simulation_repeated)}

    def print_instance(self):
        print "  {0} {1} {2} {3} {4} {5}".format(self.ID, self.strategy, self.matched, self.attractiveness, self.interest, self.opponent)

    def print_reward(self, opponent = None):
        print "  {0} {1} {2}".format(self.ID, self.strategy, round(self.get_reward(opponent), config.random_decimal_point))

    def get_reward(self, opponent = None):
        if opponent == None:
            reward = config.non_matched_penalty
        else:
            # applied cosine similarity
            if config.subjective == 1:
                # reward = opponent.attractiveness * random.uniform(0,1) * config.subjectivity_constant*( sum([a*b for a,b in zip(self.interest,opponent.interest)]) / (math.sqrt(sum([a**2 for a in self.interest])) * math.sqrt(sum([b**2 for b in opponent.interest]))) )
                reward = opponent.attractiveness + random.uniform(0,1) * config.subjectivity_constant*( sum([a*b for a,b in zip(self.interest,opponent.interest)]) / (math.sqrt(sum([a**2 for a in self.interest])) * math.sqrt(sum([b**2 for b in opponent.interest]))) )
                # reward = opponent.attractiveness * random.uniform(-1,1) * config.subjectivity_constant*( sum([a*b for a,b in zip(self.interest,opponent.interest)]) / (math.sqrt(sum([a**2 for a in self.interest])) * math.sqrt(sum([b**2 for b in opponent.interest]))) )
                # reward = opponent.attractiveness + random.uniform(-1,1) * config.subjectivity_constant*( sum([a*b for a,b in zip(self.interest,opponent.interest)]) / (math.sqrt(sum([a**2 for a in self.interest])) * math.sqrt(sum([b**2 for b in opponent.interest]))) )
                # reward = opponent.attractiveness * config.subjectivity_constant*( sum([a*b for a,b in zip(self.interest,opponent.interest)]) / (math.sqrt(sum([a**2 for a in self.interest])) * math.sqrt(sum([b**2 for b in opponent.interest]))) )
                # reward = opponent.attractiveness + config.subjectivity_constant*( sum([a*b for a,b in zip(self.interest,opponent.interest)]) / (math.sqrt(sum([a**2 for a in self.interest])) * math.sqrt(sum([b**2 for b in opponent.interest]))) )
            elif config.subjective == 0:
                reward = opponent.attractiveness
        return reward

    def get_decision(self, opponent, time):
        score = self.get_reward(opponent)
        decision, self.parameters = Strategy.get_decision(self.strategy, self.parameters, score, time)
        return decision, score

    def learn(self):
        self.parameters = Strategy.learn(self.strategy, self.parameters, self.meeting_history, self.reward_history)
        # if self.strategy == 'threshold':
        #     print self.parameters

    def learn_overtime(self):
        self.parameters = Strategy.learn_overtime(self.strategy, self.parameters, self.meeting_history)
        # if self.strategy == 'threshold':
        #     print self.parameters

    def display_secret(self):
        print("*** secret *** attractiveness: {0}".format(self.attractiveness))

    def reflection(self, opponent_value):
        self.parameters = Strategy.reflection(self.strategy, self.parameters, opponent_value)