from fastapi import FastAPI , BackgroundTasks , HTTPException,APIRouter, Depends, status
from pydantic import BaseModel
from typing import Annotated,List
import models
from sqlalchemy.orm import Session,sessionmaker
from database import engine, SessionLocal
import upload
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from sqlalchemy import create_engine , select
from datetime import datetime
import logging  
import sys
import models
from models import Article
import json
import time

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()


app.include_router(upload.router)

models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "http://localhost:5173"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add SessionMiddleware to the app
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]






#retournant des réponses appropriées aux clients de l'API en cas d'erreur.
# logging.basicConfig(filename='app.log', level=logging.ERROR)
index_name = "index_article"
name = "variable"

# Connexion à Elasticsearch
try:
    print("***************connected to elastic ****************")
    es = Elasticsearch(['https://localhost:9200'], basic_auth=('elastic', 'Q83RH6aUu5iRMA0cODIw'), verify_certs=False)
    if not es.ping():
        raise ConnectionError("Échec de la connexion à Elasticsearch.")
except ConnectionError as e:
    logging.error(f"Erreur de connexion à Elasticsearch : {e}")
    raise HTTPException(status_code=500, detail="Erreur de connexion à Elasticsearch")
except Exception as e:
    logging.error(f"Erreur lors de l'initialisation de l'objet Elasticsearch : {e}")
    raise HTTPException(status_code=500, detail="Erreur lors de l'initialisation de l'objet Elasticsearch")




SessionLocal = sessionmaker(autocommit=False, bind=engine)

# fonction qui récupère la variable (last id) qui a été indexer 
def Récupérer_id():
     
    query = {"query": {"match_all": {}}}
    result = es.search(index = name, body=query)
    hits = result['hits']['hits']
    if hits:
        return hits[0]['_source'].get('last_indexed_id')
    else:
        return None


# Fonction pour extraire les articles avec un ID supérieur au dernier indexé
def fetch_new_articles():

    last_indexed_id = Récupérer_id()    # récupérer le id de dernier article indxé 
    db = SessionLocal()   # Créer une session de base de données
    query = db.query(Article)# Récupérer tous les articles
    if last_indexed_id is not None:   # Filtrer les résultats si un dernier ID est spécifié
        query = query.filter(Article.id > last_indexed_id)
   
    articles = query.all()  # Récupérer les articles filtrés

    # db.close()# Fermer la session de la base de données
    return articles


# Fonction pour formater les données pour Elasticsearch   
def format_articles_for_elasticsearch(new_articles):
    print('format*******')
    formatted_articles = []
    print('formated article*******')
    for article in new_articles:
        formatted_article = {
            'id': article.id,
            'titre': article.titre,
            'resume': article.resume,
            'text_integral':article.text_integral ,
            'date': article.date.strftime('%Y-%m-%d'),  # Formatage de la date au format 'YYYY-MM-DD'
            'auteur': [f"{a.nom} {a.prenom}  " for a in article.auteur],
            'refs':[j.nom for j in article.refs],
            'institutions': [i.nom for i in article.institutions],
            'motscles':[k.mot for k in article.motscles],
            'url':''
        }
        formatted_articles.append(formatted_article)
    return json.dumps(formatted_articles)



# Fonction pour indexer les données dans Elasticsearch
def index_data_in_elasticsearch(formatted_data_json):
    formatted_articles = json.loads(formatted_data_json)
    # Ensure the index exists
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name , body={"mappings": {"properties": { "id": {"type": "int"},"titre": {"type": "text"}, "resume": {"type": "text"} , "text_integral": {"type": "text"} , "date": {"type": "date","format": "yyyy-MM-dd"},  "auteur": {"type": "text"}, "refs": { "type": "text"  }, "institutions": {"type": "text"} ,"motscles": {"type": "keyword"} , "url": {"type": "text"} }
                }}, ignore=400)
       
    actions = []
    for doc in formatted_articles:
        action = {
            "index": { "_index": index_name }  # Utilisation de "index" au lieu de "_op_type"
        }
        actions.append(action)
        actions.append(doc)  # Ajoutez le document après l'action

    response = es.bulk(body=actions, index=index_name)
    
     # Mise à jour du dernier ID indexé
    if not response.get("errors"):
        last_id = formatted_articles[-1]["id"]
        # Construire le corps de la mise à jour par requête de recherche
        update_by_query_body = {
            "query": {"match_all": {}},
            "script": {
                "source": "ctx._source.last_indexed_id = params.new_value",
                "lang": "painless",
                "params": {
                    "new_value": last_id # Mettez à jour avec la valeur souhaitée
                }
            }
        }
        es.update_by_query(index=name, body=update_by_query_body) # Mettre à jour le dernier id indexé 
        time.sleep(1)

    if response.get("errors"):
        for item in response["items"]:
            if "error" in item:
                error_message = item["error"]["reason"]
                print(f"Erreur lors de l'indexation : {error_message}")
                # Traitez l'erreur ici selon vos besoins
    else:
        print("Indexation réussie.")



