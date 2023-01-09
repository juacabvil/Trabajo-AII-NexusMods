from app.models import Game,Mod,Colection

from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, KEYWORD, DATETIME, ID, STORED, NUMERIC
from whoosh.qparser import QueryParser
from whoosh import query
import re, os, shutil
from whoosh import scoring

def crearIndex():
    schemMod = Schema(name=TEXT(stored=True,phrase=False), 
                    last_update=DATETIME(stored=True), 
                    uploader=TEXT(stored=True), 
                    description =TEXT(stored=True), 
                    likes=NUMERIC(stored=True), 
                    category=KEYWORD(stored=True,scorable=True), 
                    game = TEXT(stored=True))
    
    if os.path.exists("Index"):
        shutil.rmtree("Index")
    os.mkdir("Index")
    ix = create_in("Index", schema=schemMod, indexname='Mods')
    writer = ix.writer()
    i=0
    lista=Mod.objects.all()
    for m in lista:
        writer.add_document(name=str(m.name), 
                            last_update=str(m.last_update), 
                            uploader=str(m.uploader), 
                            description=str(m.description), 
                            likes=m.likes, 
                            category=str(m.category),
                            game = str(m.game.name))    
        i+=1
    writer.commit()

    schemColection = Schema(name=TEXT(stored=True,phrase=False), 
                    downloads=NUMERIC(stored=True), 
                    likes=NUMERIC(stored=True), 
                    mods =NUMERIC(stored=True), 
                    game = TEXT(stored=True))

    ixC = create_in("Index", schema=schemColection, indexname='Colections')
    writer = ixC.writer()
    j=0
    lista=Colection.objects.all()
    for c in lista:
        writer.add_document(name=str(c.name), 
                            downloads=c.downloads, 
                            likes=c.likes, 
                            mods=c.mods, 
                            game=str(m.game.name))   
        j+=1
    writer.commit()

    print('indexados '+ str(i) +'mods y ' + str(j) +' colecciones')

def buscarMods(input):
    ix=open_dir("Index",indexname='Mods')      
    with ix.searcher(weighting=scoring.Frequency) as searcher:
        query = QueryParser("description", ix.schema).parse(str(input))
        results = searcher.search(query,limit=5)
        output = [(result['name'],result['game'])  for result in results]
        print(output)
        return output

def buscarColecciones(input):
    ix=open_dir("Index",indexname="Colections")      
    with ix.searcher(weighting=scoring.Frequency) as searcher:
        query = QueryParser("name", ix.schema).parse(str(input))
        results = searcher.search(query,limit=5)
        output = [(result['name'],result['game'])  for result in results]
        print(output)
        return output
        

