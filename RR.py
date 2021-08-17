from odbAccess import *
from abaqusConstants import *
import inspect, os
import csv

# This script is written by Rosti Readioff - version 0.1 (13 August 2021)
# For the purpose of extracting menisci parameters for the EPSRC's menisci allograft transplantation study.
# Contact r.readioff@leeds.ac.uk for modification, version control and any questions about this script.

# Change the file name with to the same as the .odb file of interest
# Define the job name from current file name, remove extension, then add new extension
fN = inspect.getfile(inspect.currentframe()).split('/')[-1]
fName = fN.split('.')[0]
odbName = fName + '.odb'
myOdb = openOdb(path=odbName)
# Define step and frame
stepName = "Load1"
step = myOdb.steps[stepName]
lastFrame = step.frames[-1]

# Create a variable that refers to the displacement 'U' and 'S'
# in the last frame of the load step.
displacement = lastFrame.fieldOutputs['U']
stress = lastFrame.fieldOutputs['S']
strain = lastFrame.fieldOutputs['E']
coordinates = lastFrame.fieldOutputs['COORD']

# Create a variable that refers to the node set 'RP_FEMUR'
# located at the center of the femur bone.
# The set is not associated with the part instance 'PART-1-1'.
theInstance= myOdb.rootAssembly
# Relevant node sets
RP_Femur=theInstance.nodeSets['RP_FEMUR']
RP_Tibia=theInstance.nodeSets['RP_TIBIA']
Lat_Men_Edge=theInstance.nodeSets['LM_RIDGE']
Med_Men_Edge=theInstance.nodeSets['MM_RIDGE']
# Relevant element sets
AP_SpringForceElem=theInstance.elementSets['AP_SPRING-SPRING']
TR_SpringForceElem=theInstance.elementSets['TR_SPRING-SPRING']


# Create a variable that refers to the displacement of the node 
# set and stress & strain in element set in the last frame of the load step.
# displacement:
RP_FemurDisplacement = displacement.getSubset(region=RP_Femur)
RP_TibiaDisplacement = displacement.getSubset(region=RP_Tibia)
Lat_Men_EdgeDisplacement = displacement.getSubset(region=Lat_Men_Edge)
Med_Men_EdgeDisplacement = displacement.getSubset(region=Med_Men_Edge)

# stress S11:
AP_SpringStress0 = stress.getSubset(position=INTEGRATION_POINT,region=AP_SpringForceElem)
AP_SpringStress = AP_SpringStress0.getScalarField(componentLabel='S11').values[0].data
TR_SpringStress0 = stress.getSubset(position=INTEGRATION_POINT,region=TR_SpringForceElem)
TR_SpringStress = TR_SpringStress0.getScalarField(componentLabel='S11').values[0].data
# print(AP_SpringStress)
# print(TR_SpringStress)

# strain E11
AP_SpringStrain0 = strain.getSubset(position=INTEGRATION_POINT,region=AP_SpringForceElem)
AP_SpringStrain = AP_SpringStrain0.getScalarField(componentLabel='E11').values[0].data
TR_SpringStrain0 = strain.getSubset(position=INTEGRATION_POINT,region=TR_SpringForceElem)
TR_SpringStrain = TR_SpringStrain0.getScalarField(componentLabel='E11').values[0].data
# print(AP_SpringStrain)
# print(TR_SpringStrain)

# coordinates for RP_Femur node
RP_FemurCoord = coordinates.getSubset(region=RP_Femur)
RP_FemurCoord_x = RP_FemurCoord.getScalarField(componentLabel='COOR1').values[0].data
RP_FemurCoord_y = RP_FemurCoord.getScalarField(componentLabel='COOR2').values[0].data
RP_FemurCoord_z = RP_FemurCoord.getScalarField(componentLabel='COOR3').values[0].data
# coordinates for RP_Tibia node
RP_TibiaCoord = coordinates.getSubset(region=RP_Tibia)
RP_TibiaCoord_x = RP_TibiaCoord.getScalarField(componentLabel='COOR1').values[0].data
RP_TibiaCoord_y = RP_TibiaCoord.getScalarField(componentLabel='COOR2').values[0].data
RP_TibiaCoord_z = RP_TibiaCoord.getScalarField(componentLabel='COOR3').values[0].data
# coordinates for LM_edge and MM_edge nodes
Lat_Men_EdgeCoord = coordinates.getSubset(region=Lat_Men_Edge)
Med_Men_EdgeCoord = coordinates.getSubset(region=Med_Men_Edge)


