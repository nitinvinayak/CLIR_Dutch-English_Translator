
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


import time
import os


# Initialising the source files containing the English and Dutch Corpus'.

# In[3]:


def make_dict_dutch(foreign_l,num_dict_dutch):
    c=1
    for i in foreign_l.keys():
        num_dict_dutch[i]=c
        c+=1
    return num_dict_dutch
        


# In[4]:


ENG_FILE_SRC = "/media/ieshaan/Windows/Users/IESHAAN .LAPTOP-U40CT3MF/Downloads/Dataset-20191031T070748Z-001/Dataset/English.txt"
DUTCH_FILE_SRC = "/media/ieshaan/Windows/Users/IESHAAN .LAPTOP-U40CT3MF/Downloads/Dataset-20191031T070748Z-001/Dataset/Dutch.txt"


# In[5]:


# Test Files

ENG_TEST_FILE = 'eng.txt'
DUTCH_TEST_FILE = 'dutch.txt'


# In[6]:


# Teensy Test files

ENG_SMALL = 'small_eng.txt'
DUTCH_SMALL = 'small_dutch.txt'


# PROB_FILE -> Contains data of translation probabilities t(e|f).
# COUNT_FILE -> Contains data of counts c(e|f)

# In[7]:


PROB_FILE = 'condProb.txt'
COUNT_FILE = 'count.txt'


# In[8]:


e_file = open(ENG_SMALL,'r',encoding = 'utf-8')
d_file = open(DUTCH_SMALL,'r',encoding = 'utf-8')


# In[9]:


dutch = d_file.readlines()
eng = e_file.readlines()


# In[10]:


dutch


# In[11]:


eng


# Calculation of total number of sentences in foreign language.

# In[12]:


total_no_of_sentences = len(dutch) - 1


# In[13]:


print(total_no_of_sentences)


# The function given below removes all punctuation as well as numbers from the text for ease of translation.

# In[14]:


def remove_punc(l):
    for i in range(len(l)):
        l[i] = remove_stuff(l[i])
        l[i] = l[i][:-1].lower()
    return l


# In[15]:


def remove_stuff(l):
    a = [ '.' , '\\' , '/' , ',' , ';' , '(' , ')' , '"', "\'",'1','2','3','4','5','6','7','8','9','0','?']
    for i in a:
        l = l.replace(i, "")
    return l


# In[16]:


dutch2 = remove_punc(dutch)[:-1]
eng2 = remove_punc(eng)[:-1]


# In[17]:


dutch2


# In[18]:


eng2


# In[19]:


from collections import defaultdict


# Intialising the dutch and english dictionaries. **Key** -> Words and **Value** -> List of Line Numbers the words occurs in.

# In[20]:


dutch_line_no = defaultdict(set)
eng_line_no = defaultdict(set)


# Populating the dictionary.

# In[21]:


def assign_line_no(doc,dict_lo):
    for i in range(len(doc)):
        t = doc[i].split()
        for m in t:
            dict_lo[m].add(i)
    return dict_lo


# In[22]:


dutch_line_no = assign_line_no(dutch2, dutch_line_no)
eng_line_no = assign_line_no(eng2, eng_line_no)


# In[23]:


no_of_lines_eng = len(eng_line_no)
no_of_lines_dutch = len(dutch_line_no)


# In[24]:


print(dutch_line_no)
print()
print(eng_line_no)


# In[25]:


def initialize(foreign_no_of_words,foreign_l,english_l,num_dict_dutch,num_dict_eng):
    probabilities = {} # Initializing proablities
    #count = {} # Count
    counter = 1
    index = -1*(foreign_no_of_words)
    
    num_dict_dutch = make_dict_dutch(foreign_l,num_dict_dutch)

    for i in english_l.keys():
        for j in foreign_l.keys():
            s = i+"_"+j
            probabilities[s] = 1/foreign_no_of_words
            #count[s] = 0
        
        index = write_to_file(probabilities,i,counter,PROB_FILE,foreign_no_of_words,index,num_dict_eng)
        #write_to_file(count,i,counter,COUNT_FILE)
        counter +=1
        probabilities ={}
        
    return True
    


# In[26]:


num_dict_eng = {}
num_dict_dutch={}


# In[27]:


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


# In[28]:


t = time.process_time()
prob = initialize(no_of_lines_dutch,dutch_line_no,eng_line_no,num_dict_dutch,num_dict_eng)
elapsed_time = time.process_time() - t
print(elapsed_time)


# In[29]:


