"""
    Sentiment analysis
"""
# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import textract
import time

def read_data(file_path):
    text = textract.process(file_path)
    return text

def sentence_sentiment(sentiment):
    good_sentence = sentiment.sentences[0]
    bad_sentence = sentiment.sentences[0]

    for sentence in sentiment.sentences:
        if sentence.sentiment.score == good_sentence.sentiment.score:
            if sentence.sentiment.magnitude > good_sentence.sentiment.magnitude:
                good_sentence = sentence
        elif sentence.sentiment.score > good_sentence.sentiment.score:
            good_sentence = sentence
        
        if sentence.sentiment.score == bad_sentence.sentiment.score:
            if sentence.sentiment.magnitude < bad_sentence.sentiment.magnitude:
                bad_sentence = sentence
        elif sentence.sentiment.score < bad_sentence.sentiment.score:
            bad_sentence = sentence
    return good_sentence, bad_sentence

def post(payload):

    file_path = payload['file_path']

    client = language.LanguageServiceClient()

    text = read_data(file_path)
    document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document=document)

    good_sentence, bad_sentence = sentence_sentiment(sentiment)
    output = {
        "good_sentence": good_sentence,
        "bad_sentence": bad_sentence,
        "score": sentiment.score,
        "magnitude" : sentiment.magnitude
    }
    return output

# if __name__ == "__main__":
#     payload = {}
#     payload['file_path'] = './data/trump2.txt'
#     post(payload)