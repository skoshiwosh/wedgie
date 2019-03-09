#!/usr/bin/env python
"""
    Create a locator with added attributes for wedge. 
"""

from maya import cmds

import wedgit

def mkwdg(wdgnode_name="wdg1"):
    new_wedge = cmds.spaceLocator(n=wdgnode_name)
    this_wedge = new_wedge[0]
    cmds.select(this_wedge, r=True)
    cmds.addAttr(dt="string", longName="wdgAttr", niceName="wdgAttr")
    cmds.addAttr(at="short", longName="wdgIndex", niceName="wdgIndex", defaultValue=0)
    cmds.addAttr(at="float", longName="wdgValue", niceName="wdgValue", defaultValue=0)
    #cmds.addAttr(dt="doubleArray", longName="wdgList", niceName="wdgList")
    cmds.addAttr(dt="string", longName="wdgList", niceName="wdgList")
    return this_wedge

def connectwdg(wdgnode, node_attr, wdg_option, wdg_args=None):
    wedge_values = []
    if wdg_option == "-mx":
        if not wdg_args:
            wedge_values = wedgit.wedge_minmax()
        else:
            wedge_values = wedgit.wedge_minmax(wdg_args[0], wdg_args[1], wdg_args[2])
    elif wdg_option == "-ss":
        if not wdg_args:
            wedge_values = wedgit.wedge_startstep()
        else:
            wedge_values = wedgit.wedge_startstep(wdg_args[0], wdg_args[1], wdg_args[2])
    else:
        print("Invalid wedge option")
        return

    print(wedge_values)
    wedge_values_str = ', '.join([str(num) for num in wedge_values])
    cmds.select(wdgnode, r=True)
    wdgAttr = "%s.wdgAttr" % wdgnode
    cmds.setAttr(wdgAttr, node_attr, type="string")
    wdgList = "%s.wdgList" % wdgnode
    cmds.setAttr(wdgList, wedge_values_str, type="string")
    wdgIndex = "%s.wdgIndex" % wdgnode
    cmds.setAttr(wdgIndex, 0)
    wdgValue = "%s.wdgValue" % wdgnode
    cmds.setAttr(wdgValue, wedge_values[0])

    if cmds.isConnected(wdgValue, node_attr):
        cmds.disconnectAttr(wdgValue, node_attr)
    cmds.connectAttr(wdgValue, node_attr, force=True)   # force doesn't work
    return

def nextWdgIndex(wdgnode, up=True):
    wdgList = "%s.wdgList" % wdgnode
    wedge_values = [float(num) for num in cmds.getAttr(wdgList).split(',')]
    wdgIndex = "%s.wdgIndex" % wdgnode
    wdgValue = "%s.wdgValue" % wdgnode
    index = cmds.getAttr(wdgIndex)
    
    if up:
        index += 1
        if index >= len(wedge_values):
            index = 0
    else:
        index -= 1
        if index < 0:
            index = len(wedge_values) - 1

    cmds.setAttr(wdgIndex, index)
    cmds.setAttr(wdgValue, wedge_values[index])




#this_wdgList = [5.2, 4.7, 8.9]
#this_wdgIndex = 1
#cmds.setAttr("wdg1.wdgList", this_wdgList, type="doubleArray")
#cmds.setAttr("wdg1.wdgIndex", this_wdgIndex)
#wdgList = cmds.getAttr("wdg1.wdgList")
#wdgIndex = cmds.getAttr("wdg1.wdgIndex")
#cmds.setAttr("wdg1.wdgValue", wdgList[wdgIndex])


#wdgnode = mkwdg.mkwdg()
#mkwdg.connectwdg(wdgnode, "turbulenceField1.magnitude", "-ss", [10, 10, 3])