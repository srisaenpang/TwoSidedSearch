import numpy as np
import Agent
import config
import Strategy

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

    # print instancelist
    if config.verbose:
        print "player_left"
        for instance in instancelist_left:
            instance.print_instance()

        print "player_right"
        for instance in instancelist_right:
            instance.print_instance()

    return instancelist_left, instancelist_right
