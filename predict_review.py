import pull_data
import sentiment_analysis
import string
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from gensim.models import Word2Vec
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn import metrics
from sklearn.decomposition import PCA,TruncatedSVD

def word_data(dfs,stop_words):
    '''
    INPUT:
    dfs: list of dataframes of reviews for each airline
    stop_words: words deemed unimportant for NLP analysis

    Creates 'nlp_words' column for every dataframe with important NLP words for each review
    '''
    for df in dfs:
        lst_of_str_reviews = []
        for review in df['words']:
            review_words = ''
            for word in review.split(' '):
                if word.strip(string.punctuation).lower() not in stop_words and word:
                    review_words += '{} '.format(word)
            lst_of_str_reviews.append(review_words.strip())
        df['nlp_words'] = lst_of_str_reviews

def opt_alpha(nb,df):
    '''
    INPUT:
    nb: Naive Bayes classifier
    df: dataframe in order to train nb on

    OUTPUT:
    alpha: optimal alpha based on optimizing accuracy for data given
    '''
    params = {'alpha':[0.1, 0.2, 0.3, 0.4, 0.5]}
    gc = GridSearchCV(nb,param_grid = params,cv=10,scoring='accuracy')
    gc.fit(tfidf.fit_transform(df['nlp_words']),y)
    return gc.best_params_['alpha']

def bag_of_words(df,stop_words):
    '''
    INPUT:
    df: dataframe specifying airline reviews
    stop_words: list of words deemed unimportant for NLP analysis

    OUTPUT:
    bag_of_words: string of words deemed important for NLP analysis
    '''
    bag_of_words = []
    for x in df['words']:
        words = []
        for word in x.split(' '):
            if word.strip(string.punctuation).lower() not in stop_words and word and not (any(char.isdigit() for char in word)):
                words.append(word.strip(string.punctuation).lower())
        bag_of_words.append(' '.join(words[1:]))
    return bag_of_words

def pca_plot(dfs,stop_words):
    '''
    INPUT:
    dfs: dataframes of all airlines with respective reviews
    stop_words: list of words deemed unimportant for NLP analysis

    OUTPUT:
    PCA plot: plotting review information and respective label (positive or negative) 
    with condensed features (3)
    '''
    review_texts = []
    labels = []
    for df in dfs:
        for label in df['positive'].tolist():
            labels.append(label)
        for review in bag_of_words(df,stop_words):
            review_texts.append(review)
    
    tfidf = TfidfVectorizer(stop_words=stop_words)
    scaler = StandardScaler()

    X = tfidf.fit_transform(review_texts)
    y = labels

    svd = TruncatedSVD(n_components=3)
    result = svd.fit_transform(X)
    
    plt.figure(figsize=(30,20))
    plt.scatter(result[:,0],result[:,1],result[:,2],c = np.array(labels))

    plt.show()

def model_score(dfs,stop_words,weight_dict):
    '''
    INPUT:
    dfs: dataframes of all airlines with respective reviews
    stop_words: list of words deemed unimportant for NLP analysis
    weight_dict: dictionary with weights for positive and negative classification

    OUTPUT:
    confusion_matrix and accuracy score for each airline's predictive Naive Bayes model
    '''
    for i,df in enumerate(dfs):
        tfidf = TfidfVectorizer(stop_words=stop_words)
        X = df['nlp_words']
        y = df['positive']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

        X_train = tfidf.fit_transform(X_train)
        X_test = tfidf.transform(X_test)

        nb = MultinomialNB(class_prior = weight_dict[i])
        nb.fit(X_train,y_train)

        alpha = opt_alpha(nb,df)

        nb = MultinomialNB(alpha = alpha,class_prior = weight_dict[i])
        nb.fit(X_train,y_train)

        preds = nb.predict(X_test)
        print(metrics.confusion_matrix(y_test,preds).T)
        print(metrics.accuracy_score(y_test,preds))

if __name__ == '__main__':
    southwest_df,american_df,delta_df,united_df,ana_df,japan_df,qatar_df,dfs = pull_data.get_data()
    stop_words = sentiment_analysis.create_stop_words()
    word_data(dfs,stop_words)

    #class weights based on picking up more negative reviews while maintaining legitimate accuracy (at least 80%)
    weight_dict = {0:[.55,.45],1:[.65,.35],2:[.6,.4],3:[.5,.5],4:[.8,.2],5:[.7,.3],6:[.8,.2]}
    model_score(dfs,stop_words,weight_dict)
    
    pca_plot(dfs,stop_words)