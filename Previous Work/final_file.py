import time
import os
from collections import defaultdict
import sqlite3
import shutil
import json
import string

UPDATED_ENGLISH_FILE = 'English_Updated.txt'
UPDATED_DUTCH_FILE = 'Dutch_Updated.txt'

tr_etof = {}
tr_ftoe = {}

con = sqlite3.connect('TransProb_100.db')
crsr = con.cursor()

eng_data = []
dutch_data = []

eng_cleaned = []
dut_cleaned = []

total_no_of_sentences = -1

dutchWords_line_no = defaultdict(set)
engWords_line_no = defaultdict(set)


num_dict_eng = {}
num_dict_dutch = {}

total = {}


#CHECKED
def EngToDutchStopWords():
    eng_sw=['of', 'the', 'I', 'on', 'and', 'would', 'to', 'you', 'a', 'in', 'that', 'as', 'have', 'for', 'be', 'from', 'it', 'at', 'can', 'an', 'has', 'The', 'It', 'is', 'not', 'with', 'We', 'by', 'This', 'we', 'are', 'more', 'our', 'or', 'also', 'these', 'but', 'must']
    dut_sw=['van', 'de', 'ik', 'Aan', 'en', 'Zou', 'naar', 'u', 'een', 'in', 'dat', 'als', 'hebben', 'voor', 'worden', 'van', 'het', 'Bij', 'kan', 'een', 'heeft', 'De', 'Het', 'is', 'niet', 'met', 'Wij', 'door', 'Deze', 'wij', 'zijn', 'meer', 'onze', 'of', 'ook', 'deze', 'maar', 'moet']
    eng_sw = [i.lower() for i in eng_sw]
    dut_sw = [i.lower() for i in dut_sw]
    
    return (dict(zip(eng_sw, dut_sw)))

#CHECKED
def DutchToEngStopWords():
    eng_sw=['of', 'the', 'I', 'on', 'and', 'would', 'to', 'you', 'a', 'in', 'that', 'as', 'have', 'for', 'be', 'from', 'it', 'at', 'can', 'an', 'has', 'The', 'It', 'is', 'not', 'with', 'We', 'by', 'This', 'we', 'are', 'more', 'our', 'or', 'also', 'these', 'but', 'must']
    dut_sw=['van', 'de', 'ik', 'Aan', 'en', 'Zou', 'naar', 'u', 'een', 'in', 'dat', 'als', 'hebben', 'voor', 'worden', 'van', 'het', 'Bij', 'kan', 'een', 'heeft', 'De', 'Het', 'is', 'niet', 'met', 'Wij', 'door', 'Deze', 'wij', 'zijn', 'meer', 'onze', 'of', 'ook', 'deze', 'maar', 'moet']
    eng_sw = [i.lower() for i in eng_sw]
    dut_sw = [i.lower() for i in dut_sw]
    
    return (dict(zip( dut_sw,eng_sw)))


#CHECKED
def readfiles(Eng_File, Dutch_File,no_of_sentences):
    """
    Function to read required number of lines(no_of_sentences) from given text files  
    
    """
    e_file = open(Eng_File,'r',encoding = 'utf-8')
    d_file = open(Dutch_File,'r',encoding = 'utf-8')
    
    global dutch_data
    global eng_data
    dutch_data = d_file.readlines()[:no_of_sentences]
    eng_data = e_file.readlines()[:no_of_sentences]
    


#CHECKED
def remove_punc(l,lang):
    """
    Function to remove punctuation symbols from acquired sentences

    """
    
    for i in range(len(l)):
        l[i] = l[i][:-1].lower()
        l[i] = remove_stopwords(l[i],lang)
        l[i] = remove_stuff(l[i])
    return l

#CHECKED
def remove_stopwords(l,lang):
    eng_sw=['of', 'the', 'i', 'on', 'and', 'would', 'to', 'you', 'a', 'in', 'that', 'as', 'have', 'for', 'be', 'from', 'it', 'at', 'can', 'an', 'has', 'the', 'it', 'is', 'not', 'with', 'we', 'by', 'this', 'we', 'are', 'more', 'our', 'or', 'also', 'these', 'but', 'must']
    dut_sw=['van', 'de', 'ik', 'aan', 'en', 'zou', 'naar', 'u', 'een', 'in', 'dat', 'als', 'hebben', 'voor', 'worden', 'van', 'het', 'bij', 'kan', 'een', 'heeft', 'de', 'het', 'is', 'niet', 'met', 'wij', 'door', 'deze', 'wij', 'zijn', 'meer', 'onze', 'of', 'ook', 'deze', 'maar', 'moet']
    eng_sw = [i.lower() for i in eng_sw]
    dut_sw = [i.lower() for i in dut_sw]
    
    words = l.split()
    s = []
    
    if lang =='dutch':
        for i in words:
            if i not in dut_sw:
                s.append(i)
    elif lang =='eng':
        for i in words:
            if i not in eng_sw:
                s.append(i)
    return ' '.join(s)

