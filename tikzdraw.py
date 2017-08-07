# -*- coding: utf-8 -*-
"""
Created on Wed Aug 02 16:25:49 2017

@author: Administrator
"""

import svgparser as sp
import numpy as np
import itertools


def organize_wires(morphismlist,wirelist,edge_len=5.0):
    for morphism in morphismlist:
        south,north = [],[]
        for connection in morphism.connections:
            angle = connection[1]
            if angle[1] < 0:
                south.append(connection)
            else:
                north.append(connection)
        for side in [south,north]:
            wires_n = len(side)
            if wires_n > 1:
                shift_list = xshift_list(wires_n,edge_len)
                for j,[wire,_,i] in enumerate(side):
                    wire.changeShift(i,shift_list[j])

def preprocess(dotlist,morphismlist,nodelist,wirelist,ref_centre,unit_d):
    organize_wires(morphismlist,wirelist)
    i = 0
    points = []
    #  The relative position of ref_node is default = [0,0]
    for node in nodelist:
        node.giveId(i)
        i += 1
        relative_pos = get_relative_pos(node.centre,ref_centre,unit_d)
        points.append(relative_pos)
        node.getRelativePos(relative_pos)

def get_ref_centre(nodelist):
    centres = [node.centre for node in nodelist]
    min_d = sp.dist(centres[0], centres[1])
    min_p0,min_p1 = centres[0], centres[1]
    for p0, p1 in itertools.combinations(centres, 2):
        d = sp.dist(p0,p1)
        if d < min_d:
            min_d = d
            min_p0,min_p1 = p0,p1   
    min_x = abs(min_p0[0] - min_p1[0])
    min_y = abs(min_p0[1] - min_p1[1])
    unit_d = max(min_x, min_y)
    return [min_p0,unit_d]

def get_relative_pos(abs_pos,ref_centre,unit_d,unit=1.0): 
    rel_x = round((abs_pos[0] - ref_centre[0])/unit_d)*unit
    rel_y = -round((abs_pos[1] - ref_centre[1])/unit_d)*unit  # Different coordinate system
    return [rel_x,rel_y]

def transform_angle(sub,raound_value=30.0):
    x,y = sub  
    x,y = -x,-y  # let the node be the centre
    x += 0.000001  # avoid divide zero
    y = -y  # origin is at bottom-left corner in latex
    angle = np.arctan(y/x)* 180 / np.pi
    angle = round(angle/raound_value)*raound_value
    if y > 0 and angle < 0: 
        angle = angle + 180
    if y < 0:
        if angle < 0:
            angle = angle + 360
        else:
            angle = angle + 180
    return angle

def transform_direction(angle,morphism_dir=None):
    if morphism_dir == None:
        return round(angle/90.0)*90
    else:
        if morphism_dir == "north":
            return 90
        elif morphism_dir == "south":
            return 270
        else:
            print "wrong node"
            return 0
            
def xshift_list(wires_n,edge_len):
    shift_list = [0] * wires_n
    if wires_n % 2 == 0:
        interval = edge_len/wires_n
        shift_list[0] = -edge_len/2 + interval/2
    else:
        interval = (edge_len/2) / ((wires_n-1)/2)
        shift_list[0] = -edge_len/2
    for i in range(1,wires_n):
        shift_list[i] = shift_list[i-1] + interval
    return shift_list


                    
    
def interface_str(interface,angle):
    if type(interface) == list:  # interface is a point
        return "+(%.2f,%.2f)" % (interface[0], interface[1])
    else:  # interface is a node object
        if interface.getType() == "dot":  # A dot object
            return "(%d.center)" % (interface.node_id)
        else:  # A morphism object
            if angle >= 0 and angle <= 180:
                return "(%d.north)" % (interface.node_id)
            else:
                return "(%d.south)" % (interface.node_id)
    
def pos_str(pos):
    x,y = pos
    return "(%.2f,%.2f)" % (x,y)
    # remember to change the y coordinate? (0,0) in the bottom-left 

def node_wire_info(connectnode,sub,wire):
    angle = transform_angle(sub)
    node_str = interface_str(connectnode,angle)
    if connectnode.getType() == "morphism":
        morphism_dir = node_str[-6:-1]
        angle = transform_direction(angle,morphism_dir)
    return [node_str,angle]
                    
def draw_node(node):
    return "  \\node[%s%s%s] (%d) at %s {%s}; \n" % (node.colour, node.getType(), node.getOrientStr(),
                                                     node.node_id, pos_str(node.relative_pos), node.func_name)

