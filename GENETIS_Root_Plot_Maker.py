#!/usr/bin/env python3

#This python script takes in (parses) the simulation data of an antenna and creates
#plots of the date

#Author: Jack Tillman
#Contact Information (email): tillman.100@osu.edu
#Citations: "AraSim_Reader_Plot_Maker.py" written by Dennis Calderon (calderon-madera.1@osu.edu)

#Creating a timer to time how long it takes for the script to run
import timeit
start = timeit.default_timer()

#importing all necessary libraries for this script

#System Libraries
import argparse
import warnings
warnings.filterwarnings("ignore")

#PyRoot Libraries
import ROOT
from ROOT import gInterpreter, gSystem
from ROOT import TChain

#Python Libraries
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np 

print("All necessary libraries have been imported.")

#AraSim Specific Headers (Taken from Dennis' Code)
gInterpreter.ProcessLine('#include "/cvmfs/ara.opensciencegrid.org/trunk/centos7/source/AraSim/Position.h"')#"/users/PAS0654/dcalderon/AraSim/Position.h"')
gInterpreter.ProcessLine('#include "/cvmfs/ara.opensciencegrid.org/trunk/centos7/source/AraSim/Report.h"')#"/users/PAS0654/dcalderon/AraSim/Report.h"')
gInterpreter.ProcessLine('#include "/cvmfs/ara.opensciencegrid.org/trunk/centos7/source/AraSim/Detector.h"')#"/users/PAS0654/dcalderon/AraSim/Detector.h"')
gInterpreter.ProcessLine('#include "/cvmfs/ara.opensciencegrid.org/trunk/centos7/source/AraSim/Settings.h"')#"/users/PAS0654/dcalderon/AraSim/Settings.h"')

gSystem.Load('/cvmfs/ara.opensciencegrid.org/trunk/centos7/ara_build/lib/libAra.so')#'/users/PAS0654/dcalderon/AraSim/libAra.so') 

#Using ArgParse to read in our arguments. In this case, we're parsing in the simulation data, and an output file 
#where we'll write the plotted and graphed data to.

#Checking to make sure we have the output file parsed in, along with parsing in the rest of the necessary
#files (done via the code Dennis has written)
parser = argparse.ArgumentParser(
        description='Read AraSim file and produce some plots. Can also compare two AraSim files.')
parser.add_argument("source_1", help = "Path to the AraSim file you want to use.", nargs='+')
parser.add_argument("--source_2", "-s2", help = "Path to another AraSim file you want to comprare to.", nargs='+')
parser.add_argument("--source_3", "-s3", help = "Path to another AraSim file you want to comprare to.", nargs='+')
parser.add_argument("--source_4", "-s4", help = "Path to another AraSim file you want to comprare to.", nargs='+')
parser.add_argument("--source_5", "-s5", help = "Path to another AraSim file you want to comprare to.", nargs='+')
parser.add_argument("--source_6", "-s6", help = "Path to another AraSim file you want to comprare to.", nargs='+')

g = parser.parse_args()

#Creating a dictionary where we'll store all parsed data (files):
parsed_data_dictionary = g.__dict__

#Cleaning up the dictionary by deleting empty arguments:
parsed_data_dictionary = {k:v for k, v in parsed_data_dictionary.items() if v != None}

#Initializing the necessary variables we'll use
energy = np.power(10, 18) #energy of neutrinoes
earth_depth = 6359632.4 #depth of cores inside earth
core_x = 10000.0 #x - location of core
core_y = 10000.0 #y - location of core

#Initializing the variables we'll consider when plotting later in the script. We'll initialize each considered
#variable as an empty list:

#Position Data
xPosData = []
yPosData = []
zPosData = []

#Direct Angle Data
recAngleData0 = []
thetaAngleData0 = []
reflectAngleData0 = []

#Reflected/Refracted Angle Data 
recAngleData1 = []
thetaAngleData1 = []
reflectAngleData1 = []


#We can now write the loop to analyze all of our data in order to prepare for plotting:
print("Starting the loop to analyze the parsed simulation data.")