#CHECKED    
def remove_stuff(l):
    #a = [ ':','.' , '\\' , '/' , ',' , ';' , '(' , ')' , '"', "\'",'1','2','3','4','5','6','7','8','9','0','?']
    for i in string.punctuation + string.digits:
        l = l.replace(i, "")
    return l

#CHECKED
def remove_punctuation(l):
    """
    Function to remove punctuation symbols from acquired sentences

    """
    
    for i in range(len(l)):
        l[i] = l[i][:-1].lower()
        l[i] = remove_stuff(l[i])
    return l

#CHECKED
def assign_line_no(doc):
    dict_lo = defaultdict(set)
    for i in range(len(doc)):
        t = doc[i].split()
        for m in t:
            dict_lo[m].add(i)
    return dict_lo


def make_dict_dutch(foreign_l,num_dict_dutch):
    """
    Function to create an indexed dictionary of dutch words 
    
    """
    c=1
    for i in foreign_l.keys():
        num_dict_dutch[i]=c
        c+=1
    return num_dict_dutch

def initialize(foreign_no_of_words,foreign_l,english_l,num_dict_dutch,num_dict_eng):
    """
    Function to create pairs of English and Dutch words, and initializing their probabilities uniformly
    """
    probabilities = {} # Initializing proablities
    index = -1*(foreign_no_of_words)
    counter = 0
    
    num_dict_dutch = make_dict_dutch(foreign_l,num_dict_dutch)
    init_prob = 1/foreign_no_of_words
    
    for i in english_l.keys():
        num_dict_eng[i]=index+foreign_no_of_words
        index=index+foreign_no_of_words
    
    return num_dict_dutch, num_dict_eng

def finding_probabilities():
    """
    Function to update count for each english-dutch pair
    
    """

    global total
    global eng_cleaned
    global dut_cleaned
    global total_no_of_sentences


    for i in range(total_no_of_sentences):
        
        
        en = eng_cleaned[i]
        en_words = en.split()
        

        du = dut_cleaned[i]
        du_words = du.split()
        

        retrieved_count = {}
        retrieved_term_probability = {}

        for e in en_words:

            for d in du_words:

                comm = "select * from TransProb where ENG_WORD= '{0}' AND DUT_WORD= '{1}'".format(e,d)
                com2 = "select * from Count where ENG_WORD= '{0}' AND DUT_WORD= '{1}'".format(e,d)
                #print(comm)
                #print(com2)
                
                
                crsr.execute(comm)
                ans = crsr.fetchall()
                
                crsr.execute(com2)
                an2 = crsr.fetchall()
                try:
                    line_no2= ans[0][0]+'_'+ans[0][1]+' '+str(ans[0][2])
                    line_no = an2[0][0]+'_'+an2[0][1]+' '+str(an2[0][2])
                except:
                    #print(line_no2)
                    pass
                pr = line_no.split()
                pr2 = line_no2.split()
                
                #print(pr)
                #print(pr2)
                retrieved_count[pr[0]] = float(pr[1])
                retrieved_term_probability[pr2[0]] = float(pr2[1])
              

        print("Count and Translation probabilities retrieved")
        
        #print(retrieved_term_probability)
        print()

        s_total = {}

        for e in en_words:

            s_total[e] = 0

            for d in du_words:

                s = e+'_'+d

                s_total[e] += retrieved_term_probability[s]

       #print(s_total)
        print("S_total for each english word done")
                
        for e in en_words:

            for d in du_words:

                s = e+'_'+d

                retrieved_count[s] += (retrieved_term_probability[s]/s_total[e])

                total[d] += (retrieved_term_probability[s]/s_total[e])

        print("Counts modified and Total calculated")
        #print(retrieved_count)
        print()
        print("RETRIEVED TP")
        #print(retrieved_term_probability)
        print()
        
        for k,v in retrieved_count.items():
            
            t = k.split('_')
            e = t[0]
            d = t[1]
            #print(k)
            #print(e+" "+d)
            
            command= "UPDATE Count SET PROBABILITY={0} WHERE ENG_WORD = '{1}' AND DUT_WORD ='{2}' ".format(v,e,d)
            #print(command)
            crsr.execute(command)
                
        con.commit()
        
        print("Writeback completed into count file")


