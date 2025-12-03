# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 11:06:16 2025

@author: oerdoeg
"""


__author__ = "Balazs Ordog"
__version__ = "0.1.0"
__license__ = "Unibe"



import abfAP_GUI_utils as utils
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import pandas as pd
import os



def browse_file():
    fullpath = askopenfilename(filetypes=(("abf file", "*.abf"), ("csv file", "*.csv"),("All files", "*.*"),))
    abfname = fullpath.split('/')[-1]
    AP_data.fullpath = fullpath
    AP_data.abfname = abfname
    AP_plot.sweep_number = 0
    
    if ".abf" in AP_data.fullpath:
        AP_data.make_abf()
        abf = AP_data.abf
        label1["text"] = "Working on {}\nwhich has {} sweeps".format(AP_data.fullpath, AP_data.abf.sweepCount)
        label1["font"] = ('Arial 10')
        create_instances()
        default_params()
        analyze_all_sweeps()
        AP_plot.plot_sweeps(AP_data, abf, Vrest=True, all_peaks=True, AP_peak=True, dVdtmax=True, APD=True)
        set_to_sweep_scale()
        default_average_interval()
        Overview_Plot.draw_plot(AP_data, AP_data.abf)
    else:
        label1["text"] = "{} is not a valid .abf file".format(fullpath)
        label1["font"] = ('Arial 10')
    
def create_instances():
    abf = AP_data.abf
    abfname = AP_data.abfname
    
    AP_objects = {}
    for i in range(0, abf.sweepCount):
        abf.setSweep(sweepNumber=i,channel=0)
        Xdata = abf.sweepX.tolist()
        Ydata = abf.sweepY.tolist()
        APsweep = utils.ApSweep(abfname, i, Xdata, Ydata)
        AP_objects[i] = APsweep
    AP_data.data = AP_objects
    
    # if ".csv" in fullpath:
    #     AP_data.csvtype = True
    #     df = pd.read_csv(fullpath, header = None, delimiter = ';')
    #     print(df.head())
    #     print(df.columns)
    #     print(len(df.columns))
    #     label1["text"] = "Working on {}\nwhich has {} sweeps".format(fullpath, abf.sweepCount)
    #     label1["font"] = ('Arial 10')
    #     for i in range(0, abf.sweepCount):
    #         abf.setSweep(sweepNumber=i,channel=0)
    #         Xdata = abf.sweepX.tolist()
    #         Ydata = abf.sweepY.tolist()
    #         APsweep = utils.AP_sweep(abfname, i, Xdata, Ydata)
    #         AP_objects[i] = APsweep
        


def analyze_all_sweeps():
    for key in AP_data.data.keys():
        AP_data.data[key].update_sweep()
    


def next_file():
    dirpath = os.path.dirname(AP_data.fullpath)
    file_list = os.listdir(dirpath)
    current_index = file_list.index(AP_data.abfname)
    AP_data.abfname = file_list[current_index+1]
    AP_data.fullpath = "{}/{}".format(dirpath, AP_data.abfname)
    AP_plot.sweep_number = 0
    
    if ".abf" in AP_data.fullpath:
        AP_data.make_abf()
        abf = AP_data.abf
        label1["text"] = "Working on {}\nwhich has {} sweeps".format(AP_data.fullpath, AP_data.abf.sweepCount)
        label1["font"] = ('Arial 10')
        create_instances()
        keep_previous_params()
        analyze_all_sweeps()
        set_to_sweep_scale()
        AP_plot.plot_sweeps(AP_data, abf, Vrest=True, all_peaks=True, AP_peak=True, dVdtmax=True, APD=True)
        default_average_interval()
        Overview_Plot.draw_plot(AP_data, AP_data.abf)
    else:
        label1["text"] = "{} is not a valid .abf file".format(AP_data.fullpath)
        label1["font"] = ('Arial 10')
    

def previous_file():    
   dirpath = os.path.dirname(AP_data.fullpath)
   file_list = os.listdir(dirpath)
   current_index = file_list.index(AP_data.abfname)
   AP_data.abfname = file_list[current_index-1]
   AP_data.fullpath = "{}/{}".format(dirpath, AP_data.abfname)
   AP_plot.sweep_number = 0
   
   
   if ".abf" in AP_data.fullpath:
       AP_data.make_abf()
       abf = AP_data.abf
       label1["text"] = "Working on {}\nwhich has {} sweeps".format(AP_data.fullpath, AP_data.abf.sweepCount)
       label1["font"] = ('Arial 10')
       create_instances()
       keep_previous_params()
       analyze_all_sweeps()
       set_to_sweep_scale()
       AP_plot.plot_sweeps(AP_data, abf, Vrest=True, all_peaks=True, AP_peak=True, dVdtmax=True, APD=True)
       default_average_interval()
       Overview_Plot.draw_plot(AP_data, AP_data.abf)
   else:
       label1["text"] = "{} is not a valid .abf file".format(AP_data.fullpath)
       label1["font"] = ('Arial 10')


def default_params():
    for sw in AP_data.data.keys():
        AP_data.data[sw].Vrest_lefti = 0
        AP_data.data[sw].Vrest_righti = 30
        AP_data.data[sw].prominence1 = 80
        AP_data.data[sw].prominence2 = 20000
        AP_data.data[sw].distance = 50
        AP_data.data[sw].peak_idxs_idx = 0
    
    vrest_left_entry.delete(0, 'end')
    vrest_right_entry.delete(0, 'end')
    prominence1_entry.delete(0, 'end')
    prominence2_entry.delete(0, 'end')
    distance_entry.delete(0, 'end')
    peak_idx_entry.delete(0, 'end')

    vrest_left_entry.insert(0,AP_data.data[AP_plot.sweep_number].Vrest_lefti)
    vrest_right_entry.insert(0,AP_data.data[AP_plot.sweep_number].Vrest_righti)
    prominence1_entry.insert(0,AP_data.data[AP_plot.sweep_number].prominence1)
    prominence2_entry.insert(0,AP_data.data[AP_plot.sweep_number].prominence2)
    distance_entry.insert(0,AP_data.data[AP_plot.sweep_number].distance)
    peak_idx_entry.insert(0,AP_data.data[AP_plot.sweep_number].peak_idxs_idx)
    vrest_left_scale.config(to=len(AP_data.data[0].Xdata))
    vrest_right_scale.config(to=len(AP_data.data[0].Xdata))
    vrest_left_scale.set(AP_data.data[AP_plot.sweep_number].Vrest_lefti)
    vrest_right_scale.set(AP_data.data[AP_plot.sweep_number].Vrest_righti)

def keep_previous_params():
    vrest_lefti = int(vrest_left_entry.get())
    vrest_righti = int(vrest_right_entry.get())
    prominence1 = int(prominence1_entry.get())
    prominence2 = int(prominence2_entry.get())
    distance = int(distance_entry.get())
    peak_idxs_idx = int(peak_idx_entry.get())
    
    for sw in AP_data.data.keys():
        AP_data.data[sw].Vrest_lefti = vrest_lefti
        AP_data.data[sw].Vrest_righti = vrest_righti
        AP_data.data[sw].prominence1 = prominence1
        AP_data.data[sw].prominence2 = prominence2
        AP_data.data[sw].distance = distance
        AP_data.data[sw].peak_idxs_idx = peak_idxs_idx

def current_params():
    vrest_left_entry.delete(0, 'end')
    vrest_right_entry.delete(0, 'end')
    prominence1_entry.delete(0, 'end')
    prominence2_entry.delete(0, 'end')
    distance_entry.delete(0, 'end')
    peak_idx_entry.delete(0, 'end')

    vrest_left_entry.insert(0,AP_data.data[AP_plot.sweep_number].Vrest_lefti)
    vrest_right_entry.insert(0,AP_data.data[AP_plot.sweep_number].Vrest_righti)
    prominence1_entry.insert(0,AP_data.data[AP_plot.sweep_number].prominence1)
    prominence2_entry.insert(0,AP_data.data[AP_plot.sweep_number].prominence2)
    distance_entry.insert(0,AP_data.data[AP_plot.sweep_number].distance)
    peak_idx_entry.insert(0,AP_data.data[AP_plot.sweep_number].peak_idxs_idx)
    
    if AP_data.data[AP_plot.sweep_number].peak_count > 1:
        peaks_label["text"] = "{} peaks are detected in current sweep".format(AP_data.data[AP_plot.sweep_number].peak_count)
    else:
        peaks_label["text"] = "{} peak is detected in current sweep".format(AP_data.data[AP_plot.sweep_number].peak_count)

def update_vresti_from_scale(event):
    abf = AP_data.abf
    sw = AP_plot.sweep_number
    Vrest_lefti = int(vrest_left_scale.get())
    Vrest_righti = int(vrest_right_scale.get())
    AP_data.data[AP_plot.sweep_number].Vrest_lefti = Vrest_lefti
    AP_data.data[AP_plot.sweep_number].Vrest_righti = Vrest_righti
    vrest_left_entry.delete(0, 'end')
    vrest_right_entry.delete(0, 'end')
    vrest_left_entry.insert(0,AP_data.data[AP_plot.sweep_number].Vrest_lefti)
    vrest_right_entry.insert(0,AP_data.data[AP_plot.sweep_number].Vrest_righti)
    
    AP_data.data[sw].update_sweep()
    
    AP_plot.plot_sweeps(AP_data, abf, Vrest=True, all_peaks=True, AP_peak=True, dVdtmax=True, APD=True)

    if AP_data.data[sw].peak_count > 1:
        peaks_label["text"] = "{} peaks are detected in current sweep".format(AP_data.data[sw].peak_count)
    else:
        peaks_label["text"] = "{} peak is detected in current sweep".format(AP_data.data[sw].peak_count)

    Overview_Plot.draw_plot(AP_data, abf)   

def update_params(event):
    abf = AP_data.abf
    sw = AP_plot.sweep_number
    vrest_lefti = int(vrest_left_entry.get())
    vrest_righti = int(vrest_right_entry.get())
    prominence1 = int(prominence1_entry.get())
    prominence2 = int(prominence2_entry.get())
    distance = int(distance_entry.get())
    peak_idxs_idx = int(peak_idx_entry.get())
    
    
    AP_data.data[sw].Vrest_lefti=vrest_lefti    
    AP_data.data[sw].Vrest_righti=vrest_righti    
    AP_data.data[sw].prominence1=prominence1
    AP_data.data[sw].prominence2=prominence2
    AP_data.data[sw].distance=distance
    AP_data.data[sw].peak_idxs_idx=peak_idxs_idx
    
    AP_data.data[sw].update_sweep()
    
    AP_plot.plot_sweeps(AP_data, abf, Vrest=True, all_peaks=True, AP_peak=True, dVdtmax=True, APD=True)

    if AP_data.data[sw].peak_count > 1:
        peaks_label["text"] = "{} peaks are detected in current sweep".format(AP_data.data[sw].peak_count)
    else:
        peaks_label["text"] = "{} peak is detected in current sweep".format(AP_data.data[sw].peak_count)

    Overview_Plot.draw_plot(AP_data, abf)   
    
    
def browse_directory():
    output_folder = askdirectory()
    AP_data.output_folder = output_folder
    
   
def save_sweep_by_sweep_results():
    output = {}
    for sw in AP_data.data.keys():
       output["sw{}".format(sw)] =  AP_data.data[sw].APsum()
    df = pd.DataFrame(output)
    df = df.T
    df.to_csv('{}/{}_analysis_sum_test.csv'.format(AP_data.output_folder, AP_data.abfname))
    
def save_figs():
    plots_folder = AP_data.output_folder +"/" +AP_data.abfname+"_individual_APs/"
    if not os.path.isdir(plots_folder):
        os.mkdir(plots_folder)
    AP_data.plots_folder = plots_folder
    
    path_components = output_folder.split('/')
    if len(path_components) > 2:
            output_label['text'] = 'Saving output in .../{}'.format('/'.join(path_components[-3:]))
    else:
            output_label['text'] = 'Saving output in {}'.format(output_folder)
    
    for key in AP_data.data.keys():
        AP_plot.sweep_number = key
        AP_plot.plot_sweeps(AP_data, AP_data.abf, Vrest=True, all_peaks=True, AP_peak=True, dVdtmax=True, APD=True, savefig = True)

def set_to_sweep_scale():
    abf = AP_data.abf
    sweep_scale.config(to=abf.sweepNumber)

def update_sweep_from_sweep_scale(event):
    abf = AP_data.abf
    sweep_number = sweep_scale.get()
    AP_plot.sweep_number = sweep_number
    AP_plot.plot_sweeps(AP_data, abf, Vrest=True, all_peaks=True, AP_peak=True, dVdtmax=True, APD=True)
    current_params()
    
       
def previous_sweep():
    abf = AP_data.abf
    if AP_plot.sweep_number == 0:
        pass
    else:
        AP_plot.sweep_number = AP_plot.sweep_number - 1
        sweep_scale.set(AP_plot.sweep_number)
    AP_plot.plot_sweeps(AP_data, abf, Vrest=True, all_peaks=True, AP_peak=True, dVdtmax=True, APD=True)
    current_params()
     
def next_sweep():
    abf = AP_data.abf
    if AP_plot.sweep_number == abf.sweepCount-1:
        pass
    else:
        AP_plot.sweep_number = AP_plot.sweep_number + 1
        sweep_scale.set(AP_plot.sweep_number)
    AP_plot.plot_sweeps(AP_data, abf, Vrest=True, all_peaks=True, AP_peak=True, dVdtmax=True, APD=True)
    current_params()
    
def save_to_all():
    vrest_lefti = int(vrest_left_entry.get())
    vrest_righti = int(vrest_right_entry.get())
    prominence1 = int(prominence1_entry.get())
    prominence2 = int(prominence2_entry.get())
    distance = int(distance_entry.get())
    peak_idxs_idx = int(peak_idx_entry.get())
    
    for sw in AP_data.data.keys():
        AP_data.data[sw].Vrest_lefti=vrest_lefti    
        AP_data.data[sw].Vrest_righti=vrest_righti 
        AP_data.data[sw].prominence1 = prominence1
        AP_data.data[sw].prominence2 = prominence2
        AP_data.data[sw].distance = distance
        AP_data.data[sw].peak_idxs_idx = peak_idxs_idx    
        AP_data.data[sw].update_sweep()
    Overview_Plot.draw_plot(AP_data, AP_data.abf)

def sumplot_options_check():
    Overview_Plot.params = sumplot_options
    Overview_Plot.draw_plot(AP_data, AP_data.abf)

def default_average_interval():
    abf = AP_data.abf
    avg_interval_left_scale.config(to=abf.sweepNumber)
    avg_interval_right_scale.config(to=abf.sweepNumber)
    AP_data.avg_left = 9
    if abf.sweepNumber > AP_data.avg_left + 10:
        AP_data.avg_right = AP_data.avg_left + 9
    else:
        AP_data.avg_right = abf.sweepNumber
    
    avg_interval_left_scale.set(AP_data.avg_left)
    avg_interval_right_scale.set(AP_data.avg_right)
   

def update_avg_interval_from_scale(event):
    AP_data.avg_left = avg_interval_left_scale.get()
    AP_data.avg_right = avg_interval_right_scale.get()
    Overview_Plot.draw_plot(AP_data, AP_data.abf)
    
def average_interval_left_minus_one():
    current_avg_left = avg_interval_left_scale.get()
    new_avg_left = current_avg_left - 1
    avg_interval_left_scale.set(new_avg_left)
    AP_data.avg_left = new_avg_left
    
def average_interval_left_plus_one():
    current_avg_left = avg_interval_left_scale.get()
    new_avg_left = current_avg_left + 1
    avg_interval_left_scale.set(new_avg_left)
    AP_data.avg_left = new_avg_left
    
def average_interval_right_minus_one():
    current_avg_right = avg_interval_right_scale.get()
    new_avg_right = current_avg_right - 1
    avg_interval_right_scale.set(new_avg_right)
    AP_data.avg_right = new_avg_right
    
def average_interval_right_plus_one():
    current_avg_right = avg_interval_right_scale.get()
    new_avg_right = current_avg_right + 1
    avg_interval_right_scale.set(new_avg_right)
    AP_data.avg_right = new_avg_right
    
    

def append_summary():    
    AP_data.save_output(append = True)
    
def replace_summary():    
    AP_data.save_output(append = False)
    

def save_rep():
    df = {}
    df['Time ({})'.format(AP_data.abf.sweepUnitsX)] = AP_data.data[AP_plot.sweep_number].Xdata
    df['Sweep ({})'.format(AP_data.abf.sweepUnitsY)]  = AP_data.data[AP_plot.sweep_number].Ydata
    rep_path = '{}/{}_sw{}_representative.csv'.format(AP_data.output_folder, AP_data.abfname, AP_plot.sweep_number)
    df = pd.DataFrame(df)
    df.to_csv(rep_path)



AP_data = utils.ApData()
output_folder = ''

window_iniX = 1700
window_iniY = 950

window = tk.Tk()
window.title("Balazs`s ABF AP analyzer")
window.geometry("{}x{}+50+10".format(window_iniX, window_iniY)) 

left_frame = tk.Frame(master = window)
left_frame.pack(side=tk.LEFT, expand=True)

right_frame = tk.Frame(master = window)
right_frame.pack(side=tk.RIGHT, fill='both', expand=True)
sweep_plot_title = tk.Label(master=right_frame, text="Sweep-by-sweep plot ", font=('Arial 12 bold'))
sweep_plot_title.pack(fill=tk.X)
AP_plot = utils.ApPlot(right_frame)


sweep_buttons_frame = tk.Frame(master = right_frame)
sweep_buttons_frame.pack(fill=tk.X)
previous_button = tk.Button(master=sweep_buttons_frame, font=('Arial 10'), text="Previous sweep", command=previous_sweep)
previous_button.pack(side=tk.LEFT, padx=5, pady=5)
sweep_scale = tk.Scale(master=sweep_buttons_frame, from_=0, to=100, orient='horizontal', command=update_sweep_from_sweep_scale)
sweep_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
next_button = tk.Button(master=sweep_buttons_frame,font=('Arial 10'), text="Next sweep", command=next_sweep)
next_button.pack(side=tk.RIGHT, padx=5, pady=5)
rep_button = tk.Button(master = right_frame, font=('Arial 10'), text='Save this sweep as csv', command=save_rep)
rep_button.pack()

input_file_frame = tk.Frame(master = left_frame)
input_file_frame.pack(fill=tk.X, pady=5, padx=5)
label1 = tk.Label(master=input_file_frame,font=('Arial 10 bold'), text="Let`s open an .abf file with the AP recordings!")
label1.pack(padx=10, side=tk.LEFT)
next_file_button = tk.Button(input_file_frame, text="Next file", command=next_file)
next_file_button.pack(side=tk.RIGHT)
previous_file_button = tk.Button(input_file_frame, text="Previous file", command=previous_file)
previous_file_button.pack(side=tk.RIGHT)
browse_button = tk.Button(input_file_frame, font=('Arial 10'),text='Open File', command=browse_file)
browse_button.pack(pady = 5, padx = 5,  side=tk.RIGHT)

params_frame = tk.Frame(master=left_frame)
params_frame.pack(fill=tk.X, padx=5,pady=5)
params_label = tk.Label(master=params_frame,font=('Arial 12 bold'), text="Parameters for AP analysis")
params_label.pack(pady=5, fill=tk.X)
vrest_label = tk.Label(master=params_frame,font=('Arial 10 bold'), text="Parameters for Vrest interval")
vrest_label.pack(pady=5, fill=tk.X)
# label2_vrest = tk.Label(master=params_frame, font=('Arial 10'), text = "Enter left and right boundaries of the interval of which average will be Vrest (data points, Time * Sampling Rate)")
# label2_vrest.pack()

# vrest_entry_frame = tk.Frame(master = params_frame)
# vrest_entry_frame.pack(fill=tk.X)
vrest_left_frame = tk.Frame(master= params_frame)
vrest_left_frame.pack(fill=tk.X)
label_vrest_lefti = tk.Label(master=vrest_left_frame,font=('Arial 10'), text="Left boundary (in data points): ")
label_vrest_lefti.pack(side=tk.LEFT)
vrest_left_entry = tk.Entry(vrest_left_frame, width=5, font=('Arial 10'))
vrest_left_entry.pack(side=tk.LEFT,padx=5)
vrest_left_entry.bind('<Return>', update_params)
vrest_left_scale = tk.Scale(master = vrest_left_frame, orient='horizontal', showvalue=0, command=update_vresti_from_scale)
vrest_left_scale.pack(side=tk.LEFT, pady=10, padx=5, expand=True, fill=tk.X)

vrest_right_frame = tk.Frame(master=params_frame)
vrest_right_frame.pack(fill=tk.X)
label_vrest_righti = tk.Label(master=vrest_right_frame, font=('Arial 10'),text="Right boundary (in data points): ")
label_vrest_righti.pack(side=tk.LEFT)
vrest_right_entry = tk.Entry(vrest_right_frame, width=5, font=('Arial 10'))
vrest_right_entry.pack(side=tk.LEFT)
vrest_right_entry.bind('<Return>', update_params)
vrest_right_scale = tk.Scale(master = vrest_right_frame, orient='horizontal', showvalue=0, command=update_vresti_from_scale)
vrest_right_scale.pack(side=tk.LEFT, pady=10, padx=5, expand=True, fill=tk.X)

params_label = tk.Label(master=params_frame,font=('Arial 10 bold'), text="Parameters for AP peak detection")
params_label.pack(pady=5)

signal_peaks_frame = tk.Frame(master=params_frame)
signal_peaks_frame.pack(fill=tk.X)
prominence1_label = tk.Label(master=signal_peaks_frame,font=('Arial 10'), text="Prominence low boundary: ")
prominence1_label.pack(side=tk.LEFT)
prominence1_entry = tk.Entry(master=signal_peaks_frame, width=5, font=('Arial 10'))
prominence1_entry.pack(side=tk.LEFT, padx=5)
prominence1_entry.bind('<Return>', update_params)

prominence2_frame = tk.Frame(master=params_frame)
prominence2_frame.pack(fill=tk.X)
prominence2_label = tk.Label(master=signal_peaks_frame, font=('Arial 10'),text="Prominence high boundary: ")
prominence2_label.pack(side=tk.LEFT)
prominence2_entry = tk.Entry(master=signal_peaks_frame, width=5, font=('Arial 10'))
prominence2_entry.pack(side=tk.LEFT, padx=5)
prominence2_entry.bind('<Return>', update_params)

distance_frame = tk.Frame(master=params_frame)
distance_frame.pack(fill=tk.X)
distance_label = tk.Label(master=signal_peaks_frame, font=('Arial 10'),text="Distance: ")
distance_label.pack(side=tk.LEFT)
distance_entry = tk.Entry(master=signal_peaks_frame, width=5, font=('Arial 10'))
distance_entry.pack(side=tk.LEFT, padx=5)
distance_entry.bind('<Return>', update_params)

peaks_label = tk.Label(master=signal_peaks_frame,font=('Arial 10 bold'), text="Currently no peaks are detected")
peaks_label.pack(pady=5)


peak_idx_frame = tk.Frame(master=params_frame)
peak_idx_frame.pack(fill=tk.X)
peak_idx_label = tk.Label(master=peak_idx_frame,font=('Arial 10'), text="Which signal peak do we use as AP peak? ")
peak_idx_label.pack(side=tk.LEFT)
peak_idx_entry = tk.Entry(master=peak_idx_frame, width=5, font=('Arial 10'))
# peak_idx_entry.insert(0,AP_data.data[0].peak_idxs_idx)
peak_idx_entry.pack(side=tk.LEFT, padx=5)
peak_idx_entry.bind('<Return>', update_params)
peak_idx_expl = tk.Label(master=peak_idx_frame,font=('Arial 10'), text="If first: 0, if second: 1, etc.")
peak_idx_expl.pack(side=tk.RIGHT)

save_params_frame =tk.Frame(master=params_frame)
save_params_frame.pack(fill=tk.X, padx=5, pady=5)
# save_to_this_button = tk.Button(master=save_params_frame, text="Save params to current sweep", command=save_to_this)
# save_to_this_button.pack(side=tk.LEFT)
save_to_all_button = tk.Button(master=save_params_frame,font=('Arial 10'), text="Save current params to all sweeps", command=save_to_all)
save_to_all_button.pack()

output_frame = tk.Frame(master = left_frame)
output_frame.pack(anchor = 'center')
output_label = tk.Label(master = output_frame, text="Save Output", font=('Arial 12 bold'))
output_label.pack(anchor = 'center')

browse_button2 = tk.Button(output_frame, font=('Arial 10'),text='Open output folder', command=browse_directory)
browse_button2.pack(padx = 5, pady = 5, side=tk.LEFT)
saveresults_button = tk.Button(output_frame, font=('Arial 10'),text='Save sweep-by-sweep results', command=save_sweep_by_sweep_results)
saveresults_button.pack(padx = 5, pady = 5, side=tk.LEFT)
savefigs_button = tk.Button(output_frame, font=('Arial 10'),text='Save sweep-by-sweep plots', command=save_figs)
savefigs_button.pack(padx = 5, pady = 5, side=tk.LEFT)

summary_label = tk.Label(master=left_frame, text="Analysis Results Overview", font=('Arial 12 bold'))
summary_label.pack(fill=tk.X)

sumplot_params_frame = tk.Frame(master = left_frame)
sumplot_params_frame.pack(padx=5, pady=5, anchor='center')

sumplot_options_text = ['Vrest','AP peak', 'APD20', 'APD30', 'APD40', 'APD50', 'APD60', 'APD70', 'APD80','APD90']
sumplot_options_value = [tk.IntVar(), tk.IntVar(), tk.IntVar(),tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar() ]
sumplot_options_def_value = [1, 1, 0, 0, 0, 0, 0, 0, 0, 1]
for var, def_var in zip(sumplot_options_value, sumplot_options_def_value):
    var.set(def_var)

sumplot_options = {}
for text, value in zip(sumplot_options_text, sumplot_options_value):
    sumplot_options[text]=value
    sumplot_option_box = tk.Checkbutton(sumplot_params_frame, text = text,  variable=sumplot_options[text], command=sumplot_options_check)
    sumplot_option_box.pack(side=tk.LEFT)

sumplot_frame = tk.Frame(left_frame)
sumplot_frame.pack(fill='both')
Overview_Plot = utils.OverviewPlot(sumplot_frame, sumplot_options)

avg_interval_left_frame = tk.Frame(master = left_frame)
avg_interval_left_frame.pack(fill=tk.X)
avg_interval_left_previous_button = tk.Button(avg_interval_left_frame, text='-1 sweep', command=average_interval_left_minus_one)
avg_interval_left_previous_button.pack(side=tk.LEFT, padx=5)
avg_interval_left_scale = tk.Scale(avg_interval_left_frame, from_=0, to=100, orient='horizontal', command = update_avg_interval_from_scale)
avg_interval_left_scale.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)
# avg_interval_left_scale.place(anchor = 'center', relx = 0.5, relwidth=0.8)
avg_interval_left_next_button = tk.Button(avg_interval_left_frame, text='+1 sweep', command=average_interval_left_plus_one)
avg_interval_left_next_button.pack(side=tk.RIGHT)

avg_interval_right_frame = tk.Frame(master = left_frame)
avg_interval_right_frame.pack(fill=tk.X, pady=10)
avg_interval_right_previous_button = tk.Button(avg_interval_right_frame, text='-1 sweep', command=average_interval_right_minus_one)
avg_interval_right_previous_button.pack(side=tk.LEFT, padx=5)
avg_interval_right_scale = tk.Scale(avg_interval_right_frame, from_=0, to=100, orient='horizontal', command = update_avg_interval_from_scale)
avg_interval_right_scale.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)
# avg_interval_right_scale.place(anchor = 'center', relx = 0.5, relwidth=0.8)
avg_interval_right_next_button = tk.Button(avg_interval_right_frame, text='+1 sweep', command=average_interval_right_plus_one)
avg_interval_right_next_button.pack(side=tk.RIGHT)



# avg_interval_right = tk.Scale(left_frame, from_=0, to=100, orient='horizontal', command = update_avg_interval, bg='white')
# avg_interval_right.pack(fill=tk.X, padx=80)

save_avg_label = tk.Label(master=left_frame, text="Save summary data including the above sweeps:", font=('Arial 10'))
save_avg_label.pack(side=tk.LEFT)
replace_avg_button = tk.Button(master=left_frame, text="Replace", font=('Arial 10'), command = replace_summary)
replace_avg_button.pack(side=tk.RIGHT, padx = 5, pady = 5)
append_avg_button = tk.Button(master=left_frame, text="Append", font=('Arial 10'), command = append_summary)
append_avg_button.pack(side=tk.RIGHT, padx = 5, pady = 5)


window.protocol("WM_DELETE_WINDOW", window.destroy)

window.mainloop()





    