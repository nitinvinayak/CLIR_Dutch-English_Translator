import sqlite3
con = sqlite3.connect('TransProb1.db')
crsr = con.cursor()
create_table = """CREATE TABLE TransProb(
ENG_WORD VARCHAR(20) NOT NULL,
DUT_WORD VARCHAR(20) NOT NULL,
PROBABILITY FLOAT(12,10) NOT NULL,
PRIMARY KEY (ENG_WORD,DUT_WORD));
"""

cluster_index="""CREATE INDEX IX_ED_T ON TransProb (
	"ENG_WORD",
	"DUT_WORD"
);"""

DUT_INDEX ="""
        CREATE INDEX IX_DUT ON TransProb (DUT_WORD);
"""

ENG_INDEX ="""
        CREATE INDEX IX_ENG ON TransProb (ENG_WORD);
"""
create_table_c = """CREATE TABLE Count(
ENG_WORD VARCHAR(20) NOT NULL,
DUT_WORD VARCHAR(20) NOT NULL,
PROBABILITY FLOAT(12,10) NOT NULL,
PRIMARY KEY (ENG_WORD,DUT_WORD));
"""

cluster_index_c="""CREATE INDEX IX_ED ON Count (
	"ENG_WORD",
	"DUT_WORD"
);"""
crsr.execute(create_table_c)
crsr.execute(cluster_index_c)
crsr.execute(create_table)
crsr.execute(cluster_index)
import time
import os
UPDATED_ENGLISH_FILE = 'English_Updated.txt'
UPDATED_DUTCH_FILE = 'Dutch_Updated.txt'
ENG_TEST_FILE = 'eng.txt'
DUTCH_TEST_FILE = 'dutch.txt'
e_file = open(UPDATED_ENGLISH_FILE,'r',encoding = 'utf-8')
d_file = open(UPDATED_DUTCH_FILE,'r',encoding = 'utf-8')
dutch = d_file.readlines()[:100]
eng = e_file.readlines()[:100]
def remove_punc(l,lang):
    
    for i in range(len(l)):
        l[i] = l[i][:-1].lower()
        l[i] = remove_stopwords(l[i],lang)
        l[i] = remove_stuff(l[i])
    return l

def remove_stopwords(l,lang):
    eng_sw=['of', 'the', 'I', 'on', 'and', 'would', 'to', 'you', 'a', 'in', 'that', 'as', 'have', 'for', 'be', 'from', 'it', 'at', 'can', 'an', 'has', 'The', 'It', 'is', 'not', 'with', 'We', 'by', 'This', 'we', 'are', 'more', 'our', 'or', 'also', 'these', 'but', 'must']
    dut_sw=['van', 'de', 'ik', 'Aan', 'en', 'Zou', 'naar', 'u', 'een', 'in', 'dat', 'als', 'hebben', 'voor', 'worden', 'van', 'het', 'Bij', 'kan', 'een', 'heeft', 'De', 'Het', 'is', 'niet', 'met', 'Wij', 'door', 'Deze', 'wij', 'zijn', 'meer', 'onze', 'of', 'ook', 'deze', 'maar', 'moet']
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
dutch2 = remove_punc(dutch,'dutch')
eng2 = remove_punc(eng,'eng')
def assign_line_no(doc,dict_lo):
    for i in range(len(doc)):
        t = doc[i].split()
        for m in t:
            dict_lo[m].add(i)
    return dict_lo
from collections import defaultdict
dutch_line_no = defaultdict(set)
eng_line_no = defaultdict(set)
dutch_line_no = assign_line_no(dutch2, dutch_line_no)
eng_line_no = assign_line_no(eng2, eng_line_no)
def initialize(foreign_no_of_words,foreign_l,english_l):
    count = 0
    init_prob = 1/foreign_no_of_words
    for i in english_l.keys():
        for j in foreign_l.keys():
            c = [i,j,init_prob]
            c1 = [i,j,0]
            try:
                crsr.execute("INSERT INTO TransProb(ENG_WORD, DUT_WORD, PROBABILITY) VALUES(?,?,?)",tuple(c))
                crsr.execute("INSERT INTO Count(ENG_WORD, DUT_WORD, PROBABILITY) VALUES(?,?,?)",tuple(c1))
            except:
                print(c)
        if count>=100:
            con.commit()
            count = 0
        print(count)
        count+=1
    con.commit()
    return True
b_val = initialize(len(dutch_line_no), dutch_line_no, eng_line_no)
comm = "SELECT * FROM TransProb where ENG_WORD = 'resumption' and DUT_WORD = 'zitting'"
crsr.execute(comm)
ans = crsr.fetchall()
comm = "SELECT MAX(PROBABILITY),ENG_WORD FROM TransProb where DUT_WORD = 'hervatting'"
crsr.execute(comm)
ans = crsr.fetchall()
print(ans)
con.commit()
con.close()
def makeCount(dut_cleaned,eng_cleaned,total_no_of_sentences):   
    for i in range(total_no_of_sentences):        
        du = dut_cleaned[i]
        en = eng_cleaned[i]
        du_words = du.split()
        en_words = en.split()        
        file_name = "Count_Maintain/sen_Count" +str(i+1)+".txt"        
        f = open(file_name,'w+')        
        init_count = 0        
        for e in en_words:
            for d in du_words:
                s = e+'_'+d
                f.write('{0} {1}\n'.format(s,init_count))       
    return True
def finding_probabilities(dutch_sentences, eng_sentences,no_of_sentences,total): 
    for i in range(no_of_sentences):                
        en = eng_sentences[i]
        en_words = en.split()
        du = dutch_sentences[i]
        du_words = du.split()
        retrieved_count = {}
        retrieved_term_probability = {}
        count_file = "Count_Maintain/sen_Count"+str(i+1)+".txt"
        f = open(count_file,'r+')
        f2 = open(PROB_FILE,'r+')
        lines = f.readlines()
        lines2 = f2.readlines()        
        for i in lines:
            k = i.split()
            retrieved_count[k[0]] = float(k[1])
        for e in en_words:
            for d in du_words:
                eng_line_no = num_dict_eng[e]
                dutch_line_no = num_dict_dutch[d]
				line_no2 = lines2[eng_line_no + dutch_line_no-1]
                pr2 = line_no2.split()
                retrieved_term_probability[pr2[0]] = float(pr2[1])        
        f.close()
        f2.close()
        s_total = {}
        for e in en_words:
            s_total[e] = 0
            for d in du_words:
                s = e+'_'+d
                s_total[e] += retrieved_term_probability[s]
        for e in en_words:
            for d in du_words:
                s = e+'_'+d
                retrieved_count[s] += (retrieved_term_probability[s]/s_total[e])
                total[d] += (retrieved_term_probability[s]/s_total[e])          
        f = open(count_file,'r+')
        m = f.readlines()
        for k,v in retrieved_count.items():
            t = k.split('_')
            final_line_no = eng_line_no + dutch_line_no
            m[final_line_no-1] = '{0} {1}\n'.format(k,v)           
        f.close()
        with open(COUNT_FILE,'w') as file:
            file.writelines(m)
    return total