data_dict = {}
for i in range(len(parsed_data_dictionary.keys())):

    var_dict = {}
    #list of all variable names
    #var = ['trigg', 'weight', 'posnu_x', 'posnu_y', 'posnu_z',
            #'rec_ang_0', 'theta_rec_0', 'reflect_ang_0',
            #'dist_0', 'arrival_time_0', 'reflection_0', 
            #'l_att_0', 'view_ang_0', 'launch_ang_0',
            #'rec_ang_1', 'theta_rec_1', 'reflect_ang_1',
            #'dist_1', 'arrival_time_1', 'reflection_1', 
            #'l_att_1', 'view_ang_1', 'launch_ang_1',
            #current', 'flavor', 'elast',
            #'nnu_theta', 'nnu_phi', 'ShowerEnergy',
            #'depth', 'distance']

    new_var = ['trigg', 'posnu_x', 'posnu_y', 'posnu_z', 'rec_ang_0', 'theta_rec_0', 'reflect_ang_0', 'rec_ang_1', 'theta_rec_1', 'reflect_ang_1']

    #Writing a loop that creates a dictionary of variables along with an empty list
    #for x in var:
    for x in new_var:

        var_dict['{0}'.format(x)] = []
        #print(var_dict)

    #exit()     #Run on OSC later

    #Creating trees (used to structure and organize data):
    SimTree = [] #sets SimTree and makes empty list
    SimTree = TChain("AraTree2") #Which tree I will be chaining

    for line in list(parsed_data_dictionary.values())[i]: #for every filename in my list
            SimTree.AddFile(line)

    reportPtr = ROOT.Report()#report pointer
    eventPtr = ROOT.Event()#event pointer

    #detectorPtr = ROOT.Detector()
    #can also add more pointers if needed
    #print(reportPtr)
    #print(SimTree)

    SimTree.SetBranchAddress("report", ROOT.AddressOf(reportPtr))
    SimTree.SetBranchAddress("event", ROOT.AddressOf(eventPtr))
    #SimTree.SetBranchAddress("detector", ROOT.AddressOf(detectorPtr))
        
    #basic info of data
    totalEvents = SimTree.GetEntries()
    key = []
    key =  list(parsed_data_dictionary)[i]
        
    print('\033[1;37m{0}\033[0;0m'.format(key))
    print('Total Events: {0}'.format(totalEvents))
    print('#'*50)
        
    print(i)
    print(type(SimTree))
    #print(SimTree)
    #SimTree.Print()

    #Now we'll loop over all of the events in order to collect the data we need
    for j in range(totalEvents):
        SimTree.GetEntry(j) #Again the use of trees isn't something I'm familiar with

        #We now want to only consider triggered events that have a significant enough weight(from 0-1):
        #This was done using Dennis' prewritten code
        if (reportPtr.stations[0].Global_Pass > 0) and (eventPtr.Nu_Interaction[0].weight >= 0 and eventPtr.Nu_Interaction[0].weight <= 1):
            #print(j)
            #print(key)
            trigg = j
            var_dict['trigg'].append(j) #Keeping track of which events passed the if statement (valid data)
                        
            #If value is seen in both antennas (Top Vpol and Bot Vpol) then we take an average of two
            #var_dict['trigg'].append(j)

            #interaction position in ice
            try: 
                
                #Position Data
                posnu_x = eventPtr.Nu_Interaction[0].posnu.GetX()
                posnu_y = eventPtr.Nu_Interaction[0].posnu.GetY()
                posnu_z = eventPtr.Nu_Interaction[0].posnu.GetZ()

                #Direct Angle Data
                rec_ang_0 = 0.5 * (reportPtr.stations[0].strings[1].antennas[0].rec_ang[0] + reportPtr.stations[0].strings[1].antennas[2].rec_ang[0])
                theta_rec_0 = 0.5 * (reportPtr.stations[0].strings[1].antennas[0].theta_rec[0] + reportPtr.stations[0].strings[1].antennas[2].theta_rec[0])
                reflect_ang_0 = 0.5 * (reportPtr.stations[0].strings[1].antennas[0].reflect_ang[0] + reportPtr.stations[0].strings[1].antennas[2].reflect_ang[0])

                #Reflected/Refracted Angle Data
                rec_ang_1 = 0.5 * (reportPtr.stations[0].strings[1].antennas[0].rec_ang[1] + reportPtr.stations[0].strings[1].antennas[2].rec_ang[1])
                theta_rec_1 = 0.5 * (reportPtr.stations[0].strings[1].antennas[0].theta_rec[1] + reportPtr.stations[0].strings[1].antennas[2].theta_rec[1])
                reflect_ang_1 = 0.5 * (reportPtr.stations[0].strings[1].antennas[0].reflect_ang[1] + reportPtr.stations[0].strings[1].antennas[2].reflect_ang[1])
 
            except IndexError:
                continue

            #We can now append each coordinate position (x,y,z) to their corresponding lists
            xPosData.append(posnu_x)
            yPosData.append(posnu_y)
            zPosData.append(posnu_z)

            recAngleData0.append(rec_ang_0)
            thetaAngleData0.append(theta_rec_0)
            reflectAngleData0.append(reflect_ang_0)

            recAngleData1.append(rec_ang_1)
            thetaAngleData1.append(theta_rec_1)
            reflectAngleData1.append(reflect_ang_1)

            #Now we'll print all considered variables:
            #considered_Variables = [trigg, weight, posnu_x, posnu_y, posnu_z,
                                    #current, flavor, elast, nnu_theta, nnu_phi, 
                                    #ShowerEnergy, depth, distance]

            #Creating a new list of all considered variables (considering only position) 
            consideredVariablesPosition = [trigg, posnu_x, posnu_y, posnu_z]

            for k in range(1,len(consideredVariablesPosition)):
                var_dict['{0}'.format(new_var[k])].append(consideredVariablesPosition[k])

            


    #end of loop                                                    
    data_dict['{0}'.format(list(parsed_data_dictionary.keys())[i])] = var_dict
    print("#"*28)
    print('\n')

