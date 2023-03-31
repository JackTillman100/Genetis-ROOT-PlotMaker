import matplotlib.pyplot as plt 
from matplotlib.lines import Line2D
import numpy as np

#Defining the plotting functions used!

#Histogram Plotting Function
def hist_maker(data_dict, bin_cos, bindistance, hist_var, source, color, fontsize=12, makelabel=False):
        #print(hist_var)
        #for i in range(len(source_names)):
                #print("Plotting...")
                #print(source_names[i])
                #print("...")
        try:    
                if 'ang' in hist_var or 'theta' in hist_var or 'phi' in hist_var:
                        plt.hist(np.cos(data_dict[source]['{0}_0'.format(hist_var)]), 
                                 weights=data_dict[source]['weight'],bins=bin_cos, density=False, 
                                 histtype='step', color=color, ls='-', label=str(source)+' direct')
                        plt.hist(np.cos(data_dict[source]['{0}_1'.format(hist_var)]), 
                                 weights=data_dict[source]['weight'], bins=bin_cos, density=False, 
                                 histtype='step', color=color, ls='--', label=str(source)+' refracted')
                        plt.xlabel("Cos({0})".format(hist_var), fontsize=fontsize)
                        
                else:
                        plt.hist(data_dict[source]['{0}_0'.format(hist_var)], 
                                 weights=data_dict[source]['weight'],bins=bindistance, density=False, 
                                 histtype='step', color=color, ls='-', label=str(source)+' direct')
                        plt.hist(data_dict[source]['{0}_1'.format(hist_var)], 
                                 weights=data_dict[source]['weight'], bins=bindistance, density=False, 
                                 histtype='step', color=color, ls='--', label=str(source)+' refracted')
                        plt.xlabel("{0}".format(hist_var), fontsize=fontsize)
                        
                plt.ylabel("Events", fontsize=fontsize)
                plt.grid(linestyle='--')
                plt.tight_layout()
                if makelabel is True:
                        legend = plt.legend(custom_lines_color, legend_names, loc='best')
                        plt.gca().add_artist(legend)
                                #print(legend)
                        # else:
                        #         continue
                        #plt.tight_layout()
                    
                        #plt.savefig('test_plots/Hist_{0}_0_{0}_1_.png'.format(hist_var),dpi=300)
  
        except KeyError:
                
                if 'ang' in hist_var or 'theta' in hist_var or 'phi' in hist_var:
                        plt.hist(np.cos(data_dict[source]['{0}'.format(hist_var)]), 
                                 weights=data_dict[source]['weight'], bins=bin_cos, density=False, 
                                 histtype='step', color=color, ls='-', label=str(source))
                        plt.xlabel("Cos({0})".format(hist_var), fontsize=fontsize)
                        #legend = plt.legend(custom_legend, source_names, loc='upper left')
                        
                elif 'weight' in hist_var:
                        plt.hist(data_dict[source]['{0}'.format(hist_var)], 
                                 log=True, density=False, 
                                 histtype='step', color=color, ls='-', label=str(source))#, bins =40)
                        plt.xlabel("{0}".format(hist_var), fontsize=fontsize)
                        #legend = plt.legend(custom_legend, source_names, loc='upper center')
                        
                elif 'ShowerEnergy' in hist_var:
                        plt.hist(data_dict[source]['{0}'.format(hist_var)],
                                 density=False, weights=data_dict[source]['weight'],
                                 histtype='step', log=True, 
                                 color=color, ls='-', label=str(source))#, bins= )
                        plt.xlabel("{0}".format(hist_var), fontsize=fontsize)
                        #legend = plt.legend(custom_legend, source_names, loc='upper left')
                        
                elif 'depth' in hist_var or 'distance' in hist_var:
                        plt.hist(data_dict[source]['{0}'.format(hist_var)],
                                 density=False, weights=data_dict[source]['weight'],
                                 histtype='step', 
                                 color=color, ls='-', label=str(source), bins= 40)
                        plt.xlabel("{0}".format(hist_var), fontsize=fontsize)
                        #legend = plt.legend(custom_legend, source_names, loc='upper left')
                        
                else:
                        plt.hist(data_dict[source]['{0}'.format(hist_var)], 
                                 weights=data_dict[source]['weight'],density=False, 
                                 histtype='step', color=color, ls='-', label=str(source))#, bins= )
                        plt.xlabel("{0}".format(hist_var), fontsize=fontsize)
                        #legend = plt.legend(custom_legend, source_names, loc='best')
                        
                plt.ylabel("Events", fontsize=fontsize)
                plt.grid(linestyle='--')
                plt.tight_layout()
                #print(legend)
                if makelabel is True:
                        legend = plt.legend(custom_lines_color, legend_names, loc='best')
                        plt.gca().add_artist(legend)
                
                # if makelabel is True:
                #         plt.gca().add_artist(legend)
                # else:
                #         continue
                # #plt.tight_layout() 
                # print(makelabel)
                
                #plt.savefig('test_plots/Hist_{0}.png'.format(hist_var),dpi=300)
 
