# Extraction des classes des espèces à partir des flores camerounais.
Pour réaliser les tâches demandées dans le projet, nous avons créer deux modèles NER : un pour l'extraction des noms des espèces et l'autre est pour l'extraction des classes de descripteurs dans les paragraphes de description. les fichiers de données et de code sont regroupés dans les dossiers suivants:
## Le dossier notebooks : 
Contient les fichiers de code en format ipynb.
## get full sentences of species from the flore documents.ipynb : 
Ce fichier contient le code de l'extraction des noms des espèces à partir des flores et aussi l'extraction des titres des paragraphes qui contiennent les noms des espèces , le dataset `species_and_titles_dataframe.csv` est sous la forme suivante :
> <html>
<body>
<!--StartFragment-->

espèce | description
-- | --
Schefflera abyssinica | 1. Schefflera abyssinica
Schefflera Mannii | 3. Schefflera Mannii (Hooker fil.) Harms
Hydrocotyle sibthorpioides | 1. Hydrocotyle sibthorpioides Lamarck
Hydrocotyle hirta | 2. Hydrocotyle hirta R. Brown ex A. Richard
Hydrocotyle bonariensis | 3. Hydrocotyle bonariensis Lamarck
... | ...
Monopetalanthus Pellegrinii | 5. Monopetalanthus Pellegrinii A. Chevalier
Swartzia fistuloides | 1. Swartzia fistuloides Harms
Swartzia madagascariensis | 2. Swartzia madagascariensis Desvaux
Csesalpinia Welwitschiana | 1. Csesalpinia Welwitschiana (Oliver) Brenan
Erythrophleum ivorense | 1. Erythrophleum ivorense A. Chevalier

<!--EndFragment-->
</body>
</html>

**le dossier `generetad data` contient tous les fichiers csv que nous avons généré**
## Scrapping new species names from the plant list.ipynb
Ce fichier contient le code du scrapping des nouveaux noms d'espèces à partir du site [_the plant list_ ](http://www.theplantlist.org) 
on sauvegarde les noms des espèces dans le fichier `generetad data/species-THEPLANTLIST.txt` 
## Scrapping paragraphs from wikipedia using the plant list species.ipynb
Une étape que nous avons fait avant de commencer à coder le script de scrapping des phrases ou paragraphes qui decrivent les espèces est de stocker les espèces pas encore utilisées pour le scrapping dans un fichier `genereted data/species-THEPLANTLIST-not_scrapped.txt` car le script de scrapping est divisé en plusieurs itérations car le nombre des noms des espèces est très grand (350639 espèces) et le scrapping en utilisant Wikipedia prend du temps ,donc nous avons essayer de sauvegarder les résultats du scrapping à chaque fois dans un ficher `../genereted data/rescued_data.csv` pour éviter la perte des données de scrapping . les fichiers de données générés en utilisant ce script sont `../genereted data/rescued_data.csv` et `../genereted data/rescued_data.csv2` et `../genereted data/scrapped_wikidata.csv`
Vous trouvrez en dessous un exemple des données obtenue à partir du wikipedia en utilisant les noms des espèces extraites à partir des documents de flores .
<html>
<body>
<!--StartFragment-->

espèce | description
-- | --
Schefflera abyssinica | Le genre Schefflera constitue un groupe d’arbr...
Schefflera Mannii | Schefflera mannii (Hook.f.) Harms est une espè...
Tessmannia africana | Tessmannia est un genre de plantes dicotylédon...
Alternanthera sessilis | Alternanthera est un genre qui regroupe plus d...
Pimpinella Ledermannii | Pimpinella ledermannii H. Wolff est une espèce...
... | ...
Monopetalanthus Hedinii | Aphanocalyx hedinii est une espèce d'arbres de...
Monopetalanthus microphyllus | Monopetalanthus heitzii est une espèce de plan...
Deinbollia dasybotrys | Deinbollia est un genre de plantes de la famil...
Hydrocotyle sibthorpioides | Les hydrocotyles (Hydrocotyle) forment un genr...
Gilbertiodendron mayombense | Gilbertiodendron est un genre de plantes appar...

<!--EndFragment-->
</body>
</html>

 ## generate_train_data_merging_datasets.ipynb
On fusionne le code des trois datasets obtenu : on prend le fichier wiki_data et les titres des paragraphes avec la dataset que nous avons obtenue à partir de plant list et wikipedia .
Les descriptions obtenue à partir du wikipedia contient du bruit (descriptions du genre, des lignes manquantes ...)
Après les traitements appliqués(TOKENIZATION..) sur les datasets , on garde que les lignes qui contiennent les espèces et la description.et on crée un nouveau jeu de données sous la forme NER .

