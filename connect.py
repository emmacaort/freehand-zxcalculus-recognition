# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 12:27:23 2017

@author: 瑞婷
"""

import svgparser as sp
import element as elm
import numpy as np


def connectWire(wirelist,nodelist):
  for wire in wirelist:
    wire.connect(nodelist)

def giveScore(nodelist,wirelist,alpha,correct_ratio):
    score = 1.0 * correct_ratio
    for node in nodelist:
        if node.connection==0:
            score *= alpha
        elif node.connection==1:
            score *= 1.05
        else:
            score *= 1.2
    for wire in wirelist:
        if len(wire.connection)==0:
            score *= alpha
        elif len(wire.connection)==1:
            score *= 1.05
        else:
            score *= 1.2    
    print 'score:',score
    return score

# give output
def printOutput(wirelist,dotlist,morphismlist):
  for dot in dotlist:
    print dot.centre
  for morphism in morphismlist:
    print morphism.centre,morphism.orient
  for wire in wirelist:
    for connection in wire.connection:
      [node,angle,i] = connection
      print node.getType(),node.centre
      print angle

def drawOutput(tree,wirelist,dotlist,morphismlist):
  for wire in wirelist:
    sp.addWire(tree,wire)
  for dot in dotlist:
    sp.addDot(tree,dot)
  for morphism in morphismlist:
    sp.addMorphism(tree,morphism)
  return tree

def findWinner(supplement,correction,alpha,correct_ratio):
  maxscore = 0
  for [wirelist,dotlist,morphismlist] in supplement:
    nodelist = dotlist + morphismlist
    connectWire(wirelist,nodelist)
    score = giveScore(nodelist,wirelist,alpha,1.0)
    if score>maxscore:
      maxscore = score
      winner = [wirelist,dotlist,morphismlist]
  if correction!=None:
    for [wirelist,dotlist,morphismlist] in correction:
      nodelist = dotlist + morphismlist
      connectWire(wirelist,nodelist)
      score = giveScore(nodelist,wirelist,alpha,correct_ratio)
      print score
      if score>maxscore:
        maxscore = score
        winner = [wirelist,dotlist,morphismlist]      
  return winner
    