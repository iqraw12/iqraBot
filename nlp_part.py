import socket
import requests
import random
from nltk import ne_chunk, pos_tag, word_tokenize,sent_tokenize
from nltk.tree import Tree
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer,WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import wordnet as wn
from gingerit.gingerit import GingerIt
import truecase
from Random_replies import negative_replies,positive_replies



def word_synonyms(word):
    synonyms = []
    My_sysn = wn.synsets(word) 
    for syn in My_sysn:
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    return synonyms

def autospell(query):
    if query[-1:] != '.':
        query = query + '.'
    result = truecase.get_true_case(query)
    parser = GingerIt()
    result = parser.parse(result)['result']
    return result

def get_stopwords(query):
   stopword = stopwords.words('english')
   word_tokens = set(word_tokenize(query))
   removing_stopwords = set(word_tokens)-set(stopword)
   return removing_stopwords

def NER(query):
    print(query)
    nltk_results = ne_chunk(pos_tag(word_tokenize(query)))
    names= []
    for nltk_result in nltk_results:
        if type(nltk_result) == Tree:
            for nltk_result_leaf in nltk_result.leaves():
                names.append(nltk_result_leaf[0])
            print ('Type: ', nltk_result.label(), 'Name: ', names)
    return names

def get_ip_address(): # ip address user
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]



def generate_random_string(input_string):
    random_char = random.choice(input_string)
    return random_char

def analyze_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(text)
    compound_score = sentiment_scores['compound']
    negative_score = sentiment_scores['neg']
    if compound_score >= 0.05 and negative_score <= 0.5:
        return generate_random_string(positive_replies)
    elif compound_score <= -0.05 or negative_score > 0.5:
        return generate_random_string(negative_replies)
    else:
        return generate_random_string(positive_replies)
def get_definition(query):
    try:
        syno = word_synonyms(query)
        syn = wn.synsets(query)
        definition = syn[1].definition()
        if syn:
            return definition + " or may we can say " + syno[0]
    except:
        return None