#Scatterplot Plotting Function
def scatter_maker(var1, var2, data_dict, bin_cos, bindistance, source, color, fontsize=12):
        #print("Plotting...")
        if 'ang' in var2 or 'theta' in var2 or 'phi' in var2:
                plt.scatter(data_dict[source]['{0}'.format(var1)],
                            np.cos(data_dict[source]['{0}'.format(var2)]), 
                            s=1.0, alpha=0.25, color=color, label=str(source))
                            
                plt.xlabel("{0}".format(var1), fontsize=fontsize)
                plt.ylabel("Cos({0})".format(var2), fontsize=fontsize)
                
        else:
                        
                plt.scatter(data_dict[source]['{0}'.format(var1)], 
                            data_dict[source]['{0}'.format(var2)], 
                            s=1.0, alpha=0.25, color=color, label=str(source))
         
                plt.xlabel("{0}".format(var1), fontsize=fontsize)
                plt.ylabel("{0}".format(var2), fontsize=fontsize)
        
        plt.title("{0}".format(source), fontsize=fontsize)
        #plt.legend()
        plt.grid(linestyle='--')
        plt.tight_layout()
        # plt.savefig('test_plots/Scatter_{2}_{0}_{1}_.png'.format(var1, var2, source), dpi=300)
        # plt.clf()

#Multi-Histogram Plotting Function
def multi_hist(var1, var2, data_dict, bin_cos, bindistance, bin_dist, source, fontsize=12):
        #print("Plotting...")
        hist_dict = {}
        hist = []
        hist = plt.hist2d(data_dict[source]['{0}'.format(var1)], 
                          np.cos(data_dict[source]['{0}'.format(var2)]), 
                          bins=(bin_dist,bin_cos), weights=data_dict[source]['weight'])
        hist_dict[source] = hist
        
        plt.colorbar()#cax=cax)
        plt.title("{0}".format(source), fontsize=fontsize)
        plt.xlabel("{0}".format(var1), fontsize=fontsize)
        plt.ylabel("{0}".format(var2), fontsize=fontsize)
        #plt.gca().set_aspect("equal")        
        #plt.legend()
        #plt.grid(linestyle='--')
        plt.tight_layout()
        #plt.savefig('test_plots/2DHist_{2}_{0}_{1}_.png'.format(var1, var2, source), dpi=300)
        #plt.clf()

#Difference Histogram Plotting Function (Plots a histogram showing the difference
# between 2 data sets)
def diff_hist(var1, var2, data_dict, bin_cos, bindistance, bin_dist, source_names, source1, source2, fontsize=12):
        #print("Plotting...")
        hist_dict = {}

        if len(source_names) > 1:
                diff = hist_dict[source2][0] - hist_dict[source1][0]
                #plt.colormesh(bin_dist, bin_cos, diff, cmap='bwr')
                plt.pcolormesh(bin_dist, bin_cos, diff.T, cmap='bwr')
                plt.colorbar()
                plt.xlabel("{0}".format(var1), fontsize=fontsize)
                plt.ylabel("{0}".format(var2), fontsize=fontsize)
                plt.title("{0} vs {1}".format(source1, source2), fontsize=fontsize)
                #print(diff)

                #plt.legend()
                #plt.grid(linestyle='--')
                plt.tight_layout()
                #plt.savefig('test_plots/2DHistDiff_{2}_{3}_{0}_{1}_.png'.format(var1, var2, source1, source2), dpi=300)
                #plt.clf()
        else: 
                print("We can't make a 2D histogram showing a difference, if we only have one dataset...")
