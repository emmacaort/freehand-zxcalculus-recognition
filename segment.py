# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 19:55:25 2017

@author: Administrator
"""

import itertools
import copy
import svgparser as sp
import element as elm
import numpy as np

 
    
def matchPaths(path1,path2,threshold=10.0):
    """Get the match type of two paths.

    Each path has two ends. Calculate the distance of these ends.
    If some distance is lower than a threshold, then we consider these 
    two path could be grouped together. The match type is how these two
    paths connected.

    Args:
        path1: The first path.
        Path2: The second path. 
        threhold: The threshold number of distance.

    Returns:
        A list. The first element is the two paths. The second element is 
        the matchtype. 
        For example:

        [instance.path]

        If a key from the keys argument is missing from the dictionary,
        then that row was not found in the table.

    """
    matchtype = []
    d0 = sp.dist(path1.end1,path2.end1)
    d1 = sp.dist(path1.end1,path2.end2)
    d2 = sp.dist(path1.end2,path2.end1)
    d3 = sp.dist(path1.end2,path2.end2)
    for i,d in enumerate([d0,d1,d2,d3]):
        if d < threshold:
            matchtype.append(i)
    return [[path1,path2],matchtype]

def iterMatch(pathlist):
    """Iterate the pathlist to find the matches between each pairwise paths. 
    
    All possible match type inlcudes [0],[1],[2],[3],[0,3],[1,2]. Only valid matches
    will be appended into the matchlist.

    Args:
        pathlist: The list of all the paths.

    Returns:
        A list of all the matches. Each match includes two paths and thier
        match type. For example:

        [[element.path instance,element.path instance],[0]]
    """
    matchlist = []
    valid_matchtype = [[0],[1],[2],[3],[0,3],[1,2]]
    for i,path in enumerate(pathlist):
      restpaths = pathlist[(i+1):]
      for restpath in restpaths:
        match = matchPaths(path,restpath)
        if (match[1] in valid_matchtype): 
          matchlist.append(match)
    return matchlist

def refineMatch(matchlist):
    """
    Refine the matchlist, find matches with three or more paths
    """
    newmatchlist = matchlist[:]
    for match in matchlist:
        tempmatchlist = matchlist[:]    
        [path1,path2] = match[0]
        tempmatchlist.remove(match)  # create a copy list without current match
        match1 = None
        match2 = None
        # try to find three matches satisfying: 
        # match = [[path1,path2],[x]]; match1 = [[path2,path3],[y]]; match2 = [[path1,path3],[z]]
        for othermatch in tempmatchlist:
            if path1 in othermatch[0]:
                match1 = othermatch
            if path2 in othermatch[0]:
                match2 = othermatch
        if match1 != None and match2 != None:
            # make tempmatch = [path1,path2,path3]
            tempmatch = match1[0][:]
            tempmatch.extend(match2[0])
            # reduce the duplicate path
            tempmatch.sort()
            tempmatch = list(tempmatch for tempmatch,_ in itertools.groupby(tempmatch))
            tempmatch = [tempmatch,[]]
            if (len(tempmatch[0])==3) and (tempmatch not in newmatchlist):
                newmatchlist.append(tempmatch)
    return newmatchlist

def connect2Paths(match):
  """
  Return a new pointlist if two paths should be connected
  Return a blank pointlist if two paths should be separate
  """
  [path1,path2] = match[0]
  if match[1]==[0]:
    revpath1 = copy.deepcopy(path1.pointlist[::-1])
    temppointlist = copy.deepcopy(revpath1)
    temppointlist.extend(path2.pointlist)
    temppointlist = sp.transtoInkscapePath(temppointlist)
    return elm.path(temppointlist)
  elif match[1]==[1]:
    temppointlist = copy.deepcopy(path2.pointlist)
    temppointlist.extend(path1.pointlist)
    temppointlist = sp.transtoInkscapePath(temppointlist)
    return elm.path(temppointlist)
  elif match[1]==[2]:
    temppointlist = copy.deepcopy(path1.pointlist)
    temppointlist.extend(path2.pointlist)
    temppointlist = sp.transtoInkscapePath(temppointlist)
    return elm.path(temppointlist)
  elif match[1]==[3]:
    revpath2 = copy.deepcopy(path2.pointlist[::-1])
    temppointlist = copy.deepcopy(path1.pointlist)
    temppointlist.extend(revpath2)
    temppointlist = sp.transtoInkscapePath(temppointlist)
    return elm.path(temppointlist)
  elif match[1]==[0,3]:
    revpath2 = copy.deepcopy(path2.pointlist[::-1])
    temppointlist = copy.deepcopy(path1.pointlist)
    temppointlist.extend(revpath2)
    temppointlist = sp.transtoInkscapePath(temppointlist)
    return elm.path(temppointlist)
  else: # match[2]==[1,2]
    temppointlist = copy.deepcopy(path1.pointlist)
    temppointlist.extend(path2.pointlist)
    temppointlist = sp.transtoInkscapePath(temppointlist)
    return elm.path(temppointlist)

def connect3Paths(match):
    print '=====connect 3 paths====='
    [path1,path2,path3] = match[0]
    match1 = matchPaths(path1,path2)
    path12 = connect2Paths(match1)
    match2 = matchPaths(path12,path3)
    path123 = connect2Paths(match2)
    return path123

def connectPath(match):
    if len(match[0])==2:
        return connect2Paths(match)
    elif len(match[0])==3:
        return connect3Paths(match)
        
def yieldBinary(n):
  """
  Yield 2**n binary numbers with the same length
  The zero and one represents we use the match or not
  """
  maxnum = 2**n
  length = len(bin(maxnum-1))-2 # 2 is the length of '0b'
  for i in range(2**n):
    binary = bin(i)[2:]
    if len(binary)<length:
      omitzeros = '0'*(length-len(binary))
      binary = omitzeros+binary
    yield binary
    
def yieldHypotheses(pathlist,matchlist):
    n = len(matchlist)
    for binary in yieldBinary(n):  # each binary is one hypothesis
        print '===== binary :'+binary+' ====='
        temppathlist = pathlist[:]
        try:
            for i in range(len(binary)):
                if binary[i]=='1':
                    # using this match, combine the pair of paths to a new path
                    match = matchlist[i]
                    newpath = connectPath(match)
                    print 'newpath len:',len(newpath.pointlist)
                    if all(path in temppathlist for path in match[0]):
                        temppathlist = [path for path in temppathlist if path not in match[0]]
                        temppathlist.append(newpath)
                        for path in temppathlist:
                            print 'path in temppathlist len:',len(path.pointlist)                        
                    else:
                        raise Exception('path not in pathlist')
            #for path in temppathlist:
                #print len(path.pointlist)
            yield temppathlist
        except:
            pass

       
 
def segmentPath(pathlist,train):
  """
  For training, return a set of shapelist hypotheses
  For classifying, return one shapelist
  """
  hypotheses = []
  if train == False:  
    matchlist = iterMatch(pathlist)
    matchlist = refineMatch(matchlist)
    #print 'matchlist len after refine:',len(matchlist)
    for hypothesis in yieldHypotheses(pathlist,matchlist):
      shapelist = [elm.shape(path.pointlist) for path in hypothesis]
      hypotheses.append(shapelist)
  else:
    shapelist = [elm.shape(path.pointlist) for path in pathlist]
    hypotheses.append(shapelist)
  return hypotheses
  
def correctPathlist(pathlist):
  # check correction
  lastpath = pathlist[-1]
  testlist = pathlist[:]
  testlist.remove(lastpath)
  [replacedpath,intersect] = lastpath.checkIntersect(testlist)
  if replacedpath!=None:
    pathlist.remove(replacedpath)
    correct_ratio = 1.05**intersect
    return [segmentPath(pathlist,train=False),correct_ratio]
  else:
    return [None,1.0]