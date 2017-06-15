import numpy as np
import Agent
import config

def gen_instancelist():
    ID = 0

    instancelist_left = []
    for strategy in config.player_left:
        instancelist_left.extend([ Agent.Agent(ID+i+1, strategy) for i in range(config.player_left[strategy])])
        ID += config.player_left[strategy]

    instancelist_right = []
    for strategy in config.player_right:
        instancelist_right.extend([Agent.Agent(ID + i + 1, strategy) for i in range(config.player_right[strategy])])
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
