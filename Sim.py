import numpy as np
import Create_Agents
import random
import config
import Agent
import Strategy
import Validation

players_left, players_right = Create_Agents.gen_instancelist()



for repeated in range(config.simulation_repeated):
    print "Repeated = {0}".format(repeated + 1)

    set_of_matchings = []
    for player in players_left + players_right:
        player.matched = 0
        player.opponent = None

    matching_pool_for_left = []
    for player in players_right:
        matching_pool_for_left.append(player)

    matching_pool_for_right = []
    for player in players_left:
        matching_pool_for_right.append(player)

    # print("mathcing pool:")
    # print len(matching_pool_for_left)
    # print len(matching_pool_for_right)
    #
    # # Testing
    # exit()

    for time in range(config.simulation_time):
        if config.verbose and config.verbose_simulation:
            print " Time = {0}".format(time+1)

        available_players_left = [player for player in players_left if player.matched == 0]
        available_players_right = [player for player in players_right if player.matched == 0]
        if config.verbose and config.verbose_simulation:
            print "  |alive_players_left| = {0}".format(len(available_players_left))
            print "  |alive_players_right| = {0}".format(len(available_players_right))

        available_matching_pool_for_left = [player for player in matching_pool_for_left]
        available_matching_pool_for_right = [player for player in matching_pool_for_right]
        if config.verbose and config.verbose_simulation:
            print "  |alive_matching_pool_for_left| = {0}".format(len(available_matching_pool_for_left))
            print "  |alive_matching_pool_for_right| = {0}".format(len(available_matching_pool_for_right))

        # print [player.ID for player in available_players_left]

        set_of_meetings = []

        # find a meeting for each 'Left' players
        while len(available_players_left) > 0:
            meeting = [random.sample(available_players_left,1)[0], random.sample(available_matching_pool_for_left,1)[0]]
            set_of_meetings.append(meeting)
            # remove these players from available list
            main_player, potential_match = meeting[0], meeting[1]
            available_players_left.remove(main_player)
            available_matching_pool_for_left.remove(potential_match)


        # find a meeting for each 'Right' players
        while len(available_players_right) > 0:
            meeting = [random.sample(available_players_right, 1)[0], random.sample(available_matching_pool_for_right, 1)[0]]
            set_of_meetings.append(meeting)
            # remove these players from available list
            main_player, potential_match = meeting[0], meeting[1]
            available_players_right.remove(main_player)
            available_matching_pool_for_right.remove(potential_match)

        for meeting in set_of_meetings:
            main_player, potential_match = meeting[0], meeting[1]
            main_player_decision, main_player_utility = main_player.get_decision(potential_match, time+1)
            main_player.meeting_history[repeated + 1].append((main_player_utility, main_player_decision))
            potential_match_decision, potential_match_utility = potential_match.get_decision(main_player, time+1)
            # potential_match.meeting_history[repeated + 1].append((potential_match_utility, potential_match_decision))

            if main_player_decision == "yes" and potential_match_decision == "yes":
                set_of_matchings.append(meeting)
                main_player, potential_match = meeting[0], meeting[1]
                main_player.matched, main_player.opponent = 1, potential_match
                # potential_match.matched, potential_match.opponent = 1, main_player
                # add new players here
                if config.replacement_mode == "None" or config.replacement_mode == "Prob-Entrance":
                    if main_player in players_left:
                        print main_player.ID, potential_match.ID
                        matching_pool_for_left.remove(potential_match)
                    else:
                        print main_player.ID, potential_match.ID
                        matching_pool_for_right.remove(potential_match)
                    # if config.replacement_mode == "Prob-Entrance":
                    #     # add new players with prob.
                    #     pass
                elif config.replacement_mode == "Clone":
                    pass    # since an agent with the same property replace immediately
                else:
                    raise ValueError("Replacement Mode Error: '{0}' is unknown".format(config.replacement_mode))

            # # Expectation modification when got refused
            # elif main_player_decision == "yes" and potential_match_decision == "no":
            #     main_player.reflection(main_player.get_reward(potential_match))
            # elif main_player_decision == "no" and potential_match_decision == "yes":
            #     potential_match.reflection(potential_match.get_reward(main_player))

        if config.verbose and config.verbose_simulation:
            print "  |number_of_matched_players| = {0}".format(len(set_of_matchings))

        # # Learning Parameters (overtime)
        # for player in players_left + players_right:
        #     player.display_secret()
        #     player.learn_overtime()

        # Market Entrance
        if config.replacement_mode == "Prob-Entrance":
            for player in players_left:
                if random.uniform(0,1) >= player.replacement_prob:
                    matching_pool_for_right.append(player)
            for player in players_right:
                if random.uniform(9,1) >= player.replacement_prob:
                    matching_pool_for_left.append(player)


    # Analysis
    if config.verbose_analysis:
        print " ## Analysis ##"
        if config.verbose_analysis_matched:
            for i, matching in enumerate(set_of_matchings):
                print " Matching {0}:".format(i)
                # matching[0].print_reward(matching[1])
                # matching[1].print_reward(matching[0])
                print "  main_player_ID: {0}, threshold: {1}, self_attactiveness: {2}, got matched with ID: {3}, obtained utility: {4}".format(matching[0].ID, matching[0].parameters['threshold'], matching[0].attractiveness, matching[1].ID,matching[0].get_reward(matching[1]))
                print "   {0}".format(matching[0].meeting_history)
                print "   {0}".format(matching[0].reward_history)

        if config.verbose_analysis_non_matched:
            print " Non-Matched:"
            for player in [non_matched_player for non_matched_player in players_left + players_right]:
                if player.matched == 0:
                    # player.print_reward()
                    print "  player_ID: {0}, threshold: {1}, self_attactiveness: {2}, obtained reward: {3}".format(player.ID, player.parameters['threshold'], player.attractiveness, player.get_reward(player.opponent))
                    print "   {0}".format(player.meeting_history)
                    print "   {0}".format(player.reward_history)

    # # Testing
    # exit()

    for strategy in config.strategies:
        number = 0.0
        sum_score = 0.0
        matched = 0.0
        for agent in Strategy.Strategy_Agent_dict[strategy]:
            number += 1
            sum_score += agent.get_reward(agent.opponent)
            matched += agent.matched
        print("{0}: ".format(strategy))
        print(" Matching Rate {0}".format(matched / number))
        if matched > 0.0:
            print(" Avg. Score {0}".format(sum_score / matched))

    # Learning Parameters
    for player in players_left + players_right:
        player.display_secret()
        player.reward_history[repeated + 1] = player.get_reward(player.opponent)
        print "reward: {0}".format(player.reward_history[repeated + 1])
        player.learn()
        print player.meeting_history

