# imports
from index import anonymize_text
from pathlib import Path
from redact import Redactor
import argparse

# main function
def main():

    # sets arguments (Filename and PII's) for python script
    parser = argparse.ArgumentParser(description="Anonymize a PDF or TXT file")
    parser.add_argument("filepath", type=dir_path, nargs="+", help="Filepath for PDF or TXT file")
    parser.add_argument("-i", action="append", required=True, help="Specify PII (PERSON, NORP, FAC, ORG, GPE, LOC, PRODUCT, EVENT, WORK_OF_ART, LAW, LANGUAGE, DATE, TIME, PERCENT, MONEY, QUANTITY, ORDINAL, CARDINAL, PROPER_NOUN, EMAIL, URL, PHONE_NUMBER)",
                        default=[])

    # calls anonymize function based on whether file type is PDF or TXT
    args = parser.parse_args()
    filepath = args.filepath[0]
    pii = args.i
    if (filepath[-4 : ] == ".pdf"):
        anonymize_pdf(filepath, pii)
    else:
        anonymize_txt(filepath, pii)

# file path data type
def dir_path(path):
    if Path(path) and (path[-4 : ] == ".pdf" or path[-4 : ] == ".txt"):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")  

# anonymizes/redacts info on PDF
def anonymize_pdf(filepath, pii):

    # gets PDF file
    path = Path(filepath) 

    # creates new redacted PDF in same directory as original PDF
    redactor = Redactor(path, pii)
    redactor.redaction()

    print("Successfully Anonymized " + str(path.name) + " in new file: " + str(path.stem) + "_anonymized.pdf")


# anonymizes/redacts info on TXT
def anonymize_txt(filepath, pii):

    # reads text from TXT file
    path = Path(filepath)
    f = open(path, "r")
    text = f.read()
    f.close()

    # gets anonymized text
    text = anonymize_text(text, pii)[0]

    # creates new anonymized TXT is same directoyr as original TXT
    path = Path(str(path.parent) + "/" + str(path.stem) + "_anonymized.txt")
    f = open(path, "w+")
    f.seek(0)
    f.write(text)
    f.truncate()
    f.close()

    print("Successfully Anonymized " + str(path.name) + " in new file: " + str(path.stem) + "_anonymized.txt")

if __name__ == "__main__":
    main()
