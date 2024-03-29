#!/usr/bin/env python3

######################################
#    AraSim simple event reader      #
#        Dennis H. calderon          #
#    calderon-madera.1@osu.edu       #
######################################

#######################################################
"""
=======================
##project_test.py##
======================
Author: Dennis H. Calderon
Email: calderon-madera.1@osu.edu
Date: November 02, 2021
Modified: March 24, 2022
=======================
Descripiton: 
This PYTHON script takes two sets of AraSim output .root files. For each set, it makes a cut for triggered events, pulls variables, and makes histograms comparing the two. 

This scrpit was make for a comparison of antennas for the ARA Bicone (vpol) and an evolved antenna using GENETIS (vpol). This current verion is comparing Direct & Refracted/Reflected Events using variables (theta_rec, rec_ang, reflect_ang) for each simulation run.
=======================
Usage:
python project.py <source> [options] <source_2>
<source_1> is where the ROOT file from your AraSim output
<source_2> is path where the other ROOT file to compare
<source_3> is path where the other ROOT file to compare
<source_4> is path where the other ROOT file to compare
<source_5> is path where the other ROOT file to compare
<source_6> is path where the other ROOT file to compare.
=======================
Options:
[-s2, -s3, -s4, -s5, -s6]  tells program that you are putting in anoter source of simulation files.
=======================
example:
python all_vars.py ../output_files/AraOut.Bicone.run{0..9}.root -s2 ../output_files/AraOut.GENETIS.run{0..9}.root
=======================
"""

#######################################################
import timeit
start = timeit.default_timer()
#######################################################
print("\n")
print('\033[1;37m#\033[0;0m'*50)
print("Now running \033[1;4;5;31mproject_test.py\033[0;0m!")
print('\033[1;37m#\033[0;0m'*50)
print('\n')
##########################################
print("\033[1;37mPlease wait patiently...\033[0;0m")
print('Importing libraries...')

##########################################
#System libraries
#import sys
import argparse
#import csv
#import types
#import os
import warnings
warnings.filterwarnings("ignore")
print('...')

#PyRoot libraries
import ROOT
#from ROOT import TCanvas, TGraph
#from ROOT import gROOT
from ROOT import gInterpreter, gSystem
#from ROOT import TChain, TSelector, TTree
from ROOT import TChain
print('...')

#Python libraries
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
print('...')

#Plotting functions
import modularized_plotting_functions_test as plotMaker
print('...')

##########################################

#####
#AraSim specific headers needed
gInterpreter.ProcessLine('#include "/cvmfs/ara.opensciencegrid.org/trunk/centos7/source/AraSim/Position.h"')#"/users/PAS0654/dcalderon/AraSim/Position.h"')
gInterpreter.ProcessLine('#include "/cvmfs/ara.opensciencegrid.org/trunk/centos7/source/AraSim/Report.h"')#"/users/PAS0654/dcalderon/AraSim/Report.h"')
gInterpreter.ProcessLine('#include "/cvmfs/ara.opensciencegrid.org/trunk/centos7/source/AraSim/Detector.h"')#"/users/PAS0654/dcalderon/AraSim/Detector.h"')
gInterpreter.ProcessLine('#include "/cvmfs/ara.opensciencegrid.org/trunk/centos7/source/AraSim/Settings.h"')#"/users/PAS0654/dcalderon/AraSim/Settings.h"')

gSystem.Load('/cvmfs/ara.opensciencegrid.org/trunk/centos7/ara_build/lib/libAra.so')#'/users/PAS0654/dcalderon/AraSim/libAra.so') 

##########################################
# We want to give an output file as an input. This checks that we have a fle to read
parser = argparse.ArgumentParser(
        description='Read AraSim file and produce some plots. Can also compare two AraSim files.')
parser.add_argument("source_1", help = "Path to the AraSim file you want to use.", nargs='+')
parser.add_argument("--source_2", "-s2", help = "Path to another AraSim file you want to comprare to.", nargs='+')
parser.add_argument("--source_3", "-s3", help = "Path to another AraSim file you want to comprare to.", nargs='+')
parser.add_argument("--source_4", "-s4", help = "Path to another AraSim file you want to comprare to.", nargs='+')
parser.add_argument("--source_5", "-s5", help = "Path to another AraSim file you want to comprare to.", nargs='+')
parser.add_argument("--source_6", "-s6", help = "Path to another AraSim file you want to comprare to.", nargs='+')

g = parser.parse_args()

#print(g)
#print('#'*28)

# source_name = g.source[0].split('.')[1]
# source_2_name = g.source_2[0].split('.')[1]
# 
# print(source_name)
# print(source_2_name)
# print('#'*28)
##########################################
'''
can put this inside as well
'''

#Making a dictionary of the parsed arguments
source_dict = g.__dict__
#Deleting empty arguments from dictionary
source_dict = {k:v for k, v in source_dict.items() if v != None}
print('#'*28)
print(source_dict)
print('#'*28)
print('\n')

source_names = list(source_dict.keys())
for i in range(len(source_names)):
        source_names[i] = source_dict[source_names[i]][0].split('.')[-4]
#print(source_names)


# source_names = list(data_dict.keys())
# print(source_names)
# print(source_dict[source_names[0]])
#exit()
# source_names= []
# print(source_dict.keys())

# for x in list(source_dict.keys()):
#         source_names = source_dict[str(x)][0].split('.')[1]
#         print(source_names)
#         print(x)
#         #print(source_names[x])

# print(source_names)
# exit()


########################
##Variables needed
########################
energy = np.power(10,18)
earth_depth = 6359632.4
core_x = 10000.0
core_y = 10000.0
#stations[i].strings[j].antennas[k].GetX() << " : " <<

