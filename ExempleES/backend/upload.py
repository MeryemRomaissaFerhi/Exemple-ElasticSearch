from ast import Dict, List
from fastapi import FastAPI,HTTPException,Depends,status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, List
from pydantic import BaseModel, Field, HttpUrl
import json
from fastapi import APIRouter


router = APIRouter(
    prefix='/upload',
    tags=['upload']
)

models.Base.metadata.create_all(bind=engine)
#----baseClasses------------------------------------------------------------

    
class AuteurBase(BaseModel):
    nom:str
    prenom:str


class ArticleNonVerifieBase(BaseModel):
    titre: str
    resume: str
    text_integral: str
    date: datetime
    auteur: List[AuteurBase]
    refs: List[str]
    institutions: List[str]
    motscles: List[str]
    url: str
class ArticleBase(BaseModel):
    titre: str
    resume: str
    text_integral: str
    date: datetime = Field(default_factory=datetime.now)
    auteur: List[AuteurBase]
    refs: List[str] = []
    institutions: List[str] = []
    motscles: List[str] = []
    url:str
    
article_data = ArticleBase(
    titre = "titreeee",
    resume= ",,,, uuuiiii",
    text_integral= "eeeeeeeeeeeeeeeeeeeeeeee",
    date= datetime.now(),
    auteur=[AuteurBase(nom="Nicolas",prenom="Dup")],
    refs= ["dddd","ggggg"],
    institutions= ["dddd","ggggg"],
    motscles=["dddd","ggggg"],
    url= "https://www.youtube.com/watch?v=_rDC5BAaALU"
)

class UrlsBase(BaseModel):
    url:str

class ReferencesBase(BaseModel):
    nom:str

class InstitutionsBase(BaseModel):
    nom:str

class MotsClesBase(BaseModel):
    mot:str



#----prepare our database-----------------------------------------------------
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
db_dependency=Annotated[Session,Depends(get_db)]

#                    __________________________________
#                    |post/ get/ put/ delete  methodes|
#
#-----------------------------article non verifie-----------------------------------------------------


@router.get("/articlenonverifie/{articlenonverifie_id}", status_code=status.HTTP_200_OK)
async def get_article(articlenonverifie_id: int, db: Session = Depends(get_db)):
    articlenonverifie = db.query(models.ArticleNonVerifie).\
        options(joinedload(models.ArticleNonVerifie.auteur)).\
        options(joinedload(models.ArticleNonVerifie.refs)).\
        options(joinedload(models.ArticleNonVerifie.institutions)).\
        options(joinedload(models.ArticleNonVerifie.motscles)).\
        filter(models.ArticleNonVerifie.id == articlenonverifie_id).first()
    if articlenonverifie is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return articlenonverifie

def remove_non_utf8(input_string):
   
    cleaned_string = input_string.encode('utf-8', errors='ignore').decode('utf-8')
    return cleaned_string

@router.post("/articlenonverifie/", status_code=status.HTTP_201_CREATED)
async def add_article(articlenonverifie: ArticleNonVerifieBase, db: Session = Depends(get_db)):
    auteur_data = articlenonverifie.auteur
    refs_data = articlenonverifie.refs
    institutions_data = articlenonverifie.institutions
    motscles_data = articlenonverifie.motscles
    url_data = articlenonverifie.url

  
    auteur = [models.Auteur(nom=auteur.nom, prenom=auteur.prenom) for auteur in auteur_data]
    refs = [models.References(nom=ref) for ref in refs_data]
    institutions = [models.Institutions(nom=institution) for institution in institutions_data]
    motscles = [models.MotsCles(mot=motcle) for motcle in motscles_data]
    url = models.Urls(url=url_data)

    
    articlenonverifie_db = models.ArticleNonVerifie(
        titre=remove_non_utf8(articlenonverifie.titre),
        resume=remove_non_utf8(articlenonverifie.resume),
        text_integral=remove_non_utf8(articlenonverifie.text_integral),
        date=articlenonverifie.date,
        auteur=auteur,
        refs=refs,
        institutions=institutions,
        motscles=motscles,
        url=url
    )

    
    db.add(articlenonverifie_db)
    db.commit()
    
@router.delete("/articlenonverifies/{articlenonverifie_id}",status_code=status.HTTP_200_OK)
async def delete_articlenonverifie(articlenonverifie_id:int,db: Session = Depends(get_db)):
    db_articlenonverifie=db.query(models.ArticleNonVerifie).filter(models.ArticleNonVerifie.id==articlenonverifie_id).first()
    if db_articlenonverifie is None:
        raise  HTTPException(status_code=404,detail="articlenonverifie not found")
    db.delete(db_articlenonverifie)
    db.commit()
#------------------------------articles----------------------------------------------------------------

