'''
    Code for topic modelling
'''

import nltk
import re, inflect
import textract
import pickle
import gensim
import nltk
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from gensim import corpora
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


nltk.download('stopwords')

def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return(new_words)


def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return(new_words)


def replace_numbers(words):
    """Replace all interger occurrences in list of tokenized words with textual representation"""
    p = inflect.engine()
    new_words = []
    for word in words:
        if word.isdigit():
            new_word = p.number_to_words(word)
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words


def preprocess(words):
    """
    Function to perform the preprocessing steps.
    """
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = replace_numbers(words)
    return words


def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma
    
def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)


en_stop = set(nltk.corpus.stopwords.words('english'))

def prepare_text_for_lda(text):
    tokens = preprocess(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens

def read_data(file_path):
    text = textract.process(file_path)
    return text

def convert_text(text):
    text_data = []
    tokens = prepare_text_for_lda(text.split(' '))
    for token in tokens:
        text_data.append([token])
    return text_data

def define_corpus_n_dict(text_data):
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    pickle.dump(corpus, open('corpus.pkl', 'wb'))
    dictionary.save('dictionary.gensim')
    return dictionary, corpus

def lda_model(corpus, dictionary, num_topics, num_words):
    ldamodel = gensim.models.LdaMulticore(corpus, id2word=dictionary, num_topics=num_topics)
    topics = ldamodel.print_topics(num_words=num_words)
    return topics

def output_func(topics, num_topics, num_words):
    output = {}
    sentiment_output = {}
    for i in range(num_topics):
    
        name = 'topic_'+str(i)
        alp = []
        list_topics = topics[i][1].split('+')
        for i in range(num_words):
            top = list_topics[i].split('*')[-1]
            alp.append(top)
            output[name] = alp
        sentiment_output[name] = topic_sentiment(str(alp))
    return output, sentiment_output

def topic_sentiment(text):
    
    client = language.LanguageServiceClient()

    document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    return {
        "score" : sentiment.score,
        "magnitude" : sentiment.magnitude
    }

def post(payload):

    file_path = payload['file_path']
    num_topics = payload['num_topics']
    num_words = payload['num_words']

    text = read_data(file_path)
    text_data = convert_text(text)
    dic, cor = define_corpus_n_dict(text_data)
    ldamodel = lda_model(corpus=cor, dictionary=dic, num_topics=num_topics, num_words=num_words)
    word_output, sentiment_output = output_func(ldamodel, num_topics, num_words)

    return {
        "word_output" : word_output,
        "sentiment_output" : sentiment_output
    }