##################################
###Loop over Evenets
##################################
##########################################

print('#'*28)
print("Now lets do the loop")
print("Please wait patiently...")
print('...')
print('\n')

data_dict = {}
for i in range(len(source_dict.keys())):
        
        #General info for each simulation set
        print('#'*50)
        
        #setting trees
        var_dict = {}
        #list of all variable names
        var = ['trigg', 'weight', 'posnu_x', 'posnu_y', 'posnu_z',
               'rec_ang_0', 'theta_rec_0', 'reflect_ang_0',
               'dist_0', 'arrival_time_0', 'reflection_0', 
               'l_att_0', 'view_ang_0', 'launch_ang_0',
               'rec_ang_1', 'theta_rec_1', 'reflect_ang_1',
               'dist_1', 'arrival_time_1', 'reflection_1', 
               'l_att_1', 'view_ang_1', 'launch_ang_1',
               'current', 'flavor', 'elast',
               'nnu_theta', 'nnu_phi', 'ShowerEnergy',
               'depth', 'distance']
        
        #loop for making dictionary of variables and empty list
        for x in var:
                var_dict['{0}'.format(x)] = []
                #print('yes')
                # print(var_dict)

        SimTree = [] #sets SimTree and makes empty list
        SimTree = TChain("AraTree2") #Which tree I will be chaining
        for line in list(source_dict.values())[i]: #for every filename in my list
                SimTree.AddFile(line)
        reportPtr = ROOT.Report()#report pointer
        eventPtr = ROOT.Event()#event pointe
        #detectorPtr = ROOT.Detector()
        #can also add more pointers if needed
        #print(reportPtr)
        #print(SimTree)
        SimTree.SetBranchAddress("report", ROOT.AddressOf(reportPtr))
        SimTree.SetBranchAddress("event", ROOT.AddressOf(eventPtr))
        #SimTree.SetBranchAddress("detector", ROOT.AddressOf(detectorPtr))
        
        #basic info of data
        totalEvents = SimTree.GetEntries()
        # key = []
        # key =  list(source_dict)[i]
        
        print('\033[1;37m{0}\033[0;0m'.format(source_names[i]))
        print('Total Events: {0}'.format(totalEvents))
        print('#'*50)
        var_dict['Total_Events'] = []
        var_dict['Total_Events'] = totalEvents
        var_dict['Total_Weights'] = []
        
        #print(SimTree.GetEntry(0))
        #print(SimTree.GetEntry(1))
        #print(i)
        #print(type(SimTree))
        #print(SimTree)
        #SimTree.Print()
