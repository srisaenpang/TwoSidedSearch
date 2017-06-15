import string
import re
import random
import Strategy
import config

class Agent:

    parameters = {}

    def __init__(self, ID, strategy):
        self.ID = ID
        self.attractiveness = round(random.uniform(config.attractiveness_min,config.attractiveness_max),config.random_decimal_point)
        self.interest = [round(random.uniform(config.interest_min,config.interest_max),config.random_decimal_point) for i in range(config.category_of_interest)]
        self.matched = 0
        self.strategy = strategy
        self.opponent = None

    def print_instance(self):
        print "  {0} {1} {2} {3} {4} {5}".format(self.ID, self.strategy, self.matched, self.attractiveness, self.interest, self.opponent)

    def print_reward(self, opponent = None):
        if opponent == None:
            reward = config.non_matched_penalty
        else:
            reward = round(opponent.attractiveness + sum([a*b for a,b in zip(self.interest,opponent.interest)]), config.random_decimal_point)
        print "  {0} {1}".format(self.ID, reward)

    def get_reward(self, opponent = None):
        if opponent == None:
            reward = config.non_matched_penalty
        else:
            reward = round(opponent.attractiveness + sum([a*b for a,b in zip(self.interest,opponent.interest)]), config.random_decimal_point)
        return reward

    def get_decision(self, opponent):
        return Strategy.get_decision(self.strategy, self.parameters, opponent)

    def learn(self):
        self.parameters = Strategy.learn(self.strategy, self.parameters, self.get_reward(self.opponent))