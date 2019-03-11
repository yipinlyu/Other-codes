# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 09:25:37 2019

@author: YIPINL
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.decomposition import LatentDirichletAllocation
from nltk.corpus import stopwords
import re
from nltk.stem import WordNetLemmatizer
import os
from datetime import date, datetime, timedelta
from sklearn.decomposition import NMF
import warnings
import xlsxwriter





warnings.filterwarnings("ignore", category=FutureWarning)
os.chdir('C:/WR/')
os.getcwd()

def text_clean(text):
    clean = re.sub(r'\d+-\d+-\d+.*Additional comments\)', '', text)
    return clean


def combine_description(sd, comments):
    if pd.isnull(comments):
        return sd
    else:
        return sd + " " + comments

df = pd.read_csv("chat_queue_entry.csv", encoding = 'cp1252')

df_no_comments = df[df['comments'].isna()].reset_index(drop = True)
df_have_comments = df.dropna(subset = ['comments']).reset_index(drop = True)

df_have_comments['combine_text'] = ""

for i in range(len(df_have_comments)):
    df_have_comments.loc[i, 'combine_text'] = combine_description(
            df_have_comments.loc[i, 'short_description'], 
            df_have_comments.loc[i, 'comments'])
       

#text = df.sample().reset_index(drop = True).loc[0,'combine_text']
content = pd.DataFrame(columns = ['time','number', 'role','sentence'])

for i in range(len(df_have_comments)):
    number = df_have_comments.loc[i, 'number']
    text = df_have_comments.loc[i, 'combine_text']
    
    chat_list = text.split("\n\n")
    
    #content = pd.DataFrame(columns = ['role','sentence'])
    
    for chat in chat_list:
        if chat != '':
            try:
                chat = chat.split("\n")
                chat_time = re.findall(r"\d+-\d+-\d+ \d+:\d+:\d+", chat[0])[0]
                chat_time = datetime.strptime(chat_time, '%m-%d-%Y %H:%M:%S')
                name = re.findall(r"\d+-\d+-\d+ \d+:\d+:\d+ - (.*) \(Additional comments\)", chat[0])[0]
                sentence = chat[1]
                content = content.append({'time':chat_time, 'number': number, 'role': name, 'sentence': sentence}, ignore_index = True)
            except IndexError:
                content.append({'time':'None' ,'number':number,'role': 'no role', 'sentence': chat[0]}, ignore_index = True)


patterns = ['I am sorry', "I did't understand", 'rephrase','error']
virtual = content[content['role'] == 'SD Virtual Analyst '].reset_index(drop = True)
client = content[content['role'] != 'SD Virtual Analyst '].reset_index(drop = True)

problems = pd.DataFrame(columns = ['number', 'time', 'sentence'])

for i in range(len(virtual)):
    flag = False
    sentence = virtual.loc[i, 'sentence']
    for pattern in patterns:
        if pattern in sentence:
            flag = True
    if flag:
        problems = problems.append({'number':virtual.loc[i, 'number'],'time': virtual.loc[i, 'time'], 'sentence': sentence}, ignore_index = True)
   

problem_list = pd.unique(problems['number'])   
problem_contents = content[content['number'].isin(problem_list)]


problems.to_csv("breakpoints.csv", index = False)
problem_contents.to_csv("problem_contents.csv", index = False)



problem_contents = pd.read_csv("problem_contents.csv")




 # Create a workbook and add a worksheet.
 workbook = xlsxwriter.Workbook('contents.xlsx')
 worksheet = workbook.add_worksheet()
 problem_format = workbook.add_format({'bold': True, 'font_color': 'red'})
 # Add a bold format to use to highlight cells.
 bold = workbook.add_format({'bold': 1})

 # Add a number format for cells with money.
 money_format = workbook.add_format({'num_format': '$#,##0'})

 # Add an Excel date format.
 date_format = workbook.add_format({'num_format': 'dd/mm/yy hh:mm:ss'})

 # Adjust the column width.
 worksheet.set_column(1, 1, 15)

 # Write some data headers.

 worksheet.write('A1', 'number', bold)
 worksheet.write('B1', 'time', bold)
 worksheet.write('C1', 'role', bold)
 worksheet.write('D1', 'sentence', bold)
 
 # Start from the first cell below the headers.
 row = 1
 col = 0

 for i in (range(len(problem_contents))):
     
     number = problem_contents.loc[i, 'number']
     chat_time = problem_contents.loc[i, 'time']
     chat_time = datetime.strptime(chat_time, '%Y-%m-%d %H:%M:%S')
     role = problem_contents.loc[i, 'role']
     sentence = problem_contents.loc[i, 'sentence']
     # Convert the date string into a datetime object.

     worksheet.write_string  (row, col,     number             )
     worksheet.write_datetime(row, col + 1, chat_time, date_format )
     worksheet.write_string  (row, col + 2, role )
     for pattern in patterns:
         flag = False
         if pattern in sentence and role == "SD Virtual Analyst ":
             flag = True
     if flag:
         worksheet.write_string  (row, col + 3, sentence , problem_format)
     else:
         worksheet.write_string  (row, col + 3, sentence )
     row += 1

 # Write a total using a formula.
 workbook.close()



