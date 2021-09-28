#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 20:05:10 2021

@author: Cinthia M. Souza
"""

import os
import re
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import json

stemmer= PorterStemmer()

nltk.download('stopwords')
nltk.download('punkt')
stopwords = stopwords.words('english')

def remove_noise(text):

  #Remove "\n" da string
  text = text.replace("\n"," ")
  text = text.replace("\\n"," ")
  text = text.lower()
  text = text.strip()

  return text


def remove_noise_keys(text):

  #Remove "\n" da string
  text = text.replace("\n"," ")
  text = text.replace("\\n"," ")
  text = re.sub('^([IVXLCM]+)\\.?$', '', text)
  text = text.lower()
  text = re.sub('(.)\\1{1,}', '',text)
  text = re.sub(r'(?<!\w)([a-z])\.', '', text)
  text = re.sub(r'((\d+)[\.])(?!([\d]+))', '', text)
  text = text.replace(".","")
  text = text.strip()

  return text

def vectorize_remove_noise_keys(array, columns_name=['title', 'abstract', 'introduction', 'materials', 'results', 'conclusion']):

    try:
        vfunc = np.vectorize(remove_noise_keys)
        array = vfunc(array)
        return array
    except ValueError:
        pass

def vectorize_remove_noise(array, columns_name=['title', 'abstract', 'introduction', 'materials', 'results', 'conclusion']):

    try:
        vfunc = np.vectorize(remove_noise)
        array = vfunc(array)
        return array
    except ValueError:
        pass
    
def stemming(text):

    result = [stemmer.stem(i)for i in word_tokenize(text) if not i in stopwords]

    return " ".join(result)

def vectorize_stemming(array, columns_name=['title', 'abstract', 'introduction', 'materials', 'results', 'conclusion']):

  vfunc = np.vectorize(stemming)
  array = vfunc(array)

  return array

def get_sections (text, dictionary, list_keys_preprocess, list_keys):

    section = []

    for i in list(dictionary.keys()):

        try:
            key = list_keys[list_keys_preprocess.index(i)]

            section.append(text[key])
        except ValueError:
            pass

    return " ".join (section)

def get_methods (text, method_dict, conclusion_dict, pp_keys, list_keys):

    section = []
    aux = []
    check = False

    for i in pp_keys:
        
        if i in method_dict.keys():
            check = True

        if (i in conclusion_dict.keys() and check == True):
            break
        elif i == 'acknowledg' or i == 'supplementari materi' or i == 'refer':
            break
        elif not i in conclusion_dict.keys() and check == True:
            aux.append(i)

    for i in aux:
        try:
            key = list_keys[pp_keys.index(i)]
            section.append(text[key])
        except ValueError:
            pass

    return " ".join (section)

def get_conclusion (text, method_dict, conclusion_dict, pp_keys, list_keys):

    section = []
    aux = []
    check = False

 
    for i in pp_keys:
        
        if i in conclusion_dict.keys():
            check = True

        if (i in method_dict.keys() and check == True):
            break
        elif i == 'acknowledg' or i == 'supplementari materi' or i == 'refer':
            break
        elif not i in method_dict.keys() and check == True:
            aux.append(i)

    for i in aux:
        try:
            key = list_keys[pp_keys.index(i)]
            section.append(text[key])
        except ValueError:
            pass

    return " ".join (section)

def get_keys(text):

    keys = list(text.keys())

    cont = 0
    indice = 0
    for i in keys:
        if i.lower() == 'introduction':
            indice = cont
        cont+=1


    keys = keys[indice:]
    pp_keys = vectorize_remove_noise_keys(keys)
    pp_keys = vectorize_stemming(pp_keys)
    pp_keys = list(pp_keys)

    return keys, pp_keys

title_dict = {'titl': 'title'}
keyword_dict = {'keyword': 'keywords'}
abstract_dict = {'abstract': 'abstract'}
introduction_dict = {'introduct': 'introduction'}
method_dict = {'method': 'materials and methods', "materi": 'materials and methods', 'materi method': 'materials and methods'}
conclusion_dict = {'result': 'conclusion', 'discuss': 'conclusion', 'conclus': 'conclusion', 'result discuss':'conclusion'}


path =  "all_sections"

articles = os.listdir(path)

step = 0

for i in articles[:]:

    f = open(path +"/" + i) 
    text = json.load(f)

    try:
        keys, pp_keys = get_keys(text)

        title  = text['title']
        keyword  = text['keywords']
        abstract  = text['abstract']
        title_sections = text['title_sections']
        
        introduction  = text[keys[pp_keys.index('introduct')]]

        keys = keys[1:]
        pp_keys = pp_keys[1:]

        methods = get_methods (text, method_dict, conclusion_dict, pp_keys, keys)
        conclusion  = get_conclusion (text, method_dict, conclusion_dict, pp_keys, keys)


        if methods != '' and conclusion != '' and  introduction != '':
            
            data = {'sec_title': title, 'sec_keyword': keyword, 'title_sections':title_sections, 'sec_abstract': abstract, 'sec_introduction':introduction, 'sec_materials_and_methods': methods, 'sec_results_and_conclusion': conclusion}

            with open("{}/{}".format("dataset_articles", i), "w") as outfile: 
                json.dump(data, outfile)

           # with open("{}/{}".format("articles_summ", i.replace(".json", ".story")), "w") as outfile: 
           #     outfile.write("@target {}\n\n @source_introduction {}\n\n @source_methods {}\n\n @source_conclusion {}".format(abstract, introduction, methods, conclusion)) 
            
            step +=1

        if step %1000 == 0:
            print("Quantidade de arquivos processados: {}".format(step))
    except: 
        pass
    

re.sub('(.)\\1{2,}', '', 'iiii i')