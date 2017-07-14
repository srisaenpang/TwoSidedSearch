import numpy as np
import Agent
import config
import Strategy
import Calculation

ID_to_Agent = {None:None}
Left_ID = []
Right_ID = []

def gen_instancelist():
    ID = 0

    instancelist_left = []
    for strategy in config.player_left:
        for i in range(config.player_left[strategy]):
            new_agent = Agent.Agent(ID+i+1, strategy)
            new_agent.parameters = Strategy.inititialise_parameters(new_agent.strategy, new_agent.parameters)
            ID_to_Agent[ID+i+1] = new_agent
            Left_ID.append(ID+i+1)
            instancelist_left.extend([new_agent])
            Strategy.Strategy_Agent_dict[strategy].extend([new_agent])
        ID += config.player_left[strategy]

    instancelist_right = []
    for strategy in config.player_right:
        for i in range(config.player_right[strategy]):
            new_agent = Agent.Agent(ID+i+1, strategy)
            new_agent.parameters = Strategy.inititialise_parameters(new_agent.strategy, new_agent.parameters)
            ID_to_Agent[ID+i+1] = new_agent
            Right_ID.append(ID+i+1)
            instancelist_right.extend([new_agent])
            Strategy.Strategy_Agent_dict[strategy].extend([new_agent])
        ID += config.player_right[strategy]

    # initialise variables regarding Pearson's correlation coefficient
    Pearson_vector_xy = []
    # print instancelist
    if config.verbose:
        print "player_left"
        for instance in instancelist_left:
            instance.print_instance()
            # store data for Pearson's correlation coefficient calculation
            for opponent in instancelist_right:
                Pearson_vector_xy.append((opponent.attractiveness, instance.get_reward(opponent)))

        print "player_right"
        for instance in instancelist_right:
            instance.print_instance()
            # store data for Pearson's correlation coefficient calculation
            for opponent in instancelist_left:
                Pearson_vector_xy.append((opponent.attractiveness, instance.get_reward(opponent)))

        # Pearson's correlation coefficient calculation
        Pearson_vector_x, Pearson_vector_y = zip(*Pearson_vector_xy)
        print("Pearson's correlation coefficient: {0}".format(Calculation.pearson_correlation_coefficient(Pearson_vector_x, Pearson_vector_y)))

    return instancelist_left, instancelist_right
