from textblob import TextBlob as tb
from nltk.corpus import stopwords
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
from PIL import Image
from os import path
import numpy as np
import pull_data
import string
import tweepy


def create_stop_words():
    '''
    OUTPUT:
    stop_words: new stop words list with user added words
    '''
    stop_words = stopwords.words('english')
    for word in ['flight', 'verified', 'review', 'airlines', 'fly', 'gate',
                 'airport', 'got', 'even', 'dallas', 'ft', 'worth', 'dfw',
                 'miami', 'mia', 'a350', 'new', 'york', 'jfk', 'via', 'los',
                 'angeles', 'chicago', 'atlanta', 'atl', 'san', 'francisco',
                 'ord', 'newark', 'aircraft', 'sydney', 'b777', 'a380', 'las',
                 'vegas', 'salt', 'lake', 'doha', 'cape', 'town', 'doh', 'lax',
                 'ife', 'air', 'lines', 'line', "i've", 'flights', 'airline',
                 'plane', 'ua', 'trip', 'flew', 'flying', 'us', 'time', 'one',
                 'told', 'hour', 'sfo', 'customer', 'seat', 'southwest',
                 'american', 'aa', 'delta', 'boeing', 'united', 'ana', 'all',
                 'nippon', 'japan', 'tokyo', 'haneda', 'denver', 'houston',
                 'narita', 'nrt', 'qatar', 'al', 'mourjan', 'airways',
                 'verified', 'jal', 'japanese', 'la', 'a330', 'singapore',
                 'bangkok', 'luggage', 'made', 'way', 'pilot', 'phoenix',
                 'another', 'around', 'take', 'day', 'go', 'much', 'take',
                 'say', 'asked', 'also', 'however', 'leg', 'much', 'though',
                 'chi', 'minh', 'would', 'get', 'could', 'back', 'really']:
        stop_words.append(word)
    return stop_words


def bag_of_words(df, positive, stop_words):
    '''
    INPUT:
    df: dataframe specifying airline reviews
    positive: 1 if you want positive reviews for airline or 0 if you want
        negative reviews
    stop_words: list of words deemed unimportant for NLP analysis

    OUTPUT:
    bag_of_words: string of words deemed important for NLP analysis
    '''
    class_words = []
    for x in df[df['positive'] == positive]['words']:
        for word in x.split(' '):
            if word.strip(string.punctuation).lower() not in stop_words and word:
                class_words.append(word.strip(string.punctuation).lower())
    bag_of_words = ' '.join(class_words)
    return bag_of_words


def common_trigrams(bag_of_words):
    '''
    INPUT:
    bag_of_words: string of words used for NLP analysis

    OUTPUT:
    Returns 5 most common trigrams in positive or negative reviews for
        particular airline
    '''
    tokens = bag_of_words.split(' ')
    trigrams = [(tokens[i], tokens[i+1], tokens[i+2]) for i in
                range(0, len(tokens)-2)]
    trigrams_counter = Counter(trigrams)
    index = 1
    for key, val in trigrams_counter.most_common(20):
        for key2, val2 in trigrams_counter.most_common(20)[index:]:
            if len(set(key)-set(key2)) <= 1:
                trigrams_counter[key] += trigrams_counter[key2]
                trigrams_counter.pop(key2)
        index += 1
    return trigrams_counter.most_common(5)


def create_word_cloud(bag_of_words, stop_words, title):
    '''
    INPUT:
    bag_of_words: string of words used for NLP analysis

    OUTPUT:
    Word cloud based on words in bag_of_words in the shape of a plane! (shape of the plane-icon.png silhouette)
    '''
    d = path.dirname(__file__)
    plane_mask = np.array(Image.open(path.join(d, "plane-icon.png")))
    plt.figure(figsize=(10, 10))
    wordcloud = WordCloud(colormap='magma',
                          background_color='white',
                          mask=plane_mask,
                          stopwords=stop_words).generate(bag_of_words)
    plt.title(title, fontdict={'fontsize': 20})
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


