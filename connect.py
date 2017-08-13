# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 12:27:23 2017

@author: 瑞婷
"""

import svgparser as sp
from config import *


def connectWire(wirelist,nodelist):
    """Connect the wires and the nodes.

    Args:
        wirelist (list): A list of wires.
        nodeslist (list): A list of nodes including dots and morphisms.

    """
    for wire in wirelist:
        for [connectnode,angle,i,_] in wire.connect(nodelist):
            connectnode.addConnection([wire, angle, i])


def giveScore(nodelist,wirelist,intersect):
    """Give the connection result a score.

    The default score is 1.0. It will be evaluated by considering the intersection number and connections.

    Args:
        nodelist (list): A list of nodes.
        wirelist (list): A list of wires.
        intersect (int): The number of maximum intersections between the latest drawn stroke and each previous stroke.

    Returns:
        The score.
    """
    score = default_score
    # 1 or 2 intersections might not mean correction. But over 3 intersections are very likley to mean correction.
    # If the new path considered a correction, all the correction hypotheses will get higher scores than normal ones.
    if intersect == 1:        
        score *= beta_1
    elif intersect == 2:
        score *= beta_2
    elif intersect == 3:
        score *= beta_3
    elif intersect >= 4:
        score *= beta_4
    else:
        pass
    # If there is a node or a wire connecting to nothing, the hypothesis will have a lower score.
    elementlist = nodelist + wirelist
    for element in elementlist:
        if len(element.connections)==0:
            score *= alpha_1
        elif len(element.connections)==1:
            score *= alpha_2
        else:
            score *= alpha_3
    return score


def drawOutput(tree,wirelist,dotlist,morphismlist):
    """Draw output to a SVG.

    Args:
        tree (obj): An XML tree object.
        wirelist (list): A list of wires.
        dotlist (list): A list of dots.
        morphismlist (list): A list of morphisms.
    """
    for wire in wirelist:
        sp.addWire(tree,wire)
    for dot in dotlist:
        sp.addDot(tree,dot)
    for morphism in morphismlist:
        sp.addMorphism(tree,morphism)



def findWinner(normal,correction,intersect):
    """Find the hypothesis with the highest score.

    Give the score to each hypothesis in the normal hypotheses and correction hypotheses and find the winner.

    Args:
        normal (list): A list of hypotheses containing a wirelist, a dot list and a morphism list. This set of
                      hypotheses doesn't consider correction issue.
        correction (list): A list of hypotheses where all the hypotheses considering the latest stroke as a
                           correction stroke. This argument could be None.
        intersect (list): The number of maximum intersections between the latest drawn stroke and each previous
                          stroke. This arguments will only be used for correction hypotheses.

    Returns:
        A winner hypothesis containing a wirelist, a dot list and a morphism list.
    """
    maxscore = 0
    # Score the normal hypotheses.
    for [wirelist,dotlist,morphismlist] in normal:
        nodelist = dotlist + morphismlist
        connectWire(wirelist,nodelist)
        score = giveScore(nodelist,wirelist,0)
        if score>maxscore:
            maxscore = score
            winner = [wirelist,dotlist,morphismlist]
    # Score the correction hypotheses.
    if correction!=None:
        for [wirelist,dotlist,morphismlist] in correction:
            nodelist = dotlist + morphismlist
            connectWire(wirelist,nodelist)
            score = giveScore(nodelist,wirelist,intersect)
            if score>maxscore:
                maxscore = score
                winner = [wirelist,dotlist,morphismlist]
    return winner
    