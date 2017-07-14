import numpy as np
import config
import Agent
import itertools
import math
# import PALO_calculation

Strategy_Agent_dict = {key: [] for key in config.strategies}

def inititialise_parameters(strategy, parameters):
    if strategy == "random":
        parameters['random-threshold'] = config.random_threshold

    elif strategy == "threshold":
        parameters['threshold'] = config.threshold
        parameters['opp_dist'] = {}
        parameters['opp_prob'] = {}
        parameters['opp_answer_dist'] = {}
        parameters['opp_yes_prob'] = {}
        parameters['threshold_history'] = [parameters['threshold']]

    # elif strategy == "PALO":
    #     parameters['Theta'] = config.PALO_threshold
    #     parameters['Tau'] = [float(i)/10**config.PALO_decimal_point for i in range((config.lower_bound)*(10**config.PALO_decimal_point),(config.upper_bound)*(10**config.PALO_decimal_point)+1)]
    #     parameters['epsilon'] = config.PALO_epsilon
    #     parameters['delta'] = config.PALO_delta

    elif strategy == "best-so-far":
        parameters['best-so-far'] = config.best_so_far

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
        if config.apply_discounted_utility == 0:
            if score >= parameters['threshold']:
                decision = "yes"    # E[reward(yes)] is higher
            else:
                decision = "no"     # E[value(waiting)] is higher
        elif config.apply_discounted_utility == 1:
            if score * config.discounting_factor >= parameters['threshold']:
                decision = "yes"    # E[reward(yes)] is higher
            else:
                decision = "no"     # E[value(waiting)] is higher

    # elif strategy == "PALO":
    #     if score >= parameters['Theta']:
    #         decision = "yes"
    #     else:
    #         decision = "no"

    elif strategy == "best-so-far":
        if score >= parameters['best-so-far']:
            parameters['best-so-far'] = score
            decision = "yes"
        else:
            decision = "no"

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

def learn(strategy, parameters, meeting_history, reward_history):

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
        parameters['opp_answer_dist'] = {}
        parameters['opp_yes_prob'] = {}
        for key in meeting_history:
            # #######
            # if key < len(meeting_history) - 15:
            #     continue
            # #######
            for record in meeting_history[key]:
                try:
                    parameters['opp_dist'][record[0]] += 1
                except KeyError:
                    parameters['opp_dist'][record[0]] = 1
                if record[1] == 'yes':
                    try:
                        if reward_history[key] == record[0]:
                            parameters['opp_answer_dist'][(record[0],'yes')] += 1
                        elif reward_history[key] != record[0]:
                            parameters['opp_answer_dist'][(record[0], 'no')] += 1
                    except KeyError:
                        if reward_history[key] == record[0]:
                            parameters['opp_answer_dist'][(record[0],'yes')] = 1
                            if (record[0],'no') not in parameters['opp_answer_dist']:
                                parameters['opp_answer_dist'][(record[0], 'no')] = 0
                        elif reward_history[key] != record[0]:
                            parameters['opp_answer_dist'][(record[0], 'no')] = 1
                            if (record[0],'yes') not in parameters['opp_answer_dist']:
                                parameters['opp_answer_dist'][(record[0], 'yes')] = 0
        for opponent in parameters['opp_dist']:
            parameters['opp_prob'][opponent] = float(parameters['opp_dist'][opponent]) / sum(parameters['opp_dist'].values())
            try:
                parameters['opp_yes_prob'][opponent] = float(parameters['opp_answer_dist'][(opponent, 'yes')]) / (parameters['opp_answer_dist'][(opponent, 'yes')] + parameters['opp_answer_dist'][(opponent, 'no')])
            except KeyError:
                parameters['opp_yes_prob'][opponent] = 0.5
        print "opp_yes_prob: {0}".format(parameters['opp_yes_prob'])

        # print parameters['opp_dist']
        # print sum(parameters['opp_dist'].values())
        # print parameters['opp_answer_dist']
        print "threshold updated: from: {0}".format(parameters['threshold'])
        new_threshold = sum([parameters['opp_prob'][opponent] * parameters['opp_yes_prob'][opponent] * opponent for opponent in parameters['opp_dist']])
        parameters['threshold'] = parameters['threshold'] + config.learning_rate * (new_threshold - parameters['threshold'])
        # print [parameters['opp_prob'][opponent] * parameters['opp_yes_prob'][opponent] * opponent for opponent in parameters['opp_dist']]
        print "threshold updated: to: {0}".format(parameters['threshold'])
        parameters['threshold_history'].append(parameters['threshold'])
        print parameters['threshold_history']
        print parameters['opp_yes_prob']

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
        pass

    elif strategy == "mean-so-far":
        pass

    elif strategy == "secretary":
        pass

    elif strategy == "andria":
        pass

    return parameters

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