def word_analysis(dfs, stop_words, positive=1):
    '''
    INPUT:
    dfs: list of dataframes of reviews for each airline
    stop_words: words deemed unimportant for NLP analysis
    positive: 1 to get reviews with overall rating of 6 or more or 0 for
        reviews with overall rating of 5 or less

    OUTPUT:
    wordcloud of words that are most used in reviews that are either positive
        or negative
    '''
    airlines = [
        'Southwest Airlines', 'American Airlines', 'Delta Air Lines',
        'United Airlines', 'All Nippon Airways', 'Japan Airlines', 
        'Qatar Airways'
    ]
    i = 0
    sentiment = ''
    if positive:
        sentiment = 'Positive Words'
    else:
        sentiment = 'Negative Words'
    for df in dfs:
        sentiment_words = bag_of_words(df, positive, stop_words)
        create_word_cloud(
            sentiment_words,
            stop_words,
            f'{airlines[i]} : {sentiment}'
        )
        i += 1


def trigram_analysis(dfs, stop_words, positive=1):
    '''
    INPUT:
    dfs: list of dataframes of reviews for each airline
    stop_words: words deemed unimportant for NLP analysis
    positive: 1 to get reviews with overall rating of 6 or more or 0 for
        reviews with overall rating of 5 or less

    OUTPUT:
    pie graph of top 5 most used trigrams in reviews that are either positive
        or negative
    '''
    airlines = [
        'Southwest Airlines', 'American Airlines', 'Delta Air Lines',
        'United Airlines', 'All Nippon Airways', 'Japan Airlines',
        'Qatar Airways'
    ]
    i = 0
    sentiment = ''
    if positive:
        sentiment = 'Positive Trigrams\n'
    else:
        sentiment = 'Negative Trigrams\n'

    for df in dfs:
        sentiment_words = bag_of_words(df, positive, stop_words)
        trigrams = common_trigrams(sentiment_words)
        labels = []
        values = []
        for k, v in trigrams:
            labels.append(' '.join(k).title())
            values.append(v)
        if positive:
            colors = ['yellowgreen', 'gold', 'lightskyblue',
                      'lightcoral', 'firebrick']
        else:
            colors = ['firebrick', 'lightcoral', 'lightskyblue',
                      'gold', 'yellowgreen']
        explode = (0.1, 0, 0, 0, 0)

        plt.pie(values, explode=explode, labels=labels, colors=colors,
                autopct=make_autopct(values), shadow=True, startangle=90)
        # Set aspect ratio to be equal so that pie is drawn as a circle.
        plt.axis('equal')
        plt.title(f'{airlines[i]} : {sentiment}', fontdict={'fontsize': 20})
        i += 1
        plt.show()


def make_autopct(values):
    '''
    INPUT:
    values: number of times event (trigrams) occurs in text

    OUTPUT:
    values to be used in pie graph
    '''
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d}'.format(v=val)
    return my_autopct


def twitter_sentiment(consumer_key, consumer_secret, token, token_secret):
    '''
    INPUT:
    consumer_key,consumer_secret,token,token_secret: consumer and token keys
        created on Twitter Apps

    OUTPUT:
    Tweets that contain api search term or terms
    '''
    authorization = tweepy.OAuthHandler(consumer_key, consumer_secret)
    authorization.set_access_token(token, token_secret)

    api = tweepy.API(authorization)
    tweets = api.search('Nippon AND Airways')

    for tweet in tweets:
        print(tweet.text)
        text_analysis = tb(tweet.text)
        print('\n' + '\033[1m' + f'Sentiment score: {text_analysis.sentiment.polarity}\n\n' + '\033[0m')


if __name__ == "__main__":
    southwest_df, american_df, delta_df, united_df, ana_df, japan_df, qatar_df, dfs = pull_data.get_data()

    stop_words = create_stop_words()

    word_analysis(dfs, stop_words, 0)
    trigram_analysis(dfs, stop_words, 0)
