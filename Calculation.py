import math
import random
import numpy as np

def cosine_similarity(vector_a, vector_b):
    return ( sum([a*b for a,b in zip(vector_a,vector_b)]) / (math.sqrt(sum([a**2 for a in vector_a])) * math.sqrt(sum([b**2 for b in vector_b]))) )

def get_uniformly_random_number(mininum, maximum, floating_point):
    return round(random.uniform(mininum, maximum), floating_point)

def pearson_correlation_coefficient(vector_x, vector_y):
    x_bar = np.average(vector_x)
    y_bar = np.average(vector_y)
    return (sum([(x_i-x_bar)*(y_i-y_bar) for x_i, y_i in zip(vector_x, vector_y)])) / (math.sqrt(sum([(x_i - x_bar)**2 for x_i in vector_x])) * math.sqrt(sum([(y_i - y_bar)**2 for y_i in vector_y])))