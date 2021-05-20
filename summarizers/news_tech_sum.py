# Technology news summarizer
import math
import random
import stanza
from stanza.server import CoreNLPClient

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag
import os
import numpy as np

# Installing coreNLP if it is not installed
stanza.install_corenlp()
# Idea to extract all the relevant material from the news article
# Setting the path for the data
input_dir = '../data/texts/bbc-fulltext/bbc/tech'
input_dir = os.path.abspath(input_dir)
# Array where all the texts will be stored. With read() method
texts_read = []
for f in os.listdir(input_dir):
    with open(os.path.join(input_dir, f)) as text:
        texts_read.append(text.read())


# Summarizer of tech texts
# Receives the string of the article
# Taking into account what was found in news articles, that the most important information is found at the top of the
# article, because readers could stop reading at any given point
def summarizer(p_text: str):
    # Splitting text by \n
    partitioned_text = p_text.split('\n')
    # Remove all empty strings in the texts.
    partitioned_text = list(filter(None, partitioned_text))
    print('the partitioned text', partitioned_text)
    # Variable where the summarized text will be stored
    summarized_text = []
    # Partitioning the text into paragraphs. A paragraph is considered to have more than one sentence.
    # Nevertheless, the first two elements of the array will contain the title and leading sentence of the article. The
    # leading sentence is that that goes belowe the title
    paragraph_text = []
    for i, v in enumerate(partitioned_text):
        tokenized_segment = sent_tokenize(v)
        # Assumes title is first string of the text.
        if i == 0:
            paragraph_text.append(tokenized_segment)
        elif len(tokenized_segment) > 1:
            paragraph_text.append(tokenized_segment)
        # Checking for the leading sentence
        elif i == 1:
            paragraph_text.append(tokenized_segment)

    print('the paragraph text length', len(paragraph_text))
    # Extracting the first 20% percent (hoping that pareto principle works here) of paragraphs of the text.
    # Additionally, it also takes the first two elements of the array, that are assumed to correspond to the title and
    # the title and leading sentence
    number_of_paragraphs = math.floor((len(paragraph_text) - 2) * 0.2) + 2
    print('number of paragraphs', number_of_paragraphs)
    # Reducing number of paragraphs to analyze
    paragraph_text = paragraph_text[0:number_of_paragraphs]
    print('the paragraph text', paragraph_text)

    # Trying to remove redundant details in the remaining sentences
    # Passing the remaining elements through a pipeline to be able to understand more about the structure of the data
    # It can help to remove parenthesized elements that include further details, but are not deemed necessary for the
    # summary
    # Tokenizing the words
    # Variable where the tokenized text will be stored
    tokenized_text = []
    for paragraph in paragraph_text:
        print('the paragraph', paragraph)
        for sent in paragraph:
            print('the sentence', sent)
            tokenized_text.append(word_tokenize(sent))

    # Doing POS tagging to the remaining text. To gain more information about the structure of the text
    # Variable where the POS tagged text will be stored
    pos_text = []
    for sent in tokenized_text:
        pos_text.append(pos_tag(sent))

    # Doing the syntactic parsing of the sentence


    return pos_text


# Trying out the summarizer on the first text
the_text = summarizer(texts_read[0])
# Trying out the summarizer on a random text
random_text = summarizer(random.choice(texts_read))

# Trying out CoreNLP as a client-server
text = "Chris Manning is a nice person. Chris wrote a simple sentence. He also gives oranges to people."
with CoreNLPClient(
        annotators=['tokenize','ssplit','pos','lemma','ner', 'parse', 'depparse','coref'],
        timeout=30000,
        memory='16G') as client:
    ann = client.annotate(text)
