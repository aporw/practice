import sys
import pandas as pd
import json  
import nltk
from nltk.tokenize import word_tokenize

#Function to read input file
def readfile(filename):
    #Reading csv file with pandas
    try:
        fl = pd.read_csv(filename)

    except Exception as e:
        raise e  

    if 'Id' not in fl.columns:
        raise Exception("Invalid columns - need Id Column in file")
    
    if 'Sentence' not in fl.columns:   
        raise Exception("Invalid columns - need Sentence column in file") 

    return fl

#Function to create json 
def feature_creator(sentence_id, sentence):
    
    #Word tokenization
    words = word_tokenize(sentence)

    #Tagging
    pos_with_words = nltk.pos_tag(words)

    #Separating tags & words and saving tags separately
    tags = []
    for pos in pos_with_words:
        tags.append(pos[1])

    preposition = ['on','for','of','to','at','in','with','by']  
    
    length = len(words)

    preposition_index = []
    for ind,word in enumerate(words):
        #Checking specifically for 'to' 
        if word.lower() == 'to' and ind+1 <length and tags[ind+1]=='VB':
            continue 
        if word.lower() in preposition:
            preposition_index.append(ind)

    print(preposition_index)  
    print(tags)
    
    
    
    for i in preposition_index:


        w,t = words[i], tags[i]
        
        # Handling out of index error on both sides of list
        if i-1<0:
            wBack1,tBack1 = None,None
            wBack2,tBack2=None, None
        else:
            wBack1,tBack1 = words[i-1], tags[i-1]
            if i-2<0:
                wBack2,tBack2 = None,None
            else:      
                wBack2,tBack2 =  words[i-2], tags[i-2]
        if i+1>length-1:
            wForward1, tForward1=None, None
            wForward2,tForward2 = None, None
        else:
            wForward1, tForward1 = words[i+1], tags[i+1]
            if i+2>length-1:
                wForward2,tForward2=None, None
            else:
                wForward2,tForward2 = words[i+2], tags[i+2]

        #Save features in list ls
        ls = []

        ls.append(" ".join(filter(None,[wBack1,w])))
        ls.append(" ".join(filter(None,[w,wForward1])))
        ls.append(" ".join(filter(None,[wBack1,w, wForward1])))
        ls.append(" ".join(filter(None,[wBack2,wBack1,w])))
        ls.append(" ".join(filter(None,[w,wForward1,wForward2])))
        ls.append(" ".join(filter(None,[wBack2,wBack1,w,wForward1,wForward2])))
        ls.append(" ".join(filter(None,[tBack1,t])))
        ls.append(" ".join(filter(None,[t,tForward1])))
        ls.append(" ".join(filter(None,[tBack1,t, tForward1])))
        ls.append(" ".join(filter(None,[tBack2,tBack1,t])))
        ls.append(" ".join(filter(None,[t,tForward1,tForward2])))
        ls.append(" ".join(filter(None,[tBack2,tBack1,t,tForward1,tForward2])))

        
        output={}
        output["id"] = str("_".join([str(sentence_id),str(i)]))
        output["prep"] = words[i]
        output["features"] = ls
        
        #Saving json file with same name as ID
        with open("Output_Files/"+output["id"]+".json", "w") as outfile: 
            json.dump(output, outfile)        
           
        #print(output) 



  

if __name__ == "__main__":
    
    filename = sys.argv[1]
    file = readfile(filename)

    #Calling function over csv file
    for i in range(file.shape[0]):
       feature_creator(file['Id'][i], file['Sentence'][i])

	


