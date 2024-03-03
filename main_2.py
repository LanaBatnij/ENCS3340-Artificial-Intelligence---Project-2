import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load data into pandas dataframes
P_Tweets = pd.read_csv('PositiveTweets.tsv', sep='\t', names=['Class', 'text'])
N_Tweets = pd.read_csv('NegativeTweets.tsv', sep='\t', names=['Class', 'text'])

# Concatenate the dataframes and convert Classes to binary values
Tweets = pd.concat([P_Tweets, N_Tweets], ignore_index=True)
Tweets['Class'] = Tweets['Class'].map({'pos': 1, 'neg': 0})
# Split the data into training and testing sets
CrossTrain, CrossTest, ClassicalTrain, ClassicalTest = train_test_split(Tweets['text'], Tweets['Class'], test_size=0.25)

# Transform the text into a matrix of token counts
vectorizer = CountVectorizer()
CrossTrain_counts = vectorizer.fit_transform(CrossTrain)
CrossTest_counts = vectorizer.transform(CrossTest)

rfc = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42, min_samples_split=10, max_features='sqrt')
rfc.fit(CrossTrain_counts, ClassicalTrain)
nb = MultinomialNB()
nb.fit(CrossTrain_counts, ClassicalTrain)
svm_clf = svm.SVC(kernel='linear', C=0.1, random_state=42)
svm_clf.fit(CrossTrain_counts, ClassicalTrain)
Cross_RFC = cross_val_score(rfc, CrossTrain_counts, ClassicalTrain, cv=5)
Cross_NB = cross_val_score(nb, CrossTrain_counts, ClassicalTrain, cv=5)
Cross_SVM = cross_val_score(svm_clf, CrossTrain_counts, ClassicalTrain, cv=5)
print("Results for cross-validation:")
print("Random Forest Accuracy: %0.2f (+/- %0.2f)" % (Cross_RFC.mean(), Cross_RFC.std() * 2))
print("Naive Bayes Accuracy: %0.2f (+/- %0.2f)" % (Cross_NB.mean(), Cross_NB.std() * 2))
print("SVM Accuracy: %0.2f (+/- %0.2f)" % (Cross_SVM.mean(), Cross_SVM.std() * 2))

# Predict test set using each classifier
Classical_RFC = rfc.predict(CrossTest_counts)
Classical_NB = nb.predict(CrossTest_counts)
Classical_SVM = svm_clf.predict(CrossTest_counts)
print("Results for  classical method:")
print("Random Forest Evaluation Metrics:")
print("Accuracy: ", accuracy_score(ClassicalTest, Classical_RFC))
print("Precision: ", precision_score(ClassicalTest, Classical_RFC))
print("Recall: ", recall_score(ClassicalTest, Classical_RFC))
print("F1 score: ", f1_score(ClassicalTest, Classical_RFC))

print("Naive Bayes Evaluation Metrics:")
print("Accuracy: ", accuracy_score(ClassicalTest, Classical_NB))
print("Precision: ", precision_score(ClassicalTest, Classical_NB))
print("Recall: ", recall_score(ClassicalTest, Classical_NB))
print("F1 score: ", f1_score(ClassicalTest, Classical_NB))

print("SVM Classifier Evaluation Metrics:")
print("Accuracy: ", accuracy_score(ClassicalTest, Classical_SVM))
print("Precision: ", precision_score(ClassicalTest, Classical_SVM))
print("Recall: ", recall_score(ClassicalTest, Classical_SVM))
print("F1 score: ", f1_score(ClassicalTest, Classical_SVM))