#Now that we've analyzed and gathered all necessary data, we can generate plots using the aforementioned data
source_names = list(data_dict.keys())
print(source_names)


#print(xPosData)
#print(yPosData)
#print(zPosData)

#print(recAngleData0)
#print(thetaAngleData0)
#print(reflectAngleData0)

#print(recAngleData1)
#print(thetaAngleData1)
#print(reflectAngleData1)


#Creating lists that contain the number of elements of the x, y, and z position data arrays:
numXPos = []
numYPos = []
numZPos = []

for a in range(len(xPosData)):
	numXPos.append(a)

for b in range(len(yPosData)):
	numYPos.append(b)

for c in range(len(zPosData)):
	numZPos.append(c)

#Creating lists that contain the number of elements in the 3 direct angle data arrays
numRecAngle0 = []
numThetaAngle0 = []
numReflectAngle0 = []

for x in range(len(recAngleData0)):
    numRecAngle0.append(x)

for y in range(len(thetaAngleData0)):
    numThetaAngle0.append(y)

for z in range(len(reflectAngleData0)):
    numReflectAngle0.append(z)

#Creating lists that contain the number of elements in the 3 reflected/refracted angle data arrays
numRecAngle1 = []
numThetaAngle1 = []
numReflectAngle1 = []

for i in range(len(recAngleData1)):
    numRecAngle1.append(i)

for j in range(len(thetaAngleData1)):
    numThetaAngle1.append(j)

for k in range(len(reflectAngleData1)):
    numReflectAngle1.append(k)

#Plotting:

#######################################################################################################################################################

#Starting with the 3D Scatter Plot:
plt.figure(1, figsize = (16,9), facecolor = 'gainsboro')
ax3D = plt.axes(projection = "3d")

ax3D.scatter3D(xPosData, yPosData, zPosData, color = "navy", s = 50, marker = ".", alpha = 0.65)
plt.title("3D Scatter Plot of X, Y, & Z Positions", fontsize = 15, color = 'black', fontweight = 'bold')

#Units?
ax3D.set_xlabel("X Position (m)", fontsize = 10, color = 'black', fontweight = 'bold')
ax3D.set_ylabel("Y Position (m)", fontsize = 10, color = 'black', fontweight = 'bold')
ax3D.set_zlabel("Z Position (m)", fontsize = 10, color = 'black', fontweight = 'bold')

plt.savefig("3D_Scatter_Plot.png")
plt.clf()

