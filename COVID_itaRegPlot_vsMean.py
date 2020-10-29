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
csv_regioni = str(sys.argv[1])
csv_nazione = str(sys.argv[2])
nomeRegione = str(sys.argv[3])
data_inizio, data_fine = 0, 0


# Dictionary with all regional populations: we will use it to normalize national values
popolazione = {"Abruzzo":1305770, "Basilicata":556934, "Calabria":1924701, "Campania":5785861,
               "Emilia-Romagna":4467118,"Friuli Venezia":1211357,
               "Lazio":5865544,"Lombardia":10103969,"Marche":1518400,"Molise":302265,"Piemonte":4341375,
               "Puglia":4008296,"Sardegna":1630474,"Sicilia":4968410,"Toscana":3722729,"Trento":553928,"Bolzano":520891,
               "Umbria":880285,"Valle d'Aosta":125501,"Veneto":4907704}

popolazione_italia = 60.36e6


# DATA ACQUISITION 
# fkn easy as that file read holy smokes
pre_data_regione = pd.read_csv(csv_regioni)
pre_data_italia = pd.read_csv(csv_nazione)

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

title_size_str="15"
subtitle_size_str="13"
axis_label_size_str="12"
tick_label_size_str="10"

labelpad_val=10

# define a list for the things to plot (im so lazy jesus)
categorie = ["tamponi","nuovi_positivi","totale_positivi","ricoverati_con_sintomi","terapia_intensiva"]



# create figure, axes and adjust some paddings
fig = plt.figure(figsize=(16,8))

for i in range(len(categorie)):
	host = plt.subplot(3,2,i+1)
	data_regione[categorie[i]].plot(kind='line', ax = host)
	scaled_data_italia[categorie[i]].plot(kind='line', ax = host)

	host.set_title("%s" % categorie[i], fontsize = subtitle_size_str)

fig.subplots_adjust(hspace=.4,left=0.1,right=0.85)
plt.tight_layout(h_pad=5,rect=(0.04,0.04,0.86,0.9))

fig.suptitle("%s: confronto con la media nazionale" % nomeRegione, fontsize=title_size_str)

'''
for i in range(len(categorie)):
	host.set_title(categorie[i], fontsize = subtitle_size_str)


# plot everything
for i in range(len(categorie)):
	i.plot(x,data_regione[categorie[i]], colore=tamponi_color_str, linewidth=1, label=categorie[i])




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
'''

plt.show()

