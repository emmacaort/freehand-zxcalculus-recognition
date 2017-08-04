# -*- coding: utf-8 -*-
"""
Created on Thu Aug 03 22:21:40 2017

@author: Administrator
"""

import segment as sgm
import classify as clf
import svgparser as sp
import connect as cn

def evaluate():
    """
    train_filenames = ['circle0.svg','circle1.svg','circle2.svg','circle3.svg','morphism0.svg','morphism1.svg','morphism2.svg']
    train_labels = [1,1,1,1,-1,-1,-1]
    #train_filenames = ['circle0.svg','circle1.svg','morphism0.svg','morphism1.svg']
    #train_labels = [0,0,1,1]
    nodeclf = clf.trainSVM(train_filenames,train_labels,800,800) 
    """
    test_filenames = ['circle4.svg','circle5.svg']
    """
    testdata = []
    for filename in test_filenames:
        newdata = clf.collectData(filename)
        testdata.extend(newdata)
    
    correct = 0    
    for i,data in enumerate(testdata):
        pred = nodeclf.predict([data])
        if pred == 1:
            correct += 1
        else:
            print i
    print correct,len(testdata)
    """
    pathlist = []
    for name in test_filenames:
        tree = sp.loadFile(name)
        pathlist0 = sp.loadPaths(tree)
        pathlist.extend(pathlist0)
    path0 = pathlist[104]
    tree0 = sp.loadFile('blank.svg')
    sp.addStroke(tree0,path0)
    sp.writeFile(tree0,'c1.svg')


evaluate()