#######################################################################################################################################################

#Now plotting a 2D scatter plot of the x position:
plt.figure(2, figsize =  (16, 9), facecolor = 'gainsboro')
axX = plt.axes()

axX.scatter(numXPos, xPosData, color = "maroon", s = 50, marker = "x", alpha = 0.65)
plt.title("Scatter Plot of X Positions", fontsize = 15, color = 'black', fontweight = 'bold')

#Units?
axX.set_xlabel("Number of Each X Position Data Point", fontsize = 10, color = 'black', fontweight = 'bold')
axX.set_ylabel("X Position (m)", fontsize = 10, color = 'black', fontweight = 'bold')

plt.savefig("XPos_Scatter_Plot.png")
plt.clf()

######################################################################################################################################################

#Now plotting a 2D scatter plot of the y position:
plt.figure(3, figsize = (16, 9), facecolor = 'gainsboro')
axY = plt.axes()

axY.scatter(numYPos, yPosData, color = "darkgreen", s = 50, marker = "+", alpha = 0.65)
plt.title("Scatter Plot of Y Positions", fontsize = 15, color = 'black', fontweight = 'bold')

#Units?
axY.set_xlabel("Number of Each Y Position Data Point", fontsize = 10, color = 'black', fontweight = 'bold')
axY.set_ylabel("Y Position (m)", fontsize = 10, color = 'black', fontweight = 'bold')

plt.savefig("YPos_Scatter_Plot.png")
plt.clf()

#######################################################################################################################################################

#Lastly, plotting a 2D scatter plot of the z position:
plt.figure(4, figsize = (16, 9), facecolor = 'gainsboro')
axZ = plt.axes()

axZ.scatter(numZPos, zPosData, color = "darkgoldenrod", s = 50, marker = "2", alpha = 0.65)
plt.title("Scatter Plot of Z Positions", fontsize = 15, color = 'black', fontweight = 'bold')

#Units?
axZ.set_xlabel("Number of Each Z Position Data Point", fontsize = 10, color = 'black', fontweight = 'bold')
axZ.set_ylabel("Z Position (m)", fontsize = 10, color = 'black', fontweight = 'bold')

plt.savefig("ZPos_Scatter_Plot.png")
plt.clf()

#######################################################################################################################################################

#Now we'll add all of these plots as subplots onto 1 singular figure
axSP = plt.figure(5, figsize = (16, 16), facecolor = 'gainsboro')
plt.suptitle("Figure of 4 Scatter Plots", fontsize = 17, color = 'black', fontweight = 'bold')
 
#Adding the 3D scatter plot to the figure
ax1 = axSP.add_subplot(2, 2, 1, projection = "3d")

ax1.scatter3D(xPosData, yPosData, zPosData, color = "navy", s = 50, marker = ".", alpha = 0.65)
ax1.set_title("3D Scatter Plot of X, Y, & Z Positions", fontsize = 10, color = 'black', fontweight = 'bold')

ax1.set_xlabel("X Position (m)", fontsize = 5, color = 'black', fontweight = 'bold')
ax1.set_ylabel("Y Position (m)", fontsize = 5, color = 'black', fontweight = 'bold')
ax1.set_zlabel("Z Position (m)", fontsize = 5, color = 'black', fontweight = 'bold')

#Adding the x position scatter plot
ax2 = axSP.add_subplot(2, 2, 2)

ax2.scatter(numXPos, xPosData, color = "maroon", s = 50, marker = "x", alpha = 0.65)
ax2.set_title("Scatter Plot of X Positions", fontsize = 10, color = 'black', fontweight = 'bold')

ax2.set_xlabel("Number of Each X Position Data Point", fontsize = 5, color = 'black', fontweight = 'bold')
ax2.set_ylabel("X Position (m)", fontsize = 5, color = 'black', fontweight = 'bold')

#Adding the y position scatter plot
ax3 = axSP.add_subplot(2, 2, 3)

ax3.scatter(numYPos, yPosData, color = "darkgreen", s = 50, marker = "+", alpha = 0.65)
ax3.set_title("Scatter Plot of Y Positions", fontsize = 10, color = 'black', fontweight = 'bold')

