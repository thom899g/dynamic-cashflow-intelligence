import logging
from typing import Dict, Any
from textblob import TextBlob

class EmotionalIntelligenceModule:
    def __init__(self):
        self.sentiment_models = ['textblob', 'vader']
        logging.basicConfig(level=logging.INFO)

    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyzes sentiment of market-related news or social media posts."""
        results = {}
        try:
            for model in self.sentiment_models:
                if model == 'textblob':
                    blob = TextBlob(text)
                    results[model] = blob.sentiment.polarity
                elif model == 'vader':
                    # Assume VaderSentiment is imported and available
                    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
                    analyzer = SentimentIntensityAnalyzer()
                    results[model] = analyzer.polarity_scores(text)['compound']
            return results
        except Exception as e:
            logging.error(f"Error in sentiment analysis: {str(e)}")
            raise

    def interpret_sentiment(self, scores: Dict[str, float]) -> str:
        """Interprets sentiment scores to determine market mood."""
        try:
            average_score = sum(scores.values()) / len(scores)
            if average_score > 0.2:
                return 'bullish'
            elif average_score < -0.2:
                return 'bearish'
            else:
                return 'neutral'
        except ZeroDivisionError:
            logging.error("No sentiment models available for analysis")
            raise