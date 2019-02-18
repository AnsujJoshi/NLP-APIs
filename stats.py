"""
    Statistics of text given
"""
from collections import Counter, defaultdict
import textract
import nltk
import re
import inflect


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

from nltk.corpus import wordnet as wn
def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma
    
from nltk.stem.wordnet import WordNetLemmatizer
def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))

def prepare_text_for_lda(text):
    tokens = preprocess(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens

def read_text(file_path):
    text = textract.process(file_path)
    return text

def get_text_data(text):
    text_data = []
    tokens = prepare_text_for_lda(text.split(' '))
    for token in tokens:
        text_data.append(token)
    return text_data

def ngrams(words, n=2, padding=False):
    "Compute n-grams with optional padding"
    pad = [] if not padding else [None]*(n-1)
    grams = pad + words + pad
    return (tuple(grams[i:i+n]) for i in range(0, len(grams) - (n - 1)))

def get_data_single(text_data):
    counts = defaultdict(int)
    for ng in ngrams(text_data, 1, False):
        counts[ng] += 1
    total_words = 0
    unique_words = 0
    most_frequent_word = ''
        
    for c_n, ng_n in sorted(((c, ng) for ng, c in counts.items())):
        count_most_frequent_word = c_n
        most_frequent_word = ng_n
        total_words +=c_n
        unique_words +=len(ng_n)
    return total_words, unique_words, most_frequent_word[0], count_most_frequent_word


def get_data_bi(text_data):
    counts_bi = defaultdict(int)
    for ng in ngrams(text_data, 2, False):
        counts_bi[ng] += 1
    most_frequent_bigram = ''
    count_most_frequent_bigram = 0
    for c1, ng1 in sorted(((c, ng) for ng, c in counts_bi.items())):
        count_most_frequent_bigram = c1
        most_frequent_bigram = ng1

    return most_frequent_bigram, count_most_frequent_bigram

def post(payload):
    file_path = payload['file_path']
    text = read_text(file_path)
    text_data = get_text_data(text)
    total_words, num_of_unique_words, most_frequent_word, count_most_frequent_word = get_data_single(text_data)
    most_frequent_bigram, count_most_frequent_bigram = get_data_bi(text_data)

    return {
        "num_of_unique_words": num_of_unique_words,
        "total_words": total_words,
        "most_frequent_word": {
            "most_frequent_word": most_frequent_word,
            "count_most_frequent_word": count_most_frequent_word
        },
        "most_frequent_bigram" : {
            "most_frequent_bigram": most_frequent_bigram,
            "count_most_frequrnt_bigram":count_most_frequent_bigram
        }
    }