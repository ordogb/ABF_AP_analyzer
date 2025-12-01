

import numpy as np
import pyabf
from scipy import signal
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import os


class OverviewPlot:
    def __init__(self, master, options):
        self.master = master
        self.params = options
        self.fig, self.ax = plt.subplots()
        self.ax2 = self.ax.twinx()
        self.ax2.set_yticks([])
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.canvas, master)
        self.toolbar.update()
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.canvas.get_tk_widget().config(width = 800, height = 300)
        self.canvas.get_tk_widget().pack(fill='both', expand = True)

    
    def draw_plot(self, AP_data, abf, *args, **kwargs):
        AP_objects = AP_data.data
        self.ax.clear()
        self.ax2.clear()
        # self.ax.set_ylabel('mV', fontsize=7)
        self.ax.set_xlabel('Sweep no.', fontsize=7)
        self.ax.tick_params(axis='both', which='major', labelsize=7)
        self.ax2.tick_params(axis='both', which='major', labelsize=7)
        # self.ax2.set_ylabel('ms')
        
        APD90s = []
        AP_peaks = []
        Vrests = []
        for sw in AP_objects.keys():
            APD90s.append(AP_objects[sw].APDs[90])
            AP_peaks.append(AP_objects[sw].AP_peak)
            Vrests.append(AP_objects[sw].Vrest)
        self.ax.set_ylim(np.min(Vrests)-10,np.max(AP_peaks)+10)
        self.ax2.set_ylim(0,np.max(APD90s)+10)
        # self.ax2.set_yticks([])
        abfname = AP_data.abfname
        output_folder = AP_data.output_folder
        if self.params["Vrest"].get() == 1:
            self.ax.plot(AP_objects.keys(), [AP_objects[sw].Vrest for sw in AP_objects.keys()], label='Vrest', ls='dashed', color='blue', alpha=0.3)
        if self.params["AP peak"].get() == 1:
            self.ax.plot(AP_objects.keys(), [AP_objects[sw].AP_peak for sw in AP_objects.keys()], label='AP peak', ls='dashed', color='red', alpha=0.3)
        colors = ["blue","orange","green","red","purple","brown","pink","gray"]
        
        for repol_level, color in zip(AP_data.repol_levels, colors):
            if self.params["APD{}".format(repol_level)].get() == 1:
                self.ax2.plot(AP_objects.keys(), [AP_objects[sw].APDs[repol_level] for sw in AP_objects.keys()], label='APD{}'.format(repol_level), color=color, ls='dotted')
        
        ymin, ymax = self.ax.get_ylim()
        self.ax.vlines(AP_data.avg_left, ymin, ymax, color = 'red', alpha=0.3, ls='dashed')
        self.ax.vlines(AP_data.avg_right, ymin, ymax, color = 'red', alpha=0.3, ls='dashed')
        self.ax.fill_between([x for x in range(AP_data.avg_left, AP_data.avg_right+1)], ymin, ymax, color='red', alpha=0.3)
        self.ax.legend(loc="upper left", fontsize=7)
        self.ax2.legend(loc="upper right", fontsize=7)
        self.fig.tight_layout()
        self.canvas.draw()
        
        

class ApPlot:
    def __init__(self, master):
        self.master = master
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.canvas, master)
        self.toolbar.update()
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.sweep_number = None
    
    def plot_sweeps(self, AP_data, abf, *args, **kwargs):
        AP_objects = AP_data.data
        abfname = AP_data.abfname
        plots_folder = AP_data.plots_folder
        
        self.ax.clear()
        if not self.sweep_number:
            sw = 0
        else: 
            sw = self.sweep_number
            
        self.ax.plot(AP_objects[sw].Xdata, AP_objects[sw].Ydata, label = "sweep")
        self.ax.set_title("{}: sw {}".format(abfname, sw))
        
        self.ax.set_xlabel("{}".format(abf.sweepUnitsX))
        self.ax.set_ylabel("{}".format(abf.sweepUnitsY))
        
        ymin, ymax = self.ax.get_ylim()
        xmin, xmax = self.ax.get_xlim()
        
        if "Vrest" in kwargs and kwargs["Vrest"] == True:
           
            Vrest_lefti = AP_objects[sw].Vrest_lefti
            Vrest_righti = AP_objects[sw].Vrest_righti
            self.ax.fill_between(AP_objects[sw].Xdata[Vrest_lefti:Vrest_righti], ymin, ymax, color = "blue", alpha=0.3)
            self.ax.hlines(AP_objects[sw].Vrest, xmin, xmax, color = "blue", ls="dashed", alpha = 0.3, label = "Vrest: {} mV".format(round(AP_objects[self.sweep_number].Vrest)))

        if "all_peaks" in kwargs and kwargs["all_peaks"] == True:
            for i in AP_objects[sw].peak_idxs:
                self.ax.vlines(AP_objects[sw].Xdata[i], ymin, ymax, color='green', ls='dashed', alpha = 0.3, label="signal peaks")
     
        if "AP_peak" in kwargs and kwargs["AP_peak"] == True:
            AP_peak_idx = AP_objects[sw].AP_peak_idx
            self.ax.vlines(AP_objects[sw].Xdata[AP_peak_idx], ymin, ymax, color='red', ls='dashed', alpha = 0.3)
            self.ax.hlines(AP_objects[sw].AP_peak, xmin, xmax, color ="red", ls="dashed", alpha = 0.3, label = "AP peak: {} mV".format(round(AP_objects[self.sweep_number].AP_peak)))
    
        if "dVdtmax" in kwargs and kwargs["dVdtmax"] == True:
            self.ax.vlines(AP_objects[sw].Xdata[AP_objects[sw].dVdtmax_idx], ymin, ymax, ls='dotted', color = 'magenta', label = 'dVdtmax {} V/sec'.format(round(AP_objects[self.sweep_number].dVdtmax)))
        
        if "APD" in kwargs and kwargs["APD"] == True:
            colors = ["blue","orange","green","red","purple","brown","pink","gray"]
            for i, repol_level in enumerate(AP_objects[sw].APDidxs.keys()):
                self.ax.vlines(AP_objects[sw].Xdata[AP_objects[sw].APDidxs[repol_level]], ymin, ymax, ls='dotted', color = colors[i], label = "APD{}: {} ms".format(repol_level, round(AP_objects[self.sweep_number].APDs[repol_level])))
        self.ax.legend(loc="upper right")        
        self.canvas.draw()
        self.fig.tight_layout()
        
        if "savefig" in kwargs and kwargs["savefig"] == True:
            self.fig.savefig("{}{}_sw{}.png".format(plots_folder, abfname, sw))
    


