import time
import os
from collections import defaultdict
import sqlite3
import shutil

UPDATED_ENGLISH_FILE = 'English_Updated.txt'
UPDATED_DUTCH_FILE = 'Dutch_Updated.txt'
ENG_TEST_FILE = 'eng.txt'
DUTCH_TEST_FILE = 'dutch.txt'
con = sqlite3.connect('TransProb.db')
crsr = con.cursor()
tr_etof = {}
tr_ftoe = {}
PROB_FILE = 'condProb.txt'
COUNT_FILE = 'count.txt'

def EngToDutchStopWords():
    eng_sw=['of', 'the', 'I', 'on', 'and', 'would', 'to', 'you', 'a', 'in', 'that', 'as', 'have', 'for', 'be', 'from', 'it', 'at', 'can', 'an', 'has', 'The', 'It', 'is', 'not', 'with', 'We', 'by', 'This', 'we', 'are', 'more', 'our', 'or', 'also', 'these', 'but', 'must']
    dut_sw=['van', 'de', 'ik', 'Aan', 'en', 'Zou', 'naar', 'u', 'een', 'in', 'dat', 'als', 'hebben', 'voor', 'worden', 'van', 'het', 'Bij', 'kan', 'een', 'heeft', 'De', 'Het', 'is', 'niet', 'met', 'Wij', 'door', 'Deze', 'wij', 'zijn', 'meer', 'onze', 'of', 'ook', 'deze', 'maar', 'moet']
    eng_sw = [i.lower() for i in eng_sw]
    dut_sw = [i.lower() for i in dut_sw]    
    return (dict(zip(eng_sw, dut_sw)))

def DutchToEngStopWords():
    eng_sw=['of', 'the', 'I', 'on', 'and', 'would', 'to', 'you', 'a', 'in', 'that', 'as', 'have', 'for', 'be', 'from', 'it', 'at', 'can', 'an', 'has', 'The', 'It', 'is', 'not', 'with', 'We', 'by', 'This', 'we', 'are', 'more', 'our', 'or', 'also', 'these', 'but', 'must']
    dut_sw=['van', 'de', 'ik', 'Aan', 'en', 'Zou', 'naar', 'u', 'een', 'in', 'dat', 'als', 'hebben', 'voor', 'worden', 'van', 'het', 'Bij', 'kan', 'een', 'heeft', 'De', 'Het', 'is', 'niet', 'met', 'Wij', 'door', 'Deze', 'wij', 'zijn', 'meer', 'onze', 'of', 'ook', 'deze', 'maar', 'moet']
    eng_sw = [i.lower() for i in eng_sw]
    dut_sw = [i.lower() for i in dut_sw]   
    return (dict(zip( dut_sw,eng_sw)))

def readfiles(Eng_File, Dutch_File,no_of_sentences):
    e_file = open(Eng_File,'r',encoding = 'utf-8')
    d_file = open(Dutch_File,'r',encoding = 'utf-8')    
    dutch = d_file.readlines()[:no_of_sentences]
    eng = e_file.readlines()[:no_of_sentences]    
    return eng, dutch

def remove_punc(l,lang):
    for i in range(len(l)):
        l[i] = l[i][:-1].lower()
        l[i] = remove_stopwords(l[i],lang)
        l[i] = remove_stuff(l[i])
    return l

def remove_stopwords(l,lang):
    eng_sw=['of', 'the', 'i', 'on', 'and', 'would', 'to', 'you', 'a', 'in', 'that', 'as', 'have', 'for', 'be', 'from', 'it', 'at', 'can', 'an', 'has', 'The', 'It', 'is', 'not', 'with', 'We', 'by', 'This', 'we', 'are', 'more', 'our', 'or', 'also', 'these', 'but', 'must']
    dut_sw=['van', 'de', 'ik', 'Aan', 'en', 'cou', 'naar', 'u', 'een', 'in', 'dat', 'als', 'hebben', 'voor', 'worden', 'van', 'het', 'Bij', 'kan', 'een', 'heeft', 'De', 'Het', 'is', 'niet', 'met', 'Wij', 'door', 'Deze', 'wij', 'zijn', 'meer', 'onze', 'of', 'ook', 'deze', 'maar', 'moet']
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
    
def remove_stuff(l):
    a = [ ':','.' , '\\' , '/' , ',' , ';' , '(' , ')' , '"', "\'",'1','2','3','4','5','6','7','8','9','0','?']
    for i in a:
        l = l.replace(i, "")
    return l

def remove_punctuation(l,lang):
    for i in range(len(l)):
        l[i] = l[i][:-1].lower()
        l[i] = remove_stuff(l[i])
    return l
	
def assign_line_no(doc):
    dict_lo = defaultdict(set)
    for i in range(len(doc)):
        t = doc[i].split()
        for m in t:
            dict_lo[m].add(i)
    return dict_lo

