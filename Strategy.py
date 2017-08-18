import numpy as np
import config
import Agent
import itertools
import math
import collections
# import PALO_calculation
import copy

Strategy_Agent_dict = {key: [] for key in config.strategies}

def inititialise_parameters(strategy, parameters):
    if strategy == "random":
        parameters['random-threshold'] = config.random_threshold

    elif strategy == "threshold":
        parameters['threshold'] = config.initial_VO          # may need to change this
        parameters['opp_dist'] = {}
        parameters['opp_prob'] = {}
        parameters['opp_answer_dist'] = {}
        parameters['opp_yes_prob'] = {}
        parameters['threshold_history'] = [parameters['threshold']]
        parameters['V'] = {}

    # elif strategy == "PALO":
    #     parameters['Theta'] = config.PALO_threshold
    #     parameters['Tau'] = [float(i)/10**config.PALO_decimal_point for i in range((config.lower_bound)*(10**config.PALO_decimal_point),(config.upper_bound)*(10**config.PALO_decimal_point)+1)]
    #     parameters['epsilon'] = config.PALO_epsilon
    #     parameters['delta'] = config.PALO_delta

    elif strategy == "best-so-far":
        parameters['threshold'] = config.threshold
        parameters['opp_dist'] = {}
        parameters['opp_prob'] = {}
        parameters['opp_answer_dist'] = {}
        parameters['opp_yes_prob'] = {}
        parameters['threshold_history'] = [parameters['threshold']]
        # parameters['best-so-far'] = config.best_so_far

    elif strategy == "mean-so-far":
        parameters['list-so-far'] = []

    elif strategy == "secretary":
        parameters['best-so-far'] = config.best_so_far

    elif strategy == "andria":
        parameters['top-three'] = []

    return parameters

def get_decision(strategy, parameters, score, time):
    decision = None
    if strategy == "random":
        if score >= parameters['random-threshold']:
            decision = "yes"
        else:
            decision = "no"

    elif strategy == "threshold":
        if score >= parameters['threshold']:
            decision = "yes"  # Instant Reward is higher
        else:
            decision = "no"  # Reservation Utility is higher

        # if config.apply_discounted_utility == 0:
        #     if score >= parameters['threshold']:
        #         decision = "yes"    # E[reward(yes)] is higher
        #     else:
        #         decision = "no"     # E[value(waiting)] is higher
        # elif config.apply_discounted_utility == 1:
        #     if score >= parameters['threshold'] * config.discounting_factor**(time - config.t_0):
        #         decision = "yes"    # E[reward(yes)] is higher
        #     else:
        #         decision = "no"     # E[value(waiting)] is higher

    # elif strategy == "PALO":
    #     if score >= parameters['Theta']:
    #         decision = "yes"
    #     else:
    #         decision = "no"

    elif strategy == "best-so-far":
        if config.apply_discounted_utility == 0:
            if score >= parameters['threshold']:
                decision = "yes"    # E[reward(yes)] is higher
            else:
                decision = "no"     # E[value(waiting)] is higher
        elif config.apply_discounted_utility == 1:
            if score >= parameters['threshold'] * config.discounting_factor**(time - config.t_0):
                decision = "yes"    # E[reward(yes)] is higher
            else:
                decision = "no"     # E[value(waiting)] is higher
        # if score >= parameters['best-so-far']:
        #     parameters['best-so-far'] = score
        #     decision = "yes"
        # else:
        #     decision = "no"

    elif strategy == "mean-so-far":
        parameters['list-so-far'].append(score)
        if score >= np.mean(parameters['list-so-far']):
            decision = "yes"
        else:
            decision = "no"

    elif strategy == "secretary":
        if score >= parameters['best-so-far']:
            parameters['best-so-far'] = score
            if time >= config.secretary_calibration_time:
                decision = "yes"
            else:
                decision = "no"
        else:
            decision = "no"

    elif strategy == "andria":
        parameters['top-three'].append(score)
        parameters['top-three'] = sorted(parameters['top-three'])[::-1][0:3]
        if time >= config.andria_calibration_time:
            if score >= parameters['top-three'][2]:
                decision = "yes"
            else:
                decision = "no"
        else:
            decision = "no"

    if decision == None:
        raise ValueError("Decision Error: 'None'")

    return decision, parameters


