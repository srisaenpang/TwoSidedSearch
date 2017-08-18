import numpy as np
import copy
import config
import pickle
# import open_pickle

# def calculate_theoretical_result():
no_players = config.number_of_players
r_l = config.Bellman_gamma_l
r_r = config.Bellman_gamma_r
player_l = {}
player_r = {}
threshold_l = {}
threshold_l_prev = {}
threshold_r = {}
threshold_r_prev = {}
sorted_rank = [i+1 for i in range(no_players)]
# print sorted_rank
# exit()

# initialise selected list
selected_for_l = {}
selected_for_r = {}
selected_and_matchable_for_l = {}
selected_and_matchable_for_r = {}
for i in sorted_rank:
    selected_for_l[i] = [j+1 for j in range(i)]
    selected_for_r[i] = [j+1 for j in range(i)]

# print selected_for_r
# exit()

for i in sorted_rank:
    player_l[i] = [i, no_players-(i)+1]
    # player_r[i] = [i, config.number_of_players+no_players-(i)+1]
    player_r[i] = [i, no_players-(i)+1]

# print player_l
# print player_r
# exit()


for loop in range(100):
    # print "loop", loop+1

    for l_rank in sorted_rank:
        # print "loop start", l_rank
        E_U_max = 0
        for aim_for in sorted_rank:
            selected_and_matchable = []
            u_of_selected_and_matchable = {}
            for runner in sorted_rank:
                if runner <= aim_for and l_rank in selected_for_r[runner]:
                    selected_and_matchable.append(runner)
            # if l_rank == 5:
            #     print selected_and_matchable
            if selected_and_matchable:
                for agent in selected_and_matchable:
                    u_of_selected_and_matchable[agent] = player_r[agent][1]
                u_O = np.average(u_of_selected_and_matchable.values())
                p = float(len(u_of_selected_and_matchable))/no_players
                E_U = ( r_l * p * u_O )/( 1 - r_l + ( r_l * p ))
                if E_U > E_U_max:
                    E_U_max = E_U
                    selected_and_matchable_for_l[l_rank] = selected_and_matchable
        # print E_U_max
        threshold_l[l_rank] = E_U_max
        # print threshold_l

    for r_rank in sorted_rank:
        # print "loop start", r_rank
        E_U_max = 0
        for aim_for in sorted_rank:
            selected_and_matchable = []
            u_of_selected_and_matchable = {}
            for runner in sorted_rank:
                if runner <= aim_for and r_rank in selected_for_l[runner]:
                    selected_and_matchable.append(runner)
            # if r_rank == 5:
            #     print selected_and_matchable
            if selected_and_matchable:
                for agent in selected_and_matchable:
                    u_of_selected_and_matchable[agent] = player_l[agent][1]
                u_O = np.average(u_of_selected_and_matchable.values())
                p = float(len(u_of_selected_and_matchable))/no_players
                E_U = ( r_r * p * u_O )/( 1 - r_r + ( r_r * p ))
                if E_U > E_U_max:
                    E_U_max = E_U
                    selected_and_matchable_for_r[r_rank] = selected_and_matchable
        # print E_U_max
        threshold_r[r_rank] = E_U_max
        # print threshold_r

    # print player_l

    for i in sorted_rank:
        # print player_r[i][1]
        # print threshold_r
        selected_for_l[i] = [rank for rank in sorted_rank if player_r[rank][1] >= threshold_l[i]]
        selected_for_r[i] = [rank for rank in sorted_rank if player_l[rank][1] >= threshold_r[i]]
        # print i, selected_for_l[i], selected_for_r[i]


    print "loop", loop+1

    print threshold_l
    print threshold_r

    # print selected_for_l
    # print selected_for_r

    print selected_and_matchable_for_l
    print selected_and_matchable_for_r


    # stopping condition
    stop = 0
    if threshold_l_prev and threshold_r_prev:
        stop = 1
        for key in threshold_l_prev:
            if threshold_l_prev[key] != threshold_l[key]:
                stop = 0
                break
        for key in threshold_r_prev:
            if threshold_r_prev[key] != threshold_r[key]:
                stop = 0
                break

    if stop == 1:
        print "threshold didnt change, exit"
        break

    threshold_l_prev = copy.deepcopy(threshold_l)
    threshold_r_prev = copy.deepcopy(threshold_r)


    # print " "

print threshold_l
print threshold_r

with open(config.output_name+'theory', 'w') as f:
    pickle.dump([threshold_l, threshold_r], f)

# print player_l
# print player_r

# open_pickle.open_pickle()

print '"{0}"'.format(config.output_name)