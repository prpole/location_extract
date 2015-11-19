# coding: utf-8
import nltk
from nltk.tag.stanford import StanfordNERTagger
from geopy.geocoders import Nominatim

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

