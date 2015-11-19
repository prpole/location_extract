# coding: utf-8
import re

def remove_quotes(fname):
    with open(fname,'r') as f:
        text = f.read()
    
    quotes = re.findall('"[^"]*"',text,flags=re.DOTALL)

    for quote in quotes:
        text = text.replace(quote,'')
    return [quotes,text]


        