def running_function(no_of_iterations=10):
    """
    Function to reinitialize total for foreign words and count for eng-dutch pairs. It carries out (no_of_iterations) iterations
    It rewrites the translational probabilities back into the CondProb file.
    """
    
    global total
    global dutchWords_line_no
    global engWords_line_no
    global total_no_of_sentences
    global dut_cleaned
    global eng_cleaned



    for c_i in range(no_of_iterations):
        
        print(c_i+1)
        
        for i in engWords_line_no.keys():
            for j in dutchWords_line_no.keys():
                command= "UPDATE Count SET PROBABILITY= {0} WHERE ENG_WORD = '{1}' AND DUT_WORD ='{2}' ".format(0,i,j)
                #print(command)
                crsr.execute(command)
            con.commit()
            
                
    
        total = {}
    
        for k in dutchWords_line_no.keys():
            total[k] = 0
    
        finding_probabilities()
    
    
        print("Finding probabilities done, ",c_i)
        retrieved_count = {}
        retrieved_term_probability = {}
    
       # print(total)
        
        
        for e in engWords_line_no.keys():
            
            for d in dutchWords_line_no.keys():
                
                com2 = "select * from Count where ENG_WORD= '{0}' AND DUT_WORD= '{1}'".format(e,d)
                #print(com2)
                crsr.execute(com2)
                ans = crsr.fetchall()
                
                try:
                    line_no = ans[0][0]+'_'+ans[0][1]+' '+str(ans[0][2])
                except:
                    print(line_no)
                
                pr = line_no.split()
                
                retrieved_count[pr[0]] = float(pr[1])
            con.commit()
        
    

        print("Counts, retrieved")
        
        print()
        #print(retrieved_count)
        print()
    
        for d in dutchWords_line_no.keys():
            for e in engWords_line_no.keys():
            
                s = e+ '_' +d
                try:
                    retrieved_term_probability[s] = retrieved_count[s]/total[d]
                except:
                    print("Error encountered,")
                    print(d,total[d])
                    #a=input("Hit to continue")
                    continue
                
                command= "UPDATE TransProb SET PROBABILITY= {0} WHERE ENG_WORD = '{1}' AND DUT_WORD ='{2}' ".format(float(retrieved_term_probability[s]),e,d)
                #print(command)
                crsr.execute(command)
                
            con.commit()
        
        print("Translational Probabilites updated")
        
        
def retrieve_max(english_l):
    """
    Function to retieve the translaton with maximum probabilities for each word to be translated, i.e. to obtain the most probable translation for each word.     
    """
    global tr_etof
    global tr_ftoe
    for e in english_l.keys():
        
        #print(e,counter)
        
        comm = "SELECT MAX(PROBABILITY),DUT_WORD From TransProb where ENG_WORD = '{0}'".format(e)
        
        crsr.execute(comm)
        
        ans = crsr.fetchall()
         
        tr_etof[e] = ans[0][1]
        tr_ftoe[ans[0][1]] = e
        
def pearson_coefficient(dut_cleaned,result_dut):
    """
    Function to find Pearson Coefficient
    """
    
    resultDutWords_line_no = assign_line_no(result_dut)
    dutchWord_line_no = assign_line_no(dut_cleaned)

    tf_of_cleaned = maintain_count(dutchWord_line_no,dut_cleaned)
    
    tf_of_result = maintain_count(resultDutWords_line_no,result_dut)
    
    avg_cleaned = statistics.mean(tf_of_cleaned.values())
    avg_result = statistics.mean(tf_of_result.values())
    
    for i in tf_of_cleaned.keys():
        total_sim += ((tf_of_cleaned[i]-avg_cleaned) * (tf_of_result[i] - avg_result))
        
    stddev_cleaned = statistics.stdev(tf_of_cleaned.values())
    stddev_result = statistics.stdev(tf_of_result.values())
    
    return total_sim/(stddev_cleaned*stddev_result)