##Beaks here##
        #Now we loop over all the events 
        for j in range(totalEvents):
                #print(j)
                SimTree.GetEntry(j)
                var_dict['Total_Weights'].append(eventPtr.Nu_Interaction[0].weight)

                #var_dict['trigg_weight']
                #all_weight = eventPtr.Nu_Interaction[0].weight
                #Selecting only triggered events and a weight between 0 and 1
                if (reportPtr.stations[0].Global_Pass > 0) and (eventPtr.Nu_Interaction[0].weight >= 0 and eventPtr.Nu_Interaction[0].weight <= 1):
                        #print(j)
                        #print(key)
                        trigg = j
                        var_dict['trigg'].append(j)
                        
                        #If value is seen in both antennas (Top Vpol and Bot Vpol) then we take an average of two
                        #var_dict['trigg'].append(j)
                        try:                                                                 
                                #interaction position in ice
                                posnu_x = eventPtr.Nu_Interaction[0].posnu.GetX()
                                posnu_y = eventPtr.Nu_Interaction[0].posnu.GetY()
                                posnu_z = eventPtr.Nu_Interaction[0].posnu.GetZ()
                                
                                #Getting angle of received signal in antenna
                                #Direct solutioins
                                rec_ang_0 = ((reportPtr.stations[0].strings[1].antennas[0].rec_ang[0] + 
                                             reportPtr.stations[0].strings[1].antennas[2].rec_ang[0])/2.0)
                                reflect_ang_0 = ((reportPtr.stations[0].strings[1].antennas[0].reflect_ang[0] +
                                                 reportPtr.stations[0].strings[1].antennas[2].reflect_ang[0])/2.0)
                                theta_rec_0 = ((reportPtr.stations[0].strings[1].antennas[0].theta_rec[0] +
                                               reportPtr.stations[0].strings[1].antennas[2].theta_rec[0])/2.0)
                                
                                dist_0 = reportPtr.stations[0].strings[1].antennas[0].Dist[0]
                                arrival_time_0 = reportPtr.stations[0].strings[1].antennas[0].arrival_time[0] 
                                reflection_0 = reportPtr.stations[0].strings[1].antennas[0].reflection[0]
                                l_att_0 = reportPtr.stations[0].strings[1].antennas[0].L_att[0]
                                
                                view_ang_0 = reportPtr.stations[0].strings[1].antennas[0].view_ang[0]
                                launch_ang_0 = reportPtr.stations[0].strings[1].antennas[0].launch_ang[0]

                                #Refracted/Reflected solutions
                                rec_ang_1 = ((reportPtr.stations[0].strings[1].antennas[0].rec_ang[1] +
                                             reportPtr.stations[0].strings[1].antennas[2].rec_ang[1])/2.0)
                                reflect_ang_1 = ((reportPtr.stations[0].strings[1].antennas[0].reflect_ang[1] +
                                                 reportPtr.stations[0].strings[1].antennas[2].reflect_ang[1])/2.0)
                                theta_rec_1 = ((reportPtr.stations[0].strings[1].antennas[0].theta_rec[1] +
                                               reportPtr.stations[0].strings[1].antennas[2].theta_rec[1])/2.0)
                                
                                dist_1 = reportPtr.stations[0].strings[1].antennas[0].Dist[1]
                                arrival_time_1 = reportPtr.stations[0].strings[1].antennas[0].arrival_time[1] 
                                reflection_1 = reportPtr.stations[0].strings[1].antennas[0].reflection[1]
                                l_att_1 = reportPtr.stations[0].strings[1].antennas[0].L_att[1]
                                
                                view_ang_1 = reportPtr.stations[0].strings[1].antennas[0].view_ang[1]
                                launch_ang_1 = reportPtr.stations[0].strings[1].antennas[0].launch_ang[1]
                                
                                #incomeing neutrino info
                                nnu_theta = eventPtr.Nu_Interaction[0].nnu.Theta()
                                nnu_phi = eventPtr.Nu_Interaction[0].nnu.Phi()
                                
                                current = eventPtr.Nu_Interaction[0].currentint
                                flavor = eventPtr.nuflavorint
                                elast = eventPtr.Nu_Interaction[0].elast_y
                                
                                #weight
                                weight = eventPtr.Nu_Interaction[0].weight
                                                
                                if current == 1 and flavor == 1:
                                        ShowerEnergy = energy                                        
                                else:
                                        ShowerEnergy = energy * elast
                                
                                depth = posnu_z - earth_depth
                                distance =  ((posnu_x - core_x)**2 + (posnu_y - core_y)**2 )**(0.5)
                                #detectorPtr.stations[0].strings[1].antennas[0].GetX()
                                

                                all_var = [trigg, weight, posnu_x, posnu_y, posnu_z,
                                       rec_ang_0, theta_rec_0, reflect_ang_0,
                                       dist_0, arrival_time_0, reflection_0, 
                                       l_att_0, view_ang_0, launch_ang_0,
                                       rec_ang_1, theta_rec_1, reflect_ang_1,
                                       dist_1, arrival_time_1, reflection_1, 
                                       l_att_1, view_ang_1, launch_ang_1,
                                       current, flavor, elast,
                                       nnu_theta, nnu_phi, ShowerEnergy,
                                       depth, distance]
                               
                                for k in range(1,len(all_var)):
                                        var_dict['{0}'.format(var[k])].append(all_var[k])
                                print(j)
                                        
                        except IndexError:
                                
                                #Both antennas didn't see a signal, so we try with index 0 (Bot Vpol)
                                try: 
                                        
                                        #interaction position in ice
                                        posnu_x = eventPtr.Nu_Interaction[0].posnu.GetX()
                                        posnu_y = eventPtr.Nu_Interaction[0].posnu.GetY()
                                        posnu_z = eventPtr.Nu_Interaction[0].posnu.GetZ()
                                        
                                        #angles seen by antenna
                                        rec_ang_0 = reportPtr.stations[0].strings[1].antennas[0].rec_ang[0]
                                        theta_rec_0 = reportPtr.stations[0].strings[1].antennas[0].theta_rec[0]
                                        reflect_ang_0 = reportPtr.stations[0].strings[1].antennas[0].reflect_ang[0]
                                        
                                        dist_0 = reportPtr.stations[0].strings[1].antennas[0].Dist[0]
                                        arrival_time_0 = reportPtr.stations[0].strings[1].antennas[0].arrival_time[0] 
                                        reflection_0 = reportPtr.stations[0].strings[1].antennas[0].reflection[0]
                                        l_att_0 = reportPtr.stations[0].strings[1].antennas[0].L_att[0]
                                        
                                        view_ang_0 = reportPtr.stations[0].strings[1].antennas[0].view_ang[0]
                                        launch_ang_0 = reportPtr.stations[0].strings[1].antennas[0].launch_ang[0]
                                       
                                        rec_ang_1 = reportPtr.stations[0].strings[1].antennas[0].rec_ang[1]
                                        theta_rec_1 = reportPtr.stations[0].strings[1].antennas[0].theta_rec[1]
                                        reflect_ang_1 = reportPtr.stations[0].strings[1].antennas[0].reflect_ang[1]
                                        
                                        #other info 
                                        
                                        dist_1 = reportPtr.stations[0].strings[1].antennas[0].Dist[1]
                                        arrival_time_1 = reportPtr.stations[0].strings[1].antennas[0].arrival_time[1] 
                                        reflection_1 = reportPtr.stations[0].strings[1].antennas[0].reflection[1]
                                        l_att_1 = reportPtr.stations[0].strings[1].antennas[0].L_att[1]
                                        
                                        view_ang_1 = reportPtr.stations[0].strings[1].antennas[0].view_ang[1]
                                        launch_ang_1 = reportPtr.stations[0].strings[1].antennas[0].launch_ang[1]       
                                        
                                        #incomeing neutrino info
                                        nnu_theta = eventPtr.Nu_Interaction[0].nnu.Theta()
                                        nnu_phi = eventPtr.Nu_Interaction[0].nnu.Phi()
                                        
                                        current = eventPtr.Nu_Interaction[0].currentint
                                        flavor = eventPtr.nuflavorint
                                        elast = eventPtr.Nu_Interaction[0].elast_y
                                        
                                        #weight
                                        weight = eventPtr.Nu_Interaction[0].weight
                                                
                                        if current == 1 and flavor == 1:
                                                ShowerEnergy = energy                                        
                                        else:
                                                ShowerEnergy = energy * elast
                                                
                                        depth = posnu_z - earth_depth
                                        distance = ((posnu_x - core_x)**2 + (posnu_y - core_y)**2 )**(0.5)
                                                                                        
                                        all_var = [trigg, weight, posnu_x, posnu_y, posnu_z,
                                                   rec_ang_0, theta_rec_0, reflect_ang_0,
                                                   dist_0, arrival_time_0, reflection_0, 
                                                   l_att_0, view_ang_0, launch_ang_0,
                                                   rec_ang_1, theta_rec_1, reflect_ang_1,
                                                   dist_1, arrival_time_1, reflection_1, 
                                                   l_att_1, view_ang_1, launch_ang_1,
                                                   current, flavor, elast,
                                                   nnu_theta, nnu_phi, ShowerEnergy,
                                                   depth, distance]
                                                
                                        for k in range(1,len(all_var)):
                                                var_dict['{0}'.format(var[k])].append(all_var[k])
                                                
                                        print(str(j)+" only has Bot Vpol signal")

                                except IndexError:
                                        try: #Have this here because not always that both antenna see
                                                
                                                #interaction position in ice
                                                posnu_x = eventPtr.Nu_Interaction[0].posnu.GetX()
                                                posnu_y = eventPtr.Nu_Interaction[0].posnu.GetY()
                                                posnu_z = eventPtr.Nu_Interaction[0].posnu.GetZ()
                                                
                                                #angles seen by antenna
                                                rec_ang_0 = reportPtr.stations[0].strings[1].antennas[2].rec_ang[0]
                                                theta_rec_0 = reportPtr.stations[0].strings[1].antennas[2].theta_rec[0]
                                                reflect_ang_0 = reportPtr.stations[0].strings[1].antennas[2].reflect_ang[0]
                                                
                                                rec_ang_1 = reportPtr.stations[0].strings[1].antennas[2].rec_ang[1]
                                                theta_rec_1 = reportPtr.stations[0].strings[1].antennas[2].theta_rec[1]
                                                reflect_ang_1 = reportPtr.stations[0].strings[1].antennas[2].reflect_ang[1]
                                                
                                                #other info 
                                                dist_0 = reportPtr.stations[0].strings[1].antennas[2].Dist[0]
                                                arrival_time_0 = reportPtr.stations[0].strings[1].antennas[2].arrival_time[0] 
                                                reflection_0 = reportPtr.stations[0].strings[1].antennas[2].reflection[0]
                                                l_att_0 = reportPtr.stations[0].strings[1].antennas[2].L_att[0]
                                                
                                                view_ang_0 = reportPtr.stations[0].strings[1].antennas[2].view_ang[0]
                                                launch_ang_0 = reportPtr.stations[0].strings[1].antennas[2].launch_ang[0]
                                                
                                                dist_1 = reportPtr.stations[0].strings[1].antennas[2].Dist[1]
                                                arrival_time_1 = reportPtr.stations[0].strings[1].antennas[2].arrival_time[1] 
                                                reflection_1 = reportPtr.stations[0].strings[1].antennas[2].reflection[1]
                                                l_att_1 = reportPtr.stations[0].strings[1].antennas[2].L_att[1]
                                                
                                                view_ang_1 = reportPtr.stations[0].strings[1].antennas[2].view_ang[1]
                                                launch_ang_1 = reportPtr.stations[0].strings[1].antennas[2].launch_ang[1]       
                                                
                                                #incomeing neutrino info
                                                nnu_theta = eventPtr.Nu_Interaction[0].nnu.Theta()
                                                nnu_phi = eventPtr.Nu_Interaction[0].nnu.Phi()
                                                
                                                current = eventPtr.Nu_Interaction[0].currentint
                                                flavor = eventPtr.nuflavorint
                                                elast = eventPtr.Nu_Interaction[0].elast_y
                                                
                                                #weight
                                                weight = eventPtr.Nu_Interaction[0].weight
                                                
                                                
                                                if current == 1 and flavor == 1:
                                                        ShowerEnergy = energy                                        
                                                else:
                                                        ShowerEnergy = energy * elast
                                                        
                                                depth = posnu_z - earth_depth
                                                distance = ((posnu_x - core_x)**2 + (posnu_y - core_y)**2 )**(0.5)
                                                
                                                all_var = [trigg, weight, posnu_x, posnu_y, posnu_z,
                                                           rec_ang_0, theta_rec_0, reflect_ang_0,
                                                           dist_0, arrival_time_0, reflection_0, 
                                                           l_att_0, view_ang_0, launch_ang_0,
                                                           rec_ang_1, theta_rec_1, reflect_ang_1,
                                                           dist_1, arrival_time_1, reflection_1, 
                                                           l_att_1, view_ang_1, launch_ang_1,
                                                           current, flavor, elast,
                                                           nnu_theta, nnu_phi, ShowerEnergy,
                                                           depth, distance]
                                                        
                                                for k in range(1,len(all_var)):
                                                        var_dict['{0}'.format(var[k])].append(all_var[k])
                                                                
                                                
                                                print(str(j)+" only has Top Vpol signal")                                                             
                                        except IndexError:
                                                print("Event "+str(j)+" has no signal in either Top or Bot Vpol")
                                                #exit()
                                                continue
                                                
        
        #end of loop                                                    
        data_dict['{0}'.format(source_names[i])] = var_dict
        print("#"*28)
        print('\n')

        
