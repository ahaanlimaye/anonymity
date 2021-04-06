# imports
import spacy
from spacy.matcher import Matcher
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

# anonymizes string based on the inputted PIIs
def anonymize_text(str, pii):

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
        if (token.like_email and "EMAIL" in pii):
            txt = "<EMAIL>"
            redact.append(token.text)
        elif (token.like_url and "URL" in pii):
            txt = "<URL>"
            redact.append(token.text)
        elif (token.ent_type_ in pii):
            txt = "<" + token.ent_type_ + ">"
            redact.append(token.text)
        elif (token.pos_ in pii):
            txt = "<" + token.pos_ + ">"
            redact.append(token.text)
        else:
            txt = token.text
        text += txt + token.whitespace_

    # returns tuple of anonymized text and redacted keywords/phrases
    return (text, redact)