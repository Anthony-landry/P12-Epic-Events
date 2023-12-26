# OpenClassrooms: Projet 12 - Développez une architecture back-end sécurisée avec Python et SQL

![projet 12 Développez une architecture back-end sécurisée avec Python et SQL](.readme/Landry_anthony_P12_Epic_Event_openclassrooms_developpeur_application_python.png)

Projet réalisé dans le cadre de la formation OpenClassrooms Développeur d'Applications Python.
Il s'agit d'une application web "MVC" réalisée avec Django.
L'application LitReviews, est un réseau social permettant de demander et poster des critiques de livres.

## Installation

Pour commencer, assurez-vous d'avoir Python installé sur votre système.

Ensuite, suivez ces étapes pour installer et exécuter le programme :

1. Clonez ce dépôt dans le répertoire de votre choix en utilisant la commande suivante :
    
    ```bash
    git clone https://github.com/Anthony-landry/P12-Epic-Events
    ```
    
2. Accédez au dossier P12-Epic-Events.
    
3. Créez un nouvel environnement virtuel en utilisant la commande suivante :
    
    ```bash
    python -m venv env
    ```
    
4. Activez l'environnement virtuel :
    
    * Sur Windows :
        
        ```bash
        env\Scripts\activate.bat
        ```
        
    * Sur Linux :
        
        ```bash
        source env/bin/activate
        ```
        
5. Installez les packages requis en exécutant la commande suivante :
    
    ```bash
    pip install -r requirements.txt
    ```
    
6. placez vous à la racine du projet (là ou se trouve le fichier manage.py), puis effectuez les migrations :
    
    ```bash
    python manage.py makemigrations
    ```

    Puis,

    ```bash
    python manage.py migrate
    ```
## Création Super Utilisateur 

7. Lancer avec la commande 
```terminal
python .\manage.py createsuperuser
```
    
### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec le mail exemple `admin@gmail.com`, exemple de mot de passe `Abcd.1234!`

### Applicquer les Fixtures, création de donnée pré-rempli

8. Si necessaire lancer la commande (Sinon voir point 8): 

```terminal
python manage.py flush # (if necessary)
```

9. appliquer les fixtures création de données pré rempli: 
    
```terminal
python manage.py loaddata accounts/fixtures/users.json
python manage.py loaddata events/fixtures/event_status.json
```

10. Remplir le fichier .env :
    
un fichier .env ce trouve à la racine du pojet 


```bash
.env
SECRET_KEY='METTRE VOTRE CLE SECRET'
PSQL_USER="METTRE VOTRE UTILISATEUR POSTGRESQL"
PSQL_PASSWORD="METTRE VOTRE PASSWORD POSTGRESQL"
ALGORITHM="HS256"
SIGNING_KEY="METTRE VOTRE CLE DE CHIFFREMENT ALEATOIRE"
DEBUG="True"
DSN="METTRE VOTRE CLE DSN DE SENTRY.IO"
```
NB : éditer le puis enregistrer.

11. Vous pouvez maintenant lancer le script principal avec la commande :
    
    ```bash
    python manage.py runserver
    ```

12. Vous pouvez ensuite utiliser l'applicaton à l'adresse suivante:
    
    ```bash
    http://127.0.0.1:8000/
    ```

13. Une collection postman vous est proposé avec tout les points de terminaison de API.

Fichier nommé : **P12_OCR_CRM.postman_collection à ouvrir avec postman**.

14. Les differents doits des groupes.

**Gestion** : tous les droits\
**Vente** : Retrieve, Create, Update pour Client attribués\
**Vente** : Retrieve, Create pour Event attribués\
**Vente** : Create, Retrieve, Update pour Contract attribués\
**Support** : Retrieve pour Client  attribués\
**Support** : Retrieve, Update pour Event attribués (Update until event over)\
**Suppor**t : Retrieve pour Contract
