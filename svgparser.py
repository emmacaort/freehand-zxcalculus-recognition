# -*- coding: utf-8 -*-
"""
Created on Sat Jun 03 20:00:00 2017

@author: Administrator
"""
import xml.etree.ElementTree as ET
import element as elm
import numpy as np


teststroke_str = '"path": "M90, 202.72727966308594 L90.90908813476562, 200 L90.90908813476562, 199.09091186523438 L90.90908813476562, 197.27272033691406 L91.81818389892578, 196.36363220214844 L91.81818389892578, 195.4545440673828 L91.81818389892578, 194.5454559326172 L92.7272720336914, 193.63636779785156 L92.7272720336914, 192.72727966308594 L93.63636016845703, 191.81817626953125 L93.63636016845703, 190.90908813476562 L94.54545593261719, 190.90908813476562 L94.54545593261719, 190 L94.54545593261719, 189.09091186523438 L94.54545593261719, 188.18182373046875 L95.45454406738281, 187.27272033691406 L96.36363983154297, 186.36363220214844 L96.36363983154297, 185.4545440673828 L97.2727279663086, 185.4545440673828 L98.18181610107422, 184.5454559326172 L98.18181610107422, 183.63636779785156 L99.09091186523438, 183.63636779785156 L99.09091186523438, 182.72727966308594 L100, 182.72727966308594 L100.90908813476562, 181.81817626953125 L102.7272720336914, 180.90908813476562 L104.54545593261719, 179.09091186523438 L107.2727279663086, 176.36363220214844 L109.09091186523438, 175.4545440673828 L110, 175.4545440673828 L111.81818389892578, 174.5454559326172 L114.54545593261719, 172.72727966308594 L118.18181610107422, 170.90908813476562 L119.09091186523438, 170.90908813476562 L120, 170.90908813476562 L121.81818389892578, 170.90908813476562 L122.7272720336914, 170 L126.36363983154297, 169.09091186523438 L128.18182373046875, 169.09091186523438 L130.90908813476562, 168.18182373046875 L132.72727966308594, 167.27272033691406 L133.63636779785156, 167.27272033691406 L143.63636779785156, 166.36363220214844 L146.36363220214844, 166.36363220214844 L150.90908813476562, 166.36363220214844 L153.63636779785156, 166.36363220214844 L167.27272033691406, 166.36363220214844 L172.72727966308594, 166.36363220214844 L179.09091186523438, 167.27272033691406 L185.4545440673828, 167.27272033691406 L190.90908813476562, 168.18182373046875 L193.63636779785156, 169.09091186523438 L198.18182373046875, 169.09091186523438 L203.63636779785156, 170 L206.36363220214844, 170.90908813476562 L209.09091186523438, 170.90908813476562 L214.5454559326172, 172.72727966308594 L223.63636779785156, 175.4545440673828 L229.09091186523438, 176.36363220214844 L238.18182373046875, 179.09091186523438 L242.72727966308594, 180.90908813476562 L247.27272033691406, 182.72727966308594 L253.63636779785156, 185.4545440673828 L257.2727355957031, 187.27272033691406 L260.9090881347656, 189.09091186523438 L263.6363525390625, 191.81817626953125 L267.2727355957031, 194.5454559326172 L270, 197.27272033691406 L271.81817626953125, 198.18182373046875 L274.5454406738281, 201.81817626953125 L277.2727355957031, 203.63636779785156 L278.18182373046875, 206.36363220214844 L280, 210 L280.9090881347656, 211.81817626953125 L282.7272644042969, 213.63636779785156 L283.6363525390625, 215.4545440673828 L285.4545593261719, 219.09091186523438 L286.3636474609375, 221.81817626953125 L287.2727355957031, 223.63636779785156 L288.18182373046875, 225.4545440673828 L289.0909118652344, 228.18182373046875 L290, 231.81817626953125 L290, 233.63636779785156 L290.9090881347656, 235.4545440673828 L290.9090881347656, 239.09091186523438 L291.81817626953125, 240.90908813476562 L291.81817626953125, 242.72727966308594 L291.81817626953125, 246.36363220214844 L292.7272644042969, 250 L292.7272644042969, 254.5454559326172 L292.7272644042969, 256.3636474609375 L293.6363525390625, 260.9090881347656 L293.6363525390625, 264.5454406738281 L293.6363525390625, 268.18182373046875 L293.6363525390625, 271.81817626953125 L293.6363525390625, 274.5454406738281 L293.6363525390625, 278.18182373046875 L293.6363525390625, 282.7272644042969 L293.6363525390625, 286.3636474609375 L292.7272644042969, 288.18182373046875 L292.7272644042969, 290.9090881347656 L291.81817626953125, 294.5454406738281 L291.81817626953125, 297.2727355957031 L290.9090881347656, 298.18182373046875 L290, 300.9090881347656 L289.0909118652344, 303.6363525390625 L288.18182373046875, 307.2727355957031 L287.2727355957031, 310 L286.3636474609375, 311.81817626953125 L278.18182373046875, 328.18182373046875 L276.3636474609375, 330 L275.4545593261719, 331.81817626953125 L270, 338.18182373046875 L269.0909118652344, 339.0909118652344 L267.2727355957031, 340 L264.5454406738281, 342.7272644042969 L262.7272644042969, 343.6363525390625 L261.81817626953125, 343.6363525390625 L259.0909118652344, 345.4545593261719 L258.18182373046875, 346.3636474609375 L256.3636474609375, 347.2727355957031 L255.4545440673828, 347.2727355957031 L251.81817626953125, 348.18182373046875 L249.09091186523438, 350 L245.4545440673828, 350.9090881347656 L241.81817626953125, 350.9090881347656 L240, 350.9090881347656 L233.63636779785156, 350.9090881347656 L232.72727966308594, 350.9090881347656 L230, 350.9090881347656 L226.36363220214844, 350.9090881347656 L223.63636779785156, 350.9090881347656 L220.90908813476562, 350 L216.36363220214844, 348.18182373046875 L215.4545440673828, 348.18182373046875 L210, 346.3636474609375 L204.5454559326172, 343.6363525390625 L200, 340.9090881347656 L196.36363220214844, 340 L191.81817626953125, 335.4545593261719 L188.18182373046875, 332.7272644042969 L184.5454559326172, 329.0909118652344 L180.90908813476562, 325.4545593261719 L177.27272033691406, 321.81817626953125 L173.63636779785156, 316.3636474609375 L172.72727966308594, 315.4545593261719 L171.81817626953125, 312.7272644042969 L170, 309.0909118652344 L168.18182373046875, 306.3636474609375 L168.18182373046875, 303.6363525390625 L166.36363220214844, 300.9090881347656 L166.36363220214844, 292.7272644042969 L165.4545440673828, 290.9090881347656 L165.4545440673828, 288.18182373046875 L165.4545440673828, 286.3636474609375 L164.5454559326172, 283.6363525390625 L164.5454559326172, 275.4545593261719 L164.5454559326172, 272.7272644042969 L164.5454559326172, 270 L164.5454559326172, 265.4545593261719 L165.4545440673828, 262.7272644042969 L165.4545440673828, 259.0909118652344 L165.4545440673828, 257.2727355957031 L166.36363220214844, 254.5454559326172 L167.27272033691406, 252.72727966308594 L170, 246.36363220214844 L172.72727966308594, 241.81817626953125 L173.63636779785156, 240 L174.5454559326172, 238.18182373046875 L178.18182373046875, 235.4545440673828 L179.09091186523438, 233.63636779785156 L180, 232.72727966308594 L185.4545440673828, 227.27272033691406 L186.36363220214844, 226.36363220214844 L189.09091186523438, 225.4545440673828 L190, 223.63636779785156 L194.5454559326172, 221.81817626953125 L195.4545440673828, 221.81817626953125 L197.27272033691406, 220.90908813476562 L198.18182373046875, 220.90908813476562 L199.09091186523438, 220 L200.90908813476562, 220 L201.81817626953125, 220 L203.63636779785156, 220 L204.5454559326172, 220 L204.5454559326172, 220 '

