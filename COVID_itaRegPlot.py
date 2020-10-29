import sys
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


# AUXILIARY
# function to render invisible chart axes (i think)
def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)


# INPUT
pre_data_regione = pd.read_csv('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv')
nomeRegione = str(sys.argv[1])
data_inizio, data_fine = 0, 0


# DATA ACQUISITION 
# fkn easy as that file read holy smokes
# pre_data_regione = pd.read_csv(csv_regioni)

# reindex using region names and extract the region we want to analyze
pre_data_regione.set_index("denominazione_regione",inplace=True)
data_regione = pre_data_regione.loc[nomeRegione,:].copy()

# reindex with integers to be able to plot and create a handy column
data_regione.reset_index()
x = range(0,len(data_regione))
data_regione['index'] = range(0,len(data_regione)) 

# extract daily tamponi
temp = data_regione['tamponi']
temp2 = np.zeros(len(temp))
temp2[1:] = temp[:-1].copy()
data_regione["tamponi_giornalieri"] = (temp - temp2).copy()




# PLOT SECTION
# define some colors and fontsizes(its better to define them here trust meh)
base_color_str = "#565656"

tamponi_color_str = "#cccccc"
rapporto_np_t_color_str = "#1774ff"
nuovi_positivi_color_str = "#ff7700"

positivi_color_str = "#ffd1a8"
ricoverati_color_str = "#8f0000"
intensiva_color_str = "#000000"

title_size_str="15"
subtitle_size_str="13"
axis_label_size_str="12"
tick_label_size_str="10"

labelpad_val=10

# create axes and adjust figure
fig, (host1,host2) = plt.subplots(2,figsize=(15,9))
fig.subplots_adjust(hspace=.4,left=0.1,right=0.85)
plt.tight_layout(h_pad=5,rect=(0.04,0.04,0.86,0.9))
fig.suptitle("Diagnosi e decorso: %s" % nomeRegione, fontsize=title_size_str)
host1.set_title("Tamponi, nuovi positivi e percentuale di tamponati positivi", fontsize = subtitle_size_str)
host2.set_title("Casi attivi, ricoverati e ricoverati in terapia intensiva", fontsize = subtitle_size_str)

# setup the multiaxes
par1 = host1.twinx()
par1.spines["right"].set_position(("axes",1.1))
make_patch_spines_invisible(par1)
par1.spines["right"].set_visible(True)
par2 = host1.twinx()

par3 = host2.twinx()
par4 = host2.twinx()
par4.spines["right"].set_position(("axes",1.1))
make_patch_spines_invisible(par4)
par4.spines["right"].set_visible(True)


# plot everythin
host1.bar(x,data_regione["tamponi_giornalieri"], color=tamponi_color_str, linewidth=0, label="Tamponi")
p2, = par1.plot(x,data_regione["nuovi_positivi"]/data_regione["tamponi_giornalieri"], color=rapporto_np_t_color_str, linewidth=1, label="% tamponi positivi")
p3, = par2.plot(x,data_regione["nuovi_positivi"], color=nuovi_positivi_color_str, linewidth=3, label="Nuovi positivi")

host2.bar(x, data_regione["totale_positivi"], color=positivi_color_str, linewidth=0, label="Positivi")
p5, = par3.plot(x, data_regione["ricoverati_con_sintomi"], color=ricoverati_color_str, linewidth=2, label="Ricoverati")
p4, = par4.plot(x, data_regione["terapia_intensiva"], color=intensiva_color_str, linewidth=2, label="Terapia intensiva")


# x and y axis ranges
host1.set_xlim(0,len(x))
host1.set_ylim(0,max(data_regione["tamponi_giornalieri"])*1.1)
par1.set_ylim(0,1)
par2.set_ylim(0,max(data_regione["nuovi_positivi"]*1.1))

host2.set_xlim(0,len(x))
host2.set_ylim(0,max(data_regione["totale_positivi"])*1.1)
par3.set_ylim(0,max(data_regione["ricoverati_con_sintomi"])*1.1)
par4.set_ylim(0,max(data_regione["ricoverati_con_sintomi"])*1.1)


# cosmetics
for i in host1.spines:
	host1.spines[i].set_color(base_color_str)
	par1.spines[i].set_color(base_color_str)
	par2.spines[i].set_color(base_color_str)
	host2.spines[i].set_color(base_color_str)
	par3.spines[i].set_color(base_color_str)
	par4.spines[i].set_color(base_color_str)

# top graph cosmetics
host1.grid(axis="y",linewidth='0.5',linestyle=':', color='#aaaaaa')
host1.tick_params(axis="both", labelsize= tick_label_size_str, color = base_color_str, labelcolor = base_color_str)
host1.set_xticks([0,100,200])
host1.set_xlabel("Giorni", fontsize= axis_label_size_str, labelpad=labelpad_val, color = base_color_str)
host1.set_ylabel("Tamponi", fontsize= axis_label_size_str, labelpad=labelpad_val, color = base_color_str)

par1.tick_params(axis="y", labelsize= tick_label_size_str, color = base_color_str, labelcolor=base_color_str)
par1.set_ylabel("% positività tampone", fontsize= axis_label_size_str, labelpad=labelpad_val, color = p2.get_color() )

par2.tick_params(axis="y", labelsize= tick_label_size_str, color = base_color_str, labelcolor = base_color_str)
par2.set_ylabel("Nuovi positivi", fontsize= axis_label_size_str, labelpad=labelpad_val, color = p3.get_color())

# bottom graph cosmetics
host2.grid(axis="y",linewidth='0.5',linestyle=':', color='#aaaaaa')
host2.tick_params(axis="both", labelsize= tick_label_size_str, color = base_color_str, labelcolor = base_color_str)
host2.set_xticks([0,100,200])
host2.set_xlabel("Giorni", fontsize= axis_label_size_str, labelpad=labelpad_val, color = base_color_str)
host2.set_ylabel("Casi attivi", fontsize= axis_label_size_str, labelpad=labelpad_val, color = "#ffb682")

par3.tick_params(axis="y", labelsize= tick_label_size_str, color = base_color_str, labelcolor = base_color_str)
par3.set_ylabel("Ricoverati", fontsize= axis_label_size_str, labelpad=labelpad_val, color = p5.get_color())

par4.tick_params(axis="y", labelsize= tick_label_size_str, color = base_color_str, labelcolor = base_color_str)
par4.set_ylabel("Terapia intensiva", fontsize= axis_label_size_str, labelpad=labelpad_val, color = "#000000")


plt.show()

