import PyPDF2
pdf_file = open("pdf name","rb")
pdf_read = PyPDF2.PdfFileReader(pdf_file)
print(f"Number of pages: {pdf_read.numPages}")
pageObject = pdf_read.getPage(0)
text = pageObject.extractText()
pdf_file.close()
with open("filename.txt","w") as file:
    file.writelines(text)