def make_dict_dutch(foreign_l,num_dict_dutch):
    c=1
    for i in foreign_l.keys():
        num_dict_dutch[i]=c
        c+=1
    return num_dict_dutch

def initialize(foreign_no_of_words,foreign_l,english_l,num_dict_dutch,num_dict_eng):
    probabilities = {} # Initializing proablities
    index = -1*(foreign_no_of_words)
    counter = 0    
    num_dict_dutch = make_dict_dutch(foreign_l,num_dict_dutch)
    init_prob = 1/foreign_no_of_words    
    for i in english_l.keys():
        num_dict_eng[i]=index+foreign_no_of_words
        index=index+foreign_no_of_words    
    return num_dict_dutch, num_dict_eng

def write_to_file(probabilities,english_word,counter,file_name,foreign_no_of_words,index,num_dict_eng):
	return index, num_dict_eng

def finding_probabilities(dutch_sentences, eng_sentences,no_of_sentences,total,num_dict_dutch,num_dict_eng,count_file):    
    for i in range(no_of_sentences):        
        en = eng_sentences[i]
        en_words = en.split()
        du = dutch_sentences[i]
        du_words = du.split()
        retrieved_count = {}
        retrieved_term_probability = {}
        for e in en_words:
            for d in du_words:
                comm = "select * from TransProb where ENG_WORD= '{0}' AND DUT_WORD= '{1}'".format(e,d)
                com2 = "select * from Count where ENG_WORD= '{0}' AND DUT_WORD= '{1}'".format(e,d)
                crsr.execute(comm)
                ans = crsr.fetchall()                
                crsr.execute(com2)
                an2 = crsr.fetchall()
                try:
                    line_no2= ans[0][0]+'_'+ans[0][1]+' '+str(ans[0][2])
                    line_no = an2[0][0]+'_'+an2[0][1]+' '+str(an2[0][2])
                except:
                    print(line_no2)
                pr = line_no.split()
                pr2 = line_no2.split()                
                print(pr)
                print(pr2)
                retrieved_count[pr[0]] = float(pr[1])
                retrieved_term_probability[pr2[0]] = float(pr2[1])
        print("Count and Translation probabilities retrieved")        
        print(retrieved_term_probability)
        print()
        s_total = {}
        for e in en_words:
            s_total[e] = 0
            for d in du_words:
                s = e+'_'+d
                s_total[e] += retrieved_term_probability[s]
        print(s_total)
        print("S_total for each english word done")                
        for e in en_words:
            for d in du_words:
                s = e+'_'+d
                retrieved_count[s] += (retrieved_term_probability[s]/s_total[e])
                total[d] += (retrieved_term_probability[s]/s_total[e])
        print("Counts modified and Total calculated")
        print(retrieved_count)
        print()
        print("RETRIEVED TP")
        print(retrieved_term_probability)        
        for k,v in retrieved_count.items():            
            t = k.split('_')
            e = t[0]
            d = t[1]
            command= "UPDATE Count SET PROBABILITY={0} WHERE ENG_WORD = '{1}' AND DUT_WORD ='{2}' ".format(v,e,d)
            print(command)
            crsr.execute(command)                
        con.commit()        
        print("Writeback completed into count file")
    return total

def running_function(foreign_l, english_l, dutch_sentences, eng_sentences, no_of_sentences,num_dict_dutch,num_dict_eng,no_of_iterations=10):
    for c_i in range(no_of_iterations):        
        print(c_i+1)        
        for i in english_l.keys():
            for j in foreign_l.keys():
                command= "UPDATE Count SET PROBABILITY= {0} WHERE ENG_WORD = '{1}' AND DUT_WORD ='{2}' ".format(0,i,j)
                #print(command)
                crsr.execute(command)
            con.commit()
        total = {}   
        for k in foreign_l.keys():
            total[k] = 0    
        total = finding_probabilities(dutch_sentences,eng_sentences,no_of_sentences,total,num_dict_dutch,num_dict_eng,loc)   
        print("Finding probabilities done, ",c_i)
        retrieved_count = {}
        retrieved_term_probability = {}    
        print(total)        
        for e in english_l.keys():            
            for d in foreign_l.keys():                
                dutch_line_no = num_dict_dutch[d]                
                com2 = "select * from Count where ENG_WORD= '{0}' AND DUT_WORD= '{1}'".format(e,d)
                print(com2)
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
        print(retrieved_count)
        print()    
        for d in foreign_l.keys():
            for e in english_l.keys():            
                s = e+ '_' +d
                retrieved_term_probability[s] = retrieved_count[s]/total[d]                                  
                command= "UPDATE TransProb SET PROBABILITY= {0} WHERE ENG_WORD = '{1}' AND DUT_WORD ='{2}' ".format(float(retrieved_term_probability[s]),e,d)
                print(command)
                crsr.execute(command)                
            con.commit()        
        print("Translational Probabilites updated")
  