#print(data_dict.keys())
print('\n')
print("We have now looped over alll events and selected only triggered events")
print("Now we can let the fun begin...")
print('#'*50)
print('\n')

#print(data_dict['source_1']['distance'])
#exit()

#######################################
###Plots
#######################################
print('#'*50)
print("Now lets make some plots!")
print('#'*50)

#source_names = list(data_dict.keys())


##
w = 2.0
binsize = np.linspace(-1.0, 1.0, 41)
bindepth = 20
bindistance = np.linspace(0,4000, 21)

bin_cos = np.linspace(-1.0, 1.0, 41)
bin_dist = np.linspace(0,4000, 41)
binsize = np.linspace(-1.0, 1.0, 41)
bindepth = 20
bindistance = np.linspace(0,4000, 41)

##Setting up legends 
colors = ['r','b','g','c','m','y']

custom_lines_style = [Line2D([0], [0], color='k', ls='-'),
                      Line2D([0], [0], color='k', ls='--')]
###
#Making legends
custom_lines_color = []
for i in range(len(source_names)):
        custom_lines_color.append(Line2D([0], [0], color=colors[i], lw=4))
custom_lines_color.append(Line2D([0], [0], color='k', ls ='-'))
custom_lines_color.append(Line2D([0], [0], color='k', ls ='--'))