# Background task to  index new articles
def index_new_articles(background_tasks: BackgroundTasks ):
    
    mysql_data = fetch_new_articles()
    formatted_data = format_articles_for_elasticsearch(mysql_data)
    index_data_in_elasticsearch(formatted_data)



# Fonction pour ajouter un nouvel article à la base de données
@app.post("/add_article")
async def add_article(article, background_tasks: BackgroundTasks):
    
    # Code pour ajouter un nouvel article à la base de données
    #.....

    background_tasks.add_task(index_new_articles) # appel au fonction qui index ce nouvel article dans ElasticSearch
    return {"message": "Article ajouté avec succès."}     



# chercher dans les documents de elasticSearch le mot clé dans query 
def perform_elasticsearch_search(query: str):

    global cached_results
    cached_results = []
    
    # Construire le corps de la requête de recherche
    search_body = {
        "query": {
            "bool": {
                "should": [
                    {"match_phrase": {"titre": query}},
                    {"match_phrase": {"resume": query}},
                    {"match_phrase": {"text_integral": query}},
                    {"match_phrase": {"auteur": query}},
                    {"match_phrase": {"refs": query}},
                    {"match_phrase": {"institutions": query}},
                    {"match_phrase": {"motscles": query}}
                ]
            }
        }
    }

    # Exécuter la requête de recherche dans Elasticsearch
    search_results = es.search(index=index_name, body=search_body)
    hits = search_results["hits"]["hits"]

    formatted_results = []
    for hit in hits:
        # Extraire les champs pertinents de chaque document
        result = {
            "titre": hit['_source']['titre'],
            "resume": hit['_source'].get('resume', ''),
            "text_integral": hit['_source'].get('text_integral', ''),
            "date": hit['_source'].get('date', ''),
            "auteur": hit['_source'].get('auteur', ''),
            "refs": hit['_source'].get('refs', ''),
            "institutions": hit['_source'].get('institutions', ''),
            "motscles": hit['_source'].get('motscles', '')
        }
        formatted_results.append(result)
    cached_results.extend(formatted_results)
    return formatted_results


# Affecter une requette de recherche 
@app.get("/search/{query}")
async def search_articles(query: str):
    search_results = perform_elasticsearch_search(query)
    return {"results": search_results}


def filter_by_author(author: str):
    # Filtrer les résultats stockés dans cached_results par auteur
    filtered_results = [
        {
            "titre": result['titre'],
            "resume": result['resume'],
            "text_integral": result['text_integral'],
            "date": result['date'],
            "auteur": result['auteur'],
            "refs": result['refs'],
            "institutions": result['institutions'],
            "motscles": result['motscles'],
        }
        for result in cached_results if any(author.lower() in author_name.lower() for author_name in result['auteur'])
    ]
    return filtered_results





def filter_by_institution(institution: str):
    # Filtrer les résultats stockés dans cached_results par institution
    filtered_results = [

        {
           "titre": result['titre'],
            "resume": result['resume'],
            "text_integral": result['text_integral'],
            "date": result['date'],
            "auteur": result['auteur'],
            "refs": result['refs'],
            "institutions": result['institutions'],
            "motscles": result['motscles']

        }
        for result in cached_results if institution in result['institutions']
        
    ]
    return filtered_results


