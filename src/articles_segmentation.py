#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 20:19:22 2021

@author: Cinthia M. Souza
"""

import os
from bs4 import BeautifulSoup
import json


def get_title(soup):

  try:
    title = soup.find('article-title')
  except AttributeError:
    title = float('nan')

  return title

def get_title_section(soup):

  try:
    title_sections = soup.findall('title')
  except AttributeError:
    title_sections = float('nan')

  return title_sections

def get_keywords(soup):

  try:
    keywords = soup.find('kwd-group')
  except AttributeError:
    keywords = float('nan')

  return keywords

def get_abstract(soup):

  try:
    abstract = soup.find('abstract')
  except AttributeError:
    abstract = float('nan')

  return abstract

def get_name_sections(soup, text=False):

    sections = []
    for i in soup.find_all('title'):
        try:
            if text:
                text = i.get_text()
                sections.append(text)
            else:
                sections.append(i)
        except ValueError:
            pass

    return sections

def rewrite_xml(file_xml, name_file, sections): 

    new_tags = []
    
    j = 0
    for i in sections:

        if j == 0:
            new_tag = "<title-{}>\n {}".format(i.get_text().replace(":", "").replace(" ", "-").lower(), i)
        else:
            new_tag = "</title-{}>\n <title-{}>\n {}".format(sections[j-1].get_text().replace(":", "").replace(" ", "-").lower(), i.get_text().replace(":", "").replace(" ", "-").lower(), i)

        
        new_tags.append(new_tag)
        file_xml = file_xml.replace(str(i), new_tag)
        j+=1
        
    new_file = open("{}/{}".format("new_xml", name_file), 'w')
    new_file.write(file_xml)
    new_file.close()

    return new_tags

def text_segmentation_single(soup):

    title = get_title(soup)
    keywords = get_keywords(soup)
    abstract = get_abstract(soup)
    
    return title, keywords, abstract


read_path = "Plos"
write_path = 'new_xml'

folders = os.listdir(read_path)
count = 0

for folder in folders:

    print(folder)
    texts = os.listdir('{}/{}'.format(read_path, folder))

    for i in texts:
    
        data = {}
        try:
            
            file_xml = open("{}/{}/{}".format(read_path, folder, i)).read()
            if file_xml.lower().find('<title>INTRODUCTION</title>'.lower()) == -1:
                file_xml = file_xml.replace("<sec id=\"S1\">"," <sec id=\"S1\">\n <title>INTRODUCTION")
                f = open("{}/{}".format(read_path, i), "w")
                f.write(file_xml)
                f.close()
    
            soup  = BeautifulSoup(open("{}/{}/{}".format(read_path, folder, i)), features="lxml")
            title, keywords, abstract = text_segmentation_single(soup)
            
            sections_text = get_name_sections(soup, text=True)
            sections_tags = get_name_sections(soup, text=False)
            
            new_tags = rewrite_xml(file_xml, i, sections_tags)
            soup  = BeautifulSoup(open("{}/{}".format(write_path, i)), features="lxml")
            
            if(sections_text != []):
            
                data['title'] = str(title)
                data['keywords'] = str(keywords)
                data['abstract'] = str(abstract)
                data['title_sections'] = list(map(str,sections_text))
                
                for j in sections_text:
                    try:
                        data[j] = str(soup.find_all("title-{}".format(j.replace(":", "").replace(" ", "-").lower()))[0])
                    except IndexError:
                        pass
                #print(data)
                try:
    
                    
                    introduction = str(soup.find_all('title-introduction')[0])
        
                    #file_sum = open('../summary/' + str(i).replace('.xml', '') + '.story', 'w')
                    #file_sum.write(abstract)
                    #file_sum.close()
    
                    #file_int = open('../text/' + str(i).replace('.xml', '') + '.story', 'w')
                    #file_int.write(introduction)
                    #file_int.close()
                    
                    with open('all_sections/' + str(i).replace('.xml', '') + '.json', 'w') as file_json:
                        
                        json.dump(data, file_json)
                    
                    count+=1
                    
                    if count % 1000 == 0:
                        print("Quantidade de arquivos processados: {}".format(count))
                except IndexError:
                    pass
        except UnicodeDecodeError:
            pass
        except AttributeError:
            pass
        except OSError:
            pass
        except TypeError:
            pass


