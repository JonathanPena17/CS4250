# 1. Compute Term Frequency (TF)
tf = []
for doc in documents:
    row = [1 if term in doc.split() else 0 for term in terms]
    tf.append(row)

# 2. Compute Inverse Document Frequency (IDF)
N = len(documents)
df = [sum(column) for column in zip(*tf)]
idf = [math.log(N / (d + 1)) for d in df]

# 3. Compute TF-IDF
docMatrix = []
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
relevant_retrieved = sum([1 for i, score in enumerate(docScores) if score >= 1 and labels[i] == 'R'])
retrieved = sum([1 for score in docScores if score >= 0.1])
relevant = labels.count('R')

precision = relevant_retrieved / retrieved if retrieved > 0 else 0
recall = relevant_retrieved / relevant if relevant > 0 else 0

print(f"Precision: {precision*100:.2f}%")
print(f"Recall: {recall*100:.2f}%")