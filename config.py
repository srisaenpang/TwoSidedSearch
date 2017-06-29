# population
player_left = {"random":10, "best-so-far":10, "threshold":10, "mean-so-far":10 , "secretary":10, "andria":10}
player_right = {"random":10, "best-so-far":10, "threshold":10, "mean-so-far":10 , "secretary":10, "andria":10}
strategies = list(set([key for key in player_left] + [key for key in player_right]))

# simulation
simulation_repeated = 100
simulation_time = 100
subjective = 0
category_of_interest = subjective * 5
random_decimal_point = 2
replacement_mode = ["None", "Clone", "Prob-Entrance"][0]

# model_parameters
non_matched_penalty = 0
attractiveness_min = 0
attractiveness_max = 10
interest_min = -10
interest_max = 10
subjectivity_constant = 10

# learning_parameters
learning_rate = 0.1

# strategy_parameters initialisation
random_threshold = 0.5
threshold = attractiveness_max + (interest_max * category_of_interest) * 0.3
threshold_reduction = 0.9
best_so_far = attractiveness_min + (interest_min * interest_max * category_of_interest)
secretary_calibration_time = simulation_time * 0.3679
andria_calibration_time = simulation_time * 0.3679

# display
verbose = 1
verbose_simulation = 1
verbose_analysis = 1
verbose_analysis_matched = 1
verbose_analysis_non_matched = 1
show_validation = 1