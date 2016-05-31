from PyPDF2 import PdfFileWriter, PdfFileReader

input1 = PdfFileReader(open('HTTP.pdf', "rb"))

# analyze pdf data
print input1.getDocumentInfo()
print input1.getNumPages()
text = input1.getPage(0).extractText()
print text.encode("windows-1250", errors='backslashreplacee')

# create output document
output = PdfFileWriter()
output.addPage(input1.getPage(0))
fout = open("y.pdf", "wb")
output.write(fout)
fout.close()