![image](https://user-images.githubusercontent.com/86720032/212359411-dcab1fbb-5cf5-48f2-aed2-e7f3965e359c.png)

On divise en Train et en Test , pour créer deux listes sous la forme:
 [Text,{'entities:[[start,end,label],[start,end,label],...]}]
On sauvegarde les deux fichiers en format pkl pour les réutiliser dans d'autres script : `../merged data/train_species_data_merged.pkl` , `../merged data/test_species_data_merged.pkl`
## Create_first_Ner_model_data_from_flora_wikipedia.ipynb
Le fichier contient un premier teste du modèle NER sur une partie de notre dataset en utilisant `SPACY` , et aussi la génération des fichier  `train.spacy et test.spacy` , aussi un premier teste du modèle NER en utilisant le CPU (ce fichier est ajouté pour donner une idée sur les étapes que nous avons suivie pour créer les modèles finaux) 
## Ner_descriptors_organs.ipynb
Avant de commencer l'extraction des classes des desrcripteurs nous avons rassembler toutes les fonctions nécessaire dans un fichier `Utils_descriptors.py` qui contient la définition des fonctions de l'extraction des espèces et des descripteurs(mesures,forme,coleur) .en utilisant le script dans ce notebook nous avons généré les fichiers d'entrainements par exemple :`train_descriptors.spacy` et aussi d'autres fichiers comme `train_data_desc_mixte.pkl` ,`test_data_desc_mixte.pkl` ,Les fichiers de teste vont être transformés en format JSONL aussi pour les utilisés dans un autre code qui génère les matrices de confusion pour les modèles NER .
## Train_spacy_models_in collab_and_evaluate.ipynb

Le fichier contient des lignes de commandes pour faire l'entrainement des modèles NER en utilisant le GPU et en utilisant des fichiers train et validation à partir du drive , et aussi le chemin de l'output : 

    !python -m spacy train /content/drive/MyDrive/NER_project/ner_data/config.cfg --paths.train /content/drive/MyDrive/NER_project/ner_data/train_descriptors.spacy        --paths.dev /content/drive/MyDrive/NER_project/ner_data/train_descriptors.spacy --output /content/drive/MyDrive/NER_project/models/output_descriptors --gpu-id 0.

Aussi les commandes de l'évaluation des modèles sur les fichiers test.spacy ,par exemple : 

    !python -m spacy evaluate /content/drive/MyDrive/NER_project/models/output_species/model-best  /content/drive/MyDrive/NER_project/ner_data/test_species.spacy --gpu-id 0

<img src="https://user-images.githubusercontent.com/86720032/212369848-dd21b467-f64c-4147-9d4d-ba63da0ef67f.png" width=50% height=50%>
Le fichier contient aussi une commande pour la génération des matrices de confusion en utilisant le fichier `generate_confusion_matrix.py` , avec le chemain où nous voulons stocker notre matrice 

    !python /content/drive/MyDrive/NER_project/generate_confusion_matrix.py /content/drive/MyDrive/NER_project/models/output_descriptors/model-best /content/drive/MyDrive/NER_project/ner_data/test_descriptors.jsonl /content/drive/MyDrive/NER_project/confusion_train_out_descriptors

<img src="https://user-images.githubusercontent.com/86720032/212375167-7986982c-ef2b-47a1-bf66-abbe5a5c1ab6.png" width=40% height=40%>


Nous avons utilisé ce notebook pour générer trois modèles: un pour les espèces et un pour les classes des descripteurs ,finalement un modèle qui fait les deux tâches en même temps.les modèles sont téléchargé du Google Drive manuellemnt et sont stockés dans le fichier Streamlitapp
## Streamliapp 
le dossier streamlitapp contient les modèles NER et les fichiers nécessaires pour la création d'une image Docker.la création respecte les étapes suivantes:
* La création d'une interface Streamlit dans un le streamlit.py
* La création d'un environnement python avec `pipenv` et l'installation des packages nécessaire pour l'interface streamlit .et la genération des deux fichiers `pipfile`,`pipfile.lock`
* la génération du fichier requirements.txt
* la création du Dockerfile.
* le création du docker compose pour la création d'une image.
 > l'image obtenue est de size 8.58 GB 

<img src="https://user-images.githubusercontent.com/86720032/212375415-f222d005-5f44-47ab-8122-443fdea89243.png" width=50% height=50%>


L'image est ouverte dans `http://localhost:8081/`

<img src="https://user-images.githubusercontent.com/86720032/212376964-3881df5a-731d-45b2-800a-2c0eda63ae10.png" width=50% height=50%>

Les modèles sont stockés dans le drive suivants : [Drive modèles NER](https://drive.google.com/drive/folders/1Pt-BzTnlnJWWfFOOXJhQJeEDdK5T7xBU?usp=share_link)

## Test de l'interface 

<img src="https://user-images.githubusercontent.com/86720032/212398732-4850c7f5-c20c-403f-b615-450fb72cd120.png" width=50% height=50%>




