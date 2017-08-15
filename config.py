# coding: utf-8
"""
Updated 13 Aug 2017

@author: Ruiting
"""
#---------------------------------------------------------------------
'''
Configuration file for setting the parameters of the recognition program
'''

#---------------------------------------------------------------------
# Element parameters 
# If using an Inkscape SVG input with A4 size, do not modify
#---------------------------------------------------------------------
# Labels of the dot and the morphism
dot_label = 1
mor_label = -1

# The threshold value of opencheck ratio for a shape element. 
oc_threshold = 0.10

# The threshold value of convexcheck ratio for a shape element.
cc_threshold = 0.70

# The minimum connect distance for wire elements.
connect_min_d = 15.0

# The number of points after being reduced for a wire lement.
# Must be set at 3n where n is 1,2,3...
refined_points_n = 3

#---------------------------------------------------------------------
# Scoring parameters
# Do not modify
#---------------------------------------------------------------------
# The basic score of a hypothesis.
default_score = 1.00

# The multiplicators of different number of connections for each element. 
alpha_1, alpha_2, alpha_3 = 0.80, 1.05, 1.2

# The multiplicators of different number of intersections between the last stroke
# and one previous stroke.
beta_1, beta_2, beta_3, beta_4 = 1.05, 1.05, 1.2, 1.5

#---------------------------------------------------------------------
# Training parameters
#---------------------------------------------------------------------
# The folder containing training files.
train_folder = 'training_set'

# The files containing training dots and morphisms.
train_files = ['circle0.svg','circle1.svg','circle2.svg','circle3.svg','morphism0.svg','morphism1.svg','morphism2.svg']

# The labels of training data in the trianing files.
train_labels = [dot_label]*4 + [mor_label]*3

# The number of training dots and traning morphisms
training_dot_n = 800
training_mor_n = 800 

# The name of the dumped classifer 
clf_name = 'svm_clf.pkl'

#---------------------------------------------------------------------
# Dataset generation parameters
#---------------------------------------------------------------------
# The number of points on a generated shape.
point_n_range = [80,120]

# The centre of the generated shape.
shape_centre=[200,200]

# The radius of the generated dots.
dot_r_range=[60,80]

# The edge length of the generated morphisms.
mor_a_range = [40,70]
mor_b_range = [50,90]
mor_h_range = [30,80]

# The deformation ratio for the generated shapes.
dot_deform = 0.03
mor_deform = 0.025

#---------------------------------------------------------------------
# Testing parameters
#---------------------------------------------------------------------
# The folder contaning test files.
test_folder = 'test_set'

# The file to test.
test_file = '006.svg'

# Provide a blank background for drawing recognised diagram on it.
background = 'blank.svg'

# The folder containing outputs.
output_folder = 'outputs'

# The name of the output file.
output = 'output.svg'

# The files for evaluation.
evaluate_dots = ['circle4.svg','circle5.svg']
evaluate_morphisms = ['morphism3.svg','morphism4.svg']

#---------------------------------------------------------------------
# SVG visualisation parameters
#---------------------------------------------------------------------
# The colour of the dots. Could be red, green, grey or none.
dot_fill_colour = 'none'

# Whether the dot has a contour.
dot_contour_bool = True

# The radius of the dots.
dot_radius = 10.0

# The edge lengths of the morphisms.
morphism_a = 30.0
morphism_b = 40.0
morphism_h = 20.0

#---------------------------------------------------------------------
# LaTeX visualisation parameters
#---------------------------------------------------------------------
# The unit length of the gird for nodes.
nodegrid_unit = 1.0

# The unit length of the gird for wire points.
wiregrid_unit = 0.5

# Round the angle.
# For example, the number from 45.0 to 74.9 will be rounded to 60.0 when 
# the angle_round is 30.0
angle_round = 30.0

# The length of morphism edge. 
# Used for organising wire positions to the morphism.
mor_edge_len = 5.0

# The threhold ratio that determins a wire is a long wire.
longwire_threshold = 1.5

# The maximum number of interpoints in a long wire.
max_interpoint_n = 4


