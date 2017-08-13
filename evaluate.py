# -*- coding: utf-8 -*-
"""
Updated 13 Aug 2017

@author: Ruiting
"""

import segment as sgm
import classify as clf
import svgparser as sp
import connect as cn
from config import *


def load_clf(retrain_bool):
    """Load the classifer from local. The user can choose the retrain the model.
    
    Args:
        retrain_bool (bool): Whether to retrain the classifier.

    Returns:
        A classifier object.
    """
    if retrain_bool:
        nodeclf = clf.trainSVM(train_folder,train_files,train_labels,training_dot_n,training_mor_n)
        joblib.dump(nodeclf,clf_name)  # Dump the classifier to local        
    else:
        nodeclf = joblib.load(clf_name) 
    return nodeclf

def evaluate(nodeclf,evaluate_files,label):
    """Evaluate the classifier's accuracy and print out the results.
    
    Args:
        nodeclf (obj): A classifer object
        evaluate_files (list): A list of file names for evaluation.
        label (int): The label that the tested shapes should belongs to.
    """
    testdata = []
    for filename in evaluate_files:
        newdata = clf.collectData(test_folder,filename)
        testdata.extend(newdata)    
    correct = 0    
    for data in testdata:
        pred = nodeclf.predict([data])
        if pred == label:
            correct += 1
    print "Correct classified: %d, wrongly classified: %d, total: %d" % (correct,len(testdata)-correct,len(testdata))
    

nodeclf = load_clf(True)
evaluate(nodeclf,evaluate_dots,dot_label)
evaluate(nodeclf,evaluate_morphisms,mor_label)