# ***filtrer les résultats de la reccherche selon date de publication 
@app.get("/filter_by_publication_date/{start_date}/{end_date}")
async def filter_by_publication_date(start_date: str, end_date: str):
    # Convertir les dates fournies en objets datetime
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    # Filtrer les résultats stockés dans cached_results entre les deux dates
    filtered_results = [
        {
            "titre": result['titre'],
            "resume": result['resume'],
            "text_integral": result['text_integral'],
            "date": result['date'],
            "auteur": result['auteur'],
            "refs": result['refs'],
            "institutions": result['institutions'],
            "motscles": result['motscles']
        }
        for result in cached_results 
        if start_date <= datetime.strptime(result['date'], "%Y-%m-%d").date() <= end_date
    ]
    return filtered_results


#***filtere les résultats de la recherche selon les mots clés 
@app.get("/filter_by_keyword/{keyword}")
async def filter_by_keyword(keyword: str):
    # Filtrer les résultats stockés dans cached_results par mot-clé dans le champ texte_integral
    filtered_results = [
        {
            "titre": result['titre'],
            "resume": result['resume'],
            "text_integral": result['text_integral'],
            "date": result['date'],
            "auteur": result['auteur'],
            "refs": result['refs'],
            "institutions": result['institutions'],
            "motscles": result['motscles']
        }
        for result in cached_results if keyword in result['motscles']
    ]
    return filtered_results




# Fonction main
try:

    print('**********m***************')
    
    # créer l'index qui sauvegarde le id de dernier article indexé 
    if not es.indices.exists(index=name):
        es.indices.create(index=name, body={"mappings": {"properties": { "last_indexed_id": {"type": "long"} } }}, ignore=400)
        document_body = {"last_indexed_id": 0}
        es.index(index=name, body=document_body)
        time.sleep(1)


    # # afficher les données récupérées de la base de données   ( optionel)
    # A = fetch_new_articles()
    # jsn = format_articles_for_elasticsearch(A)
    # index_data_in_elasticsearch(jsn)

    rech = perform_elasticsearch_search("How to Teach Software Modeling")
    for result in rech:
     print("\n\n")
     print("Titre:", result["titre"])
     print("Résumé:", result["resume"])
     print("Texte intégral:", result["text_integral"])
     print("Date:", result["date"])
     print("Auteurs:", result["auteur"])
     print("Références:", result["refs"])
     print("Institutions:", result["institutions"])
     print("Mots-clés:", result["motscles"])
     print("\n")

    print ("1******************************************************")

    for result in cached_results:
        print("Titre:", result["titre"])
        print("Résumé:", result["resume"])
        print("Text intégral:", result["text_integral"])
        print("Date:", result["date"])
        print("Auteur:", result["auteur"])
        print("Références:", result["refs"])
        print("Institutions:", result["institutions"])
        print("Mots-clés:", result["motscles"])
        print("\n")



    print ("2 ******************************************************")

    keyword = "Ed Wilson   Junior"
    filtered_results = filter_by_author(keyword)
    print("pezefjkheruf")
    for result in filtered_results:
        print("Titre:", result["titre"])
        print("Résumé:", result["resume"])
        print("Text intégral:", result["text_integral"])
        print("Date:", result["date"])
        print("Auteur:", result["auteur"])
        print("Références:", result["refs"])
        print("Institutions:", result["institutions"])
        print("Mots-clés:", result["motscles"])
        print("\n")
 


 
    
except Exception as e:
    logging.error(f"Erreur d'execution : {e}")
    raise HTTPException(status_code=500, detail="Erreur d'exec")
    
SessionLocal = sessionmaker(autocommit=False, bind=engine)







"""# La fonction main 
def main () :
    print('**********main***************')
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body={"mappings": {"properties": { "id": {"type": "int"},"titre": {"type": "text"}, "resume": {"type": "text"} , "texte_integral": {"type": "text"} , "date": {"type": "date"},  "auteurs": {"type": "keyword"}, "refs": { "type": "text"  }, "institutions": {"type": "keyword"} ,"motscles": {"type": "keyword"} }
                }}, ignore=400)
    search_body = {
    "query": {"match_all": {}}}

    # Exécution de la requête de recherche
    search_result = es.search(index=index_name, body=search_body)

    # Affichage des informations de chaque document
    for hit in search_result['hits']['hits']:
        result = hit['_source']
        print("Titre:", result.get("titre"))
        print("Résumé:", result.get("resume"))
        print("Texte intégral:", result.get("texte_integral"))
        print("Date:", result.get("date"))
        print("Auteurs:", result.get("auteurs))
"""