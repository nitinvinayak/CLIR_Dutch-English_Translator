dutchFile=open("Dutch_Updated.txt","r",encoding="utf-8")
englishFile=open("English_Updated.txt","r",encoding="utf-8")

dutchList=dutchFile.readlines()[:1000]
EngList=englishFile.readlines()[:1000]

def remove_punc(l):
    for i in range(len(l)):
        l[i] = remove_stuff(l[i])
        l[i] = l[i][:-1].lower()
    return l

def remove_stuff(l):
    a = [ ':','.' , '\\' , '/' , ',' , ';' , '(' , ')' , '"', "\'",'1','2','3','4','5','6','7','8','9','0','?']
    for i in a:
        l = l.replace(i, "")
    return l

ListofTermseng={}
ListofTermsdut={}
dutchList = remove_punc(dutchList)
EngList = remove_punc(EngList)
for i in range(0,1000):
    for term in dutchList[i].split():
        if term not in ListofTermseng.keys():
            ListofTermseng[term]=1
        else:
            ListofTermseng[term]+=1
    for term in EngList[i].split():
        if term not in ListofTermsdut.keys():
            ListofTermsdut[term]=1
        else:
            ListofTermsdut[term]+=1
    print(i)
