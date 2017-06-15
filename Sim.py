import numpy as np
import Create_Agents
import random
import config
import Agent

players_left, players_right = Create_Agents.gen_instancelist()

for repeated in range(config.simulation_repeated):
    print "Repeated = {0}".format(repeated + 1)

    set_of_matchings = []
    for player in players_left + players_right:
        player.matched = 0
        player.opponent = None

    for time in range(config.simulation_time):
        if config.verbose and config.verbose_simulation:
            print " Time = {0}".format(time+1)

        available_players_left = [player for player in players_left if player.matched == 0]
        available_players_right = [player for player in players_right if player.matched == 0]
        if config.verbose and config.verbose_simulation:
            print "  |alive_players_left| = {0}".format(np.size(available_players_left))
            print "  |alive_players_right| = {0}".format(np.size(available_players_right))

        # print [player.ID for player in available_players_left]

        set_of_meetings = []
        while np.size(available_players_left) > 0 and np.size(available_players_right) > 0:
            meeting = [random.sample(available_players_left,1)[0], random.sample(available_players_right,1)[0]]
            set_of_meetings.append(meeting)
            # remove these players from available list
            player_left, player_right = meeting[0], meeting[1]
            available_players_left.remove(player_left)
            available_players_right.remove(player_right)

        for meeting in set_of_meetings:
            player_left, player_right = meeting[0], meeting[1]
            player_left_decision = player_left.get_decision(player_right)
            player_right_decision = player_right.get_decision(player_left)

            if player_left_decision == "yes" and player_right_decision == "yes":
                set_of_matchings.append(meeting)
                player_left, player_right = meeting[0], meeting[1]
                player_left.matched, player_left.opponent = 1, player_right
                player_right.matched, player_right.opponent = 1, player_left
                # add new players here

        if config.verbose and config.verbose_simulation:
            print "  |set_of_matchings| = {0}".format(np.size(set_of_matchings))

    # Analysis
    if config.verbose_analysis:
        print " ## Analysis ##"
        if config.verbose_analysis_matched:
            for i, matching in enumerate(set_of_matchings):
                print " Matching {0}:".format(i)
                matching[0].print_reward(matching[1])
                matching[1].print_reward(matching[0])

        if config.verbose_analysis_non_matched:
            print " Non-Matched:"
            for player in [non_matched_player for non_matched_player in players_left + players_right]:
                if player.matched == 0:
                    player.print_reward()

    # Learning Parameters
    for player in players_left + players_right:
        player.learn()