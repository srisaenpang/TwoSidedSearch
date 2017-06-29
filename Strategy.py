import numpy as np
import config
import Agent

Strategy_Agent_dict = {key: [] for key in config.strategies}

def inititialise_parameters(strategy, parameters):
    if strategy == "random":
        parameters['random-threshold'] = config.random_threshold

    elif strategy == "threshold":
        parameters['threshold'] = config.threshold

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

# may not need "action"
def learn(strategy, parameters, reward):

    if strategy == "random":
        pass

    elif strategy == "threshold":
        if reward == 0:
            print("threshold is reduced from {0} to {1}".format(parameters['threshold'],parameters['threshold']*config.threshold_reduction))
            parameters['threshold'] = parameters['threshold'] * config.threshold_reduction
        else:
            if reward > parameters['threshold']:
                parameters['threshold'] = reward

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

    elif strategy == "best-so-far":
        pass

    elif strategy == "mean-so-far":
        pass

    elif strategy == "secretary":
        pass

    elif strategy == "andria":
        pass

    return parameters