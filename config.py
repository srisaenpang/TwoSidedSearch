# population
player_left = {"PALO":20}
player_right = {"PALO":20}
# player_left = {"random":10, "best-so-far":10, "threshold":10, "mean-so-far":10 , "secretary":10, "andria":10}
# player_right = {"random":10, "best-so-far":10, "threshold":10, "mean-so-far":10 , "secretary":10, "andria":10}
strategies = list(set([key for key in player_left] + [key for key in player_right]))

# simulation
simulation_repeated = 20
simulation_time = 20
subjective = 0
category_of_interest = subjective * 5
random_decimal_point = 2
replacement_mode = ["None", "Clone", "Prob-Entrance"][0]

# model_parameters
attractiveness_min = -10
attractiveness_max = 10
interest_min = -10
interest_max = 10
subjectivity_constant = 10
if subjective == 0:
    subjectivity_constant = 0

# references
lower_bound = attractiveness_min - (subjectivity_constant * 1)
upper_bound = attractiveness_max + (subjectivity_constant * 1)
dynamic_range = attractiveness_max - attractiveness_min + (subjectivity_constant * 1)
non_matched_penalty = lower_bound

# learning_parameters
learning_rate = 0.1
discount_rate = 0.99

# strategy_parameters initialisation
random_threshold = 0.5
threshold = upper_bound * 1.0
threshold_reduction = 0.9
best_so_far = lower_bound
secretary_calibration_time = simulation_time * 0.3679
andria_calibration_time = simulation_time * 0.3679

# PALO parameters
PALO_threshold = threshold
PALO_decimal_point = 1
PALO_epsilon = 0.1
PALO_delta = 0.9
PALO_neighbour_range = float (dynamic_range / 1)

# display
verbose = 1
verbose_simulation = 1
verbose_analysis = 1
verbose_analysis_matched = 1
verbose_analysis_non_matched = 1
show_validation = 1