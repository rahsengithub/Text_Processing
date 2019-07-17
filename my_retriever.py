#UID : 180128022

import math # Importing math 
class Retrieve:
    # Create new Retrieve object storing index and termWeighting scheme
    def __init__(self,index, termWeighting):
        self.index = index
        self.termWeighting = termWeighting
        self.termsInDocDict = {} # Creating a dictionary to be used in Binary TW Scheme
        for j in self.index:
            for k in self.index[j]:
                if k in self.termsInDocDict:
                    self.termsInDocDict[k] += 1
                else:
                    self.termsInDocDict[k] = 1
                    
        self.docstermsDict = {} # Creating a dictionary to be used in TF TW Scheme
        for j in self.index:
            for k in self.index[j]:
                if k in self.docstermsDict:
                    self.docstermsDict[k] += (self.index[j][k])**2
                else:
                    self.docstermsDict[k] = (self.index[j][k])**2
        self.invertedIndex = {}
        
        for tfidf in self.index: 
            idf = len(self.termsInDocDict)/len(self.index[tfidf])
            idf = math.log(idf, 10) # Calculating IDF
            self.invertedIndex[tfidf] = idf
        
        self.tfidfcalcDict = {} # Creating a dictionary to be used in TFIDF TW Scheme
        for j in self.index:
            for k in self.index[j]:
                if k in self.tfidfcalcDict:
                    self.tfidfcalcDict[k] += (self.index[j][k]*self.invertedIndex[j])**2
                else:
                    self.tfidfcalcDict[k] = (self.index[j][k]*self.invertedIndex[j])**2

    
    # Method performing retrieval for specified query
    def forQuery(self, query):
        cand = Retrieve.candidatePicker(self.index, query) # For passing the Candidate List as argument
        if(self.termWeighting == 'binary'): # For retrieving the Binary Function Value
            tW_binary = Retrieve.binary(self, self.index, cand, query)
            return tW_binary
        elif(self.termWeighting == 'tf'): # For retrieving the TF Function Value
            tW_tf = Retrieve.termFrequency(self, self.index, cand, query)
            return tW_tf
        else: # For retrieving the TFIDF Function Value
            tW_tfidf = Retrieve.tfIdf(self, self.index, cand, query)
            return tW_tfidf
       
    def candidatePicker(index, query): # Creating a function for getting Candidate List
        candidate_list = []
        for keys in query:
            if keys not in index:
                continue
            for candi in index[keys]:
                if candi in candidate_list:
                    continue
                candidate_list.append(candi)
        unique_candidate_list = list(set(candidate_list))
        return(unique_candidate_list)
        
    def binary(self, index, candidate, query): # Creating a function to calculate Binary TW
        mydict = {}
        for doc_id in candidate:
            q_id_i = 0
            d_i = self.termsInDocDict[doc_id]
            for q in query:
                try:
                    if doc_id in self.index[q]:
                        q_id_i += 1
                except:
                    continue
            mydict[doc_id] = q_id_i/math.sqrt(d_i)
        ranked_mydict = sorted(mydict, key = mydict.__getitem__, reverse = True)[:10] # Top 10 retrievals
        return(ranked_mydict)
    
    def termFrequency(self, index, candidate, query): # Creating a function to calculate TF TW
        mydict = {}
        for doc_id in candidate:
            q_id_i = 0
            d_i = self.docstermsDict[doc_id]
            for q in query:
                try:
                    if doc_id in self.index[q]:
                        q_id_i += self.index[q][doc_id]
                except:
                    continue
            mydict[doc_id] = q_id_i/math.sqrt(d_i)
        ranked_mydict = sorted(mydict, key = mydict.__getitem__, reverse = True)[:10]
        return(ranked_mydict)
    
    def tfIdf(self, index, candidate, query): # Creating a function to calculate TFIDF TW
        mydict = {}
        for doc_id in candidate:
            q_id_i = 0
            d_i = self.tfidfcalcDict[doc_id]
            for q in query:
                try:
                    if doc_id in self.index[q]:
                        q_id_i += self.index[q][doc_id]*query[q]*(self.invertedIndex[q]**2)
                except:
                    continue
            mydict[doc_id] = q_id_i/math.sqrt(d_i)
        ranked_mydict = sorted(mydict, key = mydict.__getitem__, reverse = True)[:10]
        return(ranked_mydict)