legend_names = list(data_dict.keys())
legend_names.append('Direct')
legend_names.append('Refracted')

custom_legend = []
for i in range(len(source_names)):
        custom_legend.append(Line2D([0], [0], color=colors[i], lw=4))

#colors[i], lw=4))
#new_custom = custom_lines_color.append(custom_lines_style)
#new_custom = custom_lines_color.append(custom_lines_style)
#print(new_custom)

#legend_names = list(data_dict.keys())
#legend_names = []
#legend_names.append(source_names)
#legend_names.append('Direct')
#legend_names.append('Refracted')
#print(legend_names)
#print(source_names)
#print(custom_lines_color)
#exit()




#Variable arrays for plotting
hist_vars = ['rec_ang','theta_rec','view_ang','launch_ang','reflect_ang',
             'nnu_theta', 'nnu_phi',
             'dist', 'ShowerEnergy', 'depth', 'distance', 'flavor', 'elast', 'weight']
bins = [bin_cos, bin_cos, bin_cos, bin_cos, bin_cos, bindistance]
ang_strings = ['ang', 'theta', 'phi']
# var = ['trigg', 'weight', 'posnu_x', 'posnu_y', 'posnu_z',
#                'rec_ang_0', 'theta_rec_0', 'reflect_ang_0',
#                'dist_0', 'arrival_time_0', 'reflection_0', 
#                'l_att_0', 'view_ang_0', 'launch_ang_0',
#                'rec_ang_1', 'theta_rec_1', 'reflect_ang_1',
#                'dist_1', 'arrival_time_1', 'reflection_1', 
#                'l_att_1', 'view_ang_1', 'launch_ang_1',
#                'current', 'flavor', 'elast',
#                'nnu_theta', 'nnu_phi', 'ShowerEnergy',
#                'depth', 'distance']

#To plot the collected data, we will call functions from a prewritten python file


##################
#####Plotting#####
####################

print("Histograms!")
print("All at once!")
for j in range(len(hist_vars)):
        print("Plotting...")
        plt.figure(j, figsize=(8,6))
        for i in range(len(source_names)):
                #hist_maker(hist_vars[j], source_names[0], colors[0], makelabel=True)
                plotMaker.hist_maker(data_dict, bin_cos, bindistance, hist_vars[j], source_names[i], colors[i])#, makelabel=True)
                plt.title("{0}".format(data_dict[source_names[i]]['Total_Events']))
        plt.savefig('test_plots/Hist_{0}_All.png'.format(hist_vars[j]),dpi=300)
        plt.clf()

print("Bicone vs. Rest...")
for j in range(len(hist_vars)):
        print("Plotting...")
        plt.figure(j, figsize=(8,6))
        for i in range(1, len(source_names)):
                plotMaker.hist_maker(data_dict, bin_cos, bindistance, hist_vars[j], source_names[0], colors[0])#, makelabel=True)
                plotMaker.hist_maker(data_dict, bin_cos, bindistance, hist_vars[j], source_names[i], colors[i])#, makelabel=True)
                plt.title("{0}".format(data_dict[source_names[i]]['Total_Events']))
                plt.savefig('test_plots/Hist_{0}_{1}_{2}.png'.format(hist_vars[j],source_names[0],source_names[i]),dpi=300)
                plt.clf()


# for i in range(len(hist_vars)):
#         plt.figure(i, figsize=(8,6))
#         print("Plotting...")
#         hist_maker(hist_vars[i], makelabel=True)
#         #plt.gca().add_artist(legend1)
#         plt.savefig('test_plots/Hist_{0}.png'.format(hist_vars[i]),dpi=300)
#         plt.clf()
# print("Done!")

print("Scatter Plots!")

scatter_vars = ['distance', 'depth', 'dist_0', 'rec_ang_0', 'theta_rec_0']

for i in range(len(source_names)):
        print("Plotting...")
        plt.figure(i, figsize=(8,6))
        plotMaker.scatter_maker(scatter_vars[0], scatter_vars[1], data_dict, bin_cos, bindistance, source_names[i], colors[i])
        plt.title("{0}".format(data_dict[source_names[i]]['Total_Events']))
        plt.savefig('test_plots/Scatter_{2}_{0}_{1}_.png'.format(scatter_vars[0], 
                                                                 scatter_vars[1], 
                                                                 source_names[i], colors[i]), dpi=300)
        plt.clf()
print("Done!")
 
print("2D Histogram Plots!")
for i in range(len(source_names)):
        print("Plotting...")
        plt.figure(i, figsize=(8,6))
        plotMaker.multi_hist(scatter_vars[2], scatter_vars[4], data_dict, bin_cos, bindistance, bin_dist, source_names[i])
        plt.savefig('test_plots/2DHist_{2}_{0}_{1}_.png'.format(scatter_vars[2], 
                                                                scatter_vars[3], 
                                                                source_names[i]), dpi=300)
        plt.clf()
