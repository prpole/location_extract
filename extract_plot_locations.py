# coding: utf-8
import nltk
from nltk.tag.stanford import StanfordNERTagger
from geopy.geocoders import Nominatim
import re

st = StanfordNERTagger('/home/prpole/Tech/stanford-ner-2015-04-20/classifiers/english.all.3class.distsim.crf.ser.gz', '/home/prpole/Tech/stanford-ner-2015-04-20/stanford-ner.jar')

def loctag(tokes):
    tagged = st.tag(tokes)
    locations = [ x[0] for x in tagged if x[1] == 'LOCATION' ]
    return locations

def loclook(locations):
    geocator = Nominatim()
    coordinates = [ geocator.geocode(x) 
                    for x in locations
                    if geocator.geocode(x) != None ]
    cleancords = [ (x.latitude,x.longitude)
                    for x in coordinates ]
    return cleancords

def separate_quotes(text):
    #with open(fname,'r') as f:
    #    text = f.read()
    
    quotes = re.findall('"[^"]*"',text,flags=re.DOTALL)

    for quote in quotes:
        text = text.replace(quote,'')
    return [quotes,text]

def plot_quotes_vs_text(text):
    septext = separate_quotes(text)
    quotes = septext[0]
    nqtext = septext[1]
    qtokeslist = [ nltk.tokenize.word_tokenize(x) for x in quotes ]
    qtokes = []
    for x in qtokeslist:
        for y in x:
            qtokes.append(y)
    ttokes = nltk.tokenize.word_tokenize(nqtext)

    qlocs = loctag(qtokes)
    tlocs = loctag(ttokes)
    
    qcords = loclook(qlocs)
    tcords = loclook(tlocs)

    return [qcords,tcords]

 

