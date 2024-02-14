#here we create the tables we need in our database
from msilib import Table
from click import DateTime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, DateTime,TEXT,Date
from database import Base
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from uuid import UUID, uuid4


Base = declarative_base()

#____________________associations between tables in database____________________________________________________________________________________
article_auteur_association = Table(
    'article_auteur_association',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('article.id')),
    Column('auteur_id', Integer, ForeignKey('auteur.id'))
)

article_references_association = Table(
    'article_references_association',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('article.id')),
    Column('refs_id', Integer, ForeignKey('refs.id'))
)
article_institutions_association = Table(
    'article_institutions_association',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('article.id')),
    Column('institutions_id', Integer, ForeignKey('institutions.id'))
)
article_motscles_association = Table(
    'article_motscles_association',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('article.id')),
    Column('motscles_id', Integer, ForeignKey('motscles.id'))
)
favoris = Table(
    'favoris',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('article.id')),
    Column('user_id', Integer, ForeignKey('Users.id'))
)
#____________________associations between tables in database(article non verifie)_____________________________________________________________
articlenonverifie_auteur_association = Table(
    'articlenonverifie_auteur_association',
    Base.metadata,
    Column('articlenonverifie_id', Integer, ForeignKey('articleNonVerifie.id')),
    Column('auteur_id', Integer, ForeignKey('auteur.id'))
)
articlenonverifie_references_association = Table(
    'articlenonverifie_references_association',
    Base.metadata,
    Column('articlenonverifie_id', Integer, ForeignKey('articleNonVerifie.id')),
    Column('refs_id', Integer, ForeignKey('refs.id'))
)
articlenonverifie_institutions_association = Table(
    'articlenonverifie_institutions_association',
    Base.metadata,
    Column('articlenonverifie_id', Integer, ForeignKey('articleNonVerifie.id')),
    Column('institutions_id', Integer, ForeignKey('institutions.id'))
)
articlenonverifie_motscles_association = Table(
    'articlenonverifie_motscles_association',
    Base.metadata,
    Column('articlenonverifie_id', Integer, ForeignKey('articleNonVerifie.id')),
    Column('motscles_id', Integer, ForeignKey('motscles.id'))
)
#____________________________________________________________________________________________________________________

class Auteur(Base):
    __tablename__ = "auteur"
    id= Column(Integer, primary_key=True,index=True)
    nom = Column(String(16))
    prenom = Column(String(16))
    article_id=Column(Integer, ForeignKey('article.id'))
    article = relationship("Article", secondary=article_auteur_association, back_populates="auteur")
    articlenonverifie_id=Column(Integer,ForeignKey('articlenonverifie.id'))
    articlenonverifie = relationship("ArticleNonVerifie", secondary=articlenonverifie_auteur_association, back_populates="auteur")
    

class ArticleNonVerifie(Base):
    __tablename__ = "articleNonVerifie"
    id=Column(Integer, primary_key=True,index=True)
    titre=Column(String(2000))
    resume=Column(TEXT)
    date=Column(Date)
    text_integral=Column(TEXT)
    auteur = relationship("Auteur", secondary=articlenonverifie_auteur_association, back_populates="articlenonverifie")
    refs = relationship("References", secondary=articlenonverifie_references_association, back_populates="articlenonverifie")
    institutions = relationship("Institutions", secondary=articlenonverifie_institutions_association, back_populates="articlenonverifie")
    motscles = relationship("MotsCles", secondary=articlenonverifie_motscles_association, back_populates="articlenonverifie")
    url = relationship("Urls", uselist=False, back_populates="articlenonverifie")
class Favoritt(Base):
    __tablename__ = "favorit"
    id=Column(Integer, primary_key=True,index=True)
    id_user=Column(Integer)
    id_article=Column(Integer)

class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)
    titre = Column(String(2000))
    resume = Column(TEXT)
    date = Column(Date)
    text_integral=Column(TEXT)
    auteur = relationship("Auteur", secondary=article_auteur_association, back_populates="article")
    refs = relationship("References", secondary=article_references_association, back_populates="article")
    institutions = relationship("Institutions", secondary=article_institutions_association, back_populates="article")
    motscles = relationship("MotsCles", secondary=article_motscles_association, back_populates="article")
    url = relationship("Urls", uselist=False, back_populates="article")
    '''def __init__(self, **kwargs):
        self.auteur.update(kwargs)'''

class Urls(Base):
    __tablename__ = 'url'
    id = Column(Integer, primary_key=True)
    url=Column(String(200))
    article_id = Column(Integer, ForeignKey('article.id'))
    articlenonverifie_id = Column(Integer, ForeignKey('articleNonVerifie.id'))
    article = relationship("Article", uselist=False, back_populates="url")
    articlenonverifie = relationship("ArticleNonVerifie", uselist=False, back_populates="url")   

class Institutions(Base):
    __tablename__="institutions"
    id=Column(Integer,primary_key=True,index=True)
    nom=Column(String(200))
    article_id=Column(Integer,ForeignKey('article.id'))
    articlenonverifie_id = Column(Integer, ForeignKey('articleNonVerifie.id'))
    article = relationship("Article", secondary=article_institutions_association, back_populates="institutions")
    articlenonverifie = relationship("ArticleNonVerifie", secondary=articlenonverifie_institutions_association, back_populates="institutions")
    
class MotsCles(Base):
    __tablename__="motscles"
    id=Column(Integer,primary_key=True,index=True)
    mot=Column(String(50))
    article_id=Column(Integer,ForeignKey('article.id'))
    articlenonverifie_id=Column(Integer,ForeignKey('articleNonVerifie.id'))
    article = relationship("Article", secondary=article_motscles_association, back_populates="motscles")
    articlenonverifie = relationship("ArticleNonVerifie", secondary=articlenonverifie_motscles_association, back_populates="motscles")
    


class References(Base):
    __tablename__="refs"
    id=Column(Integer,primary_key=True,index=True)
    nom=Column(String(200))
    article_id=Column(Integer,ForeignKey('article.id'))
    articlenonverifie_id=Column(Integer,ForeignKey('articleNonVerifie.id'))
    article = relationship("Article", secondary=article_references_association, back_populates="refs")
    articlenonverifie = relationship("ArticleNonVerifie", secondary=articlenonverifie_references_association, back_populates="refs")