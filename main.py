#!/usr/bin/python2
# -*- coding: utf-8 -*-
"""
Updated 13 Aug 2017

@author: Ruiting
"""

import segment as sgm
import classify as clf
import svgparser as sp
import connect as cn
import tikzdraw as td
from config import *
from sklearn.externals import joblib


def main():
    """The main recognition program.
    """
    
    # Load the classifier
    nodeclf = joblib.load(clf_name) 
    
    # Load the test file
    svg = sp.loadFile(test_folder,test_file)
    pathlist = sp.loadPaths(svg)
    
    # Generate hypotheses
    hypotheses = sgm.segmentPath(pathlist,train=False)
    [corr_pathlist,intersect] = sgm.correctPathlist(pathlist)
    
    # Classifying diagram elements in each hypothesis
    normal = clf.predict(hypotheses,nodeclf)
    if corr_pathlist!=None:
        correction = clf.predict(corr_pathlist,nodeclf)
    else:
        correction = None
        
    # Score the hypotheses and finding the winner
    [wirelist,dotlist,morphismlist] = cn.findWinner(normal,correction,intersect)

    print '=====RESULT====='
    print 'Hypotheses number:',len(hypotheses)
    print('wire:',len(wirelist))
    print('dot:',len(dotlist))
    print('morphism:',len(morphismlist))
    print '================'

    # Draw outputs    
    tree = sp.loadFile(test_folder,background)
    cn.drawOutput(tree,wirelist,dotlist,morphismlist)
    sp.writeFile(tree,output)
    try:
        print 'LaTex Code:'
        latex_command = td.create_diagram(dotlist,morphismlist,wirelist)
        print latex_command
    except:
        pass

main()
