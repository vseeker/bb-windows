# -*- coding: utf-8 -*-
from PyPDF2 import PdfFileWriter,PdfFileReader
# from sys import *
import os
# print os.getcwd()
# pdf = "/HTTP.pdf"
# absPath = os.getcwd()+pdf
# os.system("open "+absPath)
def getPDF(pdfPath="HTTP.pdf",span=[1,7]):
    """参数:起始页,文件名
    返回,该文件中起始页和终止页之间的页面组成的pdf并打开"""
    pdfName = pdfPath[:-4]
    # print pdfName
    pdfReader = PdfFileReader(open("../pypdf2_test/HTTP.pdf","rb"))
    output = PdfFileWriter( )
    for el in xrange(span[0],span[1]+1):
        output.addPage(pdfReader.getPage(el))
    outputStream = file("getPdf_from{pdf}page{startPage}topage{endPage}.pdf".format(pdf=pdfName,startPage=span[0],endPage=span[1]),"wb")
    outPdfPath = os.getcwd()+'/'+"getPdf_from{pdf}page{startPage}topage{endPage}.pdf".format(pdf=pdfName,startPage=span[0],endPage=span[1])
    output.write(outputStream)
    os.system( "open " + outPdfPath )


getPDF()
# output = PdfFileWriter()
# pdfInput = PdfFileReader(open("../pypdf2_test/connector-python-en.a4.pdf","rb"))
# httpPdf = PdfFileReader(open("../pypdf2_test/HTTP.pdf","rb"))
#
# # print how many pages pdfInput has:
# print "connector-python-en.a4.pdf has %d pages." % pdfInput.getNumPages()
#
# # add page 2 from pdfInput, but rotated clockwise 90 degrees
# output.addPage(pdfInput.getPage(1).rotateClockwise(90))
#
# # add page 3 from pdfInput, rotated the other way:
# output.addPage(pdfInput.getPage(2).rotateCounterClockwise(90))
# # alt: output.addPage(pdfInput.getPage(2).rotateClockwise(270))
#
# # add page 4 from pdfInput, but first add a watermark from another PDF:
# page4 = pdfInput.getPage(3)
# # watermark = PdfFileReader(open("watermark.pdf", "rb"))
# watermark = httpPdf.getPage(0)
#
# page4.mergePage(watermark)
# output.addPage(page4)
#
#
# # add page 5 from pdfInput, but crop it to half size:
# page5 = pdfInput.getPage(4)
# page5.mediaBox.upperRight = (
#     page5.mediaBox.getUpperRight_x() / 2,
#     page5.mediaBox.getUpperRight_y() / 2
# )
# output.addPage(page5)
#
# # add some Javascript to launch the print window on opening this PDF.
# # the password dialog may prevent the print dialog from being shown,
# # comment the the encription lines, if that's the case, to try this out
# output.addJS("this.print({bUI:true,bSilent:false,bShrinkToFit:true});")
#
# # encrypt your new PDF and add a password
# password = "secret"
# output.encrypt(password)
#
# # finally, write "output" to document-output.pdf
# outputStream = file("../pypdf2_test/PyPDF2-output.pdf", "wb")
# output.write(outputStream)
