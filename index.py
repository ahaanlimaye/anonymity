# imports
import spacy
from spacy.matcher import Matcher
from collections import Counter
from string import punctuation
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe("merge_noun_chunks")
nlp.add_pipe("merge_entities")

# merges phone number's into single tokens of a nlp doc
def merge_phone_number(doc):

    # finds phone number matches in doc
    matcher = Matcher(nlp.vocab)
    pattern = [[{'ORTH': '('}, {'SHAPE': 'ddd'},{'ORTH': ')'},{'ORTH': '-', 'OP': '?'},{'SHAPE': 'ddd'},{'ORTH': '-', 'OP': '?'},{'SHAPE': 'dddd'}], # (XXX) XXX XXXX
               [{'SHAPE': 'ddd'},{'ORTH': '-'},{'SHAPE': 'ddd'},{'ORTH': '-'},{'SHAPE': 'dddd'}]] # XXX-XXX-XXXX
    matcher.add('PHONE_NUMBER', pattern)
    matches = matcher(doc)

    # iterates through phone number matches and merges them into one token each
    for i in range(len(matches)-1, -1, -1):
        with doc.retokenize() as retokenizer:
            retokenizer.merge(doc[matches[i][1]:matches[i][2]], attrs={"ENT_TYPE": "PHONE_NUMBER"})

# extracts keywords out of text
def get_keywords(text):

    # sets list for keywords
    keywords = []

    # pats-of-speech tags to recognize words on
    pos_tag = ['PROPN', 'ADJ', 'NOUN']

    # creates doc out of text and iterates through tokens, finding keywords
    doc = nlp(text.lower())
    for token in doc:
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            keywords.append(token.text)    

    # makes keywords array unique and returns it
    keywords = set(keywords)        
    return keywords

# anonymizes string based on the inputted PIIs
def anonymize_text(str, pii):

    # extracts keywords from text
    keywords = get_keywords(str)

    # creates proper nlp doc for inputted string
    text = (str)
    doc = nlp(text)
    merge_phone_number(doc)

    # sets anonymized text and redacted keyword/phrases variables
    text = ""
    redact = []

    # iterates through the tokens in the doc and anonymizes/redacts any specified PIIs
    for token in doc:
        txt = ""
        if (token.like_email and "EMAIL" in pii and token.text not in keywords):
            txt = "<EMAIL>"
            redact.append(token.text)
        elif (token.like_url and "URL" in pii and token.text not in keywords):
            txt = "<URL>"
            redact.append(token.text)
        elif (token.ent_type_ in pii and token.text not in keywords):
            txt = "<" + token.ent_type_ + ">"
            redact.append(token.text)
        elif (token.pos_ in pii and token.text not in keywords):
            txt = "<" + token.pos_ + ">"
            redact.append(token.text)
        else:
            txt = token.text
        text += txt + token.whitespace_

    # returns tuple of anonymized text and redacted keywords/phrases
    return (text, redact)