print("Done!")

print("2D Histogram Comparison Plots!")
for i in range(1,len(source_names)):
        print("Plotting...")
        plt.figure(i, figsize=(8,6))
        plotMaker.diff_hist(scatter_vars[2], scatter_vars[4], data_dict, bin_cos, bindistance, bin_dist, source_names, source_names[0], source_names[i])
        plt.savefig('test_plots/2DHistDiff_{2}_{3}_{0}_{1}_.png'.format(scatter_vars[2], 
                                                                        scatter_vars[3], 
                                                                        source_names[0], 
                                                                        source_names[i]), dpi=300)
        #plt.savefig('test_plots/2DHist_{2}_{0}_{1}_.png'.format(var), dpi=300)
        plt.clf()
print("Done!")


#print(hist_dict[source_names][0] - hist_dict[source_names][0])

hist_vars = ['rec_ang','theta_rec','view_ang','launch_ang','reflect_ang',
             'nnu_theta', 'nnu_phi',
             'dist', 'ShowerEnergy', 'depth', 'distance', 'flavor', 'elast', 'weight']


print("PDF of Histograms")
#print("Plotting...")
#making pdfs of all histogram
plt.figure(1001, figsize=(8.5,11))
plt.suptitle('All sources', fontsize=16)
#plt.subplots(4,2)
for i in range(len(source_names)):
        print("Plotting...")
        plt.subplot(3, 2, 1)
        plotMaker.hist_maker(data_dict, bin_cos, bindistance, 'nnu_theta', source_names[i], colors[i], fontsize=8)# makelabel=False)
        #plt.gca().add_artist(legend)
        plt.subplot(3, 2, 2)
        plotMaker.hist_maker(data_dict, bin_cos, bindistance, 'theta_rec', source_names[i], colors[i], fontsize=8)# makelabel=False)
        #plt.gca().add_artist(legend)
        plt.subplot(3, 2, 3)
        plotMaker.hist_maker(data_dict, bin_cos, bindistance, 'ShowerEnergy', source_names[i], colors[i], fontsize=8)# makelabel=False)
        #plt.gca().add_artist(legend)
        plt.subplot(3, 2, 4)
        plotMaker.hist_maker(data_dict, bin_cos, bindistance, 'weight', source_names[i], colors[i], fontsize=8)# makelabel=False)
        #plt.gca().add_artist(legend)
        plt.subplot(3, 2, 5)
        plotMaker.hist_maker(data_dict, bin_cos, bindistance, 'dist', source_names[i], colors[i], fontsize=8)# makelabel=False)
        #plt.gca().add_artist(legend)
        plt.subplot(3, 2, 6)
        plotMaker.hist_maker(data_dict, bin_cos, bindistance, 'depth', source_names[i], colors[i], fontsize=8)# makelabel=False)
#plt.gca().add_artist(legend)
#plt.subplot(4, 2, 7)
#plt.clf()
#plt.subplot(5, 2, 9)
#legend_1 = plt.legend(custom_lines_color, legend_names, loc='best')
#plt.gca().add_artist(legend_1)
#plt.remove(legend_1)
#remove(legned_1)
plt.savefig('test_plots/All_Sources_Histograms.pdf', dpi=300)
plt.clf()
print("Done!")



for i in range(1,len(source_names)):
        print("Plotting...")
        plt.figure(1001, figsize=(8.5,11))
        plt.suptitle('{0} and {1}'.format(source_names[0],source_names[i]), fontsize=16)

        plt.subplot(3, 2, 1)
        plotMaker.hist_maker(data_dict, bin_cos, bindistance, 'nnu_theta', source_names[0], colors[0], fontsize=8)# makelabel=False)
        plotMaker.hist_maker(data_dict, bin_cos, bindistance, 'nnu_theta', source_names[i], colors[i], fontsize=8)# makelabel=False)

        plt.subplot(3, 2, 2)
        plotMaker.hist_maker(data_dict, bin_cos, bindistance, 'theta_rec', source_names[0], colors[0], fontsize=8)# makelabel=False)
        plotMaker.hist_maker(data_dict, bin_cos, bindistance, 'theta_rec', source_names[i], colors[i], fontsize=8)# makelabel=False)

        plt.subplot(3, 2, 3)
        plotMaker.hist_maker(data_dict, bin_cos, bindistance, 'ShowerEnergy', source_names[0], colors[0], fontsize=8)# makelabel=False)
        plotMaker.hist_maker(data_dict, bin_cos, bindistance, 'ShowerEnergy', source_names[i], colors[i], fontsize=8)# makelabel=False)

        plt.subplot(3, 2, 4)
        plotMaker.hist_maker(data_dict, bin_cos, bindistance, 'weight', source_names[0], colors[0], fontsize=8)# makelabel=False)
        plotMaker.hist_maker(data_dict, bin_cos, bindistance, 'weight', source_names[i], colors[i], fontsize=8)# makelabel=False)

        plt.subplot(3, 2, 5)
        plotMaker.hist_maker(data_dict, bin_cos, bindistance, 'dist', source_names[0], colors[0], fontsize=8)# makelabel=False)
        plotMaker.hist_maker(data_dict, bin_cos, bindistance, 'dist', source_names[i], colors[i], fontsize=8)# makelabel=False)

        plt.subplot(3, 2, 6)
        plotMaker.hist_maker(data_dict, bin_cos, bindistance, 'depth', source_names[0], colors[0], fontsize=8)# makelabel=False)
        plotMaker.hist_maker(data_dict, bin_cos, bindistance, 'depth', source_names[i], colors[i], fontsize=8)# makelabel=False)

        plt.savefig('test_plots/Histograms_{0}_{1}.pdf'.format(source_names[0],source_names[i], dpi=300))
        plt.clf()