def loadFile(filename):  
  ET.register_namespace('', "http://www.w3.org/2000/svg")
  ET.register_namespace('dc',"http://purl.org/dc/elements/1.1/")
  ET.register_namespace('cc',"http://creativecommons.org/ns#")
  ET.register_namespace('rdf',"http://www.w3.org/1999/02/22-rdf-syntax-ns#")
  ET.register_namespace('svg',"http://www.w3.org/2000/svg")
  ET.register_namespace('sodipodi',"http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd")
  ET.register_namespace('inkscape',"http://www.inkscape.org/namespaces/inkscape")
  tree = ET.parse(filename)
  return tree

def parseStroke(stroke_str):
  points = stroke_str.split()
  if points[-1] == 'z' :
    points = points[:-1] 
  pointlist = [list(map(float,points[1].split(',')))]
  # the control point in inkscape is different from the normal ones
  rest = list(map(lambda item:list(map(float,item.split(','))),points[3:]))
  pointlist.extend(rest)
  return pointlist    

def dist(pos1,pos2):
  """
  Calculate the eucliean distance between two ends
  """
  return np.linalg.norm(np.array(pos1,dtype=np.float32)-np.array(pos2,dtype=np.float32))

def loadPaths(tree):
  pathlist = []
  for path in getPath(tree):
    pathlist.append(path)
  return pathlist
    