ax3.set_xlabel("Number of Each Y Position Data Point", fontsize = 5, color = 'black', fontweight = 'bold')
ax3.set_ylabel("Y Position (m)", fontsize = 5, color = 'black', fontweight = 'bold')

#Lastly, adding the z position scatter plot
ax4 = axSP.add_subplot(2, 2, 4)

ax4.scatter(numZPos, zPosData, color = "darkgoldenrod", s = 50, marker = "2", alpha = 0.65)
ax4.set_title("Scatter Plot of Z Positions", fontsize = 10, color = 'black', fontweight = 'bold')

ax4.set_xlabel("Number of Each Z Position Data Point", fontsize = 5, color = 'black', fontweight = 'bold')
ax4.set_ylabel("Z Position (m)", fontsize = 5, color = 'black', fontweight = 'bold')

#Now saving the complete figure
axSP.savefig("Subplots_Of_Position_Scatter_Plots.png")
axSP.clf()

#######################################################################################################################################################

#Plotting Histograms!

#######################################################################################################################################################

#Plotting the direct angle data histograms!

#######################################################################################################################################################

#Plotting the recAngleData0 Histogram
plt.figure(6, figsize = (16, 16), facecolor = 'gainsboro')
plt.axes()

plt.hist(recAngleData0, alpha = 0.75, color = 'fuchsia', align = 'mid', bins = 25, edgecolor = 'black')
plt.xlabel("Rec Angle (Degrees)", fontsize = 10, color = 'black', fontweight = 'bold')
plt.ylabel("Number of times each angle has occurred", fontsize = 10, color = 'black', fontweight = 'bold')
plt.title("Histogram of Direct Rec Angle Data", fontsize = 20, color = 'black', fontweight = 'bold')

plt.savefig("Direct_RecAngle_Histogram.png")
plt.clf()

#########################################################################################################################################################

#Plotting the thetaAngleData0 Histogram
plt.figure(7, figsize = (16,16), facecolor = 'gainsboro')
plt.axes()

plt.hist(thetaAngleData0, alpha = 0.75, color = 'springgreen', align = 'mid', bins = 25, edgecolor = 'black')
plt.xlabel("Theta Angle (Degrees)", fontsize = 10, color = 'black', fontweight = 'bold')
plt.ylabel("Number of times each angle has occurred", fontsize = 10, color = 'black', fontweight = 'bold')
plt.title("Histogram of Direct Theta Angle Data", fontsize = 20, color = 'black', fontweight = 'bold')

plt.savefig("Direct_ThetaAngle_Histogram.png")
plt.clf()

########################################################################################################################################################

#Plotting the reflectAngleData0 Histogram
plt.figure(8, figsize = (16, 16), facecolor = 'gainsboro')
plt.axes()

plt.hist(reflectAngleData0, alpha = 0.75, color = 'cornflowerblue', align = 'mid', bins = 25, edgecolor = 'black')
plt.xlabel("Reflect Angle (Degrees)", fontsize = 10, color = 'black', fontweight = 'bold')
plt.ylabel("Number of times each angle has occurred", fontsize = 10, color = 'black', fontweight = 'bold')
plt.title("Histogram of Direct Reflect Angle Data", fontsize = 20, color = 'black', fontweight = 'bold')

plt.savefig("Direct_ReflectAngle_Histogram.png")
plt.clf()

#######################################################################################################################################################

#Plotting the reflected/refracted angle data histograms!

#######################################################################################################################################################

#Plotting the recAngleData1 Histogram
plt.figure(9, figsize = (16, 16), facecolor = 'gainsboro')
plt.axes()

plt.hist(recAngleData1, alpha = 0.75, color = 'crimson', align = 'mid', bins = 25, edgecolor = 'black')
plt.xlabel("Rec Angle (Degrees)", fontsize = 10, color = 'black', fontweight = 'bold')
plt.ylabel("Number of times each angle has occurred", fontsize = 10, color = 'black', fontweight = 'bold')
plt.title("Histogram of Reflected/Refracted Rec Angle Data", fontsize = 20, color = 'black', fontweight = 'bold')

plt.savefig("Reflected_Refracted_RecAngle_Histogram.png")
plt.clf()

#########################################################################################################################################################