print("Done!")



#Doing it for all in a for loop
#scatter_vars = ['distance', 'depth', 'dist_0', 'rec_ang_0']
print("PDF of scatter plots, 2D Histograms, and comparison 2D Histograms")
for i in range(1,len(source_names)):
        print("Plotting...")
        plt.figure(20001, figsize=(8.5,11))
        plt.suptitle('{0} and {1}'.format(source_names[0],source_names[i]), fontsize=16)

        plt.subplot(3,2,1)
        plotMaker.scatter_maker('dist_0', 'theta_rec_0', data_dict, bin_cos, bindistance, source_names[0], colors[0], fontsize=8)
        plt.subplot(3, 2, 3)
        plotMaker.multi_hist('dist_0', 'theta_rec_0', data_dict, bin_cos, bindistance, bin_dist, source_names[0], fontsize=8)
        
        plt.subplot(3, 2, 2)
        plotMaker.scatter_maker('dist_0', 'theta_rec_0', data_dict, bin_cos, bindistance, source_names[i], colors[i], fontsize=8)
        plt.subplot(3,2,4)
        plotMaker.multi_hist('dist_0', 'theta_rec_0', data_dict, bin_cos, bindistance, bin_dist, source_names[i], fontsize=8)

        plt.subplot(3,1,3)
        plotMaker.diff_hist('dist_0', 'theta_rec_0', data_dict, bin_cos, bindistance, bin_dist, source_names, source_names[0], source_names[i], fontsize=8)
        plt.savefig('test_plots/MultiHist_{0}_{1}.pdf'.format(source_names[0],source_names[i]), dpi=300)
        plt.clf()
print("Done!") 


        
#print(range(3,len(source_names)))
#plt.subplots(4,len(source_names))
# if len(source_names) > 3 :
#         for i in range(3):
#                 print("Plotting...")
#                 print(i)
#                 plt.figure(2001, figsize=(8.5,11))
#                 plt.subplot(3, 3, i+1)
#                 scatter_maker('dist_0', 'theta_rec_0', source_names[i], fontsize=8)
#                 # scatter_maker('dist_0', 'rec_ang_0', source_names[i], fontsize=8)
#                 print(source_names[i])
#                 plt.subplot(3, 3, i+4)
#                 multi_hist('dist_0', 'theta_rec_0', source_names[i], fontsize=8)
#                 # multi_hist('dist_0', 'rec_ang_0', source_names[i], fontsize=8)
#                 # plt.subplot(3, len(source_names)-1, i+2*(len(source_names)-1)#+ 2*len(source_names))
#                 # multi_hist(scatter_vars[2], scatter_vars[3], source_names[i-1], fontsize=10)
#                 print('last plot..')        
#                 #if i < len(source_names) and len(source_names) > 1:
#                 plt.subplot(3, 3, i+7)#+ 2*len(source_names))
#                         #print(i)
#                         # diff_hist('dist_0', 'rec_ang_0', source_names[0], source_names[i], fontsize=8)
#                 diff_hist('dist_0', 'theta_rec_0', source_names[0], source_names[i], fontsize=8)
#         plt.savefig('test_plots/All_Multi_1.pdf', dpi=300)
#         plt.clf()
#         print("Done!") 

#         for i in range(3,len(source_names)):
#                 print("Plotting...")
#                 print(i)
#                 plt.figure(2001, figsize=(8.5,11))
#                 plt.subplot(3, len(source_names)-3, i+1)
#                 scatter_maker('dist_0', 'theta_rec_0', source_names[i], fontsize=8)
#                 # scatter_maker('dist_0', 'rec_ang_0', source_names[i], fontsize=8)
#                 print(source_names[i])
#                 plt.subplot(3, len(source_names)-3, i+1+len(source_names)-3)
#                 multi_hist('dist_0', 'theta_rec_0', source_names[i], fontsize=8)
#                 # multi_hist('dist_0', 'rec_ang_0', source_names[i], fontsize=8)
#                 # plt.subplot(3, len(source_names)-1, i+2*(len(source_names)-1)#+ 2*len(source_names))
#                 # multi_hist(scatter_vars[2], scatter_vars[3], source_names[i-1], fontsize=10)
#                 print('last plot..')        
#                 #if i < len(source_names) and len(source_names) > 1:
#                 # plt.subplot(3, len(source_names)-3, i+1+2*(len(source_names)-3))#+ 2*len(source_names))
#                 # print(i)
#                 # # diff_hist('dist_0', 'rec_ang_0', source_names[0], source_names[i], fontsize=8)
#                 # diff_hist('dist_0', 'theta_rec_0', source_names[0], source_names[i], fontsize=8)
#         plt.savefig('test_plots/All_Multi_2.pdf', dpi=300)
#         plt.clf()
#         print("Done!") 

        
# else:
#         for i in range(len(source_names)):
#                 print("Plotting...")
#                 plt.figure(2001, figsize=(8.5,11))
#                 plt.subplot(3, len(source_names), i+1)
#                 scatter_maker('dist_0', 'theta_rec_0', source_names[i], fontsize=8)
#                 # scatter_maker('dist_0', 'rec_ang_0', source_names[i], fontsize=8)
#                 print(source_names[i])
#                 plt.subplot(3, len(source_names), i+1+len(source_names))
#                 multi_hist('dist_0', 'theta_rec_0', source_names[i], fontsize=8)
#                 # multi_hist('dist_0', 'rec_ang_0', source_names[i], fontsize=8)
#                 # plt.subplot(3, len(source_names)-1, i+2*(len(source_names)-1)#+ 2*len(source_names))
#                 # multi_hist(scatter_vars[2], scatter_vars[3], source_names[i-1], fontsize=10)
#                 print('last plot..')        
#                 #if i < len(source_names) and len(source_names) > 1:
#                 plt.subplot(3, len(source_names), i+1+2*(len(source_names)))#+ 2*len(source_names))
#                 print(i)
#                 # diff_hist('dist_0', 'rec_ang_0', source_names[0], source_names[i], fontsize=8)
#                 diff_hist('dist_0', 'theta_rec_0', source_names[0], source_names[i], fontsize=8)
                                                
