# POPULATION PARAMETERS (It is a dictionary with the KEYS as STRATEGIES, and their VALUES as the NUMBER)
player_left = {"threshold":15}
player_right = {"threshold":15}
# #   It can be mixed like this
# player_left = {"random":10, "best-so-far":10, "threshold":10, "mean-so-far":10 , "secretary":10, "andria":10}
# player_right = {"random":10, "best-so-far":10, "threshold":10, "mean-so-far":10 , "secretary":10, "andria":10}

# These are made just for later REFERENCING
strategies = list(set([key for key in player_left] + [key for key in player_right]))
number_of_players_left = sum(player_left.values())
number_of_players_right = sum(player_right.values())
number_of_players = min(number_of_players_left, number_of_players_right)

# SIMILATION PARAMETERS
# # These namings are for automated figure generation. These bits are picked manually according to the settings
# output_name = 'output_' + 'old.method_'                   # old method means model-based learning (using value/policy iteration)
# output_name = 'output_' + '5agents_'                      # 5 Agents validation
# output_name = 'output_'                                   # Standard model (probabilistic-based learning)
# output_name = 'output_' + '5sims_'+ 'old.method_'         # # (same to those above, but run in 5 simulations)
# output_name = 'output_' + '5sims_'+ '5agents_'
# output_name = 'output_' + '5sims_'+ '5agents_'
output_name = 'output_' + '5sims_'
old_method = 0                                              # old method = 1: for model-based learning; 0 for probabilistic-based learning
if old_method == 1:
    output_name += 'old.method_'                            # # naming bits, just wanted different output names, so it won't replace the earlier ones
if old_method == 2:
    output_name += 'new.method_'
simulation_repeated = 100                                   # ROUNDS for simluation
output_name += 'Rep.' + str(simulation_repeated) + '_'
simulation_time = 30                                        # TIME LIMIT for simulations
output_name += 'Time.' + str(simulation_time) + '_'
early_stop_epsilon = 0.00                                   # If the threshold difference in all agents is equal or smaller than this, EARLY STOP
rank_analysis_mod = 1
step_update = 0                                             # o or 1; if 1, it will force a learning every time new piece of information achieved
if step_update == 1:
    output_name += 'Step.updt' + '_'
method_epsilon_threshold = 1                                # use 1 for epsilon-threshold assumption
if method_epsilon_threshold == 1:
    output_name += 'Eps.Thr' + '_'
if method_epsilon_threshold == 0:
    method_1nn = 1                                          # use 1 for non-parametric assumption (note: I manually switched this to 0 or 1, but it's no need. OK to leave this as 1, and control assumptions by method_epsilon-threshold above)
    if method_1nn == 1:
        output_name += 'Mth.1nn' + '_'
# knn = 0

forget = 1                                                  # 0 or 1; 1 to enable forgetting past
if forget == 1:
    output_name += 'Forget' + '_'
    forgetting_factor = 0.1                                 # In the Strategy.py, when count data pieces to build the distributions, forgetting factor 0.1 will filter out information gained in first 10% of the round
else:
    forgetting_factor = 0.0


exploration_mode = 0                                        # Exploration Method. 0: no exploration; 1: non-optimal exploration; 2: fixed-yes-no exploration; 3: yes-if-no-data; 4: yes-if-less-than-1%
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
    shrink_exploration_rate = 0.95                          # Reduce exploration rate by 5% every round
    output_name += 'Explr.Rt.Shrnk.' + str(shrink_exploration_rate) + '_'
force_uniform_opponent_prob = 0                             # To force replace the opponent distribution with the uniform distribution, for policy calculation (turned out to be irrelevant)
if force_uniform_opponent_prob == 1:
    output_name += 'Frce.Uniform.Prob' + '_'

plotting = 1                                                # # something from an early designs. not relevant
subjective = 0                                              # 0 or 1; 0 for ASSORTAIVE MATCHING; 1 for NON-ASSORTATIVE MATCHING
output_name += 'Subj.' + str(subjective) + '_'
t_0 = 1                                                     # time label at the first round. used to calculate discounting
category_of_property = subjective * 10                      # (for non-assortative matching)
category_of_requirement = category_of_property              # make the same number of properties and requirements
random_decimal_point = 2                                    # # to set the decimal point to those where the results are easier to read when rounded. rarely used.
replacement_mode = ["None", "Clone", "Prob-Entrance"][1]    # change only the number at the end. Normally I use 1 (clone setting).
output_name += 'Replace.' + replacement_mode + '_'
replacement_constant = (1.0 / simulation_time) * 1          # the market entrance rate. havent had a chance to play with this yet
if replacement_mode == "Prob-Entrance":
    output_name += 'Ent.Rt.' + str(replacement_constant) + '_'



# model_parameters
attractiveness_min = 0                                      # In previous design, where attractiveness is random. This set the minimum for the uniform random.
attractiveness_max = 10                                     # Same above. This is for the maximum.
property_min = -5                                           # Minimum of each propoerty
property_max = 5                                            # Maximum of each property
requirement_min = property_min                              # Set the same to the requirements
requirement_max = property_max
subjectivity_constant = 10                                  # The ratio between attractiveness score and property-requirement score. Use this to control the correlation
if subjective == 0:
    subjectivity_constant = 0

# references
lower_bound = attractiveness_min - (subjectivity_constant * 1)  # These are for later referencing
upper_bound = attractiveness_max + (subjectivity_constant * 1)
dynamic_range = upper_bound - lower_bound
non_matched_reward = lower_bound

windowing = simulation_repeated                             # consider only the information inside the window (number of rounds to consider). Since we are not using it, this is set to the maximum possible number of rounds

# Bellman's equation parameters
Bellman_epsilon_l = 0.1                                     # Bellman epsilon for LEFT agents. Note: I acutally use this one also for the leaning rate in probabilistic-based model
output_name += 'Bell.eps.l.' + str(Bellman_epsilon_l) + '_'
Bellman_epsilon_r = 0.1                                     # same to above. but this is for RIGHT agents
output_name += 'Bell.eps.r.' + str(Bellman_epsilon_r) + '_'
initial_VO = number_of_players/2                            # This is the INITAL BIASES for agents. They all initially have their thresholds at the middle
output_name += 'Ini.V.' + str(initial_VO) + '_'
Bellman_gamma_l = 0.99                                      # discounting factor for LEFT agents
output_name += 'Bell.gam.l.' + str(Bellman_gamma_l) + '_'
Bellman_gamma_r = 0.99                                      # discounting factor for RIGHT agents
output_name += 'Bell.gam.r.' + str(Bellman_gamma_r) + '_'


# strategy_parameters initialisation
random_threshold = 0.5                                      # for random agents (not in our experiment)
best_so_far = lower_bound                                   # I changed strategy 'best-so-far' a lot. this parameter is for the old one.
secretary_calibration_time = simulation_time * 0.3679       # Time required before starting accepting
andria_calibration_time = simulation_time * 0.3679

# display                                                   # These are for the early designs. can no longer use to control displaying results
verbose = 1
verbose_simulation = 1
verbose_analysis = 1
verbose_analysis_matched = 1
verbose_analysis_non_matched = 1
show_validation = 1