# def learn_overtime(strategy, parameters, meeting_history):
#
#     if strategy == "random":
#         pass
#
#     elif strategy == "threshold":
#         pass
#
#     # elif strategy == "PALO":
#     #     pass
#
#     elif strategy == "best-so-far":
#         pass
#
#     elif strategy == "mean-so-far":
#         pass
#
#     elif strategy == "secretary":
#         pass
#
#     elif strategy == "andria":
#         pass
#
#     return parameters

def learn(strategy, parameters, meeting_history, reward_history, opponent_answer, round_update, Bellman_epsilon, Bellman_gamma):

    early_stop = None

    if strategy == "random":
        pass

    elif strategy == "threshold":
        # if reward == 0:
        #     print("threshold is reduced from {0} to {1}".format(parameters['threshold'], parameters['threshold']*config.threshold_reduction))
        #     parameters['threshold'] = parameters['threshold'] * config.threshold_reduction
        # else:
        #     if reward > parameters['threshold']:
        #         parameters['threshold'] = reward

        parameters['opp_dist'] = {}
        parameters['opp_prob'] = {}
        # parameters['opp_answer_dist'] = {}
        parameters['opp_yes_prob'] = {}

        time = sum([1 for key in meeting_history if meeting_history[key] != []])

        for key in meeting_history:
            if key >= time * config.forgetting_factor and meeting_history[key] != []:      # windowing
                for record in meeting_history[key]:
                    try:
                        parameters['opp_dist'][record[0]] += 1
                    except KeyError:
                        parameters['opp_dist'][record[0]] = 1
                    # if record[1] == 'yes':
                    #     try:
                    #         if reward_history[key] == record[0]:
                    #             parameters['opp_answer_dist'][(record[0], 'yes')] += 1
                    #         elif reward_history[key] != record[0]:
                    #             parameters['opp_answer_dist'][(record[0], 'no')] += 1
                    #     except KeyError:
                    #         if reward_history[key] == record[0]:
                    #             parameters['opp_answer_dist'][(record[0], 'yes')] = 1
                    #             if (record[0], 'no') not in parameters['opp_answer_dist']:
                    #                 parameters['opp_answer_dist'][(record[0], 'no')] = 0
                    #         elif reward_history[key] != record[0]:
                    #             parameters['opp_answer_dist'][(record[0], 'no')] = 1
                    #             if (record[0], 'yes') not in parameters['opp_answer_dist']:
                    #                 parameters['opp_answer_dist'][(record[0], 'yes')] = 0


        opponent_answer_dist = {}
        for key in opponent_answer:
            if key >= time * config.forgetting_factor and opponent_answer[key] != []:
                for record in opponent_answer[key]:
                    if record[0] not in opponent_answer_dist:
                        opponent_answer_dist[record[0]] = [0, 0]

                    if record[1] == 'yes':
                        opponent_answer_dist[record[0]][0] += 1
                    elif record[1] == 'no':
                        opponent_answer_dist[record[0]][1] += 1
                    else:
                        raise ValueError
                        exit()

        print 'opponent_answer_dist', opponent_answer_dist
        print 'threshold_history', parameters['threshold_history']
        print 'reward_history', reward_history
        # exit()

        for opponent in parameters['opp_dist']:
            parameters['opp_prob'][opponent] = float(parameters['opp_dist'][opponent]) / sum(parameters['opp_dist'].values())

        if config.method_epsilon_threshold == 0 and config.method_1nn == 1:
            for opponent in parameters['opp_dist']:
                try:
                    parameters['opp_yes_prob'][opponent] = float(opponent_answer_dist[opponent][0]) / (
                    opponent_answer_dist[opponent][0] + opponent_answer_dist[opponent][1])
                    # if config.exploration_mode == 2:
                    #     pass  # add 5nn here !
                except KeyError:
                    parameters['opp_yes_prob'][opponent] = 'unk'  # set unknown prob to 1.0
                    opponent_answer_dist[opponent] = ['unk', 'unk']
                    # parameters['opp_yes_prob'][opponent] = 'unk'
            print 'parameters[opp_dist]', parameters['opp_dist']
            print 'parameters[opp_yes_prob][opponent]', parameters['opp_yes_prob']
            known_yes_prob = {key: parameters['opp_yes_prob'][key] for key in parameters['opp_yes_prob'] if parameters['opp_yes_prob'][key] != 'unk'}
            print known_yes_prob
            for key in parameters['opp_yes_prob']:
                count_yes, count_no = 0.0, 0.0
                if parameters['opp_yes_prob'][key] == 'unk':
                    mininum_distance = min([abs(key - x) for x in known_yes_prob])
                    mininum_distance_key = [key_check for key_check in known_yes_prob.keys() if abs(key_check - key) == mininum_distance]
                    count_yes = sum([opponent_answer_dist[x][0] for x in mininum_distance_key])
                    count_no = sum([opponent_answer_dist[x][1] for x in mininum_distance_key])
                    parameters['opp_yes_prob'][key] = count_yes / (count_yes + count_no)
                    if parameters['opp_yes_prob'][key] > 1.0:
                        print "wow"
                        exit()
            # print parameters['opp_yes_prob']
            # exit()

        elif config.method_epsilon_threshold == 1:
            if not opponent_answer_dist:
                return 0, parameters
            min_epsilon_threshold = max([key+0.00001 for key in opponent_answer_dist])
            min_epsilon_threshold_utility = float(sum([opponent_answer_dist[opponent][1] for opponent in opponent_answer_dist])) / sum([opponent_answer_dist[opponent][0] + opponent_answer_dist[opponent][1] for opponent in opponent_answer_dist])
            # print min_epsilon_threshold_utility
            for key in opponent_answer_dist:
                potential_epsilon = float(sum([opponent_answer_dist[opponent][0] for opponent in opponent_answer_dist if opponent >= key]) + sum([opponent_answer_dist[opponent][1] for opponent in opponent_answer_dist if opponent < key])) / sum([opponent_answer_dist[opponent][0] + opponent_answer_dist[opponent][1] for opponent in opponent_answer_dist])
                # print potential_epsilon
                if potential_epsilon < min_epsilon_threshold_utility:
                    min_epsilon_threshold_utility = potential_epsilon
                    min_epsilon_threshold = key

            print 'min_epsilon_threshold', min_epsilon_threshold
            print 'min_epsilon_threshold_utility', min_epsilon_threshold_utility

            for opponent in parameters['opp_prob']:
                if opponent >= min_epsilon_threshold:
                    parameters['opp_yes_prob'][opponent] = min_epsilon_threshold_utility
                elif opponent < min_epsilon_threshold:
                    parameters['opp_yes_prob'][opponent] = 1.0 - min_epsilon_threshold_utility

        else:
            raise KeyError, "Method Error"
            # for opponent in parameters['opp_dist']:
            #     try:
            #         parameters['opp_yes_prob'][opponent] = float(opponent_answer_dist[opponent][0]) / (
            #         opponent_answer_dist[opponent][0] + opponent_answer_dist[opponent][1])
            #         # if config.exploration_mode == 2:
            #         #     pass  # add 5nn here !
            #     except KeyError:
            #         parameters['opp_yes_prob'][opponent] = 1.0  # set unknown prob to 1.0
            #         opponent_answer_dist[opponent] = ['unk', 'unk']
            #         # parameters['opp_yes_prob'][opponent] = 'unk'

        print 'opp_yes_prob', parameters['opp_yes_prob']
        # print min_epsilon_threshold
        # print min_epsilon_threshold_utility
        print 'opponent_answer_dist', opponent_answer_dist


        print 'opp_answer_dist', parameters['opp_answer_dist']
        print 'opponent_answer', opponent_answer

        print 'opponent_answer_dist', opponent_answer_dist
        print 'opp_yes_prob', parameters['opp_yes_prob']
        print 'opp_dist', parameters['opp_dist']

        # exit()

        # if config.exploration_mode == 0 or config.exploration_mode == 1:
        #     pass
        # elif config.exploration_mode == 2:
        #     pass



        sorted_opponent = sorted([opponent for opponent in parameters['opp_yes_prob']])

        for opponent in sorted_opponent:
            # parameters['V'][opponent] = config.initial_VO
            parameters['V'][opponent] = parameters['threshold']
            # if opponent not in parameters['V']:
            #     parameters['V'][opponent] = parameters['threshold']      # later opponents may start with current threshold instead
        print "V_O: {0}".format([(opponent, parameters['V'][opponent]) for opponent in sorted_opponent])

        # exit()

        # flag_1 = 0
        # for opponent in sorted_opponent[::-1]:
        #     if flag_1 == 1:
        #         parameters['opp_yes_prob'][opponent] = 1.0
        #     elif parameters['opp_yes_prob'][opponent] == 1.0:
        #         flag_1 = 1
        # possibly inherit the prob from the nearest neighbour
        # nearest_neighbour = {}
        # sorted_known_opponent = sorted([opponent for opponent in parameters['opp_yes_prob'] if parameters['opp_yes_prob'][opponent] != 'unk'])
        # print sorted_known_opponent, parameters['opp_yes_prob']
        # for opponent in parameters['opp_yes_prob']:
        #     self_excluded_sorted_known_opponent = [x for x in sorted_known_opponent if x!= opponent]
        #     if self_excluded_sorted_known_opponent:
        #         nearest_neighbour[opponent] = self_excluded_sorted_known_opponent[ np.argmin(abs(np.subtract(self_excluded_sorted_known_opponent, opponent))) ]
        # # print sorted_opponent
        # # print nearest_neighbour
        # for opponent in parameters['opp_yes_prob']:
        #     if parameters['opp_yes_prob'][opponent] == 'unk':
        #         try:
        #             parameters['opp_yes_prob'][opponent] = parameters['opp_yes_prob'][nearest_neighbour[opponent]]
        #         except KeyError:
        #             print "*** no nearest neighbour, set prob to 0.5 ***"
        #             parameters['opp_yes_prob'][opponent] = 0.5



        # # self yes prob
        # self_yes_prob = {}
        # for opponent in sorted_opponent:
        #     if opponent >= parameters['threshold']:
        #         self_yes_prob[opponent] = 1.0
        #     else:
        #         self_yes_prob[opponent] = 0.0

        # print parameters['opp_dist']
        # print sum(parameters['opp_dist'].values())
        # print parameters['opp_answer_dist']

        # print (parameters['opp_prob'])
        if config.force_uniform_opponent_prob == 1:
            for key in parameters['opp_prob']:
                parameters['opp_prob'][key] = 1.0 / len(parameters['opp_prob'])

        # print (parameters['opp_prob'])
        # if time == 2:
        #     exit()

        print "opp_dist: {0}".format([(opponent, parameters['opp_dist'][opponent]) for opponent in sorted_opponent])
        print "opp_prob: {0}".format([(opponent, parameters['opp_prob'][opponent]) for opponent in sorted_opponent])
        print "opp_yes_prob: {0}".format([(opponent, parameters['opp_yes_prob'][opponent]) for opponent in sorted_opponent])
        # print "opp_answer_dist: {0}".format([(opponent, parameters['opp_answer_dist'][(opponent, 'yes')], parameters['opp_answer_dist'][(opponent, 'no')]) for opponent in sorted_opponent])

        print 'threshold', parameters['threshold']

        matchable_probability = {opp: (parameters['opp_prob'][opp] * parameters['opp_yes_prob'][opp]) for opp in parameters['opp_dist'] if opp >= parameters['threshold']}
        weight_average_matchable_utility = sum([opp * matchable_probability[opp] for opp in matchable_probability])
        try:
            weight_average_matchable_utility = weight_average_matchable_utility / sum(matchable_probability.values())
        except:
            pass

        r = Bellman_gamma
        p = sum(matchable_probability.values())
        u_o = weight_average_matchable_utility

        reservation_utility = r * p * u_o / (1 - r + (r * p))

        print reservation_utility

        print {opp: (parameters['opp_prob'][opp] , parameters['opp_yes_prob'][opp]) for opp in parameters['opp_dist'] if opp >= parameters['threshold']}
        print 'sum of matchable_probability.values()', sum(matchable_probability.values())
        print 'matchable_probability', matchable_probability
        print 'weight_average_matchable_utility', weight_average_matchable_utility

        print 'r', r
        print 'p', p
        print  'u_o', u_o

        # if time == 1:
        #     exit()


        print "threshold updated: from: {0}".format(parameters['threshold'])

        if config.old_method == 2:
            parameters['threshold'] = parameters['threshold'] + ( 1.0 * (reservation_utility - parameters['threshold']) )

        elif config.old_method == 1:
            exit_the_loop = 0
            last_policy = None
            current_policy = parameters['threshold']
            print "*** Bellman Calculation ***"
            while exit_the_loop == 0:
                # Value function update
                V_O_previous = copy.deepcopy(parameters['V'])
                print "V_O_previous: {0}".format([(opp, V_O_previous[opp]) for opp in sorted_opponent])
                for opponent in sorted_opponent:
                    if opponent >= current_policy:
                        print "*** {0} is more than current_policy ***".format(opponent)
                        print parameters['opp_yes_prob'][opponent] * opponent
                        print (1-parameters['opp_yes_prob'][opponent]) * sum([parameters['opp_prob'][opp] * Bellman_gamma * V_O_previous[opp] for opp in sorted_opponent])
                        parameters['V'][opponent] = (parameters['opp_yes_prob'][opponent] * opponent) + ((1-parameters['opp_yes_prob'][opponent]) * sum([parameters['opp_prob'][opp] * Bellman_gamma * V_O_previous[opp] for opp in sorted_opponent]))
                        print ("V_{0} = {1}".format(opponent, parameters['V'][opponent]))
                    elif opponent < current_policy:
                        print "*** {0} is less than current_policy ***".format(opponent)
                        print [parameters['opp_prob'][opp] * Bellman_gamma * V_O_previous[opp] for opp in sorted_opponent]
                        parameters['V'][opponent] = sum([parameters['opp_prob'][opp] * Bellman_gamma * V_O_previous[opp] for opp in sorted_opponent])
                        print ("V_{0} = {1}".format(opponent, parameters['V'][opponent]))
                print "V_O: {0}".format([(opp, parameters['V'][opp]) for opp in sorted_opponent])

                # Policy update
                print [parameters['opp_prob'][opp] * Bellman_gamma * parameters['V'][opp] for opp in sorted_opponent]
                current_policy = sum([parameters['opp_prob'][opp] * Bellman_gamma * parameters['V'][opp] for opp in sorted_opponent])
                sumprob=sum([parameters['opp_prob'][opp] for opp in sorted_opponent])
                print "sum of probs=", sumprob
                print "current_policy: {0}".format(current_policy)

                if last_policy != None:
                    if abs(current_policy - last_policy) <= Bellman_epsilon:
                        print "*** {0} is close to {1} enough, exit the loop ***".format(current_policy, last_policy)
                        exit_the_loop = 1

                last_policy = current_policy

            # # new_threshold = sum([parameters['opp_prob'][opponent] * ((parameters['opp_yes_prob'][opponent] * opponent) + ((1-parameters['opp_yes_prob'][opponent]) * config.discounting_factor * parameters['threshold'])) for opponent in parameters['opp_dist']])
            # new_threshold = sum([parameters['opp_prob'][opponent] * ((parameters['opp_yes_prob'][opponent] * self_yes_prob[opponent] * opponent) + ((1-(parameters['opp_yes_prob'][opponent] * self_yes_prob[opponent])) * config.discounting_factor * parameters['threshold'])) for opponent in parameters['opp_dist']])
            new_threshold = current_policy
            parameters['threshold'] = new_threshold
            # print [parameters['opp_prob'][opponent] * parameters['opp_yes_prob'][opponent] * opponent for opponent in parameters['opp_dist']]

        elif config.old_method == 0:
            parameters['threshold'] = parameters['threshold'] + ( Bellman_epsilon * (reservation_utility - parameters['threshold']) )

        print "threshold updated: to: {0}".format(parameters['threshold'])
        if round_update == 1:
            parameters['threshold_history'].append(parameters['threshold'])
        # early stop calculation
        early_stop = 0
        if len(parameters['threshold_history'])>=2:
            if abs(parameters['threshold_history'][-1] - parameters['threshold_history'][-2]) <= config.early_stop_epsilon:
                early_stop = 1
        print ("thresh_history: {0}".format({i + 1: round(threshold, config.random_decimal_point) for i, threshold in enumerate(parameters['threshold_history'])}))
        print ("reward_history: {0}".format(reward_history))
        print parameters['opp_yes_prob']
        # exit()
        parameters['opp_answer_dist'] = opponent_answer_dist


    # elif strategy == "PALO":
    #     delta = {}
    #     L = {}
    #     Tau = {}
    #     Theta = {1: parameters['Theta']}
    #     Delta = {}
    #     q = {}
    #     Q = [[record for record in meeting_history[repeat]] for repeat in meeting_history]
    #     for j in itertools.count(1):
    #         print ("j: {0}".format(j))
    #         exit_both_loop = 0
    #         if j not in Theta:
    #             Theta[j] = Theta[j-1]
    #             print ("copied Theta[j]: {0}".format(Theta[j]))
    #         delta[j] = (6 * parameters['delta']) / (j ** 2 * math.pi ** 2)
    #         print ("delta[j]: {0}".format(delta[j]))
    #         Tau[Theta[j]] = [Theta_i for Theta_i in parameters['Tau'] if Theta_i <= parameters['Theta'] + config.PALO_neighbour_range and Theta_i >= parameters['Theta'] - config.PALO_neighbour_range and Theta_i != parameters['Theta']]
    #         print ("Tau[Theta[j]]: {0}".format(Tau[Theta[j]]))
    #         L[j] = math.ceil(2 * (PALO_calculation.caret(Theta[j], Tau[Theta[j]], meeting_history, reward_history) / parameters['epsilon'])**2 * math.log(2 * len(Tau[Theta[j]]) / delta[j]))
    #         print ("L[j]: {0}".format(L[j]))
    #         # print PALO_calculation.caret(Theta[j], Tau[Theta[j]], meeting_history, reward)
    #         for Theta_dash in Tau[Theta[j]]:
    #             Delta[(Theta[j], Theta_dash, 0)] = 0
    #         for i in range(1, min(int(L[j]), len(Q))+1):
    #             print ("i: {0}".format(i))
    #             exit_inner_loop = 0
    #             # print i
    #             q[i] = Q[i-1]
    #             # print q[i]
    #             for Theta_dash in Tau[Theta[j]]:
    #                 Delta[(Theta[j], Theta_dash, i)] = Delta[(Theta[j], Theta_dash, i-1)] + (PALO_calculation.c(Theta_dash, q[i], reward_history[1]) - PALO_calculation.c(Theta[j], q[i], reward_history[i]))
    #             if i < L[j]:
    #                 for Theta_dash in Tau[Theta[j]]:
    #                     if (1 / i) * Delta[Theta[j], Theta_dash, i] > PALO_calculation.inner_caret(Theta[j], Theta_dash, meeting_history, reward_history) * math.sqrt( (1/(2*i)) * math.log((2*(L[j]-1)*len(Tau[Theta[j]])/(delta[j])))):
    #                         Theta[j+1] = Theta_dash
    #                         print ("theta-dash: {0}".format(Theta_dash))
    #                         print "break"
    #                         print (1 / i) * Delta[Theta[j], Theta_dash, i]
    #                         print ("1:right: {0}".format(PALO_calculation.inner_caret(Theta[j], Theta_dash, meeting_history, reward_history) * math.sqrt( (1/(2*i)) * math.log((2*(L[j]-1)*len(Tau[Theta[j]])/(delta[j]))))))
    #                         print ("Theta[j+1] = Theta_dash: {0}".format(Theta[j + 1]))
    #                         exit_inner_loop = 1
    #                         break
    #                 if exit_inner_loop == 1:
    #                     break
    #
    #                 flag_for_all = 1
    #                 for Theta_dash in Tau[Theta[j]]:
    #                     if not (1 / i) * Delta[Theta[j], Theta_dash, i] < parameters['epsilon'] - PALO_calculation.inner_caret(Theta[j], Theta_dash, meeting_history, reward_history) * math.sqrt( (1/(2*i)) * math.log((2*(L[j]-1)*len(Tau[Theta[j]])/(delta[j])))):
    #                         flag_for_all = 0
    #                 if flag_for_all == 1:
    #                     exit_both_loop = 1
    #                     break
    #
    #             else:
    #                 for Theta_dash in Tau[Theta[j]]:
    #                     if (1 / L[j]) * Delta[Theta[j], Theta_dash, L[j]] > parameters['epsilon']/2:
    #                         Theta[j+1] = Theta_dash
    #                         print ("2:left: {0}", format((1 / L[j]) * Delta[Theta[j], Theta_dash, L[j]]))
    #                         print ("2:right: {0}".format(parameters['epsilon']/2))
    #                         print ("Theta[j+1] = Theta_dash: {0}".format(Theta[j+1]))
    #                         exit_inner_loop = 1
    #                         break
    #                 if exit_inner_loop == 1:
    #                     break
    #
    #                 exit_both_loop = 1
    #                 break
    #
    #             print reward_history
    #         if exit_both_loop == 1:
    #             break
    #     parameters['Theta'] = [Theta[key] for key in Theta][::-1][0]
    #     print("Theta: {0}".format(Theta))
    #     print("threshold is updated to {0}".format(parameters['Theta']))


    elif strategy == "best-so-far":
        parameters['opp_dist'] = {}
        parameters['opp_prob'] = {}
        parameters['opp_answer_dist'] = {}
        parameters['opp_yes_prob'] = {}

        time = sum([1 for key in meeting_history if meeting_history[key] != []])

        for key in meeting_history:
            if key > time - config.windowing and meeting_history[key] != []:
                for record in meeting_history[key]:
                    try:
                        parameters['opp_dist'][record[0]] += 1
                    except KeyError:
                        parameters['opp_dist'][record[0]] = 1
                    if record[1] == 'yes':
                        try:
                            if reward_history[key] == record[0]:
                                parameters['opp_answer_dist'][(record[0], 'yes')] += 1
                            elif reward_history[key] != record[0]:
                                parameters['opp_answer_dist'][(record[0], 'no')] += 1
                        except KeyError:
                            if reward_history[key] == record[0]:
                                parameters['opp_answer_dist'][(record[0], 'yes')] = 1
                                if (record[0], 'no') not in parameters['opp_answer_dist']:
                                    parameters['opp_answer_dist'][(record[0], 'no')] = 0
                            elif reward_history[key] != record[0]:
                                parameters['opp_answer_dist'][(record[0], 'no')] = 1
                                if (record[0], 'yes') not in parameters['opp_answer_dist']:
                                    parameters['opp_answer_dist'][(record[0], 'yes')] = 0

        for opponent in parameters['opp_dist']:
            parameters['opp_prob'][opponent] = float(parameters['opp_dist'][opponent]) / sum(
                parameters['opp_dist'].values())
            try:
                parameters['opp_yes_prob'][opponent] = float(parameters['opp_answer_dist'][(opponent, 'yes')]) / (
                parameters['opp_answer_dist'][(opponent, 'yes')] + parameters['opp_answer_dist'][(opponent, 'no')])
            except KeyError:
                parameters['opp_yes_prob'][opponent] = 'unk'
        print "opp_yes_prob: {0}".format(collections.OrderedDict(sorted(parameters['opp_yes_prob'].items())))

        highest_obtained_utility = config.lower_bound
        # print [opponent for opponent in parameters['opp_dist'] if (opponent, 'yes') in parameters['opp_answer_dist']]
        got_accepted_list = [opponent for opponent in parameters['opp_dist'] if (opponent, 'yes') in parameters['opp_answer_dist'] and parameters['opp_answer_dist'][(opponent, 'yes')]>0]
        if got_accepted_list != []:
            highest_obtained_utility = max(highest_obtained_utility, max(got_accepted_list))
        print ("opp_dist: {0}".format(parameters['opp_dist']))
        print ("opp_answer_dist: {0}".format(collections.OrderedDict(sorted(parameters['opp_answer_dist'].items()))))
        print ("highest_obtained_utility: {0}",format(highest_obtained_utility))

        # print parameters['opp_dist']
        # print sum(parameters['opp_dist'].values())
        # print parameters['opp_answer_dist']
        print "threshold updated: from: {0}".format(parameters['threshold'])
        new_threshold = highest_obtained_utility

        ##### optional
        if highest_obtained_utility == 0 and len(parameters['threshold_history']) >= 2:
            if parameters['threshold_history'][-1] > parameters['threshold_history'][-2]:
                new_threshold = parameters['threshold_history'][-2]
        #####

        parameters['threshold'] = parameters['threshold'] + config.learning_rate * (config.reduce_learning_rate ** time) * (new_threshold - parameters['threshold'])
        # print [parameters['opp_prob'][opponent] * parameters['opp_yes_prob'][opponent] * opponent for opponent in parameters['opp_dist']]
        print "*** threshold updated: *** to: {0}".format(parameters['threshold'])
        parameters['threshold_history'].append(parameters['threshold'])
        print ("thresh_history: {0}".format({i+1: round(threshold,config.random_decimal_point) for i, threshold in enumerate(parameters['threshold_history'])}))
        print ("reward_history: {0}".format(reward_history))
        # pass

    elif strategy == "mean-so-far":
        pass

    elif strategy == "secretary":
        pass

    elif strategy == "andria":
        pass

    return early_stop, parameters

# def reflection(strategy, parameters, opponent_value):
#
#     if strategy == "random":
#         pass
#
#     elif strategy == "threshold":
#         parameters['threshold'] = parameters['threshold'] - config.learning_rate * (parameters['threshold'] - opponent_value)
#
#     # elif strategy == "PALO":
#     #     pass
#
#     elif strategy == "best-so-far":
#         pass
#
#     elif strategy == "mean-so-far":
#         pass
#
#     elif strategy == "secretary":
#         pass
#
#     elif strategy == "andria":
#         pass
#
#     return parameters