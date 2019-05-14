import sys
from pprint import pprint

import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya

#from maya import cmds

import wedge

kNameFlag = "-n"
kNameLongFlag = "-name"
kStartFlag = "-s"
kStartLongFlag = "-start"
kStepFlag = "-stp"
kStepLongFlag = "-step"
kNumFlag = "-num"
kNumLongFlag = "-numsteps"
kStepDirFlag = "-sdr"
kStepDirLongFlag = "-stepdir"

class WedgeCmd(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

    def doIt(self, args):
        
        name = ""
        wedge_start = 0
        wedge_step = 0
        wedge_num = 0
        wedge_step_dir = 0
        wedge_attrs = []
        wedge_steps = []
        wedge_nums = []
        wedge_dirs = []
        
        self.argData = OpenMaya.MArgDatabase(self.syntax(), args)
        
        # get wedge node.attribute arguments
        status = self.argData.getObjects(wedge_attrs)
        self.num_attrs = len(wedge_attrs)
        
        # get wedgie node name if any given
        if self.argData.isFlagSet(kNameFlag):
            name = self.argData.flagArgumentString(kNameFlag, 0)
        
        # get wedge flag lists for each of step size, number of steps and step direction
        if self.argData.isFlagSet(kStepFlag):
            wedge_steps = self.getFlagList(kStepFlag)

        if self.argData.isFlagSet(kNumFlag):
            wedge_nums = self.getFlagList(kNumFlag,"int")
        
        if self.argData.isFlagSet(kStepDirFlag):
            wedge_dirs = self.getFlagList(kStepDirFlag,"int")

        # for now pickup start values from destination attribute
        #if argData.isFlagSet(kStartFlag):
            #wedge_starts = self.getFlagList(kStartFlag)
        
        # now build wedgie
        self.redoIt(wedge_attrs, wedge_steps, wedge_nums, wedge_dirs, name)

    def redoIt(self, wedge_attrs, wedge_steps, wedge_nums, wedge_dirs, name=None):
        print "WedgeCmd:redoIt wedge_attrs",wedge_attrs
        
        # default for now, should later add flags for these
        num_steps = 1
        step_dir = 0
        
        wedgieNode = OpenMaya.MObject()
        fnDestNode = OpenMaya.MFnDependencyNode()
        if name:
            wedgieNode = fnDestNode.create("wedgie", name)
        else:
            wedgieNode = fnDestNode.create("wedgie")
        wedgieNodeName = fnDestNode.name()
        self.setResult(wedgieNodeName)

        # setup for first wedge attribute
        wgAttr1_plug = OpenMaya.MPlug(wedgieNode,WedgeNode.wgAttr1)
        wgStart1_plug = OpenMaya.MPlug(wedgieNode,WedgeNode.wgStart1)
        wgValue1_plug = OpenMaya.MPlug(wedgieNode,WedgeNode.wgValue1)
        start_value = self.setAttrs(wedge_attrs[0],wgAttr1_plug,wgStart1_plug,wgValue1_plug)
        
        wgStep1_plug = OpenMaya.MPlug(wedgieNode,WedgeNode.wgStep1)
        wgNumSteps1_plug = OpenMaya.MPlug(wedgieNode,WedgeNode.wgNumSteps1)
        wgStepDir1_plug = OpenMaya.MPlug(wedgieNode,WedgeNode.wgStepDir1)
        step_size,num_steps,step_dir = self.setOtherAttrs(0,wgStep1_plug,wgNumSteps1_plug,wgStepDir1_plug,wedge_steps,wedge_nums,wedge_dirs)
        
        wedge_args = [(wedge_attrs[0],num_steps,start_value,step_size,step_dir)]

        # setup for second wedge attribute
        if self.num_attrs > 1:
            wgAttr2_plug = OpenMaya.MPlug(wedgieNode,WedgeNode.wgAttr2)
            wgStart2_plug = OpenMaya.MPlug(wedgieNode,WedgeNode.wgStart2)
            wgValue2_plug = OpenMaya.MPlug(wedgieNode,WedgeNode.wgValue2)
            start_value = self.setAttrs(wedge_attrs[1],wgAttr2_plug,wgStart2_plug,wgValue2_plug)
            
            wgStep2_plug = OpenMaya.MPlug(wedgieNode,WedgeNode.wgStep2)
            wgNumSteps2_plug = OpenMaya.MPlug(wedgieNode,WedgeNode.wgNumSteps2)
            wgStepDir2_plug = OpenMaya.MPlug(wedgieNode,WedgeNode.wgStepDir2)
            step_size,num_steps,step_dir = self.setOtherAttrs(1,wgStep2_plug,wgNumSteps2_plug,wgStepDir2_plug,wedge_steps,wedge_nums,wedge_dirs)
            
            wedge_args.append((wedge_attrs[1],num_steps,start_value,step_size,step_dir))
       
        # setup for third wedge attribute
        if self.num_attrs > 2:
            wgAttr3_plug = OpenMaya.MPlug(wedgieNode,WedgeNode.wgAttr3)
            wgStart3_plug = OpenMaya.MPlug(wedgieNode,WedgeNode.wgStart3)
            wgValue3_plug = OpenMaya.MPlug(wedgieNode,WedgeNode.wgValue3)
            start_value = self.setAttrs(wedge_attrs[2],wgAttr3_plug,wgStart3_plug,wgValue3_plug)
            
            wgStep3_plug = OpenMaya.MPlug(wedgieNode,WedgeNode.wgStep3)
            wgNumSteps3_plug = OpenMaya.MPlug(wedgieNode,WedgeNode.wgNumSteps3)
            wgStepDir3_plug = OpenMaya.MPlug(wedgieNode,WedgeNode.wgStepDir3)
            step_size,num_steps,step_dir = self.setOtherAttrs(2,wgStep3_plug,wgNumSteps3_plug,wgStepDir3_plug,wedge_steps,wedge_nums,wedge_dirs)
            
            wedge_args.append((wedge_attrs[2],num_steps,start_value,step_size,step_dir))
            
        
        print "wedge_args"
        pprint(wedge_args)
        wedge_values = wedge.getall(wedge_args)
        print "length of wedge_values",len(wedge_values)
        pprint(wedge_values)

        # now build the wedge array attributes that drive wedgie
        md_array1 = OpenMaya.MDoubleArray()
        md_array2 = OpenMaya.MDoubleArray()
        md_array3 = OpenMaya.MDoubleArray()
        for k in range(len(wedge_values)):
            md_array1.append(wedge_values[k][0])
            if (self.num_attrs > 1):
                md_array2.append(wedge_values[k][1])
                if (self.num_attrs > 2):
                    md_array3.append(wedge_values[k][2])

        fnArray1_data = OpenMaya.MFnDoubleArrayData().create(md_array1)
        fnArray2_data = OpenMaya.MFnDoubleArrayData().create(md_array2)
        fnArray3_data = OpenMaya.MFnDoubleArrayData().create(md_array3)

        wa1_plug_object = OpenMaya.MPlug(wedgieNode,WedgeNode.wgArray1)
        wa1_plug_object.setMObject(fnArray1_data)
        wa2_plug_object = OpenMaya.MPlug(wedgieNode,WedgeNode.wgArray2)
        wa2_plug_object.setMObject(fnArray2_data)
        wa3_plug_object = OpenMaya.MPlug(wedgieNode,WedgeNode.wgArray3)
        wa3_plug_object.setMObject(fnArray3_data)
      

    def setAttrs(self, wedge_attr, attr_plug, start_plug, value_plug):
        attr_plug.setString(wedge_attr)
        dest_node_attr = wedge_attr.split('.')
        selectionList = OpenMaya.MSelectionList()
        selectionList.add(dest_node_attr[0])
        dest_node = OpenMaya.MObject()
        selectionList.getDependNode(0,dest_node)
        dest_nodeFn = OpenMaya.MFnDependencyNode(dest_node)
        dest_plug = dest_nodeFn.findPlug(dest_node_attr[1])
        start_value = round(dest_plug.asDouble(),3)
        start_plug.setDouble(start_value)
        value_plug.setDouble(start_value)
        
        mdg = OpenMaya.MDGModifier()
        mdg.connect(value_plug, dest_plug)
        mdg.doIt()
        return start_value

    def getFlagList(self, wedgeflag, flagtype="double"):
        num = self.argData.numberOfFlagUses(wedgeflag)
        flag_arglist = []
        if num > self.num_attrs:
            num = self.num_attrs
        flag_args = OpenMaya.MArgList()
        for i in range(num):
            status = self.argData.getFlagArgumentList(wedgeflag,i,flag_args)
            if flagtype == "double":
                flag_arglist.append(flag_args.asDouble(i))
            else:
                flag_arglist.append(flag_args.asInt(i))
            
        print "getFlagList: wedgeflag",wedgeflag,"flag_arglist",flag_arglist
        return flag_arglist

    def setOtherAttrs(self, index, step_plug, num_plug, dir_plug, wedge_steps, wedge_nums, wedge_dirs):
        step_size = 0.5     # default step_size if no flag set
        if len(wedge_steps) > index:
            step_size = wedge_steps[index]
        step_plug.setDouble(step_size)
        num_steps = 1
        if len(wedge_nums) > index:
            num_steps = wedge_nums[index]
        num_plug.setInt(num_steps)
        step_dir = 0
        if len(wedge_dirs) > index:
            step_dir = wedge_dirs[index]
        dir_plug.setInt(step_dir)
        return step_size,num_steps,step_dir


class WedgeNode(OpenMayaMPx.MPxNode):
    kPluginNodeId = OpenMaya.MTypeId(0x80028)       # MTypeId

    wgIndex = OpenMaya.MObject()
    
    wgAttr1 = OpenMaya.MObject()
    wgStart1 = OpenMaya.MObject()
    wgStep1 = OpenMaya.MObject()
    wgNumSteps1 = OpenMaya.MObject()
    wgValue1 = OpenMaya.MObject()
    wgArray1 = OpenMaya.MObject()
    wgStepDir1 = OpenMaya.MObject()
    
    wgAttr2 = OpenMaya.MObject()
    wgStart2 = OpenMaya.MObject()
    wgStep2 = OpenMaya.MObject()
    wgNumSteps2 = OpenMaya.MObject()
    wgValue2 = OpenMaya.MObject()
    wgArray2 = OpenMaya.MObject()
    wgStepDir2 = OpenMaya.MObject()

    wgAttr3 = OpenMaya.MObject()
    wgStart3 = OpenMaya.MObject()
    wgStep3 = OpenMaya.MObject()
    wgNumSteps3 = OpenMaya.MObject()
    wgValue3 = OpenMaya.MObject()
    wgArray3 = OpenMaya.MObject()
    wgStepDir3 = OpenMaya.MObject()
    
    wgUpdate = OpenMaya.MObject()


    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def postConstructor(self):
        print "wedgie postconstructor"
    
    def compute(self, plug, data):
        '''
            get the index and then get the array value at that index and set the connected wedge attributes to array value
        '''
        if (plug == WedgeNode.wgValue1) or (plug == WedgeNode.wgValue2) or (plug == WedgeNode.wgValue3):
            try:
                dataHandle = data.inputValue(WedgeNode.wgIndex)
            except:
                sys.stderr.write("Failed to get wedge index")
                raise
    
        elif (plug == WedgeNode.wgUpdate):
            self.update(self.thisMObject())
            data.setClean(plug)
            return
        
        else:
            print "compute nothing"
            return
            
        wedge_index = dataHandle.asInt()
        thisNode = self.thisMObject()
        thisNodeName = self.name()
        p1 = p2 = p3 = 0
        #print "compute on node %s wix change %d" % (thisNodeName, wedge_index)
        # need to add test for number of wedge attributes
        
        wa1_plug_object = OpenMaya.MPlug(thisNode,WedgeNode.wgArray1).asMObject()
        thisArray1 = OpenMaya.MFnDoubleArrayData(wa1_plug_object).array()
        if thisArray1:
            p1 = thisArray1[wedge_index]

        wa2_plug_object = OpenMaya.MPlug(thisNode,WedgeNode.wgArray2).asMObject()
        thisArray2 = OpenMaya.MFnDoubleArrayData(wa2_plug_object).array()
        if thisArray2:
            p2 = thisArray2[wedge_index]

        wa3_plug_object = OpenMaya.MPlug(thisNode,WedgeNode.wgArray3).asMObject()
        thisArray3 = OpenMaya.MFnDoubleArrayData(wa3_plug_object).array()
        if thisArray3:
            p3 = thisArray3[wedge_index]

        bOutput = data.outputValue(WedgeNode.wgValue1)
        bOutput.setFloat(p1)
 
        bOutput = data.outputValue(WedgeNode.wgValue2)
        bOutput.setFloat(p2)
        
        bOutput = data.outputValue(WedgeNode.wgValue3)
        bOutput.setFloat(p3)

        data.setClean(plug)
        return

#def setInternalValueInContext(self, plug, dataHandle, ctx):
#plug_name = plug.name()
#value = round(dataHandle.asFloat(),3)
#print "setInternalValueInContext on ", plug_name
#return OpenMaya.MPxNode.setInternalValueInContext(self, plug, dataHandle, ctx)
#return True


#def connectionMade(self, plug, otherPlug, asSrc):
#if (plug == WedgeNode.wgValue1) or (plug == WedgeNode.wgValue2) or (plug == WedgeNode.wgValue3):
#print "value connection", plug.name(), asSrc
    
    def update(self,thisNode):
        fnThisNode = OpenMaya.MFnDependencyNode(thisNode)
        thisNodeName = fnThisNode.name()
        print "need to update wedgie",thisNodeName
        return


# WedgeCmd

def cmdCreator():
    return OpenMayaMPx.asMPxPtr(WedgeCmd())

def syntaxCreator():
    syntax = OpenMaya.MSyntax()
   
    syntax.useSelectionAsDefault(False)
    syntax.setObjectType(OpenMaya.MSyntax.kStringObjects,1,3)
    
    syntax.addFlag(kNameFlag, kNameLongFlag, OpenMaya.MSyntax.kString)
    
    syntax.addFlag(kStartFlag, kStartLongFlag, OpenMaya.MSyntax.kDouble)
    syntax.makeFlagMultiUse(kStartFlag)
    syntax.addFlag(kStepFlag, kStepLongFlag, OpenMaya.MSyntax.kDouble)
    syntax.makeFlagMultiUse(kStepFlag)
    syntax.addFlag(kNumFlag, kNumLongFlag, OpenMaya.MSyntax.kUnsigned)
    syntax.makeFlagMultiUse(kNumFlag)
    syntax.addFlag(kStepDirFlag, kStepDirLongFlag, OpenMaya.MSyntax.kUnsigned)
    syntax.makeFlagMultiUse(kStepDirFlag)
    
    syntax.enableQuery(False)
    syntax.enableEdit(False)
    
    return syntax

# WedgeNode

def creator():
    return OpenMayaMPx.asMPxPtr(WedgeNode())

def initialize():
    nAttr = OpenMaya.MFnNumericAttribute()
    cAttr = OpenMaya.MFnCompoundAttribute()
    sAttr = OpenMaya.MFnTypedAttribute()
    tAttr = OpenMaya.MFnTypedAttribute()
    eAttr = OpenMaya.MFnEnumAttribute()
    
    # wedge index attribute
    WedgeNode.wgIndex = nAttr.create("wedge_index","wix", OpenMaya.MFnNumericData.kInt,0)
    #nAttr.setInternal(True)
    WedgeNode.addAttribute(WedgeNode.wgIndex)
    
    kEmptyStringAttrValue = ""
    stringData = OpenMaya.MFnStringData().create(kEmptyStringAttrValue)
    defaultDoubleArray = OpenMaya.MDoubleArray()
    arrayData = OpenMaya.MFnDoubleArrayData().create(defaultDoubleArray)
    
    WedgeNode.wgUpdate = nAttr.create("wedge_update","wup",OpenMaya.MFnNumericData.kInt,0)
    nAttr.setInternal(True)
    nAttr.setHidden(True)
    WedgeNode.addAttribute(WedgeNode.wgUpdate)
    
    # wedge 1 attributes
    WedgeNode.wgAttr1 = sAttr.create("wedge_attr1","wattr1",OpenMaya.MFnData.kString,stringData)
    WedgeNode.addAttribute(WedgeNode.wgAttr1)
    WedgeNode.wgStart1 = nAttr.create("wedge_start1","wstart1", OpenMaya.MFnNumericData.kFloat,0.0)
    WedgeNode.addAttribute(WedgeNode.wgStart1)
    WedgeNode.wgStep1 = nAttr.create("wedge_step1","wstep1", OpenMaya.MFnNumericData.kFloat,0.5)
    nAttr.setInternal(True)
    WedgeNode.addAttribute(WedgeNode.wgStep1)
    WedgeNode.wgNumSteps1 = nAttr.create("wedge_num_steps1","wnum1", OpenMaya.MFnNumericData.kInt,1)
    nAttr.setInternal(True)
    WedgeNode.addAttribute(WedgeNode.wgNumSteps1)
    WedgeNode.wgStepDir1 = eAttr.create("wedge_stepdir1","wsdr1")
    eAttr.addField("updown",0)
    eAttr.addField("up",1)
    eAttr.addField("down",2)
    eAttr.setInternal(True)
    WedgeNode.addAttribute(WedgeNode.wgStepDir1)
    
    WedgeNode.wgValue1 = nAttr.create("wedge_value1","wval1", OpenMaya.MFnNumericData.kFloat,0)
    WedgeNode.addAttribute(WedgeNode.wgValue1)
    WedgeNode.wgArray1 = tAttr.create("wedge_array1","warr1", OpenMaya.MFnData.kDoubleArray,arrayData)
    tAttr.setInternal(True)
    tAttr.setHidden(True)
    WedgeNode.addAttribute(WedgeNode.wgArray1)

    # wedge 2 attributes
    WedgeNode.wgAttr2 = sAttr.create("wedge_attr2","wattr2",OpenMaya.MFnData.kString,stringData)
    WedgeNode.addAttribute(WedgeNode.wgAttr2)
    WedgeNode.wgStart2 = nAttr.create("wedge_start2","wstart2", OpenMaya.MFnNumericData.kFloat,0.0)
    WedgeNode.addAttribute(WedgeNode.wgStart2)
    WedgeNode.wgStep2 = nAttr.create("wedge_step2","wstep2", OpenMaya.MFnNumericData.kFloat,0.5)
    WedgeNode.addAttribute(WedgeNode.wgStep2)
    WedgeNode.wgNumSteps2 = nAttr.create("wedge_num_steps2","wnum2", OpenMaya.MFnNumericData.kInt,1)
    WedgeNode.addAttribute(WedgeNode.wgNumSteps2)
    WedgeNode.wgStepDir2 = eAttr.create("wedge_stepdir2","wsdr2")
    eAttr.addField("updown",0)
    eAttr.addField("up",1)
    eAttr.addField("down",2)
    WedgeNode.addAttribute(WedgeNode.wgStepDir2)
    
    WedgeNode.wgValue2 = nAttr.create("wedge_value2","wval2", OpenMaya.MFnNumericData.kFloat,0)
    WedgeNode.addAttribute(WedgeNode.wgValue2)
    WedgeNode.wgArray2 = tAttr.create("wedge_array2","warr2", OpenMaya.MFnData.kDoubleArray,arrayData)
    tAttr.setInternal(True)
    tAttr.setHidden(True)
    WedgeNode.addAttribute(WedgeNode.wgArray2)

    # wedge 3 attributes
    WedgeNode.wgAttr3 = sAttr.create("wedge_attr3","wattr3",OpenMaya.MFnData.kString,stringData)
    WedgeNode.addAttribute(WedgeNode.wgAttr3)
    WedgeNode.wgStart3 = nAttr.create("wedge_start3","wstart3", OpenMaya.MFnNumericData.kFloat,0.0)
    WedgeNode.addAttribute(WedgeNode.wgStart3)
    WedgeNode.wgStep3 = nAttr.create("wedge_step3","wstep3", OpenMaya.MFnNumericData.kFloat,0.5)
    WedgeNode.addAttribute(WedgeNode.wgStep3)
    WedgeNode.wgNumSteps3 = nAttr.create("wedge_num_steps3","wnum3", OpenMaya.MFnNumericData.kInt,1)
    WedgeNode.addAttribute(WedgeNode.wgNumSteps3)
    WedgeNode.wgStepDir3 = eAttr.create("wedge_stepdir3","wsdr3")
    eAttr.addField("updown",0)
    eAttr.addField("up",1)
    eAttr.addField("down",2)
    WedgeNode.addAttribute(WedgeNode.wgStepDir3)

    WedgeNode.wgValue3 = nAttr.create("wedge_value3","wval3", OpenMaya.MFnNumericData.kFloat,0)
    WedgeNode.addAttribute(WedgeNode.wgValue3)
    WedgeNode.wgArray3 = tAttr.create("wedge_array3","warr3", OpenMaya.MFnData.kDoubleArray,arrayData)
    tAttr.setInternal(True)
    tAttr.setHidden(True)
    WedgeNode.addAttribute(WedgeNode.wgArray3)

    # attribute affects
    WedgeNode.attributeAffects(WedgeNode.wgIndex,WedgeNode.wgValue1)
    WedgeNode.attributeAffects(WedgeNode.wgIndex,WedgeNode.wgValue2)
    WedgeNode.attributeAffects(WedgeNode.wgIndex,WedgeNode.wgValue3)

    WedgeNode.attributeAffects(WedgeNode.wgStart1,WedgeNode.wgUpdate)
    WedgeNode.attributeAffects(WedgeNode.wgStep1,WedgeNode.wgUpdate)
    WedgeNode.attributeAffects(WedgeNode.wgNumSteps1,WedgeNode.wgUpdate)
    WedgeNode.attributeAffects(WedgeNode.wgStepDir1,WedgeNode.wgUpdate)
    
    WedgeNode.attributeAffects(WedgeNode.wgStart2,WedgeNode.wgUpdate)
    WedgeNode.attributeAffects(WedgeNode.wgStep2,WedgeNode.wgUpdate)
    WedgeNode.attributeAffects(WedgeNode.wgNumSteps2,WedgeNode.wgUpdate)
    WedgeNode.attributeAffects(WedgeNode.wgStepDir2,WedgeNode.wgUpdate)
    
    WedgeNode.attributeAffects(WedgeNode.wgStart3,WedgeNode.wgUpdate)
    WedgeNode.attributeAffects(WedgeNode.wgStep3,WedgeNode.wgUpdate)
    WedgeNode.attributeAffects(WedgeNode.wgNumSteps3,WedgeNode.wgUpdate)
    WedgeNode.attributeAffects(WedgeNode.wgStepDir3,WedgeNode.wgUpdate)


def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, 'wedgie', '0.1', 'zanefx')
    
    try:
        plugin.registerCommand( 'makewedgie', cmdCreator, syntaxCreator)
    except:
        raise RuntimeError, 'Failed to register command: makewedgie'

    try:
        plugin.registerNode('wedgie', WedgeNode.kPluginNodeId, creator, initialize)
    except:
        raise RuntimeError, 'Failed to register node: wedgie'

def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    
    try:
        plugin.deregisterCommand('makewedgie')
    except:
        raise RuntimeError, 'Failed to deregister command: makewedgie'
    
    try:
        plugin.deregisterNode(WedgeNode.kPluginNodeId)
    except:
        raise RuntimeError, 'Failed to unload node: wedgie'
