# -*- coding: utf-8 -*-
"""
Created on Sun Jun 04 17:24:34 2017

@author: Administrator
"""
from shapely import geometry as geo
import svgparser as sp
import math
import numpy as np
import matplotlib.pyplot as plt 
import time

class curve:
    """Cubic Bezier Curve.
    
    Curve is the basic unit of the path in SVG. Store the two 
    end points and two control points.

    Attributes:
        start: The start point of the bezier curve
        control1: The first control point of the bezier curve
        control2: The second control point of the bezier curve
        end: The end point of the bezier curve
    """
    def __init__(self,start,control1,control2,end):
        """Inits Curve with four points."""
        self.start = start
        self.control1 = control1
        self.control2 = control2
        self.end = end
        
    def pointlist(self):
        """Return a list of the four points. """
        pointlist = [self.start,self.control1,self.control2,self.end]
        return pointlist

class path:
    """SVG path.
    
    A Path describes one freehand stroke in the SVG. Only command
    M - move to, and C - cubic bezier curve are used.
    A path consists of one M command and 3n C command.  

    Attributes:
        ori_pointlist: 
        curves: 
        pointlist: 
        end1:
        end2:
        style:
    """
    def __init__(self,ori_pointlist):
        self.ori_pointlist = ori_pointlist
        self.getCurve()
        self.getPointlist()
        self.getEnds()
        self.style = "fill:none;stroke:#000000;stroke-width:0.26458332px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"
        
    def getCurve(self):
        self.curves = []
        listlen = len(self.ori_pointlist)
        i = 0
        interpoint = self.ori_pointlist[0]
        while i<(listlen-3):
            start = interpoint
            control1 = [start[0]+self.ori_pointlist[i+1][0],start[1]+self.ori_pointlist[i+1][1]]
            control2 = [start[0]+self.ori_pointlist[i+2][0],start[1]+self.ori_pointlist[i+2][1]]
            end = [start[0]+self.ori_pointlist[i+3][0],start[1]+self.ori_pointlist[i+3][1]]
            interpoint = end
            newcurve = curve(start,control1,control2,end)
            self.curves.append(newcurve)
            i = i + 3
            
    def getPointlist(self):
        self.pointlist = []
        for curve in self.curves:
            self.pointlist.append(curve.start)
            self.pointlist.append(curve.control1)
            self.pointlist.append(curve.control2)
            self.pointlist.append(curve.end)
        self.linestring = geo.LineString(self.pointlist)
        
    def getEnds(self):
        self.end1 = self.pointlist[0]
        self.end2 = self.pointlist[-1]

    def pointStr(self):
        pointstr = ['m',','.join(list(map(str,self.ori_pointlist[0]))),'c']
        pointstr.extend(list(map(lambda item:','.join(list(map(str,item))),self.ori_pointlist[1:])))
        return ' '.join(pointstr)
        
    def checkIntersect(self,pathlist):
        maxintersect = 0
        replacedpath = None
        for i,path in enumerate(pathlist):
            try:
              intersect = len(self.linestring.intersection(path.linestring))
            except:
              intersect = 1
            if intersect > maxintersect:
                maxintersect = intersect
                replacedpath = path
        return [replacedpath,maxintersect]