def write_to_file2(probabilities,english_word,file_name,mode = 'a'):
	file = open(file_name,'a') 
    #file.write(str(counter)+' '+english_word+'\n')
    for k,v in probabilities.items():
        file.write('{0} {1}\n'.format(k,v))
    file.close()

def retrieve_max(foreign_l,english_l,no_of_dutch_words,num_dict_dutch,num_dict_eng):
    translation_etof = {}
    translation_ftoe = {}    
    for e in english_l.keys():        
        comm = "SELECT MAX(PROBABILITY),DUT_WORD From TransProb where ENG_WORD = '{0}'".format(e)       
        crsr.execute(comm)        
        ans = crsr.fetchall()        
        translation_etof[e] = ans[0][1]
        translation_ftoe[ans[0][1]] = e
   return translation_etof,translation_ftoe

def pearson_coefficient(dut_cleaned,result_dut):   
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
        resultDutWords_line_no = assign_line_no(result_dut)
    dutchWord_line_no = assign_line_no(dut_cleaned)
    tf_of_cleaned = maintain_normalized_tf(dutchWord_line_no,dut_cleaned)    
    tf_of_result = maintained_normalized_tf(resultDutWords_line_no,result_dut)    
    total_sim = 0    
    for i in tf_of_cleaned.keys():
        total_sim += tf_of_cleaned[i] * tf_of_result[i]        
    return total_sim

def maintain_normalized_tf(doc_dict_line_no, data_clean):
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
    s = ""
    a = [ ':','.' , '\\' , '/' , ',' , ';' , '(' , ')' , '"', "\'",'1','2','3','4','5','6','7','8','9','0','?']   
    for i in eng_sentence:
        if i in a:
            s+=i
            continue           
        s += str(tr[i])
    s+='\n'
    return s
  
def translate_doc(eng_doc, translated_dict, rewrite_file, doc_lang = 'eng'):
    result_doc = []    
    for i in eng_doc:
        s = produce_sentence(i, translated_dict,doc_lang)
        result_doc.append(s)    
    with open(rewrite_file,'w') as f:
        f.writelines(result_doc)
        return result_doc

def delete_files():
    try:
        os.remove(PROB_FILE)
    except OSError as e:  ## if failed, report it back to the user ##
        print ("Error: %s - %s." % (e.filename, e.strerror))
    try:
        os.remove(COUNT_FILE)
    except OSError as e:  ## if failed, report it back to the user ##
        print ("Error: %s - %s." % (e.filename, e.strerror))

def main():   
    Eng_File = UPDATED_ENGLISH_FILE
    Dutch_File = UPDATED_DUTCH_FILE    
    eng_data, dutch_data = readfiles(Eng_File,Dutch_File,4)   
    print("Files read")  
    eng_cleaned = remove_punc(eng_data,'eng')
    dut_cleaned = remove_punc(dutch_data,'dutch')    
    total_no_of_sentences = len(dut_cleaned)   
    print("Files cleaned")    
    dutchWords_line_no = assign_line_no(dut_cleaned)
    engWords_line_no = assign_line_no(eng_cleaned)
    no_of_words_eng = len(engWords_line_no)
    no_of_words_dutch = len(dutchWords_line_no)    
    num_dict_eng = {}
    num_dict_dutch = {}
    tr_etof, tr_ftoe = retrieve_max(dutchWords_line_no,engWords_line_no,len(num_dict_dutch),num_dict_dutch,num_dict_eng)
    tr_etof.update(EngToDutchStopWords())
    tr_ftoe.update(DutchToEngStopWords())
    print(tr_etof)
    print("\n\n\n\n")
    print(tr_ftoe)

if __name__ =="__main__":
    delete_files()
    main()
con.close()

def Test_Main(to_be_translated , answer_key, lang):
    tr_etof.update(EngToDutchStopWords)
    tr_ftoe.update(DutchToEngStopWords)
      rewrite_File = 'result.txt'
	if lang == 'eng':
        result = translate_doc(to_be_translated,tr_etof, rewrite_File,'eng')
    elif lang =='dutch':
        result = translate_doc(to_be_translated,tr_ftoe, rewrite_File,'dutch')
	a_file = open(to_be_translated,'r+')
    r_file = open(rewrite_File,'r+')
    an_data = a_file.readlines()
    re_data = r_file.readlines()
    a_clean = remove_punctuations(og_data,lang)
    r_clean = remove_punctuations(og_data,lang)
    print(pearson_coefficient(r_clean,a_clean))
    print(cosine_similarity(r_clean,a_clean))