#Plotting the thetaAngleData1 Histogram
plt.figure(10, figsize = (16,16), facecolor = 'gainsboro')
plt.axes()

plt.hist(thetaAngleData1, alpha = 0.75, color = 'green', align = 'mid', bins = 25, edgecolor = 'black')
plt.xlabel("Theta Angle (Degrees)", fontsize = 10, color = 'black', fontweight = 'bold')
plt.ylabel("Number of times each angle has occurred", fontsize = 10, color = 'black', fontweight = 'bold')
plt.title("Histogram of Reflected/Refracted Theta Angle Data", fontsize = 20, color = 'black', fontweight = 'bold')

plt.savefig("Reflected_Refracted_ThetaAngle_Histogram.png")
plt.clf()

########################################################################################################################################################

#Plotting the reflectAngleData1 Histogram
plt.figure(11, figsize = (16, 16), facecolor = 'gainsboro')
plt.axes()

plt.hist(reflectAngleData1, alpha = 0.75, color = 'blue', align = 'mid', bins = 25, edgecolor = 'black')
plt.xlabel("Reflect Angle (Degrees)", fontsize = 10, color = 'black', fontweight = 'bold')
plt.ylabel("Number of times each angle has occurred", fontsize = 10, color = 'black', fontweight = 'bold')
plt.title("Histogram of Reflected/Refracted Reflect Angle Data", fontsize = 20, color = 'black', fontweight = 'bold')

plt.savefig("Reflected_Refracted_ReflectAngle_Histogram.png")
plt.clf()

#####################################################################################################################################################

#Now plotting histograms that compare the direct and reflected/refracted angle data!

#####################################################################################################################################################
    
#Plotting the recAngleData0 & recAngleData1 Histograms together
plt.figure(12, figsize = (16, 16), facecolor = 'gainsboro')
plt.axes()

plt.hist(recAngleData0, alpha = 0.50, color = 'fuchsia', align = 'mid', bins = 25, edgecolor = 'black')
plt.hist(recAngleData1, alpha = 0.50, color = 'crimson', align = 'mid', bins = 25, edgecolor = 'black')
plt.xlabel("Rec Angle (Degrees)", fontsize = 10, color = 'black', fontweight = 'bold')
plt.ylabel("Number of times each angle has occurred", fontsize = 10, color = 'black', fontweight = 'bold')
plt.legend(['Direct Rec Angle Data', 'Reflected/Refracted Rec Angle Data'], fontsize = 10, loc = 'upper right')
plt.title("Histogram of Direct & Reflected/Refracted Rec Angle Data", fontsize = 20, color = 'black', fontweight = 'bold')

plt.savefig("Combined_RecAngle_Histogram.png")
plt.clf()

#####################################################################################################################################################

#Plotting the thetaAngleData0 & thetaAngleData1 Histograms together
plt.figure(13, figsize = (16, 16), facecolor = 'gainsboro')
plt.axes()

plt.hist(thetaAngleData0, alpha = 0.50, color = 'springgreen', align = 'mid', bins = 25, edgecolor = 'black')
plt.hist(thetaAngleData1, alpha = 0.50, color = 'green', align = 'mid', bins = 25, edgecolor = 'black')
plt.xlabel("Theta Angle (Degrees)", fontsize = 10, color = 'black', fontweight = 'bold')
plt.ylabel("Number of times each angle has occurred", fontsize = 10, color = 'black', fontweight = 'bold')
plt.legend(['Direct Theta Angle Data', 'Reflected/Refracted Theta Angle Data'], fontsize = 10, loc = 'upper right')
plt.title("Histogram of Direct & Reflected/Refracted Theta Angle Data", fontsize = 20, color = 'black', fontweight = 'bold')

plt.savefig("Combined_ThetaAngle_Histogram.png")
plt.clf()

#####################################################################################################################################################

#Plotting the reflectAngleData0 & reflectAngleData1 Histograms together
plt.figure(14, figsize = (16, 16), facecolor = 'gainsboro')
plt.axes()

