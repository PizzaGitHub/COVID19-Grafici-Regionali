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


# USER INPUT
nomeRegione = str(sys.argv[1])
data_inizio, data_fine = 0, 0


# Italian population + dictionary with all regional populations: we will use it to normalize national values
popolazione = {"Abruzzo":1305770, "Basilicata":556934, "Calabria":1924701, "Campania":5785861,
               "Emilia-Romagna":4467118,"Friuli Venezia":1211357,
               "Lazio":5865544,"Lombardia":10103969,"Marche":1518400,"Molise":302265,"Piemonte":4341375,
               "Puglia":4008296,"Sardegna":1630474,"Sicilia":4968410,"Toscana":3722729,"Trento":553928,"Bolzano":520891,
               "Umbria":880285,"Valle d'Aosta":125501,"Veneto":4907704}

popolazione_italia = 60.36e6




# DATA ACQUISITION 
# fkn easy as that file read holy smokes
pre_data_regione = pd.read_csv('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv')
pre_data_italia = pd.read_csv('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv')

# reindex pre_data_regione using region names and extract the region we want to analyze
pre_data_regione.set_index("denominazione_regione",inplace=True)
data_regione = pre_data_regione.loc[nomeRegione,:].copy()

# reindex with integers to be able to plot and create a handy column
data_regione.reset_index()
x = range(0,len(data_regione))
data_regione['index'] = range(0,len(data_regione)) 

# extract daily tamponi for region
temp = data_regione['tamponi']
temp2 = np.zeros(len(temp))
temp2[1:] = temp[:-1].copy()
data_regione["tamponi_giornalieri"] = (temp - temp2).copy()

# calculate national daily tamponi
temp = pre_data_italia['tamponi']
temp2 = np.zeros(len(temp))
temp2[1:] = temp[:-1].copy()
pre_data_italia["tamponi_giornalieri"] = (temp - temp2).copy()

# scale national values according to selected region (pretty positive that this is not
# the best way to do it but it'll work for now)
scale = popolazione[nomeRegione]/popolazione_italia
pre_data_italia = pre_data_italia.drop(columns='note')
scaled_data_italia = pre_data_italia.copy()

for i in scaled_data_italia:
	if (scaled_data_italia.columns.get_loc(i)<2):
		continue
	scaled_data_italia[i] = pd.to_numeric(pre_data_italia[i]).mul(scale).copy()




# PLOT SECTION
# define some colors and fontsizes(its better to define them here trust meh)
base_color_str = "#565656"

tamponi_color_str = "#cccccc"
rapporto_np_t_color_str = "#1774ff"
nuovi_positivi_color_str = "#ff7700"

positivi_color_str = "#ffd1a8"
ricoverati_color_str = "#8f0000"
intensiva_color_str = "#000000"

suptitle_size_str="15"
subtitle_size_str="13"
axis_label_size_str="10"
tick_label_size_str="8"

labelpad_val=5
subtitlepad_val=10

# lets also define a lits of all the interesting categories
categorie = ["tamponi", "nuovi_positivi", "totale_positivi", "ricoverati_con_sintomi", "terapia_intensiva"]


fig = plt.figure(figsize = (15,9), dpi=60)
fig.suptitle("%s: confronto con media nazionale" % nomeRegione, fontsize=suptitle_size_str)
fig.subplots_adjust(top=0.912, bottom=0.077, left=0.05, right=0.97, hspace=0.52, wspace=0.085)


plot_index = 0 
for i in categorie:
	plot_index += 1 
	
	# plot the i-th graph
	axes = fig.add_subplot(3,2,plot_index)
	axes.plot(x,scaled_data_italia[i], base_color_str, linewidth=1.5, label="Media nazionale")
	axes.plot(x,data_regione[i], color=nuovi_positivi_color_str, linewidth=1.5, label="Dati regionali")
	
	# cosmetics
	axes.set_title(i, fontsize=subtitle_size_str, pad=subtitlepad_val)
	for j in axes.spines:
		axes.spines[j].set_color(base_color_str)
	axes.tick_params(axis="both", labelsize=tick_label_size_str, color=base_color_str, labelcolor=base_color_str)
	axes.set_xticks([0,100,200])
	axes.set_xlabel("Giorni", fontsize=axis_label_size_str, labelpad=labelpad_val, color=base_color_str)
	axes.grid(axis="y", linewidth='0.5', linestyle=':', color='#aaaaaa')
	axes.legend()
	
plt.show()

