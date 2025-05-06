from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def sentiment(text):
    analyzer = SentimentIntensityAnalyzer()

    # Get sentiment scores
    scores = analyzer.polarity_scores(text)

    # Determine sentiment
    if scores['compound'] >= 0.05:
        sentiment = 'positive'
    elif scores['compound'] <= -0.05:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'

    return sentiment
