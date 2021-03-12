# International Airline Review Sentiment Analysis and Prediction

This repository contains scripts and data analysis tools which were used in order to provide an in depth analysis of airline reviews.  The intent of this analysis was to compare and contrast the importance of different attributes of flight that led to positive or negative sentiments from reviewers. 

The data was collected by webscraping reviews from the website [www.AirlineQuality.com](https://www.airlinequality.com/) for the 4 largest airlines in the United States, the 2 largest airlines from Japan, and Qatar Airways, which was considered the World's best Airline by Skytrax in 2017.  Qatar Airways was used as a benchmark when comparing USA and Japan based airlines.  PostreSQL was utilized to store the data for further analysis.

# EDA

## Attribute Analysis

![image](images/Airlines_mean_ratings.png)

The above image shows the mean ratings by airline for different attributes of flight.  As we can see, the Japanese airlines tend to score higher than all the larger American carriers, but specifically stand out in the service department.

![image](images/Ground_service_barplot.png)

Where Qatar seems to stand out is the amenities that it offers as part of their flight experience as well as the customer's perception of the value for money attribute.

![image](images/Airline_valueformoney_boxplot.png)

## Cultural Analysis

Because there were so many reviews from Americans, I decided to see how Americans were rating their flight experience compared to those from other countries.

![image](images/Culture_insights_ratings.png)

From the above graph, we can see that Americans tend to rate flight experience very similarly to others when it is a high quality airline.  For lower rated airlines, Americans are much more likely to give a very negative review compared to other cultures.  We can potentially theorize that Americans tend to speak their mind more readily if they are unsatisfied with a product.  More in depth analysis and larger data availability for other cultures may be needed in order to come to more concrete conclusions.

## Perception of Value Over Time

An interesting exercise would be to examine if certain airlines were improving or getting worse over time in terms of their average overall rating.

![image](images/Airlines_rating_by_year.png)

As one can see, most airlines tended to decrease in quality over time.  This is due to the small profit margins that the airline industry is subject to and their increasing costs for fuel, salaries, and government fees/taxes.  All Nippon Airways and Qatar Airways prove that they are committed to a quality flight experience as they actually improved their flight sentiment from 2016 to 2017.

## The Effect of Bad Publicity on Perception of Quality

United had the largest drop (30%) in perception of quality from 2016 to 2017.  It is suspected that this is at least partly due to an event that unfolded on United Airlines that made it's way on the news.  On April 4th, 2017 a doctor was forcibly removed from an overbooked flight. From the below graph we can see that after people were notified of the event, the overall rating of flight satisfaction dropped drastically.  After July, we notice some recovery and then in the beginning of September, United is exonerated from the event causing more news coverage and another sharp drop in flight satisfaction.

![image](images/United_incident_plot.png)

# NLP

## Common Words Positive/Negative Reviews

For Natural Language Processing, individual words were taken from each review in order to analyze the context in which a customer decided their flight experience was negative or positive.  Below, we can see some word clouds for positive and negative words that were common for certain airlines.

![image](images/ANA_positive_wordcloud.png)
![image](images/Southwest_negative_wordcloud.png)

## Trigrams

Here, we notice the phrases that are common in positive/negative reviews.  This gives us more of a context to see why a person may be satisfied or unsatisfied with their flight experience.

![image](images/AA_positive_trigrams.png)
![image](images/Delta_negative_trigrams.png)

## Model

A Naive Bayes classification algorithm was used in order to attempt to classify reviews as positive and negative.  An accuracy of 85% was achieved in predictions among all the airlines.  Weights for positive and negative classification were optimized based on the availability of negative reviews.  Optimal alpha values for each model were determined by Grid Search.

# Conclusion

Insights that were gained from this in depth analysis can be utilized in various real world scenarios in order to more thoroughly understand the strengths and weaknesses of a company, utilize benchmarking in order to compare and contrast against other businesses in one's industry, and even to quantify the benefit or detriment that may be associated with publicity and gauge the human psychological reaction that could have an effect on the perception of quality of a product.
