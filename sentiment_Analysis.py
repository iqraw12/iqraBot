from nltk.sentiment import SentimentIntensityAnalyzer

def analyze_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(text)
    print(sentiment_scores )
    max_score = max(sentiment_scores, key=sentiment_scores.get)
    
    if max_score == 'pos':
        return 'Positive', sentiment_scores['pos']
    elif max_score == 'neg':
        return 'Negative', sentiment_scores['neg']
    elif max_score == 'compound':
        return 'Compound', sentiment_scores['compound']
    else:
        return 'Neutral', sentiment_scores['neu']

