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





# DATA ACQUISITION 

# input parameters
nomeRegione = str(sys.argv[1])
data_inizio, data_fine = 0, 0


# fkn easy as that file read holy smokes
data = pd.read_csv('dpc-covid19-ita-regioni.csv')


# reindex using region names and extract the region we want to analyze
data.set_index("denominazione_regione",inplace=True)
data_regione = data.loc[nomeRegione,:].copy()


# reindex with integers to be able to plot and create a handy column
data_regione.reset_index()
x = range(0,len(data_regione))
data_regione['index'] = range(0,len(data_regione)) 


# extract daily tamponi
temp = data_regione['tamponi'].copy()
temp2 = np.zeros(len(temp))
temp2[1:] = temp[:-1].copy()
data_regione["tamponi_giornalieri"] = temp - temp2
tamponi_giornalieri = (temp - temp2).copy()



# PLOT SECTION

# create axes and adust figure
fig, (host1,host2) = plt.subplots(2)
fig.subplots_adjust(hspace=.5,right=0.75)
fig.suptitle("Diagnosi e decorso: %s" % nomeRegione, fontsize="8")

# setup the multiaxes
par1 = host1.twinx()
par1.spines["right"].set_position(("axes",1.2))
make_patch_spines_invisible(par1)
par1.spines["right"].set_visible(True)
par2 = host1.twinx()

par3 = host2.twinx()
par4 = host2.twinx()
par4.spines["right"].set_position(("axes",1.2))
make_patch_spines_invisible(par4)
par4.spines["right"].set_visible(True)


# plot everythin: note how we use a different method (native to dataframe) to plot the bars
host1.bar(x,data_regione["tamponi_giornalieri"], color="#cccccc", linewidth=0, label="Tamponi")
p2, = par1.plot(x,data_regione["nuovi_positivi"]/tamponi_giornalieri, color="#4092b8", linewidth=1, label="% tamponi positivi")
p3, = par2.plot(x,data_regione["nuovi_positivi"], color="#ff7700", label="Nuovi positivi")
# data_regione["tamponi_giornalieri"].plot(kind="bar",ax=par2, use_index=False, color="#9a9a9a", ylim=(0,max(data_regione["tamponi_giornalieri"])*1.1))
host2.bar(x, data_regione["totale_positivi"], color="#ffd1a8", linewidth=2, label="Positivi")
p5, = par3.plot(x, data_regione["ricoverati_con_sintomi"], color="#8f0000", label="Ricoverati")
p4, = par4.plot(x, data_regione["terapia_intensiva"], color="#000000", label="Terapia intensiva")


# y axis ranges
host1.set_ylim(0,max(tamponi_giornalieri)*1.1)
par1.set_ylim(0,1)
par2.set_ylim(0,max(data_regione["nuovi_positivi"]*1.1))

host2.set_ylim(0,max(data_regione["totale_positivi"])*1.1)
par3.set_ylim(0,max(data_regione["ricoverati_con_sintomi"])*1.1)
par4.set_ylim(0,max(data_regione["ricoverati_con_sintomi"])*1.1)


# cosmetics
base_color_str = "#565656"
for i in host1.spines:
	host1.spines[i].set_color(base_color_str)
	par1.spines[i].set_color(base_color_str)
	par2.spines[i].set_color(base_color_str)
	host2.spines[i].set_color(base_color_str)
	par3.spines[i].set_color(base_color_str)
	par4.spines[i].set_color(base_color_str)

# top graph cosmetics
host1.tick_params(axis="both", labelsize="6", color = base_color_str, labelcolor = base_color_str)
host1.set_xticks([0,100,200])
host1.set_xlabel("Giorni", fontsize="6", color = base_color_str)
host1.set_ylabel("Tamponi", fontsize="6", color = base_color_str)

par1.tick_params(axis="y", labelsize="6", color = base_color_str, labelcolor=base_color_str)
par1.set_ylabel("% positività tampone", fontsize="6", color = p2.get_color() )

par2.tick_params(axis="y", labelsize="6", color = base_color_str, labelcolor = base_color_str)
par2.set_ylabel("Nuovi positivi", fontsize="6", color = p3.get_color())

# bottom graph cosmetics
host2.tick_params(axis="both", labelsize="6", color = base_color_str, labelcolor = base_color_str)
host2.set_xticks([0,100,200])
host2.set_xlabel("Giorni", fontsize="6", color = base_color_str)
host2.set_ylabel("Contagiati", fontsize="6", color = "#ffb682")

par3.tick_params(axis="y", labelsize="6", color = base_color_str, labelcolor = base_color_str)
par3.set_ylabel("Ricoverati", fontsize="6", color = p5.get_color())

par4.tick_params(axis="y", labelsize="6", color = base_color_str, labelcolor = base_color_str)
par4.set_ylabel("Terapia intensiva", fontsize="6", color = "#000000")




plt.show()