def cosine_similarity(dut_cleaned,result_dut):
    """
    Function to find cosine similarity between 2 documents
    
    Required: Clean test data before calculating cosine_similarity
    """
    
    resultDutWords_line_no = assign_line_no(result_dut)
    dutchWord_line_no = assign_line_no(dut_cleaned)

    tf_of_cleaned = maintain_normalized_tf(dutchWord_line_no,dut_cleaned)
    
    tf_of_result = maintain_normalized_tf(resultDutWords_line_no,result_dut)
    
    total_sim = 0
    
    for i in tf_of_cleaned.keys():
        total_sim += tf_of_cleaned[i] * tf_of_result[i]
        
    return total_sim

def maintain_normalized_tf(doc_dict_line_no, data_clean):
    
    """
    Function to find normalized term-frequency of a word in a document.
    
    """
    
    og_dutch_tf = {}
    
    sum_of_tf = 0
    
    for dword in doc_dict_line_no:                #for each word in the document
        dlist=[]
        dlist=list(doc_dict_line_no[dword])
        count = 0
        for i in dlist:
            count+= dut_cleaned[i].count(dword)
        
        og_dutch_tf[dword] = math.log(count)+1
        sum_of_tf += pow(og_dutch_tf[dword],2)
    
    normalized_denom = pow(sum_of_tf,0.5)
    
    for i in og_dutch_tf.keys():
        og_dutch_tf[i] = og_dutch_tf[i]/normalized_denom

        
    return og_dutch_tf
    
def produce_sentence(eng_sentence, translated_dict,doc_lang):
    """
    Function to translate a sentence.
    """
    
    s = ""

    a = string.punctuation + string.digits
    
    for i in eng_sentence:
        if i in a:
            s+=i
            continue
            
        s += str(translated_dict[i])
    
    s+='\n'
    
    return s
        
def translate_doc(eng_doc, translated_dict, rewrite_file, doc_lang = 'eng'):
    """
    Function to translate a document.
    """
    
    result_doc = []
    
    for i in eng_doc:
        s = produce_sentence(i, translated_dict,doc_lang)
        result_doc.append(s)
    
    with open(rewrite_file,'w') as f:
        f.writelines(result_doc)
    
    return result_doc

def main():
    
    
    Eng_File = UPDATED_ENGLISH_FILE
    Dutch_File = UPDATED_DUTCH_FILE
    

    readfiles(Eng_File,Dutch_File,500)
    
    print("Files read")
    
    # Cleaning Data

    global eng_cleaned
    global dut_cleaned
    
    eng_cleaned = remove_punc(eng_data,'eng')
    dut_cleaned = remove_punc(dutch_data,'dutch')

    global total_no_of_sentences
    
    total_no_of_sentences = len(dut_cleaned)

    assert(total_no_of_sentences!=-1)
    
    print("Files cleaned")
    
    # Making dictionaries

    global dutchWords_line_no
    global engWords_line_no
    
    dutchWords_line_no = assign_line_no(dut_cleaned)
    engWords_line_no = assign_line_no(eng_cleaned)
    
    #print(dutchWords_line_no)
    
    no_of_words_eng = len(engWords_line_no)
    no_of_words_dutch = len(dutchWords_line_no)
    
    #global num_dict_eng
    #global num_dict_dutch
    
    #num_dict_dutch,num_dict_eng = initialize(no_of_words_dutch , dutchWords_line_no , engWords_line_no , num_dict_dutch , num_dict_eng)
    
    #assert(prob==True)
    
    print("Initialization Done")
    
    running_function(10)
    
    print("Model Trained")
    
    global tr_etof
    global tr_ftoe

    retrieve_max(engWords_line_no)
    
    tr_etof.update(EngToDutchStopWords())
    tr_ftoe.update(DutchToEngStopWords())
    
    print(tr_etof)
    print("\n\n\n\n")
    print(tr_ftoe)
    
    with open('etof.json','w') as fp:
        json.dump(tr_etof,fp)
    
    with open('ftoe.json','w') as fp:
        json.dump(tr_ftoe,fp)
    
    #new_doc = open(TEST_FILE,'r+')
    #lines = new_doc.readlines()
    
    #b = translate_doc(lines,tr_etof,TEST_FILE)
    
    #print(b)
    
    
    #print(tr_etof)    

if __name__ =="__main__":
    main()