def addStroke(tree,newpath):  
  root = tree.getroot()
  for pathaddr in root.iter('{http://www.w3.org/2000/svg}g'):
      stroke = ET.SubElement(pathaddr,'{http://www.w3.org/2000/svg}path')  
      stroke.attrib['style'] = newpath.style
      stroke.attrib['d'] = newpath.pointStr()
      stroke.attrib['id'] = 'path'+str('1')
      stroke.attrib['inkscape:connector-curvature'] = '0'
      stroke.tail = '\n'       
  return tree    
 
def addPoint(tree,point,pointtype='c'):
  x_str,y_str = str(point[0]),str(point[1])
  root = tree.getroot()
  for pointaddr in root.iter('{http://www.w3.org/2000/svg}g'):
      point = ET.SubElement(pointaddr,'{http://www.w3.org/2000/svg}circle')
      if pointtype == 'c':
        point.attrib['style'] = 'fill: #0000ff' #blue
      else:
        point.attrib['style'] = 'fill: #FF0000' #red
      point.attrib['cx'] = x_str
      point.attrib['cy'] = y_str
      point.attrib['r'] = '0.5'
      point.tail = '\n'
  return tree

def addDot(tree,dot,color='red',radius=10):
  centre = dot.centre
  x_str,y_str = str(centre[0]),str(centre[1])
  r_str = str(radius)
  root = tree.getroot()
  for pointaddr in root.iter('{http://www.w3.org/2000/svg}g'):
      point = ET.SubElement(pointaddr,'{http://www.w3.org/2000/svg}circle')
      if color == 'red':
        point.attrib['style'] = 'fill: #FF0000' #red
      else:
        point.attrib['style'] = 'fill: ##00ff00' #green
      point.attrib['cx'] = x_str
      point.attrib['cy'] = y_str
      point.attrib['r'] = r_str
      point.tail = '\n'
  return tree