# Create csv file to record output measures
csvName = fName + '.csv'

# Printing the parameters extracted (useful for inspection).
for v1 in RP_FemurDisplacement.values:
    print 'Position_Femur = ', v1.position,'Type_Femur = ',v1.type
    print 'Label_Femur = ', v1.nodeLabel
    print 'X displacement_Femur = ', v1.data[0]
    print 'Y displacement_Femur = ', v1.data[1]
    print 'Z displacement_Femur = ', v1.data[2]
    print 'Displacement magnitude_Femur =', v1.magnitude
    with open(csvName, 'a') as csvfile:
        csvfile.write('Position_Femur,Type_Femur,Label_Femur,X displacement_Femur,Y displacement_Femur,Z displacement_Femur,Displacement Magnitude_Femur,COOR1_Femur,COOR2_Femur,COOR3_Femur\n')
        csvfile.write(str(v1.position) + ',')
        csvfile.write(str(v1.type) + ',')    
        csvfile.write(str(v1.nodeLabel) + ',')
        csvfile.write(str(v1.data[0]) + ',')
        csvfile.write(str(v1.data[1]) + ',')
        csvfile.write(str(v1.data[2]) + ',')
        csvfile.write(str(v1.magnitude)+',')
        csvfile.write(str(RP_FemurCoord_x)+',')
        csvfile.write(str(RP_FemurCoord_y)+',')
        csvfile.write(str(RP_FemurCoord_z)+'\n')
     
with open(csvName, 'a') as csvfile:
    csvfile.write('\nPosition_Tibia,Type_Tibia,Label_Tibia,X displacement_Tibia,Y displacement_Tibia,Z displacement_Tibia,Displacement Magnitude_Tibia,COOR1_Tibia,COOR2_Tibia,COOR3_Tibia\n')

# Printing the parameters extracted (useful for inspection).
for v2 in RP_TibiaDisplacement.values:
    # print 'Position_Tibia = ', v2.position,'Type_Tibia = ',v2.type
    # print 'Label_Tibia = ', v2.nodeLabel
    # print 'X displacement_Tibia = ', v2.data[0]
    # print 'Y displacement_Tibia = ', v2.data[1]
    # print 'Z displacement_Tibia = ', v2.data[2]
    # print 'Displacement magnitude_Tibia =', v2.magnitude
    with open(csvName, 'a') as csvfile:
        csvfile.write(str(v2.position) + ',')
        csvfile.write(str(v2.type) + ',')    
        csvfile.write(str(v2.nodeLabel) + ',')
        csvfile.write(str(v2.data[0]) + ',')
        csvfile.write(str(v2.data[1]) + ',')
        csvfile.write(str(v2.data[2]) + ',')
        csvfile.write(str(v2.magnitude) + ',')
        csvfile.write(str(RP_TibiaCoord_x)+',')
        csvfile.write(str(RP_TibiaCoord_y)+',')
        csvfile.write(str(RP_TibiaCoord_z)+'\n')
with open(csvName, 'a') as csvfile:
    csvfile.write('\nAP_SpringStress,TR_SpringStress,AP_SpringStrain,TR_SpringStrain\n')
    csvfile.write(str(AP_SpringStress) + ',')
    csvfile.write(str(TR_SpringStress) + ',')
    csvfile.write(str(AP_SpringStrain) + ',')
    csvfile.write(str(TR_SpringStrain) + '\n\nPosition_LM_ridge,Type_LM_ridge,Label_LM_ridge,X displacement_LM_ridge,Y displacement_LM_ridge,Z displacement_LM_ridge,Displacement Magnitude_LM_ridge\n')    
    