def finding_probabilities(dutch_sentences, eng_sentences,no_of_sentences,total):
    
    for i in range(no_of_sentences):
        
        
        en = eng_sentences[i]
        en_words = en.split()
        
        for j in range(no_of_sentences):
        
            du = dutch_sentences[j]

            du_words = du.split()

            # To already retrieve the count

            retrieved_count = {}
            retrieved_term_probability = {}

            f = open(COUNT_FILE,'r+')
            f2 = open(PROB_FILE,'r+')

            lines = f.readlines()
            lines2 = f2.readlines()

            #print(len(lines))
            #print(len(lines2))

            print(du)
            print(en)
            print()

            for e in en_words:

                for d in du_words:


                    eng_line_no = num_dict_eng[e]
                    dutch_line_no = num_dict_dutch[d]

                    #print("English",e,eng_line_no)
                    #print("Dutch",d,dutch_line_no)

                    line_no = lines[eng_line_no + dutch_line_no-1]
                    line_no2 = lines2[eng_line_no + dutch_line_no-1]

                    #print(line_no," ",line_no2)
                    pr = line_no.split()
                    pr2 = line_no2.split()
                    #print(pr,pr2)

                    retrieved_count[pr[0]] = float(pr[1])
                    retrieved_term_probability[pr2[0]] = float(pr2[1])
                    #break
                #break


            f.close()
            f2.close()


            #stop_2 = input("Calculated to Translation Probability & Retrieved Count")

            s_total = {}

            for e in en_words:

                s_total[e] = 0

                for d in du_words:

                    s = e+'_'+d

                    #print(s,e)

                    s_total[e] += retrieved_term_probability[s]


            for e in en_words:

                for d in du_words:

                    s = e+'_'+d

                    retrieved_count[s] += (retrieved_term_probability[s]/s_total[e])

                    total[d] += (retrieved_term_probability[s]/s_total[e])

            # Re-Write into the count_file

            #print()
            #print(retrieved_count)
            #print()
            #print(total)

            #temp = input("Counts modified Again")

            f = open(COUNT_FILE,'r+')

            m = f.readlines()

            for k,v in retrieved_count.items():

                t = k.split('_')

                eng_line_no=num_dict_eng[t[0]]
                dutch_line_no = num_dict_dutch[t[1]]

                final_line_no = eng_line_no + dutch_line_no

                m[final_line_no-1] = '{0} {1}\n'.format(k,v)

            f.close()

            with open(COUNT_FILE,'w') as file:
                file.writelines(m)

            #s = input("Iteration Complete: ")

        
    return total
        
    


# In[30]:


#finding_probabilties(dutch,eng,total_no_of_sentences)


# In[31]:


def running_function(foreign_l, english_l, dutch_sentences, eng_sentences, no_of_sentences,no_of_iterations = 2):
    
    for _ in range(no_of_iterations):
    
        count = {}
        counter = 1
        for i in english_l.keys():
            for j in foreign_l.keys():
                s = i+"_"+j
                count[s] = 0
            
            write_to_file2(count,i,counter,COUNT_FILE,'a')
            counter += 1
            count = {}
        
        #stopper = input("Count has been initialized")
    
    
        total = {}
    
        for k in foreign_l.keys():
            total[k] = 0
    
        #stopper_2 = input("Total has been initialized")
        
        total = finding_probabilities(dutch_sentences,eng_sentences,no_of_sentences,total)
    
        f = open(COUNT_FILE,'r+')
        f2 = open(PROB_FILE,'r+')
    
        retrieved_count = {}
        retrieved_term_probability = {}
    
        
        lines = f.readlines()
        lines2 = f2.readlines()
        
        for e in english_l.keys():
            
            for d in foreign_l.keys():
                
                eng_line_no = num_dict_eng[e]
                dutch_line_no = num_dict_dutch[d]
                
                line_no = lines[eng_line_no + dutch_line_no-1]
            #line_no2 = lines2[eng_line_no + dutch_line_no-1]
                
                pr = line_no.split()
            #pr2 = line_no2.split()
                
                retrieved_count[pr[0]] = float(pr[1])
            #retrieved_term_probability[pr2[0]] = float(pr2[1])
                
        f.close()         
        f2.close()

    
    
        for d in foreign_l.keys():
            for e in english_l.keys():
            
                s = e+ '_' +d
                retrieved_term_probability[s] = retrieved_count[s]/total[d]  
            
                eng_line_no = num_dict_eng[e]
                dutch_line_no = num_dict_dutch[d]
            
                final_line_no = eng_line_no + dutch_line_no
            
                lines2[final_line_no-1] = '{0} {1}\n'.format(s,retrieved_term_probability[s])
    
        print(lines2)
            
        with open(PROB_FILE,'w') as f:
            f.writelines(lines2)
    
        os.remove('count.txt')
        
        c = input("Iteration Completed")
            
    


# In[ ]:


t = time.process_time()
running_function(dutch_line_no,eng_line_no,dutch2,eng2,total_no_of_sentences)
elapsed_time = time.process_time() - t
print(elapsed_time)


# In[35]:


def write_to_file2(probabilities,english_word,counter,file_name,mode = 'a'):
    file = open(file_name,mode)
    #file.write(str(counter)+' '+english_word+'\n')
    for k,v in probabilities.items():
        file.write('{0} {1}\n'.format(k,v))
    file.close()


# In[32]:


#num_dict_eng


# In[33]:


#num_dict_dutch


# In[ ]:


def retrieve_max(foreign_l,english_l,no_of_dutch_words):
    
    translation = {}
    
    f = open(COUNT_FILE,'r+')
    
    lines = f.readlines()
    
    print(len(lines))
    
    counter = 1
    
    for e in english_l.keys():
        
        print(e,counter)
        eng_line_no = num_dict_eng[e]
        
        m = -1
        
        min_number = eng_line_no+1
        max_number = eng_line_no+no_of_dutch_words+1
        
        print(min_number,max_number)
        
        for i in range(min_number,max_number):
            
            t = lines[i-1]
            
            k = t.split()
            val = float(k[1])
            
            if(m < val):
                bi_word = k[0].split('_')
                dutch_word = bi_word[1]
                translation[e] = dutch_word
                m = val    
        
        counter+=1
    f.close()
    
    return translation
            
            
            
        


# In[ ]:


t = time.process_time()
tr = retrieve_max(dutch_line_no,eng_line_no,len(num_dict_dutch))
elapsed_time = time.process_time() - t
print(elapsed_time)


# In[ ]:


tr

