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
def summarizer(p_text: str):
    # Splitting text by \n
    partitioned_text = p_text.split('\n')
    # Remove all empty strings in the texts.
    partitioned_text = list(filter(None, partitioned_text))
    # Variable where the summarized text will be stored
    summarized_text = []
    # Assumes title is first string of the text
    title = partitioned_text[0]
    # Partitioning the text into paragraphs. A paragraph is considered to have more than one sentence
    paragraph_text = []
    for i in partitioned_text:
        tokenized_segment = sent_tokenize(i)
        if len(tokenized_segment) > 1:
            paragraph_text.append(tokenized_segment)

    # Extracting the first and last paragraphs of the text.
    first_paragraph = paragraph_text[0]
    last_paragraph = paragraph_text[len(paragraph_text)-1]
    print('the title', title)
    print('the first paragraph', first_paragraph)
    print('the last paragraph', last_paragraph)

