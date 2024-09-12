from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self):
        self.pipeline = pipeline("text-classification", model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
    def analyze(self, text):
        result = self.pipeline(text)[0]
        return result['label'], result['score']