def addMorphism(tree,morphism,a=30,b=40,h=20):
    """M = moveto(M X,Y)
    L = lineto(L X,Y)
    H = horizontal lineto(H X)
    V = vertical lineto(V Y)
    Z = closepath()"""
    centre = morphism.centre
    orient = morphism.orient    
    root = tree.getroot()
    corner_str = str(centre[0]+a/2) + ',' + str(centre[1]-h/2)
    for pathaddr in root.iter('{http://www.w3.org/2000/svg}g'):
        stroke = ET.SubElement(pathaddr,'{http://www.w3.org/2000/svg}path')  
        stroke.attrib['style'] = "fill:none;stroke:#000000;stroke-width:0.26458332px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"
        stroke.attrib['d'] =  'M ' + corner_str + ' h -' + str(a) + ' v ' + str(h) + ' h ' + str(b) + ' z'
        stroke.attrib['id'] = 'path'+str('1')
        stroke.attrib['inkscape:connector-curvature'] = '0'
        stroke.tail = '\n'       
    return tree    

  
def addWire(tree,wire,dot_r=10,mor_h=20):
  points = wire.refinePoints()
  if len(wire.connection)!=0:
    for [node,angle,i] in wire.connection:
      if node.getType()=='dot':
        # i is 0 or 1, then -i is 0 or -1
        # wire.ends[i] corresponds to the two end points in the end list
        # points[-i] corresponds to the two end points in the points list
        d = np.array(angle * dot_r / dist(node.centre,wire.ends[i]))
        points[-i] = np.array(node.centre)-d
      else:  # nodetype = morphism
        h = mor_h/2
        [x,y] = angle
        if node.orient in [0,3,4,7]: # north-south       
          d_y = y/abs(y)*h
          d_x = d_y*x/y
          points[-i] = [node.centre[0]-d_x,node.centre[1]-d_y]
        else:
          d_x = x/abs(x)*h
          d_y = d_x*y/x
          d = np.array(d_x,d_y)
          points[-i] = np.array(node.centre)-d
  root = tree.getroot()
  start_str = 'm '+str(points[0][0])+','+str(points[0][1])
  curve_str = ' C' 
  for point in points[1:]:
    curve_str = curve_str + ' ' +str(point[0])+','+str(point[1])
  path_str = start_str + curve_str
  for pathaddr in root.iter('{http://www.w3.org/2000/svg}g'):
      stroke = ET.SubElement(pathaddr,'{http://www.w3.org/2000/svg}path')  
      stroke.attrib['style'] = "fill:none;stroke:#000000;stroke-width:0.26458332px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"
      stroke.attrib['d'] = path_str
      stroke.attrib['id'] = 'path'+str('1')
      stroke.attrib['inkscape:connector-curvature'] = '0'
      stroke.tail = '\n'       
  return tree      

def getPath(tree):    
  root = tree.getroot()
  for stroke in root.iter('{http://www.w3.org/2000/svg}path'):
    stroke_str = stroke.attrib["d"]  
    pointlist = parseStroke(stroke_str)  
    newpath = elm.path(pointlist)
    yield newpath

def transtoInkscapePath(pointlist):
  listlen = len(pointlist)
  i = 0
  interpoint = pointlist[0]
  while i<(listlen-3):
    nextinterpoint = pointlist[i+3]
    pointlist[i+1] = [pointlist[i+1][0]-interpoint[0],pointlist[i+1][1]-interpoint[1]]
    pointlist[i+2] = [pointlist[i+2][0]-interpoint[0],pointlist[i+2][1]-interpoint[1]]
    pointlist[i+3] = [pointlist[i+3][0]-interpoint[0],pointlist[i+3][1]-interpoint[1]]
    # update the interpoint
    # the end of the current curve becomes the start of the next curve
    interpoint = nextinterpoint
    i = i + 3
  return pointlist    
    
def drawSVGPoints(tree):
  "Draw the points and control points of the path"
  for path in getPath(tree):
    for curve in path.curves:    
      tree = addPoint(tree,curve.start,'e')
      tree = addPoint(tree,curve.control1,'c')
      tree = addPoint(tree,curve.control2,'c')
  return tree
    
def writeFile(tree,newname):
  root = tree.getroot()
  root.attrib['{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}docname'] = newname
  tree.write(newname, xml_declaration=True, default_namespace='')


