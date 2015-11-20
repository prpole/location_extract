# coding: utf-8
import nltk
from nltk.tag.stanford import StanfordNERTagger
from geopy.geocoders import Nominatim
import re
from time import sleep
import csv

st = StanfordNERTagger('/home/prpole/Tech/stanford-ner-2015-04-20/classifiers/english.all.3class.distsim.crf.ser.gz','/home/prpole/Tech/stanford-ner-2015-04-20/stanford-ner.jar')

def loctag(tokes):
    tagged = st.tag(tokes)
    #locations = [ x[0] for x in tagged if x[1] == 'LOCATION' ]
    locations = []
    stopwords = ['Bank','Street','Railroad', 'Avenue','Lane']
    #manually iterating to facilitate multi-word location token grouping
    counter = 0 
    while counter < len(tagged):
        allword = []
        if tagged[counter][1] == 'LOCATION':
            allword.append(tagged[counter][0])
            position = 1
            while True:
                if tagged[counter+position][1] == 'LOCATION':
                    allword.append(tagged[counter+position][0])
                    position += 1
                else:
                    break
            counter += position
            if any([ x in stopwords for x in allword ]):
                pass
            else:
                fullloc = ' '.join(allword)
                locations.append(fullloc)
        else:
            counter += 1


    return locations

def loclook(locations):
    geocator = Nominatim(timeout=3)
    
    ### Note: no comprehension to allow for 1 sec sleep
    #coordinates = [ geocator.geocode(x) 
    #                for x in locations
    #                if geocator.geocode(x) != None ]

    coordinates = {}

    unilocs = list(set(locations))

    for location in locations:
        try:
            geo = geocator.geocode(location)
            if geo != None:
                coordinates[location] = (geo.latitude,geo.longitude)
            else:
                coordinates[location] = (0.0,0.0)
        except:
            pass
        sleep(1)

    return coordinates.items()

def separate_quotes(text):
    #with open(fname,'r') as f:
    #    text = f.read()
    
    quotes = re.findall('"[^"]*"',text,flags=re.DOTALL)

    for quote in quotes:
        text = text.replace(quote,'')
    return [quotes,text]

def plot_quotes_vs_text(fname):
    with open(fname,'r') as f:
        text = f.read().decode(encoding='utf-8',errors='ignore')
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
    write_coords([qcords,tcords],fname)

    return [qcords,tcords]

def write_coords(coords,textname):
    with open(textname+'quotes.csv','w') as f:
        cwrite = csv.writer(f)
        cwrite.writerow(['name','latitude','longitude'])
        for x in coords[0]:
            cwrite.writerow([x[0],x[1][0],x[1][1]])
    with open(textname+'narr.csv','w') as f:
        cwrite = csv.writer(f)
        cwrite.writerow(['name','latitude','longitude'])
        for x in coords[1]:
            cwrite.writerow([x[0],x[1][0],x[1][1]])


