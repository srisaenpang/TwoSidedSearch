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
            player_left_decision = player_left.get_decision(player_right, time)
            player_right_decision = player_right.get_decision(player_left, time)

            if player_left_decision == "yes" and player_right_decision == "yes":
                set_of_matchings.append(meeting)
                player_left, player_right = meeting[0], meeting[1]
                player_left.matched, player_left.opponent = 1, player_right
                player_right.matched, player_right.opponent = 1, player_left
                # add new players here
                if config.replacement_mode == "None":
                    pass
                elif config.replacement_mode == "Clone":
                    pass
                elif config.replacement_mode == "Prob-Entrance":
                    pass

            # Expectation modification when got refused
            elif player_left_decision == "yes" and player_right_decision == "no":
                player_left.reflection(player_left.get_reward(player_right))
            elif player_left_decision == "no" and player_right_decision == "yes":
                player_right.reflection(player_right.get_reward(player_left))

        if config.verbose and config.verbose_simulation:
            print "  |number_of_pairs_matched| = {0}".format(np.size(set_of_matchings)/2)

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
        player.learn()

# Validation
if config.show_validation == 1:
    Validation.validate(players_left, players_right)
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
