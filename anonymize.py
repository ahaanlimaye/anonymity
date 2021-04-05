from index import anonymize_text

f = open('C:/Users/ahaan/OneDrive/Desktop/workspace/sample_email1.txt','r+')
text = f.read()
print(text)
text = anonymize_text(text)
print(text)
f.seek(0)
f.write(text)
f.truncate()
f.close()