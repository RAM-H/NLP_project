import PyPDF2
import os

files = os.listdir('data')
for file in files:

    pdfFileObj = open('data/'+file, 'rb') 
    # creating a pdf reader object 
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
    # printing number of pages in pdf file 
    # creating a page object 
    os.mkdir('data/'+file.split('.')[0])
    for p in range(pdfReader.numPages):
        fichier = open("data/"+file.split('.')[0]+'/'+str(p+1)+".txt", "a")
        
        pageObj = pdfReader.getPage(p) 
        # print(pageObj.extractText())    
        fichier.write(pageObj.extractText())
        fichier.close()
    pdfFileObj.close() 