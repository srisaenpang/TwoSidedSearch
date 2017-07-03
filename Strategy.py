import numpy as np
import config
import Agent
import itertools
import math
import PALO_calculation

Strategy_Agent_dict = {key: [] for key in config.strategies}

def inititialise_parameters(strategy, parameters):
    if strategy == "random":
        parameters['random-threshold'] = config.random_threshold

    elif strategy == "threshold":
        parameters['threshold'] = config.threshold

    elif strategy == "PALO":
        parameters['Theta'] = config.PALO_threshold
        parameters['Tau'] = [float(i)/10**config.PALO_decimal_point for i in range((config.lower_bound)*(10**config.PALO_decimal_point),(config.upper_bound)*(10**config.PALO_decimal_point)+1)]
        parameters['epsilon'] = config.PALO_epsilon
        parameters['delta'] = config.PALO_delta

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
        if score >= parameters['threshold']:
            decision = "yes"
        else:
            decision = "no"

    elif strategy == "PALO":
        if score >= parameters['Theta']:
            decision = "yes"
        else:
            decision = "no"

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
        raise("Decision Error: None")

    return decision, parameters


def learn_overtime(strategy, parameters, meeting_history):

    if strategy == "random":
        pass

    elif strategy == "threshold":
        pass

    elif strategy == "PALO":
        pass

    elif strategy == "best-so-far":
        pass

    elif strategy == "mean-so-far":
        pass

    elif strategy == "secretary":
        pass

    elif strategy == "andria":
        pass

    return parameters

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
        pass

    elif strategy == "PALO":
        delta = {}
        L = {}
        Tau = {}
        Theta = {1: parameters['Theta']}
        Delta = {}
        q = {}
        Q = [[record for record in meeting_history[repeat]] for repeat in meeting_history]
        for j in itertools.count(1):
            print ("j: {0}".format(j))
            exit_both_loop = 0
            if j not in Theta:
                Theta[j] = Theta[j-1]
                print ("copied Theta[j]: {0}".format(Theta[j]))
            delta[j] = (6 * parameters['delta']) / (j ** 2 * math.pi ** 2)
            print ("delta[j]: {0}".format(delta[j]))
            Tau[Theta[j]] = [Theta_i for Theta_i in parameters['Tau'] if Theta_i <= parameters['Theta'] + config.PALO_neighbour_range and Theta_i >= parameters['Theta'] - config.PALO_neighbour_range and Theta_i != parameters['Theta']]
            print ("Tau[Theta[j]]: {0}".format(Tau[Theta[j]]))
            L[j] = math.ceil(2 * (PALO_calculation.caret(Theta[j], Tau[Theta[j]], meeting_history, reward_history) / parameters['epsilon'])**2 * math.log(2 * len(Tau[Theta[j]]) / delta[j]))
            print ("L[j]: {0}".format(L[j]))
            # print PALO_calculation.caret(Theta[j], Tau[Theta[j]], meeting_history, reward)
            for Theta_dash in Tau[Theta[j]]:
                Delta[(Theta[j], Theta_dash, 0)] = 0
            for i in range(1, min(int(L[j]), len(Q))+1):
                print ("i: {0}".format(i))
                exit_inner_loop = 0
                # print i
                q[i] = Q[i-1]
                # print q[i]
                for Theta_dash in Tau[Theta[j]]:
                    Delta[(Theta[j], Theta_dash, i)] = Delta[(Theta[j], Theta_dash, i-1)] + (PALO_calculation.c(Theta_dash, q[i], reward_history[1]) - PALO_calculation.c(Theta[j], q[i], reward_history[i]))
                if i < L[j]:
                    for Theta_dash in Tau[Theta[j]]:
                        if (1 / i) * Delta[Theta[j], Theta_dash, i] > PALO_calculation.inner_caret(Theta[j], Theta_dash, meeting_history, reward_history) * math.sqrt( (1/(2*i)) * math.log((2*(L[j]-1)*len(Tau[Theta[j]])/(delta[j])))):
                            Theta[j+1] = Theta_dash
                            exit_inner_loop = 1
                            break
                    if exit_inner_loop == 1:
                        break

                    flag_for_all = 1
                    for Theta_dash in Tau[Theta[j]]:
                        if not (1 / i) * Delta[Theta[j], Theta_dash, i] < parameters['epsilon'] - PALO_calculation.inner_caret(Theta[j], Theta_dash, meeting_history, reward_history) * math.sqrt( (1/(2*i)) * math.log((2*(L[j]-1)*len(Tau[Theta[j]])/(delta[j])))):
                            flag_for_all = 0
                    if flag_for_all == 1:
                        exit_both_loop = 1
                        break

                else:
                    for Theta_dash in Tau[Theta[j]]:
                        if (1 / L[j]) * Delta[Theta[j], Theta_dash, L[j]] > parameters['epsilon']/2:
                            Theta[j+1] = Theta_dash
                            exit_inner_loop = 1
                            break
                    if exit_inner_loop == 1:
                        break

                    exit_both_loop = 1
                    break

                print reward_history
            if exit_both_loop == 1:
                break
        parameters['Theta'] = [Theta[key] for key in Theta][::-1][0]
        print("Theta: {0}".format(Theta))
        print("threshold is updated to {0}".format(parameters['Theta']))


    elif strategy == "best-so-far":
        pass

    elif strategy == "mean-so-far":
        pass

    elif strategy == "secretary":
        pass

    elif strategy == "andria":
        pass

    return parameters

def reflection(strategy, parameters, opponent_value):

    if strategy == "random":
        pass

    elif strategy == "threshold":
        parameters['threshold'] = parameters['threshold'] - config.learning_rate * (parameters['threshold'] - opponent_value)

    elif strategy == "PALO":
        pass

    elif strategy == "best-so-far":
        pass

    elif strategy == "mean-so-far":
        pass

    elif strategy == "secretary":
        pass

    elif strategy == "andria":
        pass

    return parameters