class shape:
  def __init__(self,pointlist):
    self.pointlist = pointlist
    self.transPolygon()
    self.getEnds()
    self.getBound()
    self.getAttributes()
    
  def transPolygon(self):
    self.poly = geo.Polygon(self.pointlist)
    self.area = self.poly.area
    self.perim = self.poly.length
    
  def getEnds(self):
    self.end1 = self.pointlist[0]
    self.end2 = self.pointlist[-1]

  def getBound(self):
    maxpos = np.argmax(self.pointlist,axis=0)
    minpos = np.argmin(self.pointlist,axis=0)
    self.boundpos = np.concatenate((maxpos,minpos))
    self.boundpoints = [self.pointlist[i] for i in self.boundpos]
    [maxx,maxy] = np.max(self.boundpoints,axis=0)
    [minx,miny] = np.min(self.boundpoints,axis=0)
    self.xbound = [minx,maxx]
    self.ybound = [miny,maxy]

  def openCheck(self,threshold=0.10):
    dist = np.linalg.norm(np.array(self.end1,dtype=np.float32)-np.array(self.end2,dtype=np.float32))
    ratio = dist/self.perim
    if ratio > threshold:
      return True
    else:
      return False
      
  def convexCheck(self,threshold = 1.30):
    convexhull = self.poly.convex_hull
    ch_area = convexhull.area
    ratio = ch_area/self.area
    if ratio > threshold:
      return True
    else:
      return False
    #print("---intersect: %s seconds ---" % (time.time() - time1))
  def getAttributes(self):
    #self.perim = self.poly.perimeter
    self.centroid = [self.poly.centroid.x,self.poly.centroid.y]
    #self.angles = map(float,self.poly.angles.values())
    # used for classification
    self.compact = 2*math.sqrt(self.area*math.pi)/self.perim
    self.eccent = self.eccentricity()
    self.rectang = self.rectangularity()
    self.circular = self.circularity()
    self.attributes = [self.compact, self.eccent,self.rectang, self.circular]
    #self.attributes = [self.rectang, self.circular]
  def eccentricity(self):
    dist = np.matrix(self.pointlist) - np.matrix(self.centroid)
    cov = sum(list(map(lambda x:x.T*x, dist)))
    cxx,cxy,cyx,cyy = cov.item(0),cov.item(1),cov.item(2),cov.item(3)
    b = math.sqrt((cxx+cyy)**2-4*(cxx*cyy-cxy**2))
    e1 = cxx + cyy + b
    e2 = cxx + cyy - b
    return e2/e1
  def rectangularity(self):
    boundarea = (self.xbound[1]-self.xbound[0])*(self.ybound[1]-self.ybound[0])
    return self.area/boundarea
  def circularity(self):
    sub = np.array(self.boundpoints, dtype=np.float32) - np.array(self.centroid, dtype=np.float32)
    ecldndist = list(map(lambda x:np.linalg.norm(x),sub))
    r = max(ecldndist)
    self.radius = np.mean(ecldndist)
    circlearea = math.pi*r**2
    return self.area/circlearea
  def orientation(self):
    distances = [sp.dist(self.centroid,boundpoint) for boundpoint in self.boundpoints]
    cornerpoint = self.boundpoints[np.argmax(distances)]
    [dx,dy] = np.array(self.centroid) -np.array(cornerpoint)
    if dx < 0 and dy < 0:
      if dx < dy:
        return 0
      else:  
        return 1
    elif dx >= 0 and dy < 0:
      if dx < -dy:
        return 2
      else:
        return 3
    elif dx > 0 and dy > 0:
      if dx > dy:
        return 4
      else:
        return 5
    else:
      if dx > -dy:
        return 6
      else:
        return 7

class dot():
  def __init__(self,centre,poly,pointlist):
    self.centre = centre
    self.poly = poly
    self.pointlist = pointlist
    self.connection = 0
  def getType(self):
    return 'dot'
  def addConnection(self):
    self.connection += 1
    
class morphism():
  def __init__(self,centre,poly,pointlist,orient):
    self.centre = centre
    self.poly = poly
    self.pointlist = pointlist
    self.orient = orient
    self.connection = 0
  def getType(self):
    return 'morhpsim'
  def addConnection(self):
    self.connection += 1

class wire():
  def __init__(self,ends,pointlist,linestring):
    self.ends = ends
    self.pointlist = pointlist
    
  def calculateAngle(self,end,centre):
    return np.array(centre) - np.array(end)
    
  def connect(self,nodelist,threshold=10.0):
    self.connection = []
    for i,end in enumerate(self.ends):
      neighbours = []
      for node in nodelist:
        distlist = [sp.dist(end,point) for point in node.pointlist]
        mindist = min(distlist)
        if mindist < threshold:
          neighbours.append([node,mindist])
      try:
        mindist_idx = np.argmin(neighbours,axis=0)[1]
        connectnode = neighbours[mindist_idx][0]
        angle = self.calculateAngle(end,connectnode.centre)
        connectnode.addConnection()
        self.connection.append([connectnode,angle,i])
      except:
        pass
    
  def refinePoints(self,pnumber=6):
    # pnumber should be 3n
    listlen = len(self.pointlist)
    if listlen>pnumber:
      interval = listlen/float(pnumber)
      pointpos= map(lambda x:int(x*interval),range(pnumber))
      refinedpoints = [self.pointlist[i] for i in pointpos]
      refinedpoints.append(self.pointlist[-1])
    else:
      refinedpoints = self.pointlist
    # check and change ends
    return refinedpoints
    #self.refinedpoints = sp.transtoInkscapePath(refinedpoints)