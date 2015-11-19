# coding: utf-8
import nltk
from nltk.tag.stanford import NERTagger

with open('wharton_ethan_frome.txt','r') as f:
    raw = f.read()
    
st = NERTagger("/Users/phillippolefrone/Downloads/stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz","/Users/phillippolefrone/Downloads/stanford-ner-2014-06-16/stanford-ner.jar")
tokes = nltk.tokenize.word_tokenize(raw)
st.tag(tokes)
NERs = st.tag(tokes)
locations = []
for sentence in NERs:
    for word in sentence:
        if word[1] == 'LOCATION':
            locations.append(word[0])

print locations