plt.hist(reflectAngleData0, alpha = 0.50, color = 'cornflowerblue', align = 'mid', bins = 25, edgecolor = 'black')
plt.hist(reflectAngleData1, alpha = 0.50, color = 'blue', align = 'mid', bins = 25, edgecolor = 'black')
plt.xlabel("Reflect Angle (Degrees)", fontsize = 10, color = 'black', fontweight = 'bold')
plt.ylabel("Number of times each angle has occurred", fontsize = 10, color = 'black', fontweight = 'bold')
plt.legend(['Direct Reflect Angle Data', 'Reflected/Refracted Reflect Angle Data'], fontsize = 10, loc = 'upper right')
plt.title("Histogram of Direct & Reflected/Refracted Reflect Angle Data", fontsize = 20, color = 'black', fontweight = 'bold')

plt.savefig("Combined_ReflectAngle_Histogram.png")
plt.clf()

#####################################################################################################################################################

#Plotting the combined angle histograms onto a single figure
axAngleHistSP = plt.figure(15, figsize = (16, 16), facecolor = 'gainsboro')
plt.suptitle("Figure of 3 Combined Histograms", fontsize = 20, color = 'black', fontweight = 'bold')

#Adding the RecAngleData Histogram to the figure
axA = axAngleHistSP.add_subplot(3, 1, 1)
axA.hist(recAngleData0, alpha = 0.50, color = 'fuchsia', align = 'mid', bins = 25, edgecolor = 'black')
axA.hist(recAngleData1, alpha = 0.50, color = 'crimson', align = 'mid', bins = 25, edgecolor = 'black')
axA.set_xlabel("Rec Angle (Degrees)", fontsize = 10, color = 'black', fontweight = 'bold')
axA.set_ylabel("Number of times each angle has occurred", fontsize = 10, color = 'black', fontweight = 'bold')
axA.legend(['Direct Rec Angle Data', 'Reflected/Refracted Rec Angle Data'], fontsize = 10, loc = 'upper right')
axA.set_title("Histogram of Direct & Reflected/Refracted Rec Angle Data", fontsize = 15, color = 'black', fontweight = 'bold')

#Adding the ThetaAngleData Histogram to the figure
axB = axAngleHistSP.add_subplot(3, 1, 2)
axB.hist(thetaAngleData0, alpha = 0.50, color = 'springgreen', align = 'mid', bins = 25, edgecolor = 'black')
axB.hist(thetaAngleData1, alpha = 0.50, color = 'green', align = 'mid', bins = 25, edgecolor = 'black')
axB.set_xlabel("Theta Angle (Degrees)", fontsize = 10, color = 'black', fontweight = 'bold')
axB.set_ylabel("Number of times each angle has occurred", fontsize = 10, color = 'black', fontweight = 'bold')
axB.legend(['Direct Theta Angle Data', 'Reflected/Refracted Theta Angle Data'], fontsize = 10, loc = 'upper right')
axB.set_title("Histogram of Direct & Reflected/Refracted Theta Angle Data", fontsize = 15, color = 'black', fontweight = 'bold')

#Adding the ReflectAngleData Histogram to the figure
axC = axAngleHistSP.add_subplot(3, 1, 3)
axC.hist(reflectAngleData0, alpha = 0.50, color = 'cornflowerblue', align = 'mid', bins = 25, edgecolor = 'black')
axC.hist(reflectAngleData1, alpha = 0.50, color = 'blue', align = 'mid', bins = 25, edgecolor = 'black')
axC.set_xlabel("Reflect Angle (Degrees)", fontsize = 10, color = 'black', fontweight = 'bold')
axC.set_ylabel("Number of times each angle has occurred", fontsize = 10, color = 'black', fontweight = 'bold')
axC.legend(['Direct Reflect Angle Data', 'Reflected/Refracted Reflect Angle Data'], fontsize = 10, loc = 'upper right')
axC.set_title("Histogram of Direct & Reflected/Refracted Reflect Angle Data", fontsize = 15, color = 'black', fontweight = 'bold')

#Saving the figure
axAngleHistSP.savefig("Subplots_Of_Combined_Angle_Data_Histograms.png")
axAngleHistSP.clf()

#####################################################################################################################################################

print("The script has finished running and the plots have been created.")

stop = timeit.default_timer()
print('Time: \033[1;31m{0}\033[0;0m'.format(stop - start))
exit()
