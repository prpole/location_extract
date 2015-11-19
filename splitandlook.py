# coding: utf-8
import locgen
import quotextract
quotenon = quotextract.remove_quotes('wharton_ethan_frome.txt')
quotes = quotenon[0]
text = quotenon[1]
import nltk
qtokes = [nltk.tokenize.word_tokenize(x) for x in quotes ]
qtokes
qtokes[-1].append('Paris')
qtokes
ttokes = nltk.tokenize.word_tokenize(text)
ttokes
qqtokes = []
for x in qtokes:
    for y in x:
        qqtokes.append(y)
        
qqtokes
qlocs = locgen.loctag(qqtokes)
tlocs = locgen.loctag(ttokes)
qlocs
tlocs