# Validation
if config.show_validation == 1:
    Validation.validate(players_left, players_right)
    # exit() # Skip Last Results
    if config.subjective == 0:
        overall_score = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
        overall_matched = np.array([[0, 0, 0], [0, 0, 0]])
        overall_number = np.array([0.0, 0.0, 0.0])
        for strategy in config.strategies:
            score = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
            matched = [[0, 0, 0], [0, 0, 0]]
            number = [0.0, 0.0, 0.0]
            for agent in Strategy.Strategy_Agent_dict[strategy]:
                if agent in players_left:
                    number[0] += 1
                    score[0][0] += agent.get_reward(agent.opponent)
                    score[1][0] += agent.get_reward(agent.ideal_opponent)
                    if agent.opponent: matched[0][0] += 1
                    if agent.ideal_opponent: matched[1][0] += 1
                elif agent in players_right:
                    number[1] += 1
                    score[0][1] += agent.get_reward(agent.opponent)
                    score[1][1] += agent.get_reward(agent.ideal_opponent)
                    if agent.opponent: matched[0][1] += 1
                    if agent.ideal_opponent: matched[1][1] += 1
            number[2] = number[0] + number[1]
            score[0][2] = score[0][0] + score[0][1]
            score[1][2] = score[1][0] + score[1][1]
            matched[0][2] = matched[0][0] + matched[0][1]
            matched[1][2] = matched[1][0] + matched[1][1]
            overall_number += np.array(number)
            overall_score += np.array(score)
            overall_matched += np.array(matched)

            print("{0}: ".format(strategy))
            if number[0] > 0:
                print(" Left:")
                print("  Matching Rate (Actual) {0}".format(matched[0][0] / number[0]))
                print("  Matching Rate (Ideal) {0}".format(matched[1][0] / number[0]))
                if matched[0][0] > 0:
                    print("  Avg. Score (excl. zeros) (Actual) {0}".format(score[0][0] / matched[0][0]))
                print("  Avg. Score (Actual) {0}".format(score[0][0] / number[0]))
                print("  Avg. Score (Ideal) {0}".format(score[1][0] / number[0]))
            if number[1] > 0:
                print(" Right:")
                print("  Matching Rate (Actual) {0}".format(matched[0][1] / number[1]))
                print("  Matching Rate (Ideal) {0}".format(matched[1][1] / number[1]))
                if matched[0][1] > 0:
                    print("  Avg. Score (excl. zeros) (Actual) {0}".format(score[0][1] / matched[0][1]))
                print("  Avg. Score (Actual) {0}".format(score[0][1] / number[1]))
                print("  Avg. Score (Ideal) {0}".format(score[1][1] / number[1]))
            if number[2] > 0:
                print(" Both:")
                print("  Matching Rate (Actual) {0}".format(matched[0][2] / number[2]))
                print("  Matching Rate (Ideal) {0}".format(matched[1][2] / number[2]))
                if matched[0][2] > 0:
                    print("  Avg. Score (excl. zeros) (Actual) {0}".format(score[0][2] / matched[0][2]))
                print("  Avg. Score (Actual) {0}".format(score[0][2] / number[2]))
                print("  Avg. Score (Ideal) {0}".format(score[1][2] / number[2]))

        print("Overall: ")
        if overall_number[0] > 0:
            print(" Left:")
            print("  Matching Rate (Actual) {0}".format(overall_matched[0][0] / overall_number[0]))
            print("  Matching Rate (Ideal) {0}".format(overall_matched[1][0] / overall_number[0]))
            if overall_matched[0][0] > 0:
                print("  Avg. Score (excl. zeros) (Actual) {0}".format(overall_score[0][0] / overall_matched[0][0]))
            print("  Avg. Score (Actual) {0}".format(overall_score[0][0] / overall_number[0]))
            print("  Avg. Score (Ideal) {0}".format(overall_score[1][0] / overall_number[0]))
        if overall_number[1] > 0:
            print(" Right:")
            print("  Matching Rate (Actual) {0}".format(overall_matched[0][1] / overall_number[1]))
            print("  Matching Rate (Ideal) {0}".format(overall_matched[1][1] / overall_number[1]))
            if overall_matched[0][1] > 0:
                print("  Avg. Score (excl. zeros) (Actual) {0}".format(overall_score[0][1] / overall_matched[0][1]))
            print("  Avg. Score (Actual) {0}".format(overall_score[0][1] / overall_number[1]))
            print("  Avg. Score (Ideal) {0}".format(overall_score[1][1] / overall_number[1]))
        if overall_number[2] > 0:
            print(" Both:")
            print("  Matching Rate (Actual) {0}".format(overall_matched[0][2] / overall_number[2]))
            print("  Matching Rate (Ideal) {0}".format(overall_matched[1][2] / overall_number[2]))
            if overall_matched[0][2] > 0:
                print("  Avg. Score (excl. zeros) (Actual) {0}".format(overall_score[0][2] / overall_matched[0][2]))
            print("  Avg. Score (Actual) {0}".format(overall_score[0][2] / overall_number[2]))
            print("  Avg. Score (Ideal) {0}".format(overall_score[1][2] / overall_number[2]))

    elif config.subjective == 1:
        overall_score = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
        overall_matched = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        overall_number = np.array([0.0, 0.0, 0.0])
        for strategy in config.strategies:
            score = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
            matched = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            number = [0.0, 0.0, 0.0]
            for agent in Strategy.Strategy_Agent_dict[strategy]:
                if agent in players_left:
                    number[0] += 1
                    score[0][0] += agent.get_reward(agent.opponent)
                    score[1][0] += agent.get_reward(agent.ideal_opponent_left)
                    score[2][0] += agent.get_reward(agent.ideal_opponent_right)
                    if agent.opponent: matched[0][0] += 1
                    if agent.ideal_opponent_left: matched[1][0] += 1
                    if agent.ideal_opponent_right: matched[2][0] += 1
                elif agent in players_right:
                    number[1] += 1
                    score[0][1] += agent.get_reward(agent.opponent)
                    score[1][1] += agent.get_reward(agent.ideal_opponent_left)
                    score[2][1] += agent.get_reward(agent.ideal_opponent_right)
                    if agent.opponent: matched[0][1] += 1
                    if agent.ideal_opponent_left: matched[1][1] += 1
                    if agent.ideal_opponent_right: matched[2][1] += 1
            number[2] = number[0] + number[1]
            score[0][2] = score[0][0] + score[0][1]
            score[1][2] = score[1][0] + score[1][1]
            score[2][2] = score[2][0] + score[2][1]
            matched[0][2] = matched[0][0] + matched[0][1]
            matched[1][2] = matched[1][0] + matched[1][1]
            matched[2][2] = matched[2][0] + matched[2][1]
            overall_number += np.array(number)
            overall_score += np.array(score)
            overall_matched += np.array(matched)

            print("{0}: ".format(strategy))
            if number[0] > 0:
                print(" Left:")
                print("  Matching Rate (Actual) {0}".format(matched[0][0] / number[0]))
                print("  Matching Rate (Left-based) {0}".format(matched[1][0] / number[0]))
                print("  Matching Rate (Right-based) {0}".format(matched[2][0] / number[0]))
                if matched[0][0] > 0:
                    print("  Avg. Score (excl. zeros) (Actual) {0}".format(score[0][0] / matched[0][0]))
                print("  Avg. Score (Actual) {0}".format(score[0][0] / number[0]))
                print("  Avg. Score (Left-based) {0}".format(score[1][0] / number[0]))
                print("  Avg. Score (Right-based) {0}".format(score[2][0] / number[0]))
            if number[1] > 0:
                print(" Right:")
                print("  Matching Rate (Actual) {0}".format(matched[0][1] / number[1]))
                print("  Matching Rate (Left-based) {0}".format(matched[1][1] / number[1]))
                print("  Matching Rate (Right-based) {0}".format(matched[2][1] / number[1]))
                if matched[0][1] > 0:
                    print("  Avg. Score (excl. zeros) (Actual) {0}".format(score[0][1] / matched[0][1]))
                print("  Avg. Score (Actual) {0}".format(score[0][1] / number[1]))
                print("  Avg. Score (Left-based) {0}".format(score[1][1] / number[1]))
                print("  Avg. Score (Right-based) {0}".format(score[2][1] / number[1]))
            if number[2] > 0:
                print(" Both:")
                print("  Matching Rate (Actual) {0}".format(matched[0][2] / number[2]))
                print("  Matching Rate (Left-based) {0}".format(matched[1][2] / number[2]))
                print("  Matching Rate (Right-based) {0}".format(matched[2][2] / number[2]))
                if matched[0][2] > 0:
                    print("  Avg. Score (excl. zeros) (Actual) {0}".format(score[0][2] / matched[0][2]))
                print("  Avg. Score (Actual) {0}".format(score[0][2] / number[2]))
                print("  Avg. Score (Left-based) {0}".format(score[1][2] / number[2]))
                print("  Avg. Score (Right-based) {0}".format(score[2][2] / number[2]))

        print("Overall: ")
        if overall_number[0] > 0:
            print(" Left:")
            print("  Matching Rate (Actual) {0}".format(overall_matched[0][0] / overall_number[0]))
            print("  Matching Rate (Left-based) {0}".format(overall_matched[1][0] / overall_number[0]))
            print("  Matching Rate (Right-based) {0}".format(overall_matched[2][0] / overall_number[0]))
            if overall_matched[0][0] > 0:
                print("  Avg. Score (excl. zeros) (Actual) {0}".format(overall_score[0][0] / overall_matched[0][0]))
            print("  Avg. Score (Actual) {0}".format(overall_score[0][0] / overall_number[0]))
            print("  Avg. Score (Left-based) {0}".format(overall_score[1][0] / overall_number[0]))
            print("  Avg. Score (Right-based) {0}".format(overall_score[2][0] / overall_number[0]))
        if overall_number[1] > 0:
            print(" Right:")
            print("  Matching Rate (Actual) {0}".format(overall_matched[0][1] / overall_number[1]))
            print("  Matching Rate (Left-based) {0}".format(overall_matched[1][1] / overall_number[1]))
            print("  Matching Rate (Right-based) {0}".format(overall_matched[2][1] / overall_number[1]))
            if overall_matched[0][1] > 0:
                print("  Avg. Score (excl. zeros) (Actual) {0}".format(overall_score[0][1] / overall_matched[0][1]))
            print("  Avg. Score (Actual) {0}".format(overall_score[0][1] / overall_number[1]))
            print("  Avg. Score (Left-based) {0}".format(overall_score[1][1] / overall_number[1]))
            print("  Avg. Score (Right-based) {0}".format(overall_score[2][1] / overall_number[1]))
        if overall_number[2] > 0:
            print(" Both:")
            print("  Matching Rate (Actual) {0}".format(overall_matched[0][2] / overall_number[2]))
            print("  Matching Rate (Left-based) {0}".format(overall_matched[1][2] / overall_number[2]))
            print("  Matching Rate (Right-based) {0}".format(overall_matched[2][2] / overall_number[2]))
            if overall_matched[0][2] > 0:
                print("  Avg. Score (excl. zeros) (Actual) {0}".format(overall_score[0][2] / overall_matched[0][2]))
            print("  Avg. Score (Actual) {0}".format(overall_score[0][2] / overall_number[2]))
            print("  Avg. Score (Left-based) {0}".format(overall_score[1][2] / overall_number[2]))
            print("  Avg. Score (Right-based) {0}".format(overall_score[2][2] / overall_number[2]))