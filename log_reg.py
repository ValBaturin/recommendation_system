from config import ARTICLE_PATH
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import word_tokenize
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn.metrics import roc_auc_score
 
if __name__ == "__main__":
    text = []
    label = []
    for _id in set(os.listdir(ARTICLE_PATH)) & set(os.listdir('./label')):
        with open(ARTICLE_PATH + _id, 'r') as text_file, open('./label/' + _id) as label_file:
            print(_id)
            label.append(int(label_file.read()))
            text.append(text_file.read())
    print(len(label))         
    X_train, X_test, Y_train, Y_test = train_test_split(text, label,test_size=0.2)
 
    tfidf_transformer = TfidfVectorizer(tokenizer=word_tokenize)
    X_train_tfidf = tfidf_transformer.fit_transform(X_train)
 
    logreg = LogisticRegression()
    logreg.fit(X_train_tfidf, Y_train)
    X_test_tfidf = tfidf_transformer.transform(X_test)
    y_predict = logreg.predict(X_test_tfidf)
    print(roc_auc_score(Y_test, y_predict))
