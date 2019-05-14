#!/usr/bin/env python
'''
    File name: wedge.py
    Author: Suzanne Berger
    Date created: 3/1/2016
    Python Version: 2.7
'''

import sys
from pprint import pprint

# this is prototype and will probably be converted to class and could be imported into any app that uses python

# for testing

wedge_args = [
    ('node1.attr1',4,0.0,0.5,0),
    ('node2.attr2',3,100,10,1),
    ('node3.attr3',2,10,-1,1)
    ]

'''
wedge_args = [
    ('node4.attr6',4,0.0,0.5,1),
    ('node5.attr7',2,0.4,0.1,1)
    ]
'''
#wedge_args = [('node5.attr7',5,2.5,-0.5)]

def get_ranges(wedge_args):
    ''' generate all wedge ranges '''
    
    range_list = []
    for each in wedge_args:
        wedge_num = each[1]
        wedge_start = each[2]
        wedge_step = each[3]
        wedge_stepdir = each[4]
        wedge_range = [wedge_start]
        
        if wedge_stepdir == 0:
            wedge_value = wedge_start
            for n in range(wedge_num):
                wedge_value -= wedge_step
                wedge_range.append(round(wedge_value,3))
            wedge_value = wedge_start
            for n in range(wedge_num):
                wedge_value += wedge_step
                wedge_range.append(round(wedge_value,3))
        else:
            if wedge_stepdir == 2:
                wedge_step = -wedge_step
            for n in range(wedge_num):
                wedge_start += wedge_step
                wedge_range.append(round(wedge_start,3))

        range_list.append([each[0]] + wedge_range)

    return range_list

def get_values(range_list,num_attrs):
    ''' get all combination of wedge values from range_list and return a list of tuples '''
    
    wedge_values = []
    for i in range_list[0][1:]:
        if num_attrs == 1:
            this_wedge = (i,)
            wedge_values.append(this_wedge)
            continue
        for j in range_list[1][1:]:
            if num_attrs == 2:
                this_wedge = (i,j)
                wedge_values.append(this_wedge)
                continue
            for k in range_list[2][1:]:
                this_wedge = (i,j,k)
                wedge_values.append(this_wedge)

    return wedge_values


def getall(wedge_args):
    range_list = get_ranges(wedge_args)
    print "ranges"
    pprint(range_list)
    wedge_values = get_values(range_list, len(wedge_args))
    return wedge_values


# main
if __name__ == '__main__':
    
    num_attrs = len(wedge_args)
    print "wedge_args", wedge_args, num_attrs
    range_list = get_ranges(wedge_args)
    print "range_list",range_list
    wedge_values = get_values(range_list,num_attrs)
    print "wedge_values"
    pprint(wedge_values)
    
    #write_json([w1,w2,w3],wedge_items) # it may be useful to output values to json
    #write_yaml it may be better to output to yaml
    
    sys.exit(0)