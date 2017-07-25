# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 12:05:30 2017

@author: 瑞婷
"""

import element as elm
import svgparser as sp
import numpy as np
import random
import math

def randommove(point,r,ratio):
  moverange = r*ratio
  xmove = (random.random()-0.5)*2*moverange
  ymove = (random.random()-0.5)*2*moverange
  point = [point[0]+xmove,point[1]+ymove]
  return point 

def deform(pointlist,r,ratio):
  pointlist = [randommove(point,r,ratio) for point in pointlist]
  return pointlist

def circlepoint(c,r):
  """
  Generate a point [x,y] lying on a circle
  The default centre of the cicle is (200,200), default radius is 100.
  """
  x = random.uniform(-r,r)
  negative = bool(random.getrandbits(1))
  y = math.sqrt(r**2-x**2)
  if negative:
    y = -y
  return [x+c[0],y+c[1]]



def circlepointlist(pointnum,c,r,deformratio):
  """
  Generate a pointlist of points lying on a 'freehand' circle.
  The default number of points is 60. The number should be 3n.
  Points in the list are clockwise.
  """
  pointlist = [circlepoint(c,r) for _ in xrange (pointnum)]
  posy = []
  negy = []
  for point in pointlist:
    if point[1]>c[1]:
      posy.append(point)
    else:
      negy.append(point)
  posy.sort(key=lambda x:x[0])
  negy.sort(key=lambda x:x[0],reverse=True)
  pointlist = posy+negy
  pointlist.append(pointlist[0]) # make a close circle
  pointlist = deform(pointlist,r,deformratio)
  pointlist = sp.transtoInkscapePath(pointlist)
  return pointlist

def generateDotPath(pointnrange=[51,120],c=[200,200],rrange=[80,120],deformratio=0.03):
  [pointnum,r] = generateArgs([pointnrange,rrange])
  pointlist = circlepointlist(pointnum,c,r,deformratio)
  dotpath = elm.path(pointlist)
  return dotpath

def trapezoidpoint(c,a,b,h,edge):
  if a>b:
    a,b = b,a  # make sure a is smaller than b
  if edge == 0:
    # the top edge
    x = random.uniform(-1,1)*(a/2)
    y = h/2
  elif edge == 1:
    # the right edge
    y = random.uniform(-1,1)*h/2
    x = (a-b)/h * y + b/2
  elif edge == 2:
    # the bottom edge
    x = random.uniform(-a/2,b-a/2)
    y = -h/2
  else:
    # edge==3, the left edge
    x = -a/2
    y = random.uniform(-1,1)*h/2
  point = [x+c[0],y+c[1]]
  return point

def trapezoidpointlist(pointnum,c,a,b,h,deformratio):
  edges = [[] for i in range(4)]
  edge_i = [random.getrandbits(2) for i in range(pointnum)]
  for i in edge_i:
    point = trapezoidpoint(c,a,b,h,i)
    edges[i].append(point)
  edges[0].sort(key=lambda x:x[0])
  edges[1].sort(key=lambda x:x[0])
  edges[2].sort(key=lambda x:x[0],reverse=True)
  edges[3].sort(key=lambda x:x[1])
  pointlist = edges[0]+edges[1]+edges[2]+edges[3]
  #pointlist = edges[2]
  pointlist.append(pointlist[0])
  r = math.sqrt((a**2)/4+(b**2)/4)
  pointlist = deform(pointlist,r,deformratio)
  pointlist = sp.transtoInkscapePath(pointlist)
  return pointlist

def generateArgs(ranges):
  args = [random.randint(*irange) for irange in ranges]
  return args
  
def generateMorphismPath(pointnrange=[75,120],c=[200,200],arange=[60,100],brange=[80,150],hrange=[40,80],deformratio=0.03):
  """
  Generate a pointlist of points lying on a 'freehand' morphism and transorm it into a path object.
  The default number of points is 60. The number should be 3n.
  Points in the list are clockwise.
  """
  [pointnum,a,b,h] = generateArgs([pointnrange,arange,brange,hrange])
  pointlist = trapezoidpointlist(pointnum,c,a,b,h,deformratio)
  morphismpath = elm.path(pointlist)
  return morphismpath  


tree = sp.loadFile('blank.svg')  
path0 = generateDotPath()
for point in path0.pointlist:
  sp.addPoint(tree,point)
tree = sp.addStroke(tree,path0)
sp.writeFile(tree,'datatest0.svg')


