import config

def caret(Theta, Tau, meeting_history, reward_history):
    caret_max = None
    for Theta_dash in Tau:
        inner_caret_result = inner_caret(Theta, Theta_dash, meeting_history, reward_history)
        if caret_max == None or inner_caret_result >= caret_max:
            caret_max = inner_caret_result
    print ("caret_max: {0}".format(caret_max))
    return caret_max

def inner_caret(Theta, Theta_dash, meeting_history, reward_history):
    inner_caret_max = None
    inner_caret_min = None
    # print meeting_history
    Q = [[ record for record in meeting_history[repeat]] for repeat in meeting_history]
    # print Q
    for i, q in enumerate(Q):
        c_result = c(Theta_dash, q, reward_history[i+1]) - c(Theta, q, reward_history[i+1])
        if inner_caret_max == None or c_result >= inner_caret_max:
            inner_caret_max = c_result
        if inner_caret_min == None or c_result <= inner_caret_min:
            inner_caret_min = c_result
    # print ("inner_caret_max - inner_caret_min: {0}".format(inner_caret_max - inner_caret_min))
    # print ("inner_caret_min: {0}".format(inner_caret_min))
    # print ("inner_caret_max: {0}".format(inner_caret_max))
    return inner_caret_max - inner_caret_min

def c(Theta, q, reward):
    c_result = config.lower_bound
    for i, record in enumerate(q):
        if (record[0] >= Theta):
            if (record[1] == 'yes'):
                if (reward < record[0]):
                    continue
            if record[0] * config.discount_rate**i > c_result:
                c_result = record[0] * config.discount_rate**i
    # print ("c_result: {0}".format(c_result))
    return c_result