@router.get("/article/{article_id}", status_code=status.HTTP_200_OK)
async def get_article(article_id: int, db: Session = Depends(get_db)):
    article= db.query(models.Article).\
        options(joinedload(models.Article.auteur)).\
        options(joinedload(models.Article.refs)).\
        options(joinedload(models.Article.institutions)).\
        options(joinedload(models.Article.motscles)).\
        filter(models.Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.post("/article/", status_code=status.HTTP_201_CREATED)
async def add_article(article: ArticleBase, db: Session = Depends(get_db)):
    auteur_data = article.auteur
    refs_data = article.refs
    institutions_data = article.institutions
    motscles_data = article.motscles
    url_data = article.url

    
    auteur = [models.Auteur(nom=auteur.nom, prenom=auteur.prenom) for auteur in auteur_data]
    refs = [models.References(nom=ref) for ref in refs_data]
    institutions = [models.Institutions(nom=institution) for institution in institutions_data]
    motscles = [models.MotsCles(mot=motcle) for motcle in motscles_data]
    url = models.Urls(url=url_data)

    
    article_db = models.Article(
        titre=json.dumps(article.titre),
        resume=json.dumps(article.resume),
        text_integral=json.dumps(article.text_integral),
        date=article.date,
        auteur=auteur,
        refs=refs,
        institutions=institutions,
        motscles=motscles,
        url=url
    )

    
    db.add(article_db)
    db.commit()

@router.delete("/articles/{article_id}",status_code=status.HTTP_200_OK)
async def delete_article(article_id:int,db:Session = Depends(get_db)):
    db_article=db.query(models.Article).filter(models.Article.id==article_id).first()
    if db_article is None:
        raise  HTTPException(status_code=404,detail="Admin not found")
    db.delete(db_article) 
    db.commit()
#------------------------------urls----------------------------------------
@router.get("/urls/{urls_id}",status_code=status.HTTP_200_OK)
async def read_urls(urls_id:int,db:Session = Depends(get_db)):
    urls=db.query(models.Urls).filter(models.Urls.id==urls_id).first()
    if urls is None :
        raise HTTPException(status_code=404 , detail="urls not found")
    return urls

@router.post("/urls/",status_code=status.HTTP_201_CREATED)
async def add_urls(urls:UrlsBase,db:Session = Depends(get_db)):
    db_urls=models.Urls(**urls.model_dump())
    db.add(db_urls)
    db.commit()

#------------------------------auteur----------------------------------------
@router.get("/auteur/{auteur_id}",status_code=status.HTTP_200_OK)
async def read_auteur(auteur_id:int,db:Session = Depends(get_db)):
    auteur=db.query(models.Auteur).filter(models.Auteur.id==auteur_id).first()
    if auteur is None :
        raise HTTPException(status_code=404 , detail="Auteur not found")
    return auteur

@router.post("/auteur/",status_code=status.HTTP_201_CREATED)
async def add_auteur(auteur:AuteurBase,db:Session = Depends(get_db)):
    db_auteur=models.Auteur(**auteur.model_dump())
    db.add(db_auteur)
    db.commit()

#------------------------------references----------------------------------------
@router.get("/references/{references_id}",status_code=status.HTTP_200_OK)
async def read_references(refs_id:int,db:Session = Depends(get_db)):
    refs=db.query(models.Refs).filter(models.Refs.id==refs_id).first()
    if refs is None :
        raise HTTPException(status_code=404 , detail="references not found")
    return refs

@router.post("/refrences/",status_code=status.HTTP_201_CREATED)
async def add_references(refs:ReferencesBase,db:Session = Depends(get_db)):
    db_references=models.References(**refs.model_dump())
    db.add(db_references)
    db.commit()

#------------------------------institutions----------------------------------------------------------------
@router.get("/institutions/{institutions_id}",status_code=status.HTTP_200_OK)
async def read_institutions(institutions_id:int,db:Session = Depends(get_db)):
    institutions=db.query(models.Institutions).filter(models.Institutions.id==institutions_id).first()
    if institutions is None :
        raise HTTPException(status_code=404 , detail="institutions not found")
    return institutions

@router.post("/institutions/",status_code=status.HTTP_201_CREATED)
async def add_institutions(institutions:InstitutionsBase,db:Session = Depends(get_db)):
    db_institutions=models.Institutions(**institutions.model_dump())
    db.add( db_institutions)
    db.commit()

#------------------------------motscles----------------------------------------------------------------
@router.get("/motscles/{motscles_id}",status_code=status.HTTP_200_OK)
async def read_motscles(motscles_id:int,db:Session = Depends(get_db)):
    motscles=db.query(models.MotsCles).filter(models.MotsCles.id==motscles_id).first()
    if motscles is None :
        raise HTTPException(status_code=404 , detail="motscles not found")
    return motscles

@router.post("/motscles/",status_code=status.HTTP_201_CREATED)
async def add_motscles(motscles:MotsClesBase,db:Session = Depends(get_db)):
    db_motscles=models.MotsCles(**motscles.model_dump())
    db.add( db_motscles)
    db.commit()


#-----------------------------------------------------------------------------
@router.get("/favoris/",status_code=status.HTTP_200_OK)
async def get_favoris(user_id: int,db:Session = Depends(get_db)):
    favoris=db.query(models.Favoritt).filter(models.Favoritt.id_user==user_id).all()
    if favoris is None :
        raise HTTPException(status_code=404 , detail="ARTICLE not found")
    article_ids = [fav.id_article for fav in favoris]
    return article_ids

@router.post("/{article_id}/{user_id}", status_code=status.HTTP_201_CREATED)
async def add_favorit(article_id: int, user_id: int, db: Session = Depends(get_db)):
    # Check if the article and user exist
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    user = db.query(models.users).filter(models.users.id == user_id).first()

    if not article:
        raise HTTPException(status_code=404, detail=f"Article with id {article_id} not found")

    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

    # Create and add the favorite entry
    favorit = models.Favoritt(id_user=user_id, id_article=article_id)
    db.add(favorit)
    db.commit()

    return {"message": "Favorite article added successfully"}