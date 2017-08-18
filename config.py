# population
# player_left = {"PALO":20}
# player_right = {"PALO":20}
player_left = {"threshold":15}
player_right = {"threshold":15}
# player_left = {"best-so-far":20}
# player_right = {"best-so-far":20}
# player_left = {"random":10, "best-so-far":10, "threshold":10, "mean-so-far":10 , "secretary":10, "andria":10}
# player_right = {"random":10, "best-so-far":10, "threshold":10, "mean-so-far":10 , "secretary":10, "andria":10}
strategies = list(set([key for key in player_left] + [key for key in player_right]))
number_of_players_left = sum(player_left.values())
number_of_players_right = sum(player_right.values())
number_of_players = min(number_of_players_left, number_of_players_right)

# simulation
# output_name = 'output_' + 'old.method_'
# output_name = 'output_' + '5agents_'
# output_name = 'output_'
# output_name = 'output_' + '5sims_'+ 'old.method_'
# output_name = 'output_' + '5sims_'+ '5agents_'
# output_name = 'output_' + '5sims_'+ '5agents_'
output_name = 'output_' + '5sims_'
old_method = 0
if old_method == 1:
    output_name += 'old.method_'
if old_method == 2:
    output_name += 'new.method_'
simulation_repeated = 100
output_name += 'Rep.' + str(simulation_repeated) + '_'
# output_name = 'output'+'_'+str(simulation_repeated)
simulation_time = 30
output_name += 'Time.' + str(simulation_time) + '_'
# early_stop_epsilon = 0.01
early_stop_epsilon = 0.00
rank_analysis_mod = 1
step_update = 0
if step_update == 1:
    output_name += 'Step.updt' + '_'
method_epsilon_threshold = 1
if method_epsilon_threshold == 1:
    output_name += 'Eps.Thr' + '_'
if method_epsilon_threshold == 0:
    method_1nn = 0
    if method_1nn == 1:
        output_name += 'Mth.1nn' + '_'
# knn = 0

forget = 1
if forget == 1:
    output_name += 'Forget' + '_'
    forgetting_factor = 0.1
else:
    forgetting_factor = 0.0


exploration_mode = 0      # 0:no exploration , 1:non-optimal exploration, 2:fixed-yes-no exploration 3:yes-if-no-data 4:yes-if-less-than-1%
output_name += 'Explr.Md.' + str(exploration_mode) + '_'
if exploration_mode == 1:
    exploration_rate = 0.03
    output_name += 'Explr.Rt.' + str(exploration_rate) + '_'
if exploration_mode == 2:
    yes_rate = 0.015
    output_name += 'Ys.Rt.' + str(yes_rate) + '_'
    no_rate = 0.015
    output_name += 'No.Rt.' + str(no_rate) + '_'
if exploration_mode == 4:
    data_percentage = 0.01
    output_name += 'Data.Percent.' + str(data_percentage) + '_'
if exploration_mode != 0:
    shrink_exploration_rate = 0.95
    output_name += 'Explr.Rt.Shrnk.' + str(shrink_exploration_rate) + '_'
force_uniform_opponent_prob = 0
if force_uniform_opponent_prob == 1:
    output_name += 'Frce.Uniform.Prob' + '_'

plotting = 1
subjective = 0
output_name += 'Subj.' + str(subjective) + '_'
# apply_discounted_utility = 0      # 0 for no, 1 for yes
# discounting_factor = 0.9
# if apply_discounted_utility == 0:
#     discounting_factor = 1
t_0 = 1
category_of_property = subjective * 10
category_of_requirement = category_of_property
random_decimal_point = 2
replacement_mode = ["None", "Clone", "Prob-Entrance"][1]
output_name += 'Replace.' + replacement_mode + '_'
replacement_constant = (1.0 / simulation_time) * 1
if replacement_mode == "Prob-Entrance":
    output_name += 'Ent.Rt.' + str(replacement_constant) + '_'



# model_parameters
attractiveness_min = 0
attractiveness_max = 10
property_min = -5
property_max = 5
requirement_min = property_min
requirement_max = property_max
subjectivity_constant = 10
if subjective == 0:
    subjectivity_constant = 0

# references
lower_bound = attractiveness_min - (subjectivity_constant * 1)
upper_bound = attractiveness_max + (subjectivity_constant * 1)
dynamic_range = upper_bound - lower_bound
non_matched_reward = lower_bound

# # learning_parameters
# learning_rate = 0.1
# reduce_learning_rate = 1
# discount_rate = 0.99
windowing = simulation_repeated
# threshold_shrink = 0.9

# Bellman's equation parameters
Bellman_epsilon_l = 0.1
output_name += 'Bell.eps.l.' + str(Bellman_epsilon_l) + '_'
Bellman_epsilon_r = 0.1
output_name += 'Bell.eps.r.' + str(Bellman_epsilon_r) + '_'
initial_VO = number_of_players/2
output_name += 'Ini.V.' + str(initial_VO) + '_'
Bellman_gamma_l = 0.99
output_name += 'Bell.gam.l.' + str(Bellman_gamma_l) + '_'
Bellman_gamma_r = 0.99
output_name += 'Bell.gam.r.' + str(Bellman_gamma_r) + '_'


# strategy_parameters initialisation
random_threshold = 0.5
# threshold = upper_bound * 0.1
# threshold = upper_bound/2
# threshold_reduction = 0.9
best_so_far = lower_bound
secretary_calibration_time = simulation_time * 0.3679
andria_calibration_time = simulation_time * 0.3679

# # PALO parameters
# PALO_threshold = threshold
# PALO_decimal_point = 1
# PALO_epsilon =20
# PALO_delta = 1
# PALO_neighbour_range = float (dynamic_range / 7)

# display
verbose = 1
verbose_simulation = 1
verbose_analysis = 1
verbose_analysis_matched = 1
verbose_analysis_non_matched = 1
show_validation = 1