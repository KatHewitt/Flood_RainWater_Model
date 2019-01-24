#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: KatHewitt
"""


def makescalar(diff, group_total, flow_scalar):
    
    
    if diff > 0:                                
        group_total += diff                     
        flow_scalar.append(diff/group_total)     
    else:
        flow_scalar.append(0)                   
        

def checkmax(diff, rain_area, max_output):
    
    if diff > 0:                                
        if rain_area < max_output:              
            checkmax.flow = rain_area           
        else:
            checkmax.flow = max_output          
 
          
def addrain(rain_area, rainfall):
    
    for i in range (len(rain_area)):            
        for j in range (len(rain_area)):    
            rain_area[i][j] += rainfall         


def clear(diff, flow_scalar, group_total):
    
    diff.clear()
    flow_scalar.clear()
    group_total = 0
    return group_total