def draw_wire(out_str,in_str,out_angle=None,in_angle=None,xshift="",interpoints=None):
    if out_angle == None or in_angle == None:
        return "  \draw %s to %s; \n" % (out_str, in_str)
    else:
        return "  \draw[out=%d,in=%d] %s to %s; \n" %(out_angle, in_angle, out_str, in_str)

def draw_longwire(out_str,in_str,out_angle,in_angle,interpoints_str):
    return "  \draw %s%s%s; \n" %(out_str, interpoints_str, in_str)
        
    
def create_diagram(dotlist,morphismlist,wirelist):
    nodelist = dotlist+morphismlist
    [ref_centre,unit_d] = get_ref_centre(nodelist)
    preprocess(dotlist,morphismlist,nodelist,wirelist,ref_centre,unit_d)
    
    command ="\\[\\begin{tikzpicture} \n"
    
    for node in nodelist:      
        node_str = draw_node(node)
        command += node_str
        out_in = [[0,0],[0,0]]  # To record absolute position of out_node and in_node
    for wire in wirelist:
        connected_ends = []
        for [connectnode, sub, i, shift] in wire.connections:
            if i == 0:  # connectnode == out_node
                out_in[0] = connectnode.centre
                [out_str, out_angle] = node_wire_info(connectnode,sub,wire)
                if shift != 0:
                    shift_str = "([xshift=%.3fmm]" % (shift)
                    out_str = shift_str + out_str[1:]
            if i == 1:  # connectnode == in_node 
                out_in[1] = connectnode.centre
                [in_str, in_angle] = node_wire_info(connectnode,sub,wire)
                if shift != 0:
                    shift_str = "([xshift=%.3fmm]" % (shift)
                    in_str = shift_str + in_str[1:]
            connected_ends.append(i)
        # At least one end connects to nothing
        # These ends connect to a point
        if len(connected_ends) < 2:  
            rest_i = [i for i in [0,1] if i not in connected_ends]
            for i in rest_i:
                end = wire.ends[i]
                out_in[i] = wire.ends[i]
                relative_pos = get_relative_pos(end,ref_centre,unit_d)
                if i == 0:                     
                    sub = [x-y for x, y in zip(wire.pointlist[1],end)]
                    out_angle = transform_direction(transform_angle(sub))
                    out_str = interface_str(relative_pos,out_angle)
                if i == 1: 
                    sub = [x-y for x, y in zip(wire.pointlist[-2],end)]
                    in_angle = transform_direction(transform_angle(sub))
                    in_str = interface_str(relative_pos,in_angle)
        wire_len = wire.getLength()
        len_times = wire_len/unit_d  
        if wire_len > unit_d * 1.5:
            point_n = int(round(len_times))  # The 1 compensates for the removed start and end points
            if point_n > 4:
                point_n =4
            interpoints = wire.refinePoints(point_n)[1:-1]
            interpoints_str = ""
            relative_points = []
            # Create a list of relative interpoints.
            for i,point in enumerate(interpoints):
                if i==0:
                    rel_point = get_relative_pos(point,out_in[0],unit_d/2,0.5)
                else:
                    rel_point = get_relative_pos(point,interpoints[i-1],unit_d/2,0.5)
                relative_points.append(rel_point)
            # Create the strings of wires
            previous_in_angle = 0
            for i,point in enumerate(relative_points):                
                if i == 0:
                    p_out_angle = out_angle
                    previous_point = out_in[0]
                else:
                    p_out_angle = (previous_in_angle+180)%360  # The opposite direction of the in_angle of the previous point
                    previous_point = interpoints[i-1]
                current_point = interpoints[i]
                sub = [-previous_point[0]+current_point[0],-previous_point[1]+current_point[1]]
                p_in_angle = transform_angle(sub)
                p_in_angle = transform_direction(p_in_angle)
                previous_in_angle = p_in_angle
                point_str = " to [out=%d, in=%d] +%s" %(p_out_angle,p_in_angle,pos_str(point))
                interpoints_str += point_str
            last_out = (p_in_angle+180)%360
            last_str = " to [out=%d, in=%d]" % (last_out,in_angle)
            interpoints_str += last_str
            wire_str = draw_longwire(out_str,in_str,out_angle,in_angle,interpoints_str)
        else:
            wire_str = draw_wire(out_str,in_str,out_angle,in_angle)
        command += wire_str
    command += "\\end{tikzpicture}\\] \n" 
    return command
