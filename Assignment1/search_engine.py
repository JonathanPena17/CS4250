#-------------------------------------------------------------------------
# AUTHOR: Jonathan Peña
# FILENAME: search_engine.py
# SPECIFICATION: Complete the Python program (search_engine.py) that will read the file collection.csv 
#                and output the precision/recall of a proposed search engine given the query q ={cat and dogs}
# FOR: CS 4250- Assignment #1
# TIME SPENT: 2 hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with standard arrays

#importing some Python libraries
import csv
import math

documents = []
labels = []

#reading the data in a csv file
with open('/Users/jonathanpena/Documents/CS4250/Assignment1/collection.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
         if i > 0:  # skipping the header
            documents.append (row[0])
            labels.append(row[1].strip())

#Conduct stopword removal.
#--> add your Python code here
stopWords = {'I', 'and', 'She', 'They', 'her', 'their'}

for i in range(len(documents)):
    cleaned_doc = []
    for word in documents[i].split():
        if word not in stopWords:
            cleaned_doc.append(word)
    documents[i] = ' '.join(cleaned_doc)

#Conduct stemming.
#--> add your Python code here
steeming = {
  "cats": "cat",
  "dogs": "dog",
  "loves": "love",
}

for i in range(len(documents)):
    stemmed_doc = []
    for word in documents[i].split():
        if word in steeming:
            stemmed_doc.append(steeming[word])
        else:
            stemmed_doc.append(word)
    documents[i] = ' '.join(stemmed_doc)

#Identify the index terms.
#--> add your Python code here
terms = []

for doc in documents:
    for term in doc.split():
        if term not in terms:
            terms.append(term)

#Build the tf-idf term weights matrix.
#--> add your Python code here
docMatrix = []

# 1. Compute Term Frequency (TF)
tf = []
for doc in documents:
    total_terms = len(doc.split())
    row = [doc.split().count(term)/total_terms for term in terms]  
    tf.append(row)

# 2. Compute Document Frequency (DF) for each term
df = [sum(1 for row in tf if row[terms.index(term)] > 0) for term in terms]

# 3. Compute Inverse Document Frequency (IDF)
N = len(documents)
idf = [math.log10(N / d) if d != 0 else 0 for d in df]  # Handle the case where d=0.

# 4. Compute TF-IDF
for row in tf:
    tf_idf_row = [tf_value * idf_value for tf_value, idf_value in zip(row, idf)]
    docMatrix.append(tf_idf_row)

#Calculate the document scores (ranking) using document weigths (tf-idf) calculated before and query weights (binary - have or not the term).
#--> add your Python code here
docScores = []
query_terms = ["cat", "dog"]
for row in docMatrix:
    score = sum([row[terms.index(term)] for term in query_terms])
    docScores.append(score)

#Calculate and print the precision and recall of the model by considering that the search engine will return all documents with scores >= 0.1.
#--> add your Python code here
relevant_retrieved = sum([1 for i, score in enumerate(docScores) if score >= 0.1 and labels[i] == 'R'])
retrieved = sum([1 for score in docScores if score >= 0.1])
relevant = labels.count('R')

precision = relevant_retrieved / retrieved if retrieved > 0 else 0
recall = relevant_retrieved / relevant if relevant > 0 else 0

print(f"Precision: {precision*100:.2f}%")
print(f"Recall: {recall*100:.2f}%")