class ApData:
    repol_levels = [x for x in range(20,100,10)]

    def __init__(self):
        self.data = {} #to hold ApSweep instances
        self.output_folder = None
        self.fullpath = None
        self.abfname = None
        self.plots_folder = None
        self.csvtype = None
        self.avg_left = None #first sweep which taken into account for average data
        self.avg_right = None #last sweep taken into account for average data
    
    def make_abf(self):
        self.abf = pyabf.ABF(self.fullpath)
    
    def create_output(self):
        self.output = {}
        self.output['ABF'] = self.abfname
        self.output['First sweep included'] = self.avg_left
        self.output['Last sweep included'] = self.avg_right
        self.output['Sampling rate'] = self.data[0].sr
        self.output['BCL (sec)'] = self.data[0].bcl

        Vrests = []
        APpeaks = []
        dVdtmaxs = []
        APDs = {repol_level: [] for repol_level in self.repol_levels}
       
            
        for sw in self.data.keys():
            Vrests.append(self.data[sw].Vrest)                
            APpeaks.append(self.data[sw].AP_peak)                
            dVdtmaxs.append(self.data[sw].dVdtmax)
            for repol_level in self.repol_levels:
                APDs[repol_level].append(self.data[sw].APDs[repol_level])  
        
        self.output['avg Vrest (mV)'] = np.average(Vrests)    
        self.output['avg Vrest SD (mV)'] = np.std(Vrests)    
        self.output['avg AP peak (mV)'] = np.average(APpeaks)    
        self.output['avg AP peak SD (mV)'] = np.std(APpeaks)    
        self.output['avg dVdtmax (V/sec)'] = np.average(dVdtmaxs)    
        self.output['avg dVdtmax SD'] = np.std(dVdtmaxs)
        
        for repol_level in self.repol_levels:
            self.output['avg APD{}'.format(repol_level)] = np.average(APDs[repol_level])
            APD_diff_list = [b - a for a,b in zip(APDs[repol_level], APDs[repol_level][1:])]
            self.output['APD{} STV'.format(repol_level)] = abs(np.sum(APD_diff_list)) / ((len(APD_diff_list)-1) * np.sqrt(2))
        
               
        output = pd.Series(self.output, index=self.output.keys())
        output_filename = 'APD_averages2.csv'
        print("{}/{}".format(self.output_folder, output_filename))
        
        #save analysis params and results
        
        if os.path.exists("{}/{}".format(self.output_folder, output_filename)):
            old = pd.read_csv("{}/{}".format(self.output_folder, output_filename), index_col = 0)
            print(old.columns)
            existing_column = [col for col in old.columns if old[col].str.contains(self.abfname).any()]
            print(existing_column)
            
            
            if len(existing_column) == 0:
                new = [old, output]
                df = pd.concat(new, axis=1)
                df.columns = df.loc['ABF']
                df.to_csv("{}/{}".format(self.output_folder,output_filename))
            else:
                old = old.drop(existing_column, axis=1)
                new = [old, output]
                df = pd.concat(new, axis=1)
                df.columns = df.loc['ABF']
                df.to_csv("{}/{}".format(self.output_folder, output_filename))
        else:
            output.to_csv("{}/{}".format(self.output_folder,output_filename))
        
        
        
        
