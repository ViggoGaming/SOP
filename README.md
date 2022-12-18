# SOP
Dette repository indeholder alt min kode og anvendte datasæt til mit studieområdeprojekt

# Eget datasæt
!["Graf"](./out.png)

# Eksternt datasæt fra kaggle
!["Graf"](./external.png)

# Guide til at køre mit program på egen computer
*OBS: Denne guide forudsætter at du har Python 3.10+ installeret på din computer*

Start med at downloade dette GitHub repository som en `.zip` fil eller via git kommandoen:
`git clone https://github.com/ViggoGaming/SOP.git`

Herefter skal du åbne en terminal i `SOP` mappen, eller skifte mappen du står i inde i din terminal, med følgende kommando:
`cd SOP`

Nu skal du installere alle de nødvendige Python biblioteker med følgende kommando:
`pip3 install -r requirements.txt`

Nu kan du køre to forskellige Python filer, enten `main.py`, som understøtter mit eget datasæt eller `main_external_dataset.py` som understøtter det eksterne datasæt
De kan køres med følgende kommandoer:
*Program til eget datasæt*
`python3 -m streamlit run main.py` 
*Program til eksternt datasæt*
`python3 -m streamlit run main_external_dataset.py` 

Herefter vil der automatisk åbnes et vindue i din browser hvor du kan uploade henholdsvis `./datasets/SOP_dataset_mini.csv` eller `./datasets/external-dataset_kaggle.csv`
