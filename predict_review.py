import pull_data
import sentiment_analysis
import string
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn import metrics

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


if __name__ == '__main__':
    southwest_df,american_df,delta_df,united_df,ana_df,japan_df,qatar_df,dfs = pull_data.get_data()
    stop_words = sentiment_analysis.create_stop_words()
    word_data(dfs,stop_words)

    for df in dfs:
        tfidf = TfidfVectorizer(stop_words=stop_words)
        X = df['nlp_words']
        y = df['positive']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

        X_train = tfidf.fit_transform(X_train)
        X_test = tfidf.transform(X_test)

        nb = MultinomialNB(alpha = 0.3)
        nb.fit(X_train,y_train)

        # params = {'alpha':[0.1, 0.2, 0.3, 0.4, 0.5]}
        # gc = GridSearchCV(nb,param_grid = params,cv=10,scoring='accuracy')
        # gc.fit(tfidf.fit_transform(df['nlp_words']),y)
        # print(gc.best_estimator_,gc.best_score_)
        #Best accuracy scores are achieved with an alpha of 0.3

        preds = nb.predict(X_test)
        print(metrics.confusion_matrix(y_test,preds).T)
        print(metrics.accuracy_score(y_test,preds))