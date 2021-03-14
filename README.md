# International Airline Review Sentiment Analysis and Prediction

This repository contains scripts and data analysis tools which were used in order to provide an in depth analysis of airline reviews.  The intent of this analysis was to compare and contrast the importance of different attributes of flight that led to positive or negative reviews from airline customers. 

The data was collected by webscraping reviews from the website [AirlineQuality.com](https://www.airlinequality.com/) for the 4 largest airlines in the United States, the 2 largest airlines from Japan, and Qatar Airways, which was considered the world's best airline by Skytrax in 2017.  Qatar Airways was used as a benchmark when comparing USA and Japan based airlines.  PostreSQL was utilized in order to store the large amounts of data for further analysis.

<br />

<div align="center">
  <img src="images/Airlines_mean_ratings.png">
</div>

# EDA

## Attribute Analysis

The barplots shown above, in the introduction to this repository, depict the mean ratings by airline for each different attribute of flight.  As we can see, the Japanese airlines tend to score higher than all the larger American carriers, but specifically stand out in the service department.

<br />

<div align="center">
  <img src="images/Ground_service_barplot.png">
</div>

<br />

Where Qatar Airways seems to stand out is the amenities that it offers as part of their flight experience.  This motivates their customers to rate their perception of value for money very highly for this carrier.

<br />

<div align="center">
  <img src="images/Airline_valueformoney_boxplot.png">
</div>

## Cultural Analysis

Because there were so many reviews from Americans, I decided to see how Americans were rating their flight experience compared to those from other countries.

<br />

<div align="center">
  <img src="images/Culture_insights_ratings.png">
</div>

<br />

From the graph above, we can see that Americans tend to rate flight experience very similarly to people of other nationalities when it is a high quality airline.  For lower rated airlines, Americans are much more likely to give a very negative review compared to other cultures.  We can potentially theorize that Americans tend to expect more for their money when they are buying a product or service, even if it's of lower value.  More in depth analysis and larger data availability for other cultures may be needed in order to come to more concrete conclusions.

## Perception of Value Over Time

An interesting exercise would be to examine if certain airlines were improving or getting worse over time in terms of their average overall rating.

<br />

<div align="center">
  <img src="images/Airlines_rating_by_year.png">
</div>

<br />

As one can see, most airlines tended to decrease in perceived quality over time.  This is due to the small profit margins that the airline industry is subject to and their ever increasing costs for fuel, salaries, and government fees and taxes.  All Nippon Airways and Qatar Airways prove that they are committed to a quality flight experience as they actually improved their flight sentiment from 2016 to 2017.

## The Effect of Bad Publicity on Perception of Quality

United Airlines suffered the largest drop (30%) in perception of quality from 2016 to 2017.  We can suspect that this is at least partly due to an event that unfolded on United Airlines that made it's way on the news.  On April 4th, 2017 a doctor was forcibly removed from an overbooked flight. From the below graph we can see that after people were notified of the event, the overall rating of flight satisfaction dropped drastically.  After July, we notice some recovery and then in the beginning of September, United is exonerated from the event causing more news coverage and another sharp drop in flight satisfaction.

<br />

<div align="center">
  <img src="images/United_incident_plot.png">
</div>

# NLP

## Common Words in Positive & Negative Reviews

Individual words were taken from each review in order to analyze the context in which a customer decided their flight experience was negative or positive.  Below, we can see some word clouds for positive and negative words that were common for certain airlines.

<br />

<div align="center">
  <img src="images/ANA_positive_wordcloud.png">
  <img src="images/Southwest_negative_wordcloud.png">
</div>

## Trigrams

With trigrams, we can examine triplets of words that would be used with legitimate frequency in positive or negative reviews.  This gives us more of a context to see why a person may be satisfied or dissatisfied with their flight experience.

<br />

<div align="center">
  <img src="images/AA_positive_trigrams.png">
  <img src="images/Delta_negative_trigrams.png">
</div>

## Model

A Naive Bayes classification algorithm was used in order to attempt to classify reviews as positive and negative.  An accuracy of 85% was achieved in predictions among all the airlines.  Weights for positive and negative classification were optimized based on the availability of negative reviews.  Optimal alpha values for each model were determined by Grid Search.

# Conclusion

Insights that were gained from this in depth analysis can be utilized in various real world scenarios in order to more thoroughly understand the strengths and weaknesses of a company, utilize benchmarking in order to compare and contrast against other businesses in one's industry, and even to quantify the benefit or detriment that may be associated with publicity and gauge the human psychological reaction that could have an effect on the perception of quality of a product.
