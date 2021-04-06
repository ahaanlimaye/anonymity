# imports
from index import anonymize_text
from pathlib import Path
import fitz
  
class Redactor:
    
    # static methods work independent of class object
    @staticmethod
    def get_pii(lines, pii):
        
        """ Function to get all the lines """
          
        redact = []
        for line in lines:
            
            redact += anonymize_text(line, pii)[1]

        return redact
  
    # constructor
    def __init__(self, path, pii):
        self.path = path
        self.pii = pii
  
    def redaction(self):
        
        """ main redactor code """
          
        # opening the pdf
        doc = fitz.open(self.path)
          
        # iterating through pages
        for page in doc:
            
            # _wrapContents is needed for fixing
            # alignment issues with rect boxes in some
            # cases where there is alignment issue
            page.wrapContents()
              
            # geting the rect boxes which consists the matching email regex
            pii_data = self.get_pii(page.getText("text").split('\n'), self.pii)
            # print(sensitive)
            # print()
            for data in pii_data:
                areas = page.searchFor(data)
                  
                # drawing outline over sensitive datas
                [page.addRedactAnnot(area, fill = (0, 0, 0)) for area in areas]
                  
            # applying the redaction
            page.apply_redactions()
              
        # saving it to a new pdf
        newPath = Path(str(self.path.parent) + "/" + str(self.path.stem) + "_anonymized.pdf")
        doc.save(newPath)