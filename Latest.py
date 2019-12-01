
# coding: utf-8

# In[ ]:


#import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns
import time
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float,PrimaryKeyConstraint


# Initialising the source files containing the English and Dutch Corpus'.

# In[ ]:


def make_dict_dutch(foreign_l,num_dict_dutch):
    c=1
    for i in foreign_l.keys():
        num_dict_dutch[i]=c
        c+=1
    return num_dict_dutch
        


# In[ ]:


ENG_FILE_SRC = "/media/ieshaan/Windows/Users/IESHAAN .LAPTOP-U40CT3MF/Downloads/Dataset-20191031T070748Z-001/Dataset/English.txt"
DUTCH_FILE_SRC = "/media/ieshaan/Windows/Users/IESHAAN .LAPTOP-U40CT3MF/Downloads/Dataset-20191031T070748Z-001/Dataset/Dutch.txt"


# In[ ]:


# Test Files

ENG_TEST_FILE = 'eng.txt'
DUTCH_TEST_FILE = 'dutch.txt'


# In[ ]:


# Teensy Test files

ENG_SMALL = 'English2.txt'
DUTCH_SMALL = 'Dutch2.txt'


# PROB_FILE -> Contains data of translation probabilities t(e|f).
# COUNT_FILE -> Contains data of counts c(e|f)

# In[ ]:


PROB_FILE = 'condProb.txt'
COUNT_FILE = 'count.txt'


# In[ ]:


e_file = open(ENG_SMALL,'r',encoding = 'utf-8')
d_file = open(DUTCH_SMALL,'r',encoding = 'utf-8')


# In[ ]:


dutch = d_file.readlines()
eng = e_file.readlines()


# Calculation of total number of sentences in foreign language.

# In[ ]:


total_no_of_sentences = len(dutch)


# The function given below removes all punctuation as well as numbers from the text for ease of translation.

# In[ ]:


def remove_punc(l):
    for i in range(len(l)):
        l[i] = remove_stuff(l[i])
        l[i] = l[i][:-1]
    return l


# In[ ]:


def remove_stuff(l):
    a = [ '.' , '\\' , '/' , ',' , ';' , '(' , ')' , '"', "\'",'1','2','3','4','5','6','7','8','9','0','?']
    for i in a:
        l = l.replace(i, "")
    return l


# In[ ]:


dutch2 = remove_punc(dutch)
eng2 = remove_punc(eng)


# In[ ]:


from collections import defaultdict


# Intialising the dutch and english dictionaries. **Key** -> Words and **Value** -> List of Line Numbers the words occurs in.

# In[ ]:


dutch_line_no = defaultdict(set)
eng_line_no = defaultdict(set)


# Populating the dictionary.

# In[ ]:


def assign_line_no(doc,dict_lo):
    for i in range(len(doc)):
        t = doc[i].split()
        for m in t:
            dict_lo[m].add(i)
    return dict_lo


# In[ ]:


dutch_line_no = assign_line_no(dutch2, dutch_line_no)
eng_line_no = assign_line_no(eng2, eng_line_no)


# In[ ]:


no_of_lines_eng = len(eng_line_no)
no_of_lines_dutch = len(dutch_line_no)


# In[ ]:




engine = create_engine('sqlite:///college7.db', echo = True)
meta = MetaData()

tProb = Table(
   'tProb', meta, 
   Column('english', String), 
   Column('dutch', String), 
   Column('prob', Float),
   PrimaryKeyConstraint('english', 'dutch', name='tProb')
)
meta.create_all(engine)


# In[ ]:


def initialize(foreign_no_of_words,foreign_l,english_l,num_dict_dutch,num_dict_eng):
    # probabilities = {} # Initializing proablities
    # #count = {} # Count
    # counter = 1
    # index = -1*(foreign_no_of_words)
    
    # num_dict_dutch = make_dict_dutch(foreign_l,num_dict_dutch)
    #s=0
    for i in english_l.keys():
        for j in foreign_l.keys():
            ins = tProb.insert().values(english = i, dutch= j, prob= 1/foreign_no_of_words)
            #s+=1
            #print(s/7059.85)
            conn = engine.connect()
            a=conn.execute(ins)
            #print("running")
            # s = i+"_"+j
            # probabilities[s] = 1/foreign_no_of_words
            # #count[s] = 0
        
        # index = write_to_file(probabilities,i,counter,PROB_FILE,foreign_no_of_words,index,num_dict_eng)
        # #write_to_file(count,i,counter,COUNT_FILE)
        # counter +=1
        # probabilities ={}
        
    return True
    


# In[ ]:





# In[ ]:


num_dict_eng = {}
num_dict_dutch={}


# In[ ]:


def write_to_file(probabilities,english_word,counter,file_name,foreign_no_of_words,index,num_dict_eng):
    file = open(file_name,'a')
    #file.write(str(counter)+' '+english_word+'\n')
    num_dict_eng[english_word]=index+foreign_no_of_words
    index=index+foreign_no_of_words
    #print(counter)
    for k,v in probabilities.items():
        file.write('{0} {1}\n'.format(k,v))
    file.close()
    return index


# In[ ]:


t = time.process_time()
prob = initialize(no_of_lines_dutch,dutch_line_no,eng_line_no,num_dict_dutch,num_dict_eng)
elapsed_time = time.process_time() - t
print(elapsed_time)




