"""
    Entity recogination API
"""
import textract
import six
from os import sys
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


def read_text(file_path):
    text = textract.process(file_path)
    return text

def entity_sentiment_text(text):
    """Detects entity sentiment in the provided text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    document = types.Document(
        content=text.encode('utf-8'),
        type=enums.Document.Type.PLAIN_TEXT)

    # encoding = enums.EncodingType.UTF32
    # if sys.maxunicode == 65535:
    #     encoding = enums.EncodingType.UTF16
    
    entity_sentiment = client.analyze_entity_sentiment(document)#, encoding)
    
    return entity_sentiment

order_dict = {
    "1": "Person",
    "2": "Location",
    "3": "Organization",
    "4": "Event",
    "5": "Work-of-Art",
    "6": "Consumer-goods",
    "7": "Other"
}


def output_func(entity_sentiment):
    output = {}
    for entity in entity_sentiment.entities:
        output[entity.mentions[0].text.content]={
            "type": order_dict[str(entity.type)],
            "score": entity.mentions[0].sentiment.score,
            "magnitude": entity.mentions[0].sentiment.magnitude
        }
    
    return output

def post(payload):
    file_path = payload['file_path']
    import time
    a = time.time()
    text = read_text(file_path)
    b = time.time()
    entity_sentiment = entity_sentiment_text(text)
    c = time.time()
    output = output_func(entity_sentiment)
    d = time.time()
    print('read_text')
    print(b-a)
    print("entity_sentiment")
    print(c-b)
    print('output_func')
    print(d-c)
    return output