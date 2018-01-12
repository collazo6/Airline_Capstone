import pull_data
import string
import re
import numpy as np
from wordcloud import WordCloud
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import GridSearchCV
from collections import Counter
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

def create_stop_words():
    stop_words = stopwords.words('english')
    for word in ['flight','verified','review','airlines','fly','gate','airport',
                 'got','even','dallas','ft','worth','dfw','miami','again"verified',
                 'new','york','jfk','via','los','angeles','chicago','atlanta','atl',
                 'san','francisco','ord','newark','aircraft','sydney','b777','a380',
                 'las','vegas','salt','lake','doha','cape','town','doh','lax','ife',
                 'air','lines','line',"i've",'flights','airline','plane','ua','',
                 'trip','flew','flying','us','time','one','told','hour','sfo',
                 'customer','seat','southwest','american','aa','delta','boeing',
                 'united','ana','all','nippon','japan','tokyo','haneda','houston',
                 'narita','nrt','qatar','al','mourjan','airways','verified',
                 'jal','japanese','la']:
        stop_words.append(word)
    return stop_words
    
def bag_of_words(df,positive,stop_words):
    class_words = []
    for x in df[df['positive'] == positive]['words']:
        for word in x.split(' '):
            if word.strip(string.punctuation).lower() not in stop_words and word.strip(string.punctuation) not in set(string.punctuation) and word:
                class_words.append(word.strip(string.punctuation).lower())
    bag_of_words = ' '.join(class_words)
    return bag_of_words

def common_trigrams(bag_of_words):
    tokens = bag_of_words.split(' ')
    trigrams = [(tokens[i],tokens[i+1],tokens[i+2]) for i in range(0,len(tokens)-2)]
    trigrams_counter = Counter(trigrams)
    index = 1
    for key,val in trigrams_counter.most_common(20):
        for key2,val2 in trigrams_counter.most_common(20)[index:]:
            if len(set(key)-set(key2)) <= 1:
                trigrams_counter[key] += trigrams_counter[key2]
                trigrams_counter.pop(key2)
        index+=1
    return trigrams_counter.most_common(5)

def create_word_cloud(bag_of_words):
    plt.figure(figsize=(10,10))
    wordcloud = WordCloud(colormap = 'magma',background_color='white').generate(bag_of_words)
    plt.imshow(wordcloud,interpolation='bilinear')
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    southwest_df,american_df,delta_df,united_df,ana_df,japan_df,qatar_df,dfs = pull_data.get_data()

    stop_words = create_stop_words()

    for df in dfs: 
        positive_words = bag_of_words(df,1,stop_words)
        negative_words = bag_of_words(df,0,stop_words)
        positive_trigrams = common_trigrams(positive_words)
        negative_trigrams = common_trigrams(negative_words)
        print(positive_trigrams)
        print(negative_trigrams)
        create_word_cloud(positive_words)
        create_word_cloud(negative_words)

    
    