#         plt.savefig('test_plots/Testing_All_Multi.pdf', dpi=300)
#         plt.clf()
#         print("Done!") 
        
                
        
# for i in range(len(source_names)):
#         print("Plotting...")
#         print(i)
#         plt.subplot(3, len(source_names), i+1)
#         scatter_maker('dist_0', 'theta_rec_0', source_names[i], fontsize=8)
#         # scatter_maker('dist_0', 'rec_ang_0', source_names[i], fontsize=8)
#         print(source_names[i])
#         plt.subplot(3, len(source_names), i+1+len(source_names))
#         multi_hist('dist_0', 'theta_rec_0', source_names[i], fontsize=8)
#         # multi_hist('dist_0', 'rec_ang_0', source_names[i], fontsize=8)
#         # plt.subplot(3, len(source_names)-1, i+2*(len(source_names)-1)#+ 2*len(source_names))
#         # multi_hist(scatter_vars[2], scatter_vars[3], source_names[i-1], fontsize=10)
#         print('last plot..')        
#         if i < len(source_names) and len(source_names) > 1:
#                 plt.subplot(3, len(source_names), i+1+2*(len(source_names)))#+ 2*len(source_names))
#                 print(i)
#                 # diff_hist('dist_0', 'rec_ang_0', source_names[0], source_names[i], fontsize=8)
#                 diff_hist('dist_0', 'theta_rec_0', source_names[0], source_names[i], fontsize=8)
                

# plt.savefig('test_plots/Testing_All_Multi.pdf', dpi=300)
# print("Done!") 
# print(np.array(range(1,2)))
# print(np.array(range(2)))
# print(range(2))

# print(hist_dict)
# print(range(1,len(source_names)))
# print(range(0,len(source_names)))
# print(range(len(source_names)))
# print(source_names[1])
# print(range(2))
# print(len(range(2)))

# print(custom_legend)
# print(custom_legend[0])
# IceVolume = (4.0/3.0)*np.pi*(3000**3)*(10**-9)
# IceVolume = 8.4823 * np.power(10,10)#e+10

#######################################
###General Info
#######################################
# for i in range(len(source_names)):
#         print('#'*28)
#         print('\033[1;37m{0}\033[0;0m'.format(source_names[i]))
#         print('#'*28)
#         print('\033[4;37mEvents\033[0;0m')
#         print('Triggered: \033[1;31m{0}\033[0;0m'.format(len(data_dict[source_names[i]]['trigg'])))
#         print('Usable: \033[1;31m{0}\033[0;0m'.format(len(data_dict[source_names[i]]['weight'])))
#         print('Weighted: \033[1;31m{0}\033[0;0m'.format(np.sum(data_dict[source_names[i]]['weight'])))
#         print('Effective Volume: \033[1;31m{0}\033[0;0m'.format(IceVolume * 4.0 * np.pi * (
#                                              np.sum(data_dict[source_names[i]]['weight'])/totalEvents)))
#         print(IceVolume)
#         #print(source_dict.items())
#         print(totalEvents)
#         print('#'*50)
#         print('\n')

IceVolume = 8.4823 * 10#np.power(10,10)#e+10
for i in range(len(source_names)):
        print('#'*28)
        print('\033[1;37m{0}\033[0;0m'.format(source_names[i]))
        print('#'*28)
        # print('\033[4;37mEvents\033[0;0m')
        print('Total Events: \033[1;31m{0}\033[0;0m'.format(data_dict[source_names[i]]['Total_Events']))
        print('Triggered: \033[1;31m{0}\033[0;0m'.format(len(data_dict[source_names[i]]['trigg'])))
        print('Usable: \033[1;31m{0}\033[0;0m'.format(len(data_dict[source_names[i]]['weight'])))
        print('Weighted: \033[1;31m{0}\033[0;0m'.format(np.sum(data_dict[source_names[i]]['weight'])))
        print('Effective Volume: \033[1;31m{0}\033[0;0m'.format(IceVolume * 4.0 * np.pi * (
                np.sum(data_dict[source_names[i]]['weight'])/data_dict[source_names[i]]['Total_Events'])))
        # print('Test Effective Volume: \033[1;31m{0}\033[0;0m'.format(IceVolume * 4.0 * np.pi * (
        #         np.sum(data_dict[source_names[i]]['Total_Weights'])/data_dict[source_names[i]]['Total_Events'])))

        print('#'*50)
        print('\n')

#exit()




stop = timeit.default_timer()
print('Time: \033[1;31m{0}\033[0;0m'.format(stop - start))
exit()
'''
I think this is the equation AraSim uses:
Veff_test = IceVolume * 4. * PI * Total_Weight / (double)(settings1->NNU);
The IceVolume would be 4/3pi*R^3, and I think R is 3000 m, and then NNU for each root file should be 30000 (so 3*10^6 for each individual)
v'''