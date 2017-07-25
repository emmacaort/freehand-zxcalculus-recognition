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
    #filenames = ['circle0.svg','circle1.svg','morphism0.svg','morphism1.svg','morphism2.svg']
    filenames = ['circle0.svg','morphism0.svg']
    labels = [0,1]
    nodeclf = clf.trainSVM(filenames,labels)
    svg = sp.loadFile('zx2.svg')
    pathlist = sp.loadPaths(svg)
    hypotheses = sgm.segmentPath(pathlist,train=False)
    supplement = clf.predict(hypotheses,nodeclf)
    [corr_pathlist,correct_ratio] = sgm.correctPathlist(pathlist)
    if corr_pathlist!=None:
        correction = clf.predict(corr_pathlist,nodeclf)
    else:
        correction = None
    alpha=0.8
    [wirelist,dotlist,morphismlist] = cn.findWinner(supplement,correction,alpha,correct_ratio)
    print '=====WINNER====='
    print('wire:',len(wirelist))
    print('dot:',len(dotlist))
    print('morphism:',len(morphismlist))
    tree = sp.loadFile('blank.svg')
    cn.drawOutput(tree,wirelist,dotlist,morphismlist)    
    print 'len of hypotheses:',len(hypotheses)
    sp.writeFile(tree,'c1.svg')
    
    for wire in wirelist:
        print len(wire.pointlist)
main()
