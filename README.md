# COVID19: Grafici Regionali

Due brevi script per parsing del file CSV pubblicato quotidianamente dalla protezione civile sull'andamento dell'epidemia di COVID-19 a livello regionale.

## COVID_itaRegPlot.py
L'output del programma consiste in due grafici in cui sono rappresentati gli andamenti giornalieri di:
 
 - Nuovi tamponi / Nuovi positivi / percentuali dei tamponi positivi
 - Positivi / ricoverati / ricoverati in terapia intensiva

relativi alla regione specificata dall'utente.

Dello script esistono 2 release: una scaricabile ed eseguibile in locale l'altra reperibile direttamente su Google Colab, cliccando sull'icona sottostante:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1shxxe7AmXR61BY5tYpp3AdYurL-b8Kts#scrollTo=5MnIjStE9luA&forceEdit=true&sandboxMode=true)

## Istruzioni versione Colab 
Dopo aver aperto il notebook Colab, inserire alla voce nomeRegione nella sezione INPUT il nome della regione di interesse fra apici (ad esempio "Lombardia") e premere CTRL+Invio. In fondo alla pagina appariranno i grafici di output

### Istruzioni utilizzo in locale (Linux)

*Prerequisiti*: è necessario avere installato sul proprio pc python 3.x completo dei pacchetti Numpy, Matplotlib e Pandas.

Scaricare lo script da 

Aprire quindi il terminale nella stessa posizione ed eseguire
```
$ python COVID_itaRegPlot <"nome_regione">
```
con il nome della regione di interesse inserito fra apici al posto di <"nome_regione">, per esempio `$ python COVID_itaRegPlot "Emilia-Romagna"`
