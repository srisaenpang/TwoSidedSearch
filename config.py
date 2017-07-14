# population
# player_left = {"PALO":20}
# player_right = {"PALO":20}
player_left = {"threshold":5}
player_right = {"threshold":5}
# player_left = {"random":10, "best-so-far":10, "threshold":10, "mean-so-far":10 , "secretary":10, "andria":10}
# player_right = {"random":10, "best-so-far":10, "threshold":10, "mean-so-far":10 , "secretary":10, "andria":10}
strategies = list(set([key for key in player_left] + [key for key in player_right]))

# simulation
simulation_repeated = 100
simulation_time = 10
subjective = 0
apply_discounted_utility = 0      # 0 for no, 1 for yes
discounting_factor = 0.99
category_of_property = subjective * 10
category_of_requirement = category_of_property
random_decimal_point = 2
replacement_mode = ["None", "Clone", "Prob-Entrance"][1]
replacement_constant = (1.0 / simulation_time) * 1
# replacement_mode = "Peace"

# model_parameters
attractiveness_min = 0
attractiveness_max = 10
property_min = -10
property_max = 10
requirement_min = property_min
requirement_max = property_max
subjectivity_constant = 100
if subjective == 0:
    subjectivity_constant = 0

# references
lower_bound = attractiveness_min - (subjectivity_constant * 1)
upper_bound = attractiveness_max + (subjectivity_constant * 1)
dynamic_range = upper_bound - lower_bound
non_matched_reward = lower_bound

# learning_parameters
learning_rate = 0.1
discount_rate = 0.99

# strategy_parameters initialisation
random_threshold = 0.5
# threshold = upper_bound * 0.1
threshold = upper_bound / 2
threshold_reduction = 0.9
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