# Printing the parameters extracted (useful for inspection).
for v3 in Lat_Men_EdgeDisplacement.values:
    # print 'Position_LM_ridge = ', v3.position,'Type_LM_ridge = ',v3.type
    # print 'Label_LM_ridge = ', v3.nodeLabel
    # print 'X displacement_LM_ridge = ', v3.data[0]
    # print 'Y displacement_LM_ridge = ', v3.data[1]
    # print 'Z displacement_LM_ridge = ', v3.data[2]
    # print 'Displacement magnitude_LM_ridge =', v3.magnitude
    with open(csvName, 'a') as csvfile:
        csvfile.write(str(v3.position) + ',')
        csvfile.write(str(v3.type) + ',')    
        csvfile.write(str(v3.nodeLabel) + ',')
        csvfile.write(str(v3.data[0]) + ',')
        csvfile.write(str(v3.data[1]) + ',')
        csvfile.write(str(v3.data[2]) + ',')
        csvfile.write(str(v3.magnitude) + '\n')
with open(csvName, 'a') as csvfile:
    csvfile.write('\nCOOR1_LM_ridge,COOR2_LM_ridge,COOR3_LM_ridge\n')
    
for i in range (len(Lat_Men_EdgeCoord.values)):
    Lat_Men_EdgeCoord_x=(Lat_Men_EdgeCoord.getScalarField(componentLabel='COOR1').values[i].data)
    Lat_Men_EdgeCoord_y=(Lat_Men_EdgeCoord.getScalarField(componentLabel='COOR2').values[i].data)
    Lat_Men_EdgeCoord_z=(Lat_Men_EdgeCoord.getScalarField(componentLabel='COOR3').values[i].data)
    with open(csvName, 'a') as csvfile:
        csvfile.write(str(Lat_Men_EdgeCoord_x)+',')
        csvfile.write(str(Lat_Men_EdgeCoord_y)+',')
        csvfile.write(str(Lat_Men_EdgeCoord_z)+'\n')
                    
with open(csvName, 'a') as csvfile:
    csvfile.write('\nPosition_MM_ridge,Type_MM_ridge,Label_MM_ridge,X displacement_MM_ridge,Y displacement_MM_ridge,Z displacement_MM_ridge,Displacement Magnitude_MM_ridge\n')
    
# Printing the parameters extracted (useful for inspection).
for v4 in Med_Men_EdgeDisplacement.values:
    # print 'Position_MM_ridge = ', v4.position,'Type_MM_ridge = ',v4.type
    # print 'Label_MM_ridge = ', v4.nodeLabel
    # print 'X displacement_MM_ridge = ', v4.data[0]
    # print 'Y displacement_MM_ridge = ', v4.data[1]
    # print 'Z displacement_MM_ridge = ', v4.data[2]
    # print 'Displacement magnitude_MM_ridge =', v4.magnitude
    with open(csvName, 'a') as csvfile:
        csvfile.write(str(v4.position) + ',')
        csvfile.write(str(v4.type) + ',')    
        csvfile.write(str(v4.nodeLabel) + ',')
        csvfile.write(str(v4.data[0]) + ',')
        csvfile.write(str(v4.data[1]) + ',')
        csvfile.write(str(v4.data[2]) + ',')
        csvfile.write(str(v4.magnitude) + '\n')
with open(csvName, 'a') as csvfile:
    csvfile.write('\nCOOR1_MM_ridge,COOR2_MM_ridge,COOR3_MM_ridge\n')     
    
for ii in range (len(Med_Men_EdgeCoord.values)):
    Med_Men_EdgeCoord_x=(Med_Men_EdgeCoord.getScalarField(componentLabel='COOR1').values[ii].data)
    Med_Men_EdgeCoord_y=(Med_Men_EdgeCoord.getScalarField(componentLabel='COOR2').values[ii].data)
    Med_Men_EdgeCoord_z=(Med_Men_EdgeCoord.getScalarField(componentLabel='COOR3').values[ii].data)
    with open(csvName, 'a') as csvfile:
        csvfile.write(str(Med_Men_EdgeCoord_x)+',')
        csvfile.write(str(Med_Men_EdgeCoord_y)+',')
        csvfile.write(str(Med_Men_EdgeCoord_z)+'\n')
    
myOdb.close()