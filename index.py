import spacy
from spacy.matcher import Matcher
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe("merge_noun_chunks")
nlp.add_pipe("merge_entities")

def merge_phone_number(doc):
    matcher = Matcher(nlp.vocab)
    pattern = [[{'ORTH': '('}, {'SHAPE': 'ddd'},{'ORTH': ')'},{'ORTH': '-', 'OP': '?'},{'SHAPE': 'ddd'},{'ORTH': '-', 'OP': '?'},{'SHAPE': 'dddd'}],
               [{'SHAPE': 'ddd'},{'ORTH': '-'},{'SHAPE': 'ddd'},{'ORTH': '-'},{'SHAPE': 'dddd'}]]
    matcher.add('PHONE_NUMBER', pattern)
    matches = matcher(doc)
    for i in range(len(matches)-1, -1, -1):
        with doc.retokenize() as retokenizer:
            retokenizer.merge(doc[matches[i][1]:matches[i][2]], attrs={"ENT_TYPE": "PHONE_NUMBER"})


def anonymize_text(str):
    text = (str)
    doc = nlp(text)
    merge_phone_number(doc)
    text = ""
    redact = []
    ent_types = ["PERSON", "ORG", "GPE", "LOC", "DATE", "TIME", "MONEY"]
    for token in doc:
        txt = ""
        if (token.like_email):
            txt = "<EMAIL>"
            redact.append(token.text)
        elif (token.like_url):
            txt = "<URL>"
            redact.append(token.text)
        elif (token.ent_type_ in ent_types):
            txt = "<" + token.ent_type_ + ">"
            redact.append(token.text)
        # elif (len(token.ent_type_) > 0):
        #     txt = "<" + token.ent_type_ + ">"
        #     redact.append(token.text)
        # elif (token.pos_ == "PROPN"):
        #     txt = "<PROPER_NOUN>"
        #     redact.append(token.text)
        else:
            txt = token.text
        text += txt + token.whitespace_
    return (text, redact)

# import pdfplumber

# with pdfplumber.open(r'Resume - Ahaan Limaye.pdf') as pdf:
#     first_page = pdf.pages[0]
#     text = first_page.extract_text()
#     print(anonymize_text(text))

# f = open('sample_email1.txt','r+')
# text = f.read()
# print(text)
# text = anonymize_text(text)
# print(text)
# f.seek(0)
# f.write(text)
# f.truncate()
# f.close()

# inp_text = "My name is Ahaan Limaye. I like to go skiing in Vermont. If you guys have any questions please email me at ahaan.limaye@gmail.com or call me at 908-821-6332."
# print(anonymize_text(inp_text))