class ApSweep:
    def __init__(self, abfname, sw, Xdata, Ydata):
        self.abfname = abfname
        self.sw = sw #sweep number
        self.Xdata = Xdata
        self.Ydata = Ydata
        
        #defaults
        self.Vrest_lefti = 0
        self.Vrest_righti = 30
        self.prominence1 = 80
        self.prominence2 = 20000
        self.distance = 50
        self.peak_idxs_idx = 0
        
        self.analyse()        
    
    def analyse(self):
        self.calc_sr()  #self.sr, sampling rate in Hz
        self.calc_bcl() #self.bcl, basic cycle length in sec
        self.calc_Vrest(self.Vrest_lefti, self.Vrest_righti) # -> Vrests
        self.calc_peaks() # -> peak_idxs, peak_count
        self.calc_AP_peak_idx() # -> AP_peak_idx
        self.calc_AP_peak() # -> AP_peak
        self.calc_AP_amplitude() # -> AP_amplitude
        self.calc_dVdtmax() # -> dVdtmax in V/sec, dVdtmax_idx
        self.calc_APD_idxs() # -> APD20_idx, APD30_idx ....
        self.calc_APDs() # -> APD20s, APD30s ....
    
    def APsum(self):
        data = [
            self.abfname,
            self.sw,
            self.sr,
            self.bcl,
            self.Vrest_lefti,
            self.Vrest_righti,
            self.prominence1,
            self.prominence2,
            self.distance,
            self.peak_idxs_idx,
            round(self.Vrest,2),
            round(self.AP_peak,2),
            round(self.dVdtmax, 2),
            ]
        for key in self.APDs.keys():
            data.append(round(self.APDs[key],2))
        index = [
            "ABF",
            "Sweep",
            "Sampling rate (Hz)",
            "BCL (sec)",
            "Verst_lefti",
            "Verst_righti",
            "prominence1",
            "prominence2",
            "distance",
            "peak_idxs_idx",
            "Vrest (mV)",
            "AP peak (mV)",
            "dVdtmax (V/sec)"
            ]
        for key in self.APDs.keys():
            index.append("APD{}".format(key))
        ser = pd.Series(data=data, index=index)
        return ser

    
    def calc_APD_idxs(self):
        APDidxs = {}
        
        for repol_level in ApData.repol_levels:
            Vapd = self.AP_peak - self.AP_amplitude * (repol_level/100)
            
            apd_idx_mask = self.AP_peak_idx + np.argwhere(self.Ydata[self.AP_peak_idx:] <= Vapd)
            APD_idx = int(apd_idx_mask[0][0])
            APDidxs[repol_level] = APD_idx
        
        self.APDidxs = APDidxs
        
    def calc_APDs(self):
        APDs = {}
        for repol_level in self.APDidxs.keys():
            apd = (self.Xdata[self.APDidxs[repol_level] - self.dVdtmax_idx]) * 1000 # in ms
            APDs[repol_level] = apd 
        self.APDs = APDs
       
    
    def calc_dVdtmax(self):
        ydata = np.asarray(self.Ydata)
        Vrest_array = np.empty(ydata.shape)
        Vrest_array.fill(self.Vrest)

        AP_mask = np.where(ydata > self.Vrest , ydata, Vrest_array)
        # slope = np.diff(AP_mask[AP_peak_idx-slope_range_left:AP_peak_idx]) #from previously used script
        slope = np.diff(AP_mask[:self.AP_peak_idx]) # current version

        # fig,ax = plt.subplots()
        # ax.plot(self.Ydata)
        # ax.plot(AP_mask)
        # ymin, ymax = ax.get_ylim()
        # xmin, xmax = ax.get_xlim()
        # ax.vlines(self.AP_peak_idx, ymin, ymax)
        # ax.plot(range(1, self.AP_peak_idx), slope)
        # exit()
        
        # dVdtmax_idx = np.argmax(slope) + AP_peak_idx - slope_range_left # from previously used script
        self.dVdtmax_idx = np.argmax(slope) #current version
        self.dVdtmax = np.max(slope) * self.sr / 1000 # in V/sec
    
    def calc_AP_amplitude(self):
        self.AP_amplitude = self.AP_peak - self.Vrest
    
    def calc_AP_peak_idx(self):
        self.AP_peak_idx = self.peak_idxs[self.peak_idxs_idx]
            
    def calc_AP_peak(self): # the peak in mV, depending on which peak idx was selected
        self.AP_peak = self.Ydata[self.AP_peak_idx]
       
    
    def calc_peaks(self):
        self.peak_idxs, _ = signal.find_peaks(self.Ydata, prominence = (self.prominence1, self.prominence2), distance=self.distance)
        self.peak_count = len(self.peak_idxs)
        
    def calc_Vrest(self, Vrest_lefti, Vrest_righti):
        self.Vrest = np.average(self.Ydata[self.Vrest_lefti:self.Vrest_righti])
    
    def calc_sr(self):
        sr = 1/(self.Xdata[1]-self.Xdata[0]) #in Hz
        self.sr = sr
    
    def calc_bcl(self):
        self.bcl = len(self.Xdata)/self.sr
            