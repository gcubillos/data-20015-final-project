# Technology news summarizer
import math
import random
import stanza

from stanza.server import CoreNLPClient
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag
import os
import numpy as np

# Installing stanza if it isn't installed yet
# stanza.install_corenlp()
# Installing the English model if it hasn't been installed
# stanza.download_corenlp_models(model='english', version='4.1.0', dir="YOUR_CORENLP_FOLDER")
# Idea to extract all the relevant material from the news article
# Setting the path for the data
input_dir = '../data/texts/bbc-fulltext/bbc/tech'
input_dir = os.path.abspath(input_dir)
# Array where all the texts will be stored. With read() method
texts_read = []
for f in os.listdir(input_dir):
    with open(os.path.join(input_dir, f)) as text:
        texts_read.append(text.read())

# Setting up the constituency parser
client = CoreNLPClient(
    annotators=['parse'],
    timeout=30000,
    memory='16G')


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
    # summary. The idea is to keep the most relevant elements from the sentence.
    # Just the constituency parsing will be done.
    # Tokenizing the words
    # Variable where the parsed text will be stored
    parsed_text = []
    for paragraph in paragraph_text:
        print('the paragraph', paragraph)
        for sent in paragraph:
            print('the sentence', sent)
            # Doing the constituency parsing of the sentence
            processed_sentence = parsing_text(sent)
            parsed_text.append(processed_sentence)

    return parsed_text, paragraph_text


# With the constituency parsing the idea is to keep the essential elements of the sentence. The idea that is being
# tried to transmit
# The method receives a sentence and returns the first NP and VP of each sentence
def parsing_text(p_sent: str):
    # Variable where the processed sentence will be stored
    processed_sentence = ""
    # Getting the constituency parse of the sentence
    current_sentence = client.annotate(p_sent).sentence[0]
    print('the current sentence', current_sentence)
    # Processing the constituency parse of the sentence
    parse_tree = current_sentence.parseTree
    finished_processing = False
    # while not finished_processing:
    #     current_node = parse_tree
    #     # Traversing the tree to find the first NP, which will be included in the summary
    #     try:
    #         current_node.child[0].value
    #     except TypeError:
    #         pass
    # Variable where the noun phrase will be stored
    np_value = None
    # Variable where the verb phrase will be stored
    vp_value = None
    processing_node(parse_tree, np_value, vp_value)

    return processed_sentence


# Checking whether it has a NP
# The node is taken as input. Also empty array that will contain both the remaining noun phrases and verb phrases
def processing_node(p_node, p_np, p_vp):
    # Variable where the final extracted sentence will be stored
    final_sentence = None
    num_children = len(p_node.child)
    for i in range(num_children):
        # Is the child a NP?
        if p_node.child[i].value == 'NP' and not p_np:
            p_np = finding_np(p_node.child[i], p_np, p_vp)
        elif p_node.child[i].value == 'VP' and not p_vp:
            p_vp = finding_vp(p_node.child[i], p_np, p_vp)

    return final_sentence


# Method that finds the first np
def finding_np(p_node, p_np, p_vp):
    num_children = len(p_node.child)
    found_np = False
    for i in range(num_children):
        # Is the child a NP?
        # If it is stop looking for other NPs
        if p_node.child[i].value == 'NP':
            finding_np(p_node.child[i], p_np, p_vp)
            break
        if i == num_children - 1:
            found_np = True

    if found_np:
        p_np = p_node

    return p_np


# Method that processes VP
def finding_vp(p_node, p_np, p_vp):
    structure = None
    found_first_np = False
    num_children = len(p_node.child)
    return p_vp


# Trying out the summarizer on the first text
the_text = [summarizer(texts_read[0])]
# Trying out the summarizer on a random text
random_text = [summarizer(random.choice(texts_read))]

# Trying out stanza as annotation
# text = "The Kyrgyz Republic, a small, mountainous state of the former Soviet republic, is using invisible ink and " \
#        "ultraviolet readers in the country's elections as part of a drive to prevent multiple voting. "

# # Submit request to the server
# ann = client.annotate(text)
# # Get first sentence
# sentence = ann.sentence[0]
# # get the constituency parse of the first sentence
# print('---')
# print('constituency parse of first sentence')
# constituency_parse = sentence.parseTree
# print(constituency_parse)
#
# # get the first subtree of the constituency parse
# print('---')
# print('first subtree of constituency parse')
# print(constituency_parse.child[0])
