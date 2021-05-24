# Technology news summarizer
import math
import os

from nltk.tokenize import sent_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from stanza.protobuf import CoreNLP_pb2
from stanza.server import CoreNLPClient

# Installing stanza if it isn't installed yet
# stanza.install_corenlp()
# Installing the English model if it hasn't been installed
# stanza.download_corenlp_models(model='english', version='4.1.0', dir="core_nlp_folder")
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

# Initializing the detokenizer
detokenizer = TreebankWordDetokenizer()


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
    # leading sentence is that that goes below the title
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
            # Doing the constituency parsing of the sentence and return the first NP and VP
            processed_sentence = processing_text(sent)
            parsed_text.append(processed_sentence)

    return parsed_text, paragraph_text


# With the constituency parsing the idea is to keep the essential elements of the sentence. The idea that is being
# tried to transmit
# The method receives a sentence and returns the first NP and VP of each sentence
def processing_text(p_sent: str):
    # Getting the constituency parse of the sentence
    current_sentence = client.annotate(p_sent).sentence[0]
    print('the current sentence', current_sentence)
    # Processing the constituency parse of the sentence
    parse_tree = current_sentence.parseTree
    # Returning the corresponding np and vp. Variable where the processed sentence will be stored
    processed_sentence = processing_s(parse_tree)
    return processed_sentence


# Checking whether it has a NP
# The node is taken as input
# TODO: Make sure that the methods return what you want them to return and that they properly concatenate the values
def processing_s(p_node: CoreNLP_pb2.ParseTree):
    # Variable where the final extracted sentence will be stored
    final_sentence = finding_np(p_node) + ' ' + finding_vp(p_node)

    return final_sentence


# Method that finds the first np
def finding_np(p_node: CoreNLP_pb2.ParseTree):
    # Variable where the np phrase will be stored
    np = ""
    # Variable where the np tree is stored
    np_tree = None
    num_children = len(p_node.child)
    found_np = False
    for i in range(num_children):
        # Is the child a NP?
        # If it is stop looking for other NPs
        if p_node.child[i].value == 'NP':
            np += finding_np(p_node.child[i])
            break
        # Is the child a sentence
        elif p_node.child[i].value == 'S':
            np += finding_np(p_node.child[i])
            break
        if i == num_children - 1:
            found_np = True

    if found_np and np == "":
        np = extract_terminal(p_node)

    return np


# Method that processes VP
def process_vp(p_node: CoreNLP_pb2.ParseTree):
    found_first_np = False
    # # Variable where an np, if there exists one will be stored
    # the_np = ""
    # Variable where the vp will be stored
    the_vp = ""
    # Variable where the symbols "S" and "VP" will be stored. To make elif shorter
    symbols = ['S', 'VP']
    num_children = len(p_node.child)
    for i in range(num_children):
        if p_node.child[i].value == 'NP' and not found_first_np:
            found_first_np = True
            the_vp += finding_np(p_node.child[i])
        elif p_node.child[i].value == 'VP':
            the_vp += process_vp(p_node.child[i])
        # Is the child a sentence
        elif p_node.child[i].value == 'S':
            the_vp += ' ' + finding_vp(p_node.child[i])
        # Adding everything that goes before the first np
        elif p_node.child[i].value != 'NP' and not found_first_np:
            # TODO: Not sure if it generalizes well
            the_vp += p_node.child[i].child[0].value + ' '
    return the_vp


# Method that finds the first vp
def finding_vp(p_node: CoreNLP_pb2.ParseTree):
    # Variable where the vp phrase will be stored
    vp = ""
    # Variable where the np tree is stored
    vp_tree = None
    num_children = len(p_node.child)
    found_vp = False
    for i in range(num_children):
        # Is the child a VP?
        # If it is stop looking for other VPs
        if p_node.child[i].value == 'VP':
            vp += process_vp(p_node.child[i])
            break
        # Is the child a sentence
        elif p_node.child[i].value == 'S':
            vp += finding_vp(p_node.child[i])
            break
        if i == num_children - 1:
            found_vp = True

    if found_vp and vp == "":
        vp += extract_terminal(p_node)

    return vp


# Method that extracts the terminal elements from the sentences in order to arrive to the final sentence.
# Extracts if it is a tree
def extract_terminal(p_tree):
    # Phrase where the constituent just in string form will be stored
    transformed_string = ""
    if p_tree:
        # Array where the different tokens will be stored. That will then be detokenized
        tokens = []
        # Getting number of children
        num_children = len(p_tree.child)
        for i in range(num_children):
            tokens.append(p_tree.child[i].child[0].value)

        transformed_string = detokenizer.detokenize(tokens)
    return transformed_string


# Trying out the summarizer parts in sample sentences
# Array that contains sample sentences
sample_sentences = [
    "Ink helps drive democracy in Asia",
    "The Kyrgyz Republic, a small, mountainous state of the former Soviet republic, is using invisible ink and "
    "ultraviolet readers in the country's elections as part of a drive to prevent multiple voting. ",
    "A US woman is suing Hewlett Packard (HP), saying its printer ink cartridges are secretly programmed to expire on "
    "a certain date. "
]
# Annotating the sentences. Array of annotations
parses = []
# Array that will contain the nps
nps = []
# Array that will contain the vps
vps = []
for sent in sample_sentences:
    current_parse = client.annotate(sent).sentence[0].parseTree
    parses.append(current_parse)
    np_01 = ""
    vp_01 = ""
    # Testing the np function
    current_np = finding_np(current_parse)
    nps.append(current_np)
    print('the np for the sentence is:', current_np)
    # Testing the vp function
    current_vp = finding_vp(current_parse)
    vps.append(current_vp)
    print('the vp for the sentence is:', current_vp)


# Trying out the summarizer on the first text
the_text = [summarizer(texts_read[0])]
# Trying out the summarizer on a random text
# random_text = [summarizer(random.choice(texts_read))]
