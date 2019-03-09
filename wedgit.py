#!/usr/bin/env python
"""
    Return numeric list with values derived from input arguments.
    
    File: wedgit.py
    Author: Suzanne Berger
    Date Created: 09/21/2018
    Python Version: 2.7
"""

import sys
from pprint import pprint

def wedge_minmax(start_value = 0.5, end_value = 1.5, factor = 0.25):
    """ Create list of wedge values using input start end values and scale factor increment. """

    wedge_values = [start_value]

    next_value = start_value
    step_value = round((end_value - start_value) * factor, 2)
    while True:
        next_value += step_value
        if next_value < end_value:
            wedge_values.append(round(next_value,3))
        else:
            break

    wedge_values.append(end_value)

    print(">>> Wedge list derived from start {}, end {}, and step factor {}".
          format(start_value, end_value, factor))
    pprint(wedge_values)
    return wedge_values


def wedge_startstep(start_value = 0.5, step_size = 0.25, num_steps = 3):
    """ Create list of wedge values using input start value, step size and number of steps. """

    wedge_values = [start_value]
    next_value = start_value
    for i in range(num_steps - 1):
        next_value += step_size
        wedge_values.append(round(next_value,3))

    print(">>> Wedge list derived from start {}, step size {}, and step number {}".
          format(start_value, step_size, num_steps))
    pprint(wedge_values)
    return wedge_values


def usage():
    """ Print help message """
    
    print(">>> Usage >>> Return numeric list with values derived from input arguments.")
    print("Enter either '-mx' or '-ss' as first argument to select wedging method.")
    print("If no arguments given after option then defaults will be used")
    print("For option '-mx', enter arguments for <min value> <max value> <step factor>")
    print("For option '-ss', enter arguments for <start value> <step factor> <number of steps>")


########################################################################################################
# main
########################################################################################################
if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        sys.exit(1)

    wedge_option = sys.argv[1]
    wedge1_values = wedge2_values = []
        
    if wedge_option == "-mx" and len(sys.argv) == 2:
        wedge1_values = wedge_minmax()

    elif wedge_option == "-ss" and len(sys.argv) == 2:
        wedge2_values = wedge_startstep()

    elif wedge_option == "-mx":
        try:
            wdg_min = float(sys.argv[2])
            wdg_max = float(sys.argv[3])
            wdg_factor = float(sys.argv[4])
            wedge1_values = wedge_minmax(wdg_min, wdg_max, wdg_factor)
        except:
            print("%s *** Error *** Invalid arguments" % sys.argv[0])
            usage()
            sys.exit(1)

    elif wedge_option == "-ss":
        try:
            wdg_min = float(sys.argv[2])
            wdg_step = float(sys.argv[3])
            wdg_num = int(sys.argv[4])
            wedge2_values = wedge_startstep(wdg_min, wdg_step, wdg_num)
        except:
            print("%s *** Error *** Invalid arguments" % sys.argv[0])
            usage()
            sys.exit(1)

    sys.exit()

