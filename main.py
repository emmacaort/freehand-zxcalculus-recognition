#!/usr/bin/python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 14:37:30 2017

@author: 瑞婷
"""
import segment as sgm
import classify as clf
import svgparser as sp
import connect as cn


def main():
    print 'Training the node classifier...'
    filenames = ['circle0.svg','circle1.svg','circle2.svg','circle3.svg','morphism0.svg','morphism1.svg','morphism2.svg']
    labels = [1,1,1,1,-1,-1,-1]
    nodeclf = clf.trainSVM(filenames,labels,1,1)
    svg = sp.loadFile('003.svg')
    pathlist = sp.loadPaths(svg)
    
    print 'Generating hypotheses...'
    hypotheses = sgm.segmentPath(pathlist,train=False)
    [corr_pathlist,intersect] = sgm.correctPathlist(pathlist)
    
    print 'Classifying diagram elements in each hypothesis...'
    normal = clf.predict(hypotheses,nodeclf)
    if corr_pathlist!=None:
        correction = clf.predict(corr_pathlist,nodeclf)
    else:
        correction = None
        
    print 'Scoring the hypotheses and finding the winner...'
    [wirelist,dotlist,morphismlist] = cn.findWinner(normal,correction,intersect)

    print '=====WINNER====='
    print 'Hypotheses number:',len(hypotheses)
    print('wire:',len(wirelist))
    print('dot:',len(dotlist))
    print('morphism:',len(morphismlist))
    tree = sp.loadFile('blank.svg')
    cn.drawOutput(tree,wirelist,dotlist,morphismlist)      
    sp.writeFile(tree,'c1.svg')
    
main()
