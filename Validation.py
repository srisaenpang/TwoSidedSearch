import config
import operator
import Create_Agents
import Agent
import copy

def validate(players_left, players_right):
    # Assortative
    if config.subjective == 0:
        ideal_match = {}
        # sort left
        ID_to_attractiveness_left = {}
        for player in players_left:
            ID_to_attractiveness_left[player.ID] = player.attractiveness
        sorted_left = sorted(ID_to_attractiveness_left.items(), key=operator.itemgetter(1))[::-1]
        # sort right
        ID_to_attractiveness_right = {}
        for player in players_right:
            ID_to_attractiveness_right[player.ID] = player.attractiveness
        sorted_right = sorted(ID_to_attractiveness_right.items(), key=operator.itemgetter(1))[::-1]
        for i in range(min(len(sorted_left), len(sorted_right))):
            ideal_match[sorted_left[i][0]] = (sorted_right[i][0], sorted_right[i][1])
            ideal_match[sorted_right[i][0]] = (sorted_left[i][0], sorted_left[i][1])
        # assign ideal matches
        for player in players_left:
            player.ideal_opponent = Create_Agents.ID_to_Agent[ideal_match[player.ID][0]]
        for player in players_right:
            player.ideal_opponent = Create_Agents.ID_to_Agent[ideal_match[player.ID][0]]

    # Non Assortative (Gale-Shapley Algorithm)
    elif config.subjective == 1:
        StableMatching = {}
        StableMatching_backup = {}
        for player in players_left:
            preferences = {}
            for potential_match in players_right:
                preferences[potential_match.ID] = player.get_reward(potential_match)
            ranked = [item[0] for item in sorted(preferences.items(), key=operator.itemgetter(1))[::-1]]
            StableMatching[player.ID] = [0, ranked, None]
        for player in players_right:
            preferences = {}
            for potential_match in players_left:
                preferences[potential_match.ID] = player.get_reward(potential_match)
            ranked = [item[0] for item in sorted(preferences.items(), key=operator.itemgetter(1))[::-1]]
            StableMatching[player.ID] = [0, ranked, None]
        StableMatching_backup = copy.deepcopy(StableMatching)

        # Left focused
        exit_the_loop = 0
        while(exit_the_loop == 0):
            exit_the_loop = 1
            for player in players_left:
                if StableMatching[player.ID][0] == 0 and len(StableMatching[player.ID][1]) > 0:
                    exit_the_loop = 0
                    target_ID = StableMatching[player.ID][1].pop(0)
                    if StableMatching[target_ID][0] == 0:
                        # (m, w) become engaged
                        StableMatching[player.ID][0] = 1
                        StableMatching[player.ID][2] = target_ID
                        StableMatching[target_ID][0] = 1
                        StableMatching[target_ID][2] = player.ID
                    else:
                        if StableMatching[target_ID][1].index(player.ID) < StableMatching[target_ID][1].index(StableMatching[target_ID][2]):
                            # m' become free
                            StableMatching[StableMatching[target_ID][2]][0] = 0
                            StableMatching[StableMatching[target_ID][2]][2] = None
                            # (m, w) become engaged
                            StableMatching[player.ID][0] = 1
                            StableMatching[player.ID][2] = target_ID
                            StableMatching[target_ID][2] = player.ID
        # assign ideal matches
        for player in players_left:
            player.ideal_opponent_left = Create_Agents.ID_to_Agent[StableMatching[player.ID][2]]
        for player in players_right:
            player.ideal_opponent_left = Create_Agents.ID_to_Agent[StableMatching[player.ID][2]]
        # print StableMatching
        # print [(key, StableMatching[key][2]) for key in StableMatching]

        # Right focused

        # un-engage all players
        StableMatching = copy.deepcopy(StableMatching_backup)
        # print  StableMatching
        exit_the_loop = 0
        while(exit_the_loop == 0):
            exit_the_loop = 1
            for player in players_right:
                if StableMatching[player.ID][0] == 0 and len(StableMatching[player.ID][1]) > 0:
                    exit_the_loop = 0
                    target_ID = StableMatching[player.ID][1].pop(0)
                    if StableMatching[target_ID][0] == 0:
                        # (m, w) become engaged
                        StableMatching[player.ID][0] = 1
                        StableMatching[player.ID][2] = target_ID
                        StableMatching[target_ID][0] = 1
                        StableMatching[target_ID][2] = player.ID
                    else:
                        if StableMatching[target_ID][1].index(player.ID) < StableMatching[target_ID][1].index(StableMatching[target_ID][2]):
                            # m' become free
                            StableMatching[StableMatching[target_ID][2]][0] = 0
                            StableMatching[StableMatching[target_ID][2]][2] = None
                            # (m, w) become engaged
                            StableMatching[player.ID][0] = 1
                            StableMatching[player.ID][2] = target_ID
                            StableMatching[target_ID][2] = player.ID

        # assign ideal matches
        for player in players_left:
            player.ideal_opponent_right = Create_Agents.ID_to_Agent[StableMatching[player.ID][2]]
        for player in players_right:
            player.ideal_opponent_right = Create_Agents.ID_to_Agent[StableMatching[player.ID][2]]
        # print StableMatching
        # print [(key,StableMatching[key][2]) for key in StableMatching]

    print "Ideal Opponent: Assigned!"