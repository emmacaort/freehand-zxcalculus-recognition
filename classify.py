# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 22:21:32 2016

@author: Administrator
"""

from shapely import geometry as geo
import svgparser as sp
import element as elm
import segment as sgm
import dataset as ds
from sklearn import svm,linear_model
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier




def collectData(filename,train):
  """
  Collect path information from the file
  """
  data = []
  tree = sp.loadFile(filename)
  pathlist = sp.loadPaths(tree)
  shapelist = sgm.segmentPath(pathlist,train)[0]
  for shape in shapelist:
    shape.getAttributes()
    data.append(shape.attributes)
  return data

def generateData(nodetype,num):
  """
  Nodetype is 'dot' or 'morphism'.
  Return a list of attrubites and a list of labels. 
  """
  data = []
  y = []
  if nodetype=='dot':
    dotpathlist = [ds.generateDotPath() for _ in xrange (num)]
    shapelist = sgm.segmentPath(dotpathlist,train=True)[0]
    for shape in shapelist:
      shape.getAttributes()
      data.append(shape.attributes)
    newy = [0]*len(data)
    y.extend(newy)
  elif nodetype=='morphism':
    morphismpathlist = [ds.generateMorphismPath() for _ in xrange (num)]
    shapelist = sgm.segmentPath(morphismpathlist,train=True)[0]
    for shape in shapelist:
      shape.getAttributes()
      data.append(shape.attributes)
    newy = [1]*len(data)
    y.extend(newy)
  else:
    pass
  return data,y
  
def trainSVM(filenames,labels):
  """
  Train the classifier
  Inputs are a list of filenames and a list of labels
  dot => 0, morphism => 1
  """
  data = []
  y = []
  if len(filenames)!=len(labels):
    print('wrong input')
  else:
    for filename,label in zip(filenames,labels):
      newdata = collectData(filename,train=True)
      newy = [label]*len(newdata)
      data.extend(newdata)
      y.extend(newy)
    dotdata,doty = generateData('dot',10)
    mordata,mory = generateData('morphism',10)
    data.extend(dotdata)
    y.extend(doty)
    data.extend(mordata)
    y.extend(mory)
    #clf = svm.LinearSVC()
    clf = svm.SVC(probability=True)
    clf.fit(data, y)
  return clf
  
def predict(hypotheses,clf):
  """
  Give prediction of all the paths in one file
  Input pathlist is a list of path objects
  Create new path object by: newpath = elm.path(pointlist)
  Get pointlist by: newpointlist = sp.paseStroke(path_str)
  Return a list of type names
  """
  classifications = []
  for shapelist in hypotheses:
    wirelist = []
    dotlist = []
    morphismlist = []
    for shape in shapelist:
      if shape.openCheck() or shape.convexCheck():
        linestring = geo.LineString(shape.pointlist)  
        wirelist.append(elm.wire([shape.end1,shape.end2],shape.pointlist,linestring))
      else:
        shape.getAttributes()
        pred = clf.predict([shape.attributes])
        #print pred
        #confidence = clf.decision_function([shape.attributes])
        #confidence = clf.predict_proba([shape.attributes])
        #print pred, confidence
        if pred==[0]:
          dotlist.append(elm.dot(shape.centroid,shape.poly,shape.pointlist))
          #print 'dot'
        else:
          orient = shape.orientation()
          morphismlist.append(elm.morphism(shape.centroid,shape.poly,shape.pointlist,orient))
    classifications.append([wirelist,dotlist,morphismlist])
    print '==============='
    print('wire:',len(wirelist))
    print('dot:',len(dotlist))
    print('morphism:',len(morphismlist))
  return classifications






