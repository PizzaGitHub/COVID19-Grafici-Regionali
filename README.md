# COVID19: Grafici Regionali

Due brevi script per parsing del file CSV pubblicato quotidianamente dalla protezione civile sull'andamento dell'epidemia di COVID-19 a livello regionale.

## COVID_itaRegPlot.py
L'output del programma consiste in due grafici in cui sono rappresentati gli andamenti giornalieri di:
 
 - Nuovi tamponi / Nuovi positivi / percentuali dei tamponi positivi
 - Positivi / ricoverati / ricoverati in terapia intensiva

relativi alla regione specificata dall'utente.


### Istruzioni versione Colab
Aprire il notebook cliccando sull'icona sottostante:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1shxxe7AmXR61BY5tYpp3AdYurL-b8Kts#scrollTo=5MnIjStE9luA&forceEdit=true&sandboxMode=true)

Inserire poi alla voce `nomeRegione` nella sezione INPUT il nome della regione di interesse fra apici (ad esempio "Lombardia") e premere CTRL+Invio. In fondo alla pagina appariranno i grafici di output.

### Istruzioni utilizzo in locale (Linux)

**Prerequisiti**: è necessario avere installato sul proprio pc python 3.x completo dei pacchetti Numpy, Matplotlib e Pandas.

Da terminale eseguire 
```
https://github.com/PizzaGitHub/COVID_itaRegPlot.git
```
Dopo aver estratto i contenuti della cartella compressa, portarsi all'interno di COVID_ita_RegPlot-main ed eseguire 
```
$ python COVID_itaRegPlot.py <"nome_regione">
```
con il nome della regione di interesse inserito fra apici al posto di <"nome_regione">, per esempio `$ python COVID_itaRegPlot "Emilia-Romagna"`
