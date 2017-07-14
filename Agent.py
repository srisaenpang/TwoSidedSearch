import string
import re
import random
import Strategy
import config
import math
import Calculation

class Agent:
    def __init__(self, ID, strategy):
        self.ID = ID
        self.attractiveness = Calculation.get_uniformly_random_number(config.attractiveness_min, config.attractiveness_max, config.random_decimal_point)
        self.properties = [Calculation.get_uniformly_random_number(config.property_min, config.property_max, config.random_decimal_point) for i in range(config.category_of_property)]
        self.requirements = [Calculation.get_uniformly_random_number(config.requirement_min, config.requirement_max, config.random_decimal_point) for i in range(config.category_of_requirement)]
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
        self.replacement_prob = config.replacement_constant     # may depends on time_past and self_attractiveness

    def print_instance(self):
        print "  {0} {1} {2} {3} {4} {5} {6}".format(self.ID, self.strategy, self.matched, self.attractiveness, self.properties, self.requirements, self.opponent)

    def print_reward(self, opponent = None):
        print "  {0} {1} {2}".format(self.ID, self.strategy, self.get_reward(opponent))

    def get_reward(self, opponent = None):
        if opponent == None:
            reward = config.non_matched_reward
        else:
            # applied cosine similarity
            if config.subjective == 1:
                reward = opponent.attractiveness + config.subjectivity_constant * Calculation.cosine_similarity(self.requirements, opponent.properties)
            elif config.subjective == 0:
                reward = opponent.attractiveness
        return round(reward, config.random_decimal_point)

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

