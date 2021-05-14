# Technology news summarizer
from nltk.tokenize import sent_tokenize
import os

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
    # Variable to store the title
    title = []
    # Variable to store the leading sentence. The sentence that goes below the title. I believe it contains important
    # information
    leading_sentence = []
    # Partitioning the text into paragraphs. A paragraph is considered to have more than one sentence
    paragraph_text = []
    for i, v in enumerate(partitioned_text):
        tokenized_segment = sent_tokenize(v)
        print('the i value', i, 'the tokenized segment', tokenized_segment)
        # Assumes title is first string of the text
        if i == 0:
            title = tokenized_segment
        elif len(tokenized_segment) > 1:
            paragraph_text.append(tokenized_segment)
        # Checking for the leading sentence
        elif i == 1:
            leading_sentence = tokenized_segment

    # TODO: Extracting the first 20% percent (hoping that pareto works here) of paragraphs of the text.
    first_paragraph = paragraph_text[0]
    last_paragraph = paragraph_text[len(paragraph_text) - 1]
    print('the title', title)
    print('the leading sentence', leading_sentence)
    print('the first paragraph', first_paragraph)
    print('the last paragraph', last_paragraph)


# Trying out the summarizer on the first text
summarizer(texts_read[0])
