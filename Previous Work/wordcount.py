engfile=open("English.txt","r",encoding="utf-8")
count=0
freqofEngTerms={}
for sentence in engfile.readlines():
    for term in sentence.split():
        if term in freqofEngTerms.keys():
            freqofEngTerms[term]+=1
        else:
            freqofEngTerms[term]=1
print(freqofEngTerms)
