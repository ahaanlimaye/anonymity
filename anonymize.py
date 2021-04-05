from index import anonymize_text
from pathlib import Path
import pdfplumber

def anonymize_pdf(filepath):
    path = Path(filepath)
    f = pdfplumber.open(path)
    text = ""
    for page in f.pages:
        text += page.extract_text() + "\n"
    f.close()

    text = anonymize_text(text)

    path = Path(str(path.parent) + "/" + str(path.stem) + "_anonymized.txt") 
    print(path)  
    f = open(path, "w+")
    f.write(text)
    f.close()

def anonymize_txt(filepath):
    path = Path(filepath)
    f = open(path,"r")
    text = f.read()
    f.close()

    text = anonymize_text(text)

    path = Path(str(path.parent) + "/" + str(path.stem) + "_anonymized.txt")  
    f = open(path, "w+")
    f.seek(0)
    f.write(text)
    f.truncate()
    f.close()

if __name__ == "__main__":
    anonymize_pdf("C:\\Users\\ahaan\\OneDrive\\Desktop\\workspace\\Resume-AhaanLimaye.pdf")