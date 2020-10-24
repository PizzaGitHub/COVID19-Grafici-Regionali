# COVID_itaRegPlot

Breve script per parsing del file CSV pubblicato quotidianamente dalla protezione civile sull'andamento dell'epidemia di COVID-19 a livello regionale.
L'output del programma consiste in due grafici in cui sono rappresentati gli andamenti giornalieri di:
 
 - Nuovi tamponi / Nuovi positivi / percentuali dei tamponi positivi
 - Positivi / ricoverati / ricoverati in terapia intensiva

relativi alla regione specificata dall'utente.

## Prerequisiti
E' necessario avere installato sul proprio pc python 3.x completo dei pacchetti Numpy, Matplotlib e Pandas

## Utilizzo

Dall'indirizzo https://github.com/pcm-dpc/COVID-19/blob/master/dati-regioni/dpc-covid19-ita-regioni.csv aprire il "dpc-covid19-ita-regioni.csv" più recente e salvarne una copia .csv in locale.
Scaricare poi lo script COVID_itaRegPlot.py e salvarlo nella stessa cartella del file .csv.

Aprire quindi il terminale nella stessa posizione ed eseguire

$ python COVID_itaRegPlot <nome_regione>

con il nome della regione di interesse